import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.product_service import ProductService
from backend.category_service import CategoryService
from backend.measurement_service import MeasurementService
from PIL import Image, ImageTk
import os
from frontend.category_form import UniversalProductForm
from frontend.measurement_form import MeasurementForm

class InventoryManagement:
    def __init__(self, parent, user_session=None):
        self.parent = parent
        self.product_service = ProductService()
        self.category_service = CategoryService()
        self.measurement_service = MeasurementService()
        self.current_category = None
        self.selected_category_name = None
        self.user_session = user_session
        self.all_products = []  # Store all products for search
        self.is_search_mode = False  # Track if we're in search mode
        self.search_results = []  # Store search results
        
        # Initialize all UI attributes to None to prevent attribute errors
        self.scrollable_frame = None
        self.canvas = None
        self.scrollbar = None
        self.status_label = None
        self.search_var = None
        self.search_entry = None
        self.add_product_btn = None
        self.category_buttons = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup complete UI for inventory management with compact layout"""
        # Main container
        main_frame = tk.Frame(self.parent, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            header_frame,
            text="📦 INVENTORY MANAGEMENT",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        ).pack(pady=15)
        
        # Control Panel - Single line with search and action buttons
        control_frame = tk.Frame(main_frame, bg='#34495e')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Left side - Search functionality
        left_controls = tk.Frame(control_frame, bg='#34495e')
        left_controls.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Search section
        search_frame = tk.Frame(left_controls, bg='#34495e')
        search_frame.pack(fill=tk.X)
        
        tk.Label(
            search_frame,
            text="🔍",
            font=('Arial', 12),
            fg='white',
            bg='#34495e'
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Arial', 11),
            width=20,
            relief='solid',
            bd=1
        )
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5), ipady=3)
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        self.search_entry.bind('<Return>', self.perform_search)
        
        # Search buttons
        search_btn = tk.Button(
            search_frame,
            text="Search",
            font=('Arial', 9, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.perform_search,
            cursor='hand2',
            width=6
        )
        search_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_search_btn = tk.Button(
            search_frame,
            text="Clear",
            font=('Arial', 9),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=self.clear_search,
            cursor='hand2',
            width=6
        )
        clear_search_btn.pack(side=tk.LEFT)
        
        # Right side - Action buttons in same line
        right_controls = tk.Frame(control_frame, bg='#34495e')
        right_controls.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Action buttons frame
        action_buttons_frame = tk.Frame(right_controls, bg='#34495e')
        action_buttons_frame.pack(side=tk.TOP)
        
        refresh_btn = tk.Button(
            action_buttons_frame,
            text="🔄 Refresh",
            font=('Arial', 9, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.refresh_all,
            cursor='hand2',
            width=10
        )
        refresh_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # NEW: Add Measurement Button
        add_measurement_btn = tk.Button(
            action_buttons_frame,
            text="📏 Add Measurement",
            font=('Arial', 9, 'bold'),
            bg='#9b59b6',  # Purple color to distinguish from other buttons
            fg='white',
            relief='flat',
            command=self.add_measurement,
            cursor='hand2',
            width=12
        )
        add_measurement_btn.pack(side=tk.LEFT, padx=(0, 5))

        # FIX: Define add_product_btn first, then configure command separately
        self.add_product_btn = tk.Button(
            action_buttons_frame,
            text="+ Add Product",
            font=('Arial', 9, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            cursor='hand2',
            state='disabled',
            width=12
        )
        self.add_product_btn.pack(side=tk.LEFT)
        
        # Category buttons below the search/action line
        category_frame = tk.Frame(main_frame, bg='#34495e')
        category_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Define 5 categories with colors and icons
        self.categories = {
            'Paint': {'color': '#e74c3c', 'icon': '🎨', 'enabled': True},
            'Sanitary': {'color': '#3498db', 'icon': '🚿', 'enabled': True},
            'Roof Sheet': {'color': '#2ecc71', 'icon': '🏗️', 'enabled': True},
            'Limination Sheet': {'color': '#9b59b6', 'icon': '📄', 'enabled': True},
            'Hardware': {'color': '#f39c12', 'icon': '🔧', 'enabled': True}
        }
        
        # Create category buttons container
        category_buttons_container = tk.Frame(category_frame, bg='#34495e')
        category_buttons_container.pack(pady=8)
        
        # Create category buttons
        self.category_buttons = {}
        for category_name, props in self.categories.items():
            if props['enabled']:
                # Enabled categories - normal button
                btn = tk.Button(
                    category_buttons_container,
                    text=f"{props['icon']} {category_name}",
                    font=('Arial', 10, 'bold'),
                    bg='#34495e',
                    fg='white',
                    relief='flat',
                    bd=0,
                    cursor='hand2',
                    command=lambda cn=category_name: self.select_category(cn),
                    width=15,
                    height=1
                )
            else:
                # Disabled categories - grayed out button
                btn = tk.Button(
                    category_buttons_container,
                    text=f"{props['icon']} {category_name}",
                    font=('Arial', 10, 'bold'),
                    bg='#2c3e50',  # Darker background for disabled
                    fg='#7f8c8d',  # Gray text for disabled
                    relief='flat',
                    bd=0,
                    cursor='arrow',
                    command=lambda cn=category_name: self.show_not_implemented(cn),
                    width=15,
                    height=1,
                    state='disabled'  # Actually disable the button
                )
            btn.pack(side=tk.LEFT, padx=3)
            self.category_buttons[category_name] = btn
        
        # Status bar to show current view
        self.status_frame = tk.Frame(main_frame, bg='#ecf0f1')
        self.status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = tk.Label(
            self.status_frame,
            text="📁 Please select a category to view products",
            font=('Arial', 10),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        self.status_label.pack(pady=5)
        
        # Products Container with scrollable canvas
        self.products_container = tk.Frame(main_frame, bg='#f8f9fa')
        self.products_container.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable canvas for products
        self.canvas = tk.Canvas(self.products_container, bg='#f8f9fa', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.products_container, orient="vertical", command=self.canvas.yview)
        
        # Initialize scrollable_frame properly
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f8f9fa')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Update canvas width after packing
        self.parent.update_idletasks()
        self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width())
        
        # Bind resize event
        self.canvas.bind('<Configure>', lambda e: self._update_canvas_width())

        # FIX: Now set the command for add_product_btn after it's created
        self.add_product_btn.config(command=self.add_product)

        # Initial load - AFTER UI is fully set up
        self.refresh_all()

    # ADD THE MISSING add_product METHOD HERE - BEFORE IT'S USED
    def add_product(self):
        """Add new product using universal form"""
        if not self.current_category:
            messagebox.showwarning("Warning", "Please select a category first!")
            return
        
        try:
            categories = self.category_service.get_all_categories()
            category_name = ""
            for cat in categories:
                if cat[0] == self.current_category:
                    category_name = cat[1]
                    break
            
            # Use Universal Form for ALL categories
            UniversalProductForm(
                parent=self.parent,
                product_service=self.product_service,
                current_category=self.current_category,
                refresh_callback=lambda: self.load_products(self.current_category),
                category_name=category_name
            )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {str(e)}")

    def _update_canvas_width(self):
        """Update canvas window width to match canvas width"""
        try:
            if self.canvas and self.canvas.winfo_exists():
                canvas_width = self.canvas.winfo_width()
                if canvas_width > 1:
                    self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        except:
            pass
        
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if self.canvas and self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _ensure_scrollable_frame(self):
        """Safety check to ensure scrollable_frame exists"""
        return hasattr(self, 'scrollable_frame') and self.scrollable_frame is not None

    def _ensure_status_label(self):
        """Safety check to ensure status_label exists"""
        return hasattr(self, 'status_label') and self.status_label is not None

    # NEW METHOD: Add Measurement
    def add_measurement(self):
        """Open measurement form dialog"""
        try:
            # Open measurement form dialog
            MeasurementForm(
                parent=self.parent,
                refresh_callback=self.on_measurement_added
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open measurement form: {str(e)}")

    def on_measurement_added(self):
        """Callback when measurement is added successfully"""
        messagebox.showinfo("Success", "Measurement unit added successfully!")
        # You can add any additional refresh logic here if needed
        # For example, refresh the current category view if it uses measurements
        if self.current_category:
            self.load_products(self.current_category)

    def show_not_implemented(self, category_name):
        """Show message for categories that are not implemented yet"""
        messagebox.showinfo(
            "Coming Soon", 
            f"{category_name} category is not implemented yet.\n\n"
            f"This feature will be available in a future update."
        )

    def refresh_all(self):
        """Refresh all data and reset view"""
        try:
            # Load all products for search functionality
            self.all_products = self.product_service.get_all_products()
            self.load_categories()
            self.clear_search()
            # Only update status if status_label exists
            if self._ensure_status_label():
                self.update_status("Ready - Select a category to view products")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh data: {str(e)}")

    def update_status(self, message):
        """Update status bar message"""
        # Safety check before using status_label
        if not self._ensure_status_label():
            return
            
        try:
            self.status_label.config(text=message)
        except Exception as e:
            print(f"Error updating status: {e}")

    def on_search_change(self, event=None):
        """Handle real-time search as user types"""
        search_term = self.search_var.get().strip()
        if len(search_term) >= 2:  # Start searching after 2 characters
            self.perform_search()
        elif len(search_term) == 0:
            self.clear_search()

    def perform_search(self, event=None):
        """Perform search across selected category products"""
        search_term = self.search_var.get().strip()
        
        if not search_term:
            self.clear_search()
            return
        
        # Only search if a category is selected
        if not self.current_category:
            messagebox.showwarning("Warning", "Please select a category first to search products!")
            self.search_var.set("")
            return
        
        try:
            self.search_results = []
            
            # Get products from current category
            category_products = self.product_service.get_products_by_category(self.current_category)
            
            for product in category_products:
                if self.matches_search(product, search_term):
                    self.search_results.append(product)
            
            # Display search results
            self.is_search_mode = True
            self.display_products(self.search_results)
            
            # Update status only if status_label exists
            if self._ensure_status_label():
                result_count = len(self.search_results)
                if result_count == 0:
                    self.update_status(f"🔍 No products found for '{search_term}' in {self.selected_category_name}")
                else:
                    self.update_status(f"🔍 Found {result_count} products for '{search_term}' in {self.selected_category_name}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")

    def matches_search(self, product, search_term):
        """Check if product matches search criteria in all fields"""
        try:
            # Unpack product data based on schema
            if len(product) >= 14:
                (product_id, category_id, company, ptype, color,
                 sale_price, purchase_price, packing, volume, current_stock, 
                 image_path, created_at, updated_at, category_name) = product[:14]
            else:
                return False
            
            search_term = search_term.lower()
            
            # Search in all relevant fields
            searchable_fields = [
                str(company).lower(),
                str(ptype).lower(),
                str(color).lower(),
                str(packing).lower(),
                str(volume).lower()
            ]
            
            return any(search_term in field for field in searchable_fields)
            
        except Exception:
            return False

    def clear_search(self):
        """Clear search and return to category view"""
        if hasattr(self, 'search_var') and self.search_var:
            self.search_var.set("")
        self.is_search_mode = False
        self.search_results = []
        
        if self.current_category:
            # Return to previously selected category view
            self.load_products(self.current_category)
            # Only update status if status_label exists
            if self._ensure_status_label():
                self.update_status(f"📁 Viewing {self.selected_category_name} category")
        else:
            # Show category selection message
            self.show_select_category_message()

    def select_category(self, category_name):
        """Handle category button click - only for enabled categories"""
        # Check if this category is enabled
        if not self.categories[category_name]['enabled']:
            self.show_not_implemented(category_name)
            return
        
        # Reset all buttons to default state
        for name, btn in self.category_buttons.items():
            if self.categories[name]['enabled']:  # Only reset enabled buttons
                btn.config(bg='#34495e')
        
        # Highlight selected button
        self.category_buttons[category_name].config(bg=self.categories[category_name]['color'])
        
        # Set selected category
        self.selected_category_name = category_name
        
        try:
            # Normal category selection
            category_id = self.category_service.get_category_by_name(category_name)
            
            if category_id:
                self.current_category = category_id
                self.is_search_mode = False
                if hasattr(self, 'add_product_btn') and self.add_product_btn:
                    self.add_product_btn.config(state='normal')
                self.load_products(category_id)
                # Only update status if status_label exists
                if self._ensure_status_label():
                    self.update_status(f"📁 Viewing {category_name} category")
            else:
                messagebox.showerror("Error", f"Category '{category_name}' not found!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load category: {str(e)}")

    def load_categories(self):
        """Load categories from backend service"""
        try:
            categories = self.category_service.get_all_categories()
            
            # Check if all our predefined categories exist
            for category_name, props in self.categories.items():
                if props['enabled']:  # Only create enabled categories
                    exists = any(cat[1] == category_name for cat in categories)
                    if not exists:
                        # Create missing category
                        self.category_service.add_category(category_name, f"Products for {category_name}")
            
            # Show message to select a category if none is selected
            if not self.selected_category_name:
                self.show_select_category_message()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load categories: {str(e)}")

    def show_select_category_message(self):
        """Show message when no category is selected"""
        # Safety check before using scrollable_frame
        if not self._ensure_scrollable_frame():
            return
            
        self.clear_products_display()
        
        empty_frame = tk.Frame(self.scrollable_frame, bg='#f8f9fa')
        empty_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            empty_frame,
            text="📁 Please Select a Category",
            font=('Arial', 18, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(expand=True, pady=(100, 20))
        
        tk.Label(
            empty_frame,
            text="Click on a category button to view and search products",
            font=('Arial', 12),
            fg='#7f8c8d',
            bg='#f8f9fa'
        ).pack(expand=True, pady=10)

    def load_products(self, category_id):
        """Load products for selected category"""
        try:
            products = self.product_service.get_products_by_category(category_id)
            self.display_products(products)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {str(e)}")

    def display_products(self, products):
        """Display products in grid layout"""
        # Safety check before using scrollable_frame
        if not self._ensure_scrollable_frame():
            return
            
        self.clear_products_display()
        
        if not products:
            # Show empty state
            empty_frame = tk.Frame(self.scrollable_frame, bg='#f8f9fa')
            empty_frame.pack(fill=tk.BOTH, expand=True)
            
            if self.is_search_mode:
                message_text = "🔍 No products found matching your search"
                help_text = "Try different search terms"
            else:
                message_text = "📭 No products found in this category"
                help_text = "Click 'Add Product' to add your first product"
            
            tk.Label(
                empty_frame,
                text=message_text,
                font=('Arial', 16),
                fg='#7f8c8d',
                bg='#f8f9fa'
            ).pack(expand=True, pady=50)
            
            tk.Label(
                empty_frame,
                text=help_text,
                font=('Arial', 12),
                fg='#bdc3c7',
                bg='#f8f9fa'
            ).pack(expand=True, pady=10)
            return
        
        # Create grid card view
        self.create_grid_card_view(products)

    def clear_products_display(self):
        """Clear products display area"""
        # Safety check before using scrollable_frame
        if not self._ensure_scrollable_frame():
            return
            
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def create_grid_card_view(self, products):
        """Create grid layout with product cards - UPDATED FOR REDUCED CARDS"""
        # Safety check before using scrollable_frame
        if not self._ensure_scrollable_frame():
            return
            
        # Clear existing content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Create a container frame for the grid to ensure consistent sizing
        grid_container = tk.Frame(self.scrollable_frame, bg='#f8f9fa')
        grid_container.pack(fill=tk.BOTH, expand=True)
        
        # Create cards in grid layout with proper spacing
        row = 0
        col = 0
        max_cols = 5  # INCREASED FROM 4 TO 5 (since cards are smaller)
        
        for product in products:
            # Create card
            card = self.create_product_card(grid_container, product)
            
            if card:
                # Place card in grid with fixed size
                card.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')  # Reduced padding
                
                # Configure grid weights for responsive layout
                grid_container.grid_columnconfigure(col, weight=1, minsize=200)  # REDUCED FROM 220 TO 150
                grid_container.grid_rowconfigure(row, weight=0, minsize=320)     # Adjusted height
                
                # Move to next position
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
        
        # If there are remaining columns in the last row, configure them
        for i in range(col, max_cols):
            grid_container.grid_columnconfigure(i, weight=1, minsize=150)  # Reduced minsize
        
        # Update canvas scroll region
        grid_container.update_idletasks()
        if self.canvas and self.canvas.winfo_exists():
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_product_card(self, parent, product):
        """Create individual product card - REDUCED SIZE with WRAP LENGTH"""
        try:
            # Handle different database schemas
            if len(product) >= 14:
                product_id = product[0]
                category_id = product[1]
                company = product[2]
                product_type = product[3]
                color = product[4]
                sale_price = product[5]
                purchase_price = product[6]
                packing = product[7]
                volume = product[8]
                current_stock = product[9]
                image_path = product[10]
                created_at = product[11]
                updated_at = product[12]
                category_name = product[13] if len(product) > 13 else "Unknown"
            elif len(product) == 13:
                product_id = product[0]
                category_id = product[1]
                company = product[2]
                product_type = product[3]
                sale_price = product[4]
                purchase_price = product[5]
                packing = product[6]
                volume = product[7]
                current_stock = product[8]
                image_path = product[9]
                created_at = product[10]
                updated_at = product[11]
                category_name = product[12]
                color = "N/A"
            else:
                print(f"ERROR: Unexpected product length: {len(product)}")
                return None
        
            # Create outer frame with REDUCED dimensions
            outer_frame = tk.Frame(
                parent,
                bg='#f8f9fa',
                width=140,    # REDUCED FROM 160 TO 140
                height=300    # REDUCED FROM 320 TO 300
            )
            outer_frame.grid_propagate(False)
            
            # Create card frame with REDUCED dimensions
            card_frame = tk.Frame(
                outer_frame,
                bg='white',
                relief='solid',
                bd=1,
                width=140,    # REDUCED FROM 160 TO 140
                height=300    # REDUCED FROM 320 TO 300
            )
            card_frame.pack_propagate(False)
            card_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)  # Reduced padding
            
            # 1. Product Image - TOP with REDUCED height
            image_frame = tk.Frame(card_frame, bg='#e0e0e0')
            image_frame.pack(fill=tk.X, padx=4, pady=(8, 4))  # Reduced padding
            image_frame.pack_propagate(False)
            image_frame.configure(height=80)  # REDUCED FROM 100 TO 80
            
            try:
                if image_path and os.path.exists(image_path):
                    img = Image.open(image_path)
                    img = img.resize((150, 60), Image.Resampling.LANCZOS)  # Reduced image size
                    photo = ImageTk.PhotoImage(img)
                    img_label = tk.Label(image_frame, image=photo, bg='#e0e0e0')
                    img_label.image = photo
                    img_label.pack(expand=True, fill='both')
                else:
                    # Category-specific placeholder icons with smaller font
                    if category_name and category_name.lower() == 'paint':
                        placeholder_text = "🎨 Paint"
                    elif category_name and category_name.lower() == 'sanitary':
                        placeholder_text = "🚿 Sanitary"
                    elif category_name and category_name.lower() == 'roof sheet':
                        placeholder_text = "🏗️ Roof Sheet"
                    elif category_name and category_name.lower() == 'limination sheet':
                        placeholder_text = "📄 Limination Sheet"
                    elif category_name and category_name.lower() == 'hardware':
                        placeholder_text = "🔧 Hardware"
                    else:
                        placeholder_text = "📦 No Image"
                        
                    placeholder = tk.Label(
                        image_frame, 
                        text=placeholder_text, 
                        font=('Arial', 10),  # Reduced font size
                        bg='#e0e0e0',
                        fg='#7f8c8d'
                    )
                    placeholder.pack(expand=True, fill='both')
            except Exception as e:
                placeholder = tk.Label(
                    image_frame, 
                    text="🖼️ Error", 
                    font=('Arial', 9),  # Reduced font size
                    bg='#e0e0e0',
                    fg='#e74c3c'
                )
                placeholder.pack(expand=True, fill='both')
            
            # 2. Product Details - MIDDLE with FLEXIBLE SPACE
            details_frame = tk.Frame(card_frame, bg='white')
            details_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)  # Reduced padding
            
            # Format prices in PKR
            def format_price(price):
                try:
                    return "₨{:,.0f}".format(float(price))
                except:
                    return "₨0"
            
            # FIXED: Updated labels from "Purchase" to "Purchase Price" and "Sale" to "Sale Price"
            if category_name and category_name.lower() == 'paint':
                # Paint category - simplified fields (NO MEASUREMENT)
                details = [
                    ("Company", company),
                    ("Type", product_type),
                    ("Color", color),
                    ("Packing", packing),
                    ("Purchase Price", format_price(purchase_price)),  # CHANGED
                    ("Sale Price", format_price(sale_price)),          # CHANGED
                    ("Stock", f"{current_stock} units")
                ]
            else:
                # ALL OTHER CATEGORIES - WITH MEASUREMENT SYSTEM
                details = [
                    ("Company", company),
                    ("Type", product_type),
                    ("Color", color),
                    ("Purchase Price", format_price(purchase_price)),  # CHANGED
                    ("Sale Price", format_price(sale_price))           # CHANGED
                ]
                
                # 🔥 UPDATED SECTION: Add size/volume for relevant categories - INCLUDES HARDWARE NOW
                if volume and volume != "N/A":
                    if category_name and category_name.lower() in ['sanitary', 'roof sheet', 'limination sheet', 'hardware']:
                        details.insert(3, ("Size", volume))
                
                # Add measurement-based stock display
                if packing and packing.startswith("Unit: "):
                    measurement_name = packing.replace("Unit: ", "")
                    details.append(("Stock", f"{current_stock} {measurement_name}"))
                else:
                    details.append(("Stock", f"{current_stock} units"))
            
            # Create labels for each detail with WRAP LENGTH
            for i, (label, value) in enumerate(details):
                # Create a frame for each row
                row_frame = tk.Frame(details_frame, bg='white')
                row_frame.pack(fill=tk.X, pady=1)
                
                # Label (bold) with INCREASED width for longer labels
                lbl = tk.Label(
                    row_frame,
                    text=label + ":",
                    font=('Arial', 10, 'bold'),  # Reduced font size
                    fg='#2c3e50',
                    bg='white',
                    anchor='w',
                    width=12  # INCREASED FROM 8 TO 12 for longer labels
                )
                lbl.pack(side=tk.LEFT)
                
                # Value with WRAP LENGTH for text adjustment
                val_text = str(value)
                val = tk.Label(
                    row_frame,
                    text=val_text,
                    font=('Arial', 10),  # Reduced font size
                    fg='#34495e',
                    bg='white',
                    anchor='w',
                    wraplength=400,  # ADDED WRAP LENGTH - text will wrap after 80 pixels
                    justify='left'
                )
                val.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # 3. Action buttons - BOTTOM with REDUCED layout
            button_frame = tk.Frame(card_frame, bg='white')
            button_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=4, pady=(4, 8))  # Reduced padding
            button_frame.pack_propagate(False)
            button_frame.configure(height=18)  # Reduced height
            
            # Create a container for buttons with fixed width
            button_container = tk.Frame(button_frame, bg='white')
            button_container.pack(fill=tk.X, expand=True)
            
            # Edit Button with smaller font
            edit_btn = tk.Button(
                button_container,
                text="✏️ Edit",
                font=('Arial', 8, 'bold'),  # Reduced font size
                bg='#3498db',
                fg='white',
                relief='raised',
                bd=1,
                width=3,     # Reduced width
                height=1,    # Reduced height
                cursor='hand2',
                command=lambda pid=product_id: self.edit_product(pid)
            )
            edit_btn.pack(side=tk.LEFT, padx=(0, 3), fill=tk.X, expand=True)  # Reduced padding
            
            # Delete Button with smaller font
            delete_btn = tk.Button(
                button_container,
                text="🗑️ Delete",
                font=('Arial', 8, 'bold'),  # Reduced font size
                bg='#e74c3c',
                fg='white',
                relief='raised',
                bd=1,
                width=3,     # Reduced width
                height=1,    # Reduced height
                cursor='hand2',
                command=lambda pid=product_id: self.delete_product(pid)
            )
            delete_btn.pack(side=tk.RIGHT, padx=(3, 0), fill=tk.X, expand=True)  # Reduced padding
            
            return outer_frame
            
        except Exception as e:
            print(f"Error creating product card: {e}")
            return None

    def edit_product(self, product_id):
        """Edit product from selected category"""
        try:
            # Find product in current category
            products = self.product_service.get_products_by_category(self.current_category)
            product_data = None
            category_name = self.selected_category_name
            
            for product in products:
                if product[0] == product_id:
                    product_data = self.unpack_product_data(product)
                    break
            
            if not product_data:
                messagebox.showerror("Error", "Product not found!")
                return
            
            # Use Universal Form for editing
            UniversalProductForm(
                parent=self.parent,
                product_service=self.product_service,
                current_category=self.current_category,
                refresh_callback=lambda: self.load_products(self.current_category),
                category_name=category_name,
                product_id=product_id,
                product_data=product_data
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit product: {str(e)}")

    def unpack_product_data(self, product):
        """Helper to unpack product data for editing"""
        try:
            if len(product) >= 14:
                product_id = product[0]
                category_id = product[1]
                company = product[2]
                product_type = product[3]
                color = product[4]
                sale_price = product[5]
                purchase_price = product[6]
                packing = product[7]  # This stores measurement info or Color Code for Limination Sheet
                volume = product[8]
                current_stock = product[9]
                image_path = product[10]
                created_at = product[11]
                updated_at = product[12]
                category_name = product[13] if len(product) > 13 else "Unknown"
            elif len(product) == 13:
                product_id = product[0]
                category_id = product[1]
                company = product[2]
                product_type = product[3]
                sale_price = product[4]
                purchase_price = product[5]
                packing = product[6]  # This stores measurement info or Color Code for Limination Sheet
                volume = product[7]
                current_stock = product[8]
                image_path = product[9]
                created_at = product[10]
                updated_at = product[11]
                category_name = product[12]
                color = "N/A"
            else:
                return None
            
            return {
                'category_id': category_id,
                'company': company,
                'type': product_type,
                'color': color,
                'sale_price': sale_price,
                'purchase_price': purchase_price,
                'packing': packing,  # This will be used for measurement system
                'volume': volume,
                'current_stock': current_stock,
                'image_path': image_path
            }
        except Exception as e:
            print(f"Error unpacking product: {e}")
            return None

    def delete_product(self, product_id):
        """Delete product functionality"""
        result = messagebox.askyesno(
            "Confirm Delete", 
            "Are you sure you want to delete this product?\nThis action cannot be undone."
        )
        if result:
            try:
                deleted_count = self.product_service.delete_product(product_id)
                if deleted_count > 0:
                    messagebox.showinfo("Success", "Product deleted successfully!")
                    self.load_products(self.current_category)  # Refresh current category
                else:
                    messagebox.showerror("Error", "Failed to delete product!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product: {str(e)}")
# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# from backend.product_service import ProductService
# from backend.category_service import CategoryService
# from backend.measurement_service import MeasurementService
# from PIL import Image, ImageTk
# import os
# from frontend.category_form import UniversalProductForm
# from frontend.measurement_form import MeasurementForm

# class InventoryManagement:
#     def __init__(self, parent, user_session=None):
#         self.parent = parent
#         self.product_service = ProductService()
#         self.category_service = CategoryService()
#         self.measurement_service = MeasurementService()
#         self.current_category = None
#         self.selected_category_name = None
#         self.user_session = user_session
#         self.all_products = []  # Store all products for search
#         self.is_search_mode = False  # Track if we're in search mode
#         self.search_results = []  # Store search results
        
#         # Initialize all UI attributes to None to prevent attribute errors
#         self.scrollable_frame = None
#         self.canvas = None
#         self.scrollbar = None
#         self.status_label = None
#         self.search_var = None
#         self.search_entry = None
#         self.add_product_btn = None
#         self.category_buttons = {}
        
#         self.setup_ui()
        
#     def setup_ui(self):
#         """Setup complete UI for inventory management with compact layout"""
#         # Main container
#         main_frame = tk.Frame(self.parent, bg='#f8f9fa')
#         main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
#         # Header
#         header_frame = tk.Frame(main_frame, bg='#2c3e50')
#         header_frame.pack(fill=tk.X, pady=(0, 10))
        
#         tk.Label(
#             header_frame,
#             text="📦 INVENTORY MANAGEMENT",
#             font=('Arial', 18, 'bold'),
#             fg='white',
#             bg='#2c3e50'
#         ).pack(pady=15)
        
#         # Control Panel - Single line with search and action buttons
#         control_frame = tk.Frame(main_frame, bg='#34495e')
#         control_frame.pack(fill=tk.X, pady=(0, 10))
        
#         # Left side - Search functionality
#         left_controls = tk.Frame(control_frame, bg='#34495e')
#         left_controls.pack(side=tk.LEFT, padx=10, pady=10)
        
#         # Search section
#         search_frame = tk.Frame(left_controls, bg='#34495e')
#         search_frame.pack(fill=tk.X)
        
#         tk.Label(
#             search_frame,
#             text="🔍",
#             font=('Arial', 12),
#             fg='white',
#             bg='#34495e'
#         ).pack(side=tk.LEFT, padx=(0, 5))
        
#         # Search entry
#         self.search_var = tk.StringVar()
#         self.search_entry = tk.Entry(
#             search_frame,
#             textvariable=self.search_var,
#             font=('Arial', 11),
#             width=20,
#             relief='solid',
#             bd=1
#         )
#         self.search_entry.pack(side=tk.LEFT, padx=(0, 5), ipady=3)
#         self.search_entry.bind('<KeyRelease>', self.on_search_change)
#         self.search_entry.bind('<Return>', self.perform_search)
        
#         # Search buttons
#         search_btn = tk.Button(
#             search_frame,
#             text="Search",
#             font=('Arial', 9, 'bold'),
#             bg='#3498db',
#             fg='white',
#             relief='flat',
#             command=self.perform_search,
#             cursor='hand2',
#             width=6
#         )
#         search_btn.pack(side=tk.LEFT, padx=(0, 5))
        
#         clear_search_btn = tk.Button(
#             search_frame,
#             text="Clear",
#             font=('Arial', 9),
#             bg='#95a5a6',
#             fg='white',
#             relief='flat',
#             command=self.clear_search,
#             cursor='hand2',
#             width=6
#         )
#         clear_search_btn.pack(side=tk.LEFT)
        
#         # Right side - Action buttons in same line
#         right_controls = tk.Frame(control_frame, bg='#34495e')
#         right_controls.pack(side=tk.RIGHT, padx=10, pady=10)
        
#         # Action buttons frame
#         action_buttons_frame = tk.Frame(right_controls, bg='#34495e')
#         action_buttons_frame.pack(side=tk.TOP)
        
#         refresh_btn = tk.Button(
#             action_buttons_frame,
#             text="🔄 Refresh",
#             font=('Arial', 9, 'bold'),
#             bg='#3498db',
#             fg='white',
#             relief='flat',
#             command=self.refresh_all,
#             cursor='hand2',
#             width=10
#         )
#         refresh_btn.pack(side=tk.LEFT, padx=(0, 5))
        
#         # NEW: Add Measurement Button
#         add_measurement_btn = tk.Button(
#             action_buttons_frame,
#             text="📏 Add Measurement",
#             font=('Arial', 9, 'bold'),
#             bg='#9b59b6',  # Purple color to distinguish from other buttons
#             fg='white',
#             relief='flat',
#             command=self.add_measurement,
#             cursor='hand2',
#             width=12
#         )
#         add_measurement_btn.pack(side=tk.LEFT, padx=(0, 5))

#         # FIX: Properly define add_product_btn attribute
#         self.add_product_btn = tk.Button(
#             action_buttons_frame,
#             text="+ Add Product",
#             font=('Arial', 9, 'bold'),
#             bg='#27ae60',
#             fg='white',
#             relief='flat',
#             command=self.add_product,
#             cursor='hand2',
#             state='disabled',
#             width=12
#         )
#         self.add_product_btn.pack(side=tk.LEFT)
        
#         # Category buttons below the search/action line
#         category_frame = tk.Frame(main_frame, bg='#34495e')
#         category_frame.pack(fill=tk.X, pady=(0, 10))
        
#         # Define 5 categories with colors and icons
#         self.categories = {
#             'Paint': {'color': '#e74c3c', 'icon': '🎨', 'enabled': True},
#             'Sanitary': {'color': '#3498db', 'icon': '🚿', 'enabled': True},
#             'Roof Sheet': {'color': '#2ecc71', 'icon': '🏗️', 'enabled': True},
#             'Limination Sheet': {'color': '#9b59b6', 'icon': '📄', 'enabled': True},
#             'Hardware': {'color': '#f39c12', 'icon': '🔧', 'enabled': True}
#         }
        
#         # Create category buttons container
#         category_buttons_container = tk.Frame(category_frame, bg='#34495e')
#         category_buttons_container.pack(pady=8)
        
#         # Create category buttons
#         self.category_buttons = {}
#         for category_name, props in self.categories.items():
#             if props['enabled']:
#                 # Enabled categories - normal button
#                 btn = tk.Button(
#                     category_buttons_container,
#                     text=f"{props['icon']} {category_name}",
#                     font=('Arial', 10, 'bold'),
#                     bg='#34495e',
#                     fg='white',
#                     relief='flat',
#                     bd=0,
#                     cursor='hand2',
#                     command=lambda cn=category_name: self.select_category(cn),
#                     width=15,
#                     height=1
#                 )
#             else:
#                 # Disabled categories - grayed out button
#                 btn = tk.Button(
#                     category_buttons_container,
#                     text=f"{props['icon']} {category_name}",
#                     font=('Arial', 10, 'bold'),
#                     bg='#2c3e50',  # Darker background for disabled
#                     fg='#7f8c8d',  # Gray text for disabled
#                     relief='flat',
#                     bd=0,
#                     cursor='arrow',
#                     command=lambda cn=category_name: self.show_not_implemented(cn),
#                     width=15,
#                     height=1,
#                     state='disabled'  # Actually disable the button
#                 )
#             btn.pack(side=tk.LEFT, padx=3)
#             self.category_buttons[category_name] = btn
        
#         # Status bar to show current view
#         self.status_frame = tk.Frame(main_frame, bg='#ecf0f1')
#         self.status_frame.pack(fill=tk.X, pady=(0, 10))
        
#         self.status_label = tk.Label(
#             self.status_frame,
#             text="📁 Please select a category to view products",
#             font=('Arial', 10),
#             fg='#2c3e50',
#             bg='#ecf0f1'
#         )
#         self.status_label.pack(pady=5)
        
#         # Products Container with scrollable canvas
#         self.products_container = tk.Frame(main_frame, bg='#f8f9fa')
#         self.products_container.pack(fill=tk.BOTH, expand=True)
        
#         # Create scrollable canvas for products
#         self.canvas = tk.Canvas(self.products_container, bg='#f8f9fa', highlightthickness=0)
#         self.scrollbar = ttk.Scrollbar(self.products_container, orient="vertical", command=self.canvas.yview)
        
#         # Initialize scrollable_frame properly
#         self.scrollable_frame = tk.Frame(self.canvas, bg='#f8f9fa')
        
#         self.scrollable_frame.bind(
#             "<Configure>",
#             lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#         )
        
#         self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
#         self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
#         # Pack canvas and scrollbar
#         self.canvas.pack(side="left", fill="both", expand=True)
#         self.scrollbar.pack(side="right", fill="y")
        
#         # Bind mouse wheel for scrolling
#         self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
#         # Update canvas width after packing
#         self.parent.update_idletasks()
#         self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width())
        
#         # Bind resize event
#         self.canvas.bind('<Configure>', lambda e: self._update_canvas_width())

#         # Initial load - AFTER UI is fully set up
#         self.refresh_all()

#     def _update_canvas_width(self):
#         """Update canvas window width to match canvas width"""
#         try:
#             if self.canvas and self.canvas.winfo_exists():
#                 canvas_width = self.canvas.winfo_width()
#                 if canvas_width > 1:
#                     self.canvas.itemconfig(self.canvas_window, width=canvas_width)
#         except:
#             pass
        
#     def _on_mousewheel(self, event):
#         """Handle mouse wheel scrolling"""
#         if self.canvas and self.canvas.winfo_exists():
#             self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

#     def _ensure_scrollable_frame(self):
#         """Safety check to ensure scrollable_frame exists"""
#         return hasattr(self, 'scrollable_frame') and self.scrollable_frame is not None

#     def _ensure_status_label(self):
#         """Safety check to ensure status_label exists"""
#         return hasattr(self, 'status_label') and self.status_label is not None

#     # NEW METHOD: Add Measurement
#     def add_measurement(self):
#         """Open measurement form dialog"""
#         try:
#             # Open measurement form dialog
#             MeasurementForm(
#                 parent=self.parent,
#                 refresh_callback=self.on_measurement_added
#             )
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to open measurement form: {str(e)}")

#     def on_measurement_added(self):
#         """Callback when measurement is added successfully"""
#         messagebox.showinfo("Success", "Measurement unit added successfully!")
#         # You can add any additional refresh logic here if needed
#         # For example, refresh the current category view if it uses measurements
#         if self.current_category:
#             self.load_products(self.current_category)

#     def show_not_implemented(self, category_name):
#         """Show message for categories that are not implemented yet"""
#         messagebox.showinfo(
#             "Coming Soon", 
#             f"{category_name} category is not implemented yet.\n\n"
#             f"This feature will be available in a future update."
#         )

#     def refresh_all(self):
#         """Refresh all data and reset view"""
#         try:
#             # Load all products for search functionality
#             self.all_products = self.product_service.get_all_products()
#             self.load_categories()
#             self.clear_search()
#             # Only update status if status_label exists
#             if self._ensure_status_label():
#                 self.update_status("Ready - Select a category to view products")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to refresh data: {str(e)}")

#     def update_status(self, message):
#         """Update status bar message"""
#         # Safety check before using status_label
#         if not self._ensure_status_label():
#             return
            
#         try:
#             self.status_label.config(text=message)
#         except Exception as e:
#             print(f"Error updating status: {e}")

#     def on_search_change(self, event=None):
#         """Handle real-time search as user types"""
#         search_term = self.search_var.get().strip()
#         if len(search_term) >= 2:  # Start searching after 2 characters
#             self.perform_search()
#         elif len(search_term) == 0:
#             self.clear_search()

#     def perform_search(self, event=None):
#         """Perform search across selected category products"""
#         search_term = self.search_var.get().strip()
        
#         if not search_term:
#             self.clear_search()
#             return
        
#         # Only search if a category is selected
#         if not self.current_category:
#             messagebox.showwarning("Warning", "Please select a category first to search products!")
#             self.search_var.set("")
#             return
        
#         try:
#             self.search_results = []
            
#             # Get products from current category
#             category_products = self.product_service.get_products_by_category(self.current_category)
            
#             for product in category_products:
#                 if self.matches_search(product, search_term):
#                     self.search_results.append(product)
            
#             # Display search results
#             self.is_search_mode = True
#             self.display_products(self.search_results)
            
#             # Update status only if status_label exists
#             if self._ensure_status_label():
#                 result_count = len(self.search_results)
#                 if result_count == 0:
#                     self.update_status(f"🔍 No products found for '{search_term}' in {self.selected_category_name}")
#                 else:
#                     self.update_status(f"🔍 Found {result_count} products for '{search_term}' in {self.selected_category_name}")
                
#         except Exception as e:
#             messagebox.showerror("Error", f"Search failed: {str(e)}")

#     def matches_search(self, product, search_term):
#         """Check if product matches search criteria in all fields"""
#         try:
#             # Unpack product data based on schema
#             if len(product) >= 14:
#                 (product_id, category_id, company, ptype, color,
#                  sale_price, purchase_price, packing, volume, current_stock, 
#                  image_path, created_at, updated_at, category_name) = product[:14]
#             else:
#                 return False
            
#             search_term = search_term.lower()
            
#             # Search in all relevant fields
#             searchable_fields = [
#                 str(company).lower(),
#                 str(ptype).lower(),
#                 str(color).lower(),
#                 str(packing).lower(),
#                 str(volume).lower()
#             ]
            
#             return any(search_term in field for field in searchable_fields)
            
#         except Exception:
#             return False

#     def clear_search(self):
#         """Clear search and return to category view"""
#         if hasattr(self, 'search_var') and self.search_var:
#             self.search_var.set("")
#         self.is_search_mode = False
#         self.search_results = []
        
#         if self.current_category:
#             # Return to previously selected category view
#             self.load_products(self.current_category)
#             # Only update status if status_label exists
#             if self._ensure_status_label():
#                 self.update_status(f"📁 Viewing {self.selected_category_name} category")
#         else:
#             # Show category selection message
#             self.show_select_category_message()

#     def select_category(self, category_name):
#         """Handle category button click - only for enabled categories"""
#         # Check if this category is enabled
#         if not self.categories[category_name]['enabled']:
#             self.show_not_implemented(category_name)
#             return
        
#         # Reset all buttons to default state
#         for name, btn in self.category_buttons.items():
#             if self.categories[name]['enabled']:  # Only reset enabled buttons
#                 btn.config(bg='#34495e')
        
#         # Highlight selected button
#         self.category_buttons[category_name].config(bg=self.categories[category_name]['color'])
        
#         # Set selected category
#         self.selected_category_name = category_name
        
#         try:
#             # Normal category selection
#             category_id = self.category_service.get_category_by_name(category_name)
            
#             if category_id:
#                 self.current_category = category_id
#                 self.is_search_mode = False
#                 if hasattr(self, 'add_product_btn') and self.add_product_btn:
#                     self.add_product_btn.config(state='normal')
#                 self.load_products(category_id)
#                 # Only update status if status_label exists
#                 if self._ensure_status_label():
#                     self.update_status(f"📁 Viewing {category_name} category")
#             else:
#                 messagebox.showerror("Error", f"Category '{category_name}' not found!")
                
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to load category: {str(e)}")

#     def load_categories(self):
#         """Load categories from backend service"""
#         try:
#             categories = self.category_service.get_all_categories()
            
#             # Check if all our predefined categories exist
#             for category_name, props in self.categories.items():
#                 if props['enabled']:  # Only create enabled categories
#                     exists = any(cat[1] == category_name for cat in categories)
#                     if not exists:
#                         # Create missing category
#                         self.category_service.add_category(category_name, f"Products for {category_name}")
            
#             # Show message to select a category if none is selected
#             if not self.selected_category_name:
#                 self.show_select_category_message()
                
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to load categories: {str(e)}")

#     def show_select_category_message(self):
#         """Show message when no category is selected"""
#         # Safety check before using scrollable_frame
#         if not self._ensure_scrollable_frame():
#             return
            
#         self.clear_products_display()
        
#         empty_frame = tk.Frame(self.scrollable_frame, bg='#f8f9fa')
#         empty_frame.pack(fill=tk.BOTH, expand=True)
        
#         tk.Label(
#             empty_frame,
#             text="📁 Please Select a Category",
#             font=('Arial', 18, 'bold'),
#             fg='#2c3e50',
#             bg='#f8f9fa'
#         ).pack(expand=True, pady=(100, 20))
        
#         tk.Label(
#             empty_frame,
#             text="Click on a category button to view and search products",
#             font=('Arial', 12),
#             fg='#7f8c8d',
#             bg='#f8f9fa'
#         ).pack(expand=True, pady=10)

#     def load_products(self, category_id):
#         """Load products for selected category"""
#         try:
#             products = self.product_service.get_products_by_category(category_id)
#             self.display_products(products)
            
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to load products: {str(e)}")

#     def display_products(self, products):
#         """Display products in grid layout"""
#         # Safety check before using scrollable_frame
#         if not self._ensure_scrollable_frame():
#             return
            
#         self.clear_products_display()
        
#         if not products:
#             # Show empty state
#             empty_frame = tk.Frame(self.scrollable_frame, bg='#f8f9fa')
#             empty_frame.pack(fill=tk.BOTH, expand=True)
            
#             if self.is_search_mode:
#                 message_text = "🔍 No products found matching your search"
#                 help_text = "Try different search terms"
#             else:
#                 message_text = "📭 No products found in this category"
#                 help_text = "Click 'Add Product' to add your first product"
            
#             tk.Label(
#                 empty_frame,
#                 text=message_text,
#                 font=('Arial', 16),
#                 fg='#7f8c8d',
#                 bg='#f8f9fa'
#             ).pack(expand=True, pady=50)
            
#             tk.Label(
#                 empty_frame,
#                 text=help_text,
#                 font=('Arial', 12),
#                 fg='#bdc3c7',
#                 bg='#f8f9fa'
#             ).pack(expand=True, pady=10)
#             return
        
#         # Create grid card view
#         self.create_grid_card_view(products)

#     def clear_products_display(self):
#         """Clear products display area"""
#         # Safety check before using scrollable_frame
#         if not self._ensure_scrollable_frame():
#             return
            
#         for widget in self.scrollable_frame.winfo_children():
#             widget.destroy()

#     def create_grid_card_view(self, products):
#         """Create grid layout with product cards - UPDATED FOR REDUCED CARDS"""
#         # Safety check before using scrollable_frame
#         if not self._ensure_scrollable_frame():
#             return
            
#         # Clear existing content
#         for widget in self.scrollable_frame.winfo_children():
#             widget.destroy()
        
#         # Create a container frame for the grid to ensure consistent sizing
#         grid_container = tk.Frame(self.scrollable_frame, bg='#f8f9fa')
#         grid_container.pack(fill=tk.BOTH, expand=True)
        
#         # Create cards in grid layout with proper spacing
#         row = 0
#         col = 0
#         max_cols = 5  # INCREASED FROM 4 TO 5 (since cards are smaller)
        
#         for product in products:
#             # Create card
#             card = self.create_product_card(grid_container, product)
            
#             if card:
#                 # Place card in grid with fixed size
#                 card.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')  # Reduced padding
                
#                 # Configure grid weights for responsive layout
#                 grid_container.grid_columnconfigure(col, weight=1, minsize=200)  # REDUCED FROM 220 TO 150
#                 grid_container.grid_rowconfigure(row, weight=0, minsize=320)     # Adjusted height
                
#                 # Move to next position
#                 col += 1
#                 if col >= max_cols:
#                     col = 0
#                     row += 1
        
#         # If there are remaining columns in the last row, configure them
#         for i in range(col, max_cols):
#             grid_container.grid_columnconfigure(i, weight=1, minsize=150)  # Reduced minsize
        
#         # Update canvas scroll region
#         grid_container.update_idletasks()
#         if self.canvas and self.canvas.winfo_exists():
#             self.canvas.configure(scrollregion=self.canvas.bbox("all"))

#     def create_product_card(self, parent, product):
#         """Create individual product card - REDUCED SIZE with WRAP LENGTH"""
#         try:
#             # Handle different database schemas
#             if len(product) >= 14:
#                 product_id = product[0]
#                 category_id = product[1]
#                 company = product[2]
#                 product_type = product[3]
#                 color = product[4]
#                 sale_price = product[5]
#                 purchase_price = product[6]
#                 packing = product[7]
#                 volume = product[8]
#                 current_stock = product[9]
#                 image_path = product[10]
#                 created_at = product[11]
#                 updated_at = product[12]
#                 category_name = product[13] if len(product) > 13 else "Unknown"
#             elif len(product) == 13:
#                 product_id = product[0]
#                 category_id = product[1]
#                 company = product[2]
#                 product_type = product[3]
#                 sale_price = product[4]
#                 purchase_price = product[5]
#                 packing = product[6]
#                 volume = product[7]
#                 current_stock = product[8]
#                 image_path = product[9]
#                 created_at = product[10]
#                 updated_at = product[11]
#                 category_name = product[12]
#                 color = "N/A"
#             else:
#                 print(f"ERROR: Unexpected product length: {len(product)}")
#                 return None
        
#             # Create outer frame with REDUCED dimensions
#             outer_frame = tk.Frame(
#                 parent,
#                 bg='#f8f9fa',
#                 width=140,    # REDUCED FROM 160 TO 140
#                 height=300    # REDUCED FROM 320 TO 300
#             )
#             outer_frame.grid_propagate(False)
            
#             # Create card frame with REDUCED dimensions
#             card_frame = tk.Frame(
#                 outer_frame,
#                 bg='white',
#                 relief='solid',
#                 bd=1,
#                 width=140,    # REDUCED FROM 160 TO 140
#                 height=300    # REDUCED FROM 320 TO 300
#             )
#             card_frame.pack_propagate(False)
#             card_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)  # Reduced padding
            
#             # 1. Product Image - TOP with REDUCED height
#             image_frame = tk.Frame(card_frame, bg='#e0e0e0')
#             image_frame.pack(fill=tk.X, padx=4, pady=(8, 4))  # Reduced padding
#             image_frame.pack_propagate(False)
#             image_frame.configure(height=80)  # REDUCED FROM 100 TO 80
            
#             try:
#                 if image_path and os.path.exists(image_path):
#                     img = Image.open(image_path)
#                     img = img.resize((150, 60), Image.Resampling.LANCZOS)  # Reduced image size
#                     photo = ImageTk.PhotoImage(img)
#                     img_label = tk.Label(image_frame, image=photo, bg='#e0e0e0')
#                     img_label.image = photo
#                     img_label.pack(expand=True, fill='both')
#                 else:
#                     # Category-specific placeholder icons with smaller font
#                     if category_name and category_name.lower() == 'paint':
#                         placeholder_text = "🎨 Paint"
#                     elif category_name and category_name.lower() == 'sanitary':
#                         placeholder_text = "🚿 Sanitary"
#                     elif category_name and category_name.lower() == 'roof sheet':
#                         placeholder_text = "🏗️ Roof Sheet"
#                     elif category_name and category_name.lower() == 'limination sheet':
#                         placeholder_text = "📄 Limination Sheet"
#                     elif category_name and category_name.lower() == 'hardware':
#                         placeholder_text = "🔧 Hardware"
#                     else:
#                         placeholder_text = "📦 No Image"
                        
#                     placeholder = tk.Label(
#                         image_frame, 
#                         text=placeholder_text, 
#                         font=('Arial', 10),  # Reduced font size
#                         bg='#e0e0e0',
#                         fg='#7f8c8d'
#                     )
#                     placeholder.pack(expand=True, fill='both')
#             except Exception as e:
#                 placeholder = tk.Label(
#                     image_frame, 
#                     text="🖼️ Error", 
#                     font=('Arial', 9),  # Reduced font size
#                     bg='#e0e0e0',
#                     fg='#e74c3c'
#                 )
#                 placeholder.pack(expand=True, fill='both')
            
#             # 2. Product Details - MIDDLE with FLEXIBLE SPACE
#             details_frame = tk.Frame(card_frame, bg='white')
#             details_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)  # Reduced padding
            
#             # Format prices in PKR
#             def format_price(price):
#                 try:
#                     return "₨{:,.0f}".format(float(price))
#                 except:
#                     return "₨0"
            
#             # FIXED: Updated labels from "Purchase" to "Purchase Price" and "Sale" to "Sale Price"
#             if category_name and category_name.lower() == 'paint':
#                 # Paint category - simplified fields (NO MEASUREMENT)
#                 details = [
#                     ("Company", company),
#                     ("Type", product_type),
#                     ("Color", color),
#                     ("Packing", packing),
#                     ("Purchase Price", format_price(purchase_price)),  # CHANGED
#                     ("Sale Price", format_price(sale_price)),          # CHANGED
#                     ("Stock", f"{current_stock} units")
#                 ]
#             else:
#                 # ALL OTHER CATEGORIES - WITH MEASUREMENT SYSTEM
#                 details = [
#                     ("Company", company),
#                     ("Type", product_type),
#                     ("Color", color),
#                     ("Purchase Price", format_price(purchase_price)),  # CHANGED
#                     ("Sale Price", format_price(sale_price))           # CHANGED
#                 ]
                
#                 # Add size/volume for relevant categories
#                 if volume and volume != "N/A":
#                     if category_name and category_name.lower() == 'sanitary':
#                         details.insert(3, ("Size", volume))
#                     elif category_name and category_name.lower() in ['roof sheet', 'limination sheet']:
#                         details.insert(3, ("Size", volume))
                
#                 # Add measurement-based stock display
#                 if packing and packing.startswith("Unit: "):
#                     measurement_name = packing.replace("Unit: ", "")
#                     details.append(("Stock", f"{current_stock} {measurement_name}"))
#                 else:
#                     details.append(("Stock", f"{current_stock} units"))
            
#             # Create labels for each detail with WRAP LENGTH
#             for i, (label, value) in enumerate(details):
#                 # Create a frame for each row
#                 row_frame = tk.Frame(details_frame, bg='white')
#                 row_frame.pack(fill=tk.X, pady=1)
                
#                 # Label (bold) with INCREASED width for longer labels
#                 lbl = tk.Label(
#                     row_frame,
#                     text=label + ":",
#                     font=('Arial', 10, 'bold'),  # Reduced font size
#                     fg='#2c3e50',
#                     bg='white',
#                     anchor='w',
#                     width=12  # INCREASED FROM 8 TO 12 for longer labels
#                 )
#                 lbl.pack(side=tk.LEFT)
                
#                 # Value with WRAP LENGTH for text adjustment
#                 val_text = str(value)
#                 val = tk.Label(
#                     row_frame,
#                     text=val_text,
#                     font=('Arial', 10),  # Reduced font size
#                     fg='#34495e',
#                     bg='white',
#                     anchor='w',
#                     wraplength=400,  # ADDED WRAP LENGTH - text will wrap after 80 pixels
#                     justify='left'
#                 )
#                 val.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
#             # 3. Action buttons - BOTTOM with REDUCED layout
#             button_frame = tk.Frame(card_frame, bg='white')
#             button_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=4, pady=(4, 8))  # Reduced padding
#             button_frame.pack_propagate(False)
#             button_frame.configure(height=18)  # Reduced height
            
#             # Create a container for buttons with fixed width
#             button_container = tk.Frame(button_frame, bg='white')
#             button_container.pack(fill=tk.X, expand=True)
            
#             # Edit Button with smaller font
#             edit_btn = tk.Button(
#                 button_container,
#                 text="✏️ Edit",
#                 font=('Arial', 8, 'bold'),  # Reduced font size
#                 bg='#3498db',
#                 fg='white',
#                 relief='raised',
#                 bd=1,
#                 width=3,     # Reduced width
#                 height=1,    # Reduced height
#                 cursor='hand2',
#                 command=lambda pid=product_id: self.edit_product(pid)
#             )
#             edit_btn.pack(side=tk.LEFT, padx=(0, 3), fill=tk.X, expand=True)  # Reduced padding
            
#             # Delete Button with smaller font
#             delete_btn = tk.Button(
#                 button_container,
#                 text="🗑️ Delete",
#                 font=('Arial', 8, 'bold'),  # Reduced font size
#                 bg='#e74c3c',
#                 fg='white',
#                 relief='raised',
#                 bd=1,
#                 width=3,     # Reduced width
#                 height=1,    # Reduced height
#                 cursor='hand2',
#                 command=lambda pid=product_id: self.delete_product(pid)
#             )
#             delete_btn.pack(side=tk.RIGHT, padx=(3, 0), fill=tk.X, expand=True)  # Reduced padding
            
#             return outer_frame
            
#         except Exception as e:
#             print(f"Error creating product card: {e}")
#             return None

#     def add_product(self):
#         """Add new product using universal form"""
#         if not self.current_category:
#             messagebox.showwarning("Warning", "Please select a category first!")
#             return
        
#         try:
#             categories = self.category_service.get_all_categories()
#             category_name = ""
#             for cat in categories:
#                 if cat[0] == self.current_category:
#                     category_name = cat[1]
#                     break
            
#             # Use Universal Form for ALL categories
#             UniversalProductForm(
#                 parent=self.parent,
#                 product_service=self.product_service,
#                 current_category=self.current_category,
#                 refresh_callback=lambda: self.load_products(self.current_category),
#                 category_name=category_name
#             )
                
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to add product: {str(e)}")

#     def edit_product(self, product_id):
#         """Edit product from selected category"""
#         try:
#             # Find product in current category
#             products = self.product_service.get_products_by_category(self.current_category)
#             product_data = None
#             category_name = self.selected_category_name
            
#             for product in products:
#                 if product[0] == product_id:
#                     product_data = self.unpack_product_data(product)
#                     break
            
#             if not product_data:
#                 messagebox.showerror("Error", "Product not found!")
#                 return
            
#             # Use Universal Form for editing
#             UniversalProductForm(
#                 parent=self.parent,
#                 product_service=self.product_service,
#                 current_category=self.current_category,
#                 refresh_callback=lambda: self.load_products(self.current_category),
#                 category_name=category_name,
#                 product_id=product_id,
#                 product_data=product_data
#             )
            
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to edit product: {str(e)}")

#     def unpack_product_data(self, product):
#         """Helper to unpack product data for editing"""
#         try:
#             if len(product) >= 14:
#                 product_id = product[0]
#                 category_id = product[1]
#                 company = product[2]
#                 product_type = product[3]
#                 color = product[4]
#                 sale_price = product[5]
#                 purchase_price = product[6]
#                 packing = product[7]  # This stores measurement info or Color Code for Limination Sheet
#                 volume = product[8]
#                 current_stock = product[9]
#                 image_path = product[10]
#                 created_at = product[11]
#                 updated_at = product[12]
#                 category_name = product[13] if len(product) > 13 else "Unknown"
#             elif len(product) == 13:
#                 product_id = product[0]
#                 category_id = product[1]
#                 company = product[2]
#                 product_type = product[3]
#                 sale_price = product[4]
#                 purchase_price = product[5]
#                 packing = product[6]  # This stores measurement info or Color Code for Limination Sheet
#                 volume = product[7]
#                 current_stock = product[8]
#                 image_path = product[9]
#                 created_at = product[10]
#                 updated_at = product[11]
#                 category_name = product[12]
#                 color = "N/A"
#             else:
#                 return None
            
#             return {
#                 'category_id': category_id,
#                 'company': company,
#                 'type': product_type,
#                 'color': color,
#                 'sale_price': sale_price,
#                 'purchase_price': purchase_price,
#                 'packing': packing,  # This will be used for measurement system
#                 'volume': volume,
#                 'current_stock': current_stock,
#                 'image_path': image_path
#             }
#         except Exception as e:
#             print(f"Error unpacking product: {e}")
#             return None

#     def delete_product(self, product_id):
#         """Delete product functionality"""
#         result = messagebox.askyesno(
#             "Confirm Delete", 
#             "Are you sure you want to delete this product?\nThis action cannot be undone."
#         )
#         if result:
#             try:
#                 deleted_count = self.product_service.delete_product(product_id)
#                 if deleted_count > 0:
#                     messagebox.showinfo("Success", "Product deleted successfully!")
#                     self.load_products(self.current_category)  # Refresh current category
#                 else:
#                     messagebox.showerror("Error", "Failed to delete product!")
#             except Exception as e:
#                 messagebox.showerror("Error", f"Failed to delete product: {str(e)}")