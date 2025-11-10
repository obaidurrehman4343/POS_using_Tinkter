import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.database import Database
from PIL import Image, ImageTk
import os
from frontend.roof_sheet import RoofSheetForm

class InventoryManagement:
    def __init__(self, parent):
        self.parent = parent
        self.db = Database()
        self.current_category = None
        self.selected_category_name = None  # 🆕 ADDED: Initialize category memory
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="📦 Inventory Management",
            font=('Arial', 20, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(side=tk.LEFT)
        
        # Add Category Button
        add_category_btn = tk.Button(
            header_frame,
            text="+ Add Category",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.add_category,
            cursor='hand2'
        )
        add_category_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Add Product Button
        self.add_product_btn = tk.Button(
            header_frame,
            text="+ Add Product",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.add_product,
            cursor='hand2',
            state='disabled'
        )
        self.add_product_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Category Selection Frame
        category_frame = tk.Frame(main_frame, bg='#f8f9fa', relief='solid', bd=1, padx=15, pady=15)
        category_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            category_frame,
            text="Select Category:",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Category Dropdown
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(
            category_frame,
            textvariable=self.category_var,
            state='readonly',
            width=20,
            font=('Arial', 11)
        )
        self.category_dropdown.pack(side=tk.LEFT, padx=(0, 10))
        self.category_dropdown.bind('<<ComboboxSelected>>', self.on_category_select)
        
        # Refresh Categories Button
        refresh_btn = tk.Button(
            category_frame,
            text="🔄 Refresh",
            font=('Arial', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=self.load_categories,
            cursor='hand2'
        )
        refresh_btn.pack(side=tk.LEFT)
        
        # Products Container
        self.products_container = tk.Frame(main_frame, bg='white')
        self.products_container.pack(fill=tk.BOTH, expand=True)
        
        # Initial load
        self.load_categories()

    def load_categories(self):
        categories = self.db.get_all_categories()
        category_names = [category[1] for category in categories]
        self.category_dropdown['values'] = category_names
        
        if category_names:
            # 🆕 FIXED: Only set category if we have a remembered selection
            if self.selected_category_name and self.selected_category_name in category_names:
                self.category_var.set(self.selected_category_name)
                self.on_category_select()
            else:
                # 🆕 Don't automatically select any category - leave it empty
                self.category_var.set('')  # Empty selection
                self.add_product_btn.config(state='disabled')
                self.show_select_category_message()
        else:
            self.category_var.set('')
            self.add_product_btn.config(state='disabled')
            self.show_no_categories_message()

    def on_category_select(self, event=None):
        category_name = self.category_var.get()
        if category_name:
            # Remember the selected category name
            self.selected_category_name = category_name
            
            categories = self.db.get_all_categories()
            category_id = None
            for cat in categories:
                if cat[1] == category_name:
                    category_id = cat[0]
                    break
            
            if category_id:
                self.current_category = category_id
                self.add_product_btn.config(state='normal')
                self.load_products(category_id)
        else:
            # 🆕 Handle case when category is deselected
            self.current_category = None
            self.add_product_btn.config(state='disabled')
            self.show_select_category_message()
        
    def show_select_category_message(self):
        """Show message when no category is selected"""
        for widget in self.products_container.winfo_children():
            widget.destroy()
        
        empty_frame = tk.Frame(self.products_container, bg='white')
        empty_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            empty_frame,
            text="📁 Please Select a Category",
            font=('Arial', 18, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(expand=True, pady=(100, 20))
        
        tk.Label(
            empty_frame,
            text="Choose a category from dropdown to view products",
            font=('Arial', 12),
            fg='#7f8c8d',
            bg='white'
        ).pack(expand=True, pady=10)
    
    def show_no_categories_message(self):
        """Show message when no categories exist"""
        for widget in self.products_container.winfo_children():
            widget.destroy()
        
        empty_frame = tk.Frame(self.products_container, bg='white')
        empty_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            empty_frame,
            text="📂 No Categories Found",
            font=('Arial', 18, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(expand=True, pady=(100, 20))
        
        tk.Label(
            empty_frame,
            text="Click 'Add Category' to create your first category",
            font=('Arial', 12),
            fg='#7f8c8d',
            bg='white'
        ).pack(expand=True, pady=10)

    def add_product(self):
        """Add new product"""
        if not self.current_category:
            messagebox.showwarning("Warning", "Please select a category first!")
            return
        
        # Get category name for form customization
        categories = self.db.get_all_categories()
        category_name = ""
        for cat in categories:
            if cat[0] == self.current_category:
                category_name = cat[1]
                break
        
        # Open product form based on category
        if category_name.lower() == 'paint':
            self.open_paint_form()
        elif category_name.lower() == 'roof sheet':
            # 🆕 Use Roof Sheet Form
            RoofSheetForm(
                parent=self.parent,
                db=self.db,
                current_category=self.current_category,
                refresh_callback=lambda: self.load_products(self.current_category)
            )
        else:
            self.open_generic_form(category_name)
    
    def load_products(self, category_id):
        # Clear existing content
        for widget in self.products_container.winfo_children():
            widget.destroy()
        
        products = self.db.get_products_by_category(category_id)
        
        if not products:
            # Show empty state
            empty_frame = tk.Frame(self.products_container, bg='white')
            empty_frame.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(
                empty_frame,
                text="📭 No products found in this category",
                font=('Arial', 16),
                fg='#7f8c8d',
                bg='white'
            ).pack(expand=True, pady=50)
            
            tk.Label(
                empty_frame,
                text="Click 'Add Product' to add your first product",
                font=('Arial', 12),
                fg='#bdc3c7',
                bg='white'
            ).pack(expand=True, pady=10)
            return
        
        # Create grid card view
        self.create_grid_card_view(products)
    
    def create_grid_card_view(self, products):
        """Create grid layout with 4 cards per row"""
        # Clear existing content
        for widget in self.products_container.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        canvas = tk.Canvas(self.products_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.products_container, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create cards in grid layout with proper spacing
        row = 0
        col = 0
        max_cols = 4  # Reduced from 5 to 4 for better spacing
        
        for product in products:
            # Create card
            card = self.create_product_card(scrollable_frame, product)
            
            # Place card in grid with proper spacing
            card.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            # Configure grid weights for responsive layout
            scrollable_frame.grid_columnconfigure(col, weight=1)
            scrollable_frame.grid_rowconfigure(row, weight=0)
            
            # Move to next position
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # If there are remaining columns in the last row, configure them
        for i in range(col, max_cols):
            scrollable_frame.grid_columnconfigure(i, weight=1)
    
    def create_product_card(self, parent, product):
        # Handle different database schemas
        try:
            if len(product) == 14:  # New schema with color (14 values)
                (product_id, category_id, company, product_type, color,
                sale_price, purchase_price, packing, volume, current_stock, 
                image_path, created_at, updated_at, category_name) = product
            elif len(product) == 13:  # Schema without color
                (product_id, category_id, company, product_type, 
                sale_price, purchase_price, packing, volume, current_stock, 
                image_path, created_at, updated_at, category_name) = product
                color = "N/A"
            else:
                (product_id, category_id, company, product_type, product_name,
                sale_price, purchase_price, packing, volume, current_stock, 
                image_path, created_at, updated_at, category_name) = product
                color = "N/A"
        except ValueError as e:
            print(f"Error unpacking product: {e}")
            print(f"Product tuple: {product}")
            return tk.Frame(parent, width=220, height=350, bg='red')
        
        # Create card frame with MORE HEIGHT for buttons
        card_frame = tk.Frame(
            parent,
            bg='#f8f9fa',
            relief='solid',
            bd=1,
            width=220,
            height=350  # Increased from 320 to 350
        )
        card_frame.pack_propagate(False)
        card_frame.grid_propagate(False)
        
        # Configure grid weights
        card_frame.grid_rowconfigure(0, weight=0)  # Image
        card_frame.grid_rowconfigure(1, weight=1)  # Details
        card_frame.grid_rowconfigure(2, weight=0)  # Buttons
        
        # 1. Product Image - TOP
        image_frame = tk.Frame(card_frame, bg='#e0e0e0', height=120)
        image_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=(10, 5))
        
        try:
            if image_path and os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(image_frame, image=photo, bg='#e0e0e0')
                img_label.image = photo
                img_label.pack(expand=True, fill='both')
            else:
                # 🆕 Category-specific placeholder icons
                if category_name and category_name.lower() == 'roof sheet':
                    placeholder_text = "🏗️ Roof Sheet"
                elif category_name and category_name.lower() == 'paint':
                    placeholder_text = "🎨 Paint"
                else:
                    placeholder_text = "🖼️ No Image"
                    
                placeholder = tk.Label(
                    image_frame, 
                    text=placeholder_text, 
                    font=('Arial', 10),
                    bg='#e0e0e0',
                    fg='#7f8c8d'
                )
                placeholder.pack(expand=True, fill='both')
        except Exception as e:
            placeholder = tk.Label(
                image_frame, 
                text="🖼️ Image Error", 
                font=('Arial', 10),
                bg='#e0e0e0',
                fg='#e74c3c'
            )
            placeholder.pack(expand=True, fill='both')
        
        # 2. Product Details - MIDDLE (Expandable)
        details_frame = tk.Frame(card_frame, bg='#f8f9fa')
        details_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        
        # Format prices in PKR
        def format_price(price):
            try:
                return "{:,.0f} PKR".format(float(price))
            except:
                return "0 PKR"
        
        # 🆕 DIFFERENT DETAILS FOR DIFFERENT CATEGORIES
        if category_name and category_name.lower() == 'roof sheet':
            # Roof Sheet specific details
            details = [
                ("Company", company),
                ("Type", product_type),
                ("Color", color),
                ("Volume", volume or "N/A"),  # 🆕 Show Volume instead of Packing
                ("Purchase", format_price(purchase_price)),
                ("Sale", format_price(sale_price)),
                ("Stock", f"{current_stock} sheets")  # 🆕 Show "sheets" instead of "units"
            ]
        elif category_name and category_name.lower() == 'paint':
            # Paint specific details
            details = [
                ("Company", company),
                ("Type", product_type),
                ("Color", color),
                ("Packing", packing or "N/A"),
                ("Purchase", format_price(purchase_price)),
                ("Sale", format_price(sale_price)),
                ("Stock", f"{current_stock} units")
            ]
        else:
            # Default for other categories
            details = [
                ("Company", company),
                ("Type", product_type),
                ("Color", color),
                ("Packing", packing or "N/A"),
                ("Purchase", format_price(purchase_price)),
                ("Sale", format_price(sale_price)),
                ("Stock", f"{current_stock} units")
            ]
        
        # Create labels for each detail
        for i, (label, value) in enumerate(details):
            # Create a frame for each row
            row_frame = tk.Frame(details_frame, bg='#f8f9fa')
            row_frame.pack(fill=tk.X, pady=1)
            
            # Label (bold)
            lbl = tk.Label(
                row_frame,
                text=label + ":",
                font=('Arial', 9, 'bold'),
                fg='#2c3e50',
                bg='#f8f9fa',
                anchor='w',
                width=8
            )
            lbl.pack(side=tk.LEFT)
            
            # Value
            val = tk.Label(
                row_frame,
                text=str(value)[:15] + ("..." if len(str(value)) > 15 else ""),  # Truncate long text
                font=('Arial', 9),
                fg='#34495e',
                bg='#f8f9fa',
                anchor='w'
            )
            val.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 3. Action buttons - BOTTOM (ALWAYS VISIBLE)
        button_frame = tk.Frame(card_frame, bg='#f8f9fa', height=40)
        button_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=(5, 10))
        button_frame.grid_propagate(False)  # Fixed height for buttons
        
        # Configure button frame grid
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        # Single Edit Button
        edit_btn = tk.Button(
            button_frame,
            text="✏️ Edit",
            font=('Arial', 9, 'bold'),
            bg='#3498db',
            fg='white',
            relief='raised',
            bd=1,
            command=lambda pid=product_id: self.edit_product(pid)
        )
        edit_btn.grid(row=0, column=0, padx=(0, 5), sticky='ew')
        
        # Single Delete Button  
        delete_btn = tk.Button(
            button_frame,
            text="🗑️ Delete",
            font=('Arial', 9, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='raised',
            bd=1,
            command=lambda pid=product_id: self.delete_product(pid)
        )
        delete_btn.grid(row=0, column=1, padx=(5, 0), sticky='ew')
        
        return card_frame

    def edit_product(self, product_id):
        """Edit product functionality"""
        # Get product data from database
        products = self.db.get_all_products()
        product_data = None
        category_name = ""
        
        for product in products:
            if product[0] == product_id:
                product_data = product
                # Get category name from the product tuple (last element)
                category_name = product[-1] if len(product) > 13 else ""
                break
        
        if not product_data:
            messagebox.showerror("Error", "Product not found!")
            return
        
        # Unpack product data based on schema
        if len(product_data) == 14:
            (pid, category_id, company, ptype, color,
            sale_price, purchase_price, packing, volume, current_stock, 
            image_path, created_at, updated_at, category_name) = product_data
        else:
            messagebox.showerror("Error", "Cannot edit this product format")
            return
        
        # 🆕 Open appropriate edit dialog based on category
        if category_name and category_name.lower() == 'roof sheet':
            # Use roof sheet specific edit dialog
            self.open_roof_sheet_edit_dialog(product_id, {
                'company': company,
                'type': ptype,
                'color': color,
                'volume': volume,  # Volume for dimensions
                'sale_price': sale_price,
                'purchase_price': purchase_price,
                'current_stock': current_stock,
                'image_path': image_path,
                'category_id': category_id
            })
        else:
            # Use existing edit dialog for other categories (paint, etc.)
            self.open_edit_dialog(product_id, {
                'company': company,
                'type': ptype,
                'color': color,
                'packing': packing,  # Packing for paint
                'volume': volume,
                'sale_price': sale_price,
                'purchase_price': purchase_price,
                'current_stock': current_stock,
                'image_path': image_path,
                'category_id': category_id
            })

    def open_roof_sheet_edit_dialog(self, product_id, product_data):
        """Open roof sheet specific edit dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Edit Roof Sheet Product")
        dialog.geometry("450x550")  # Smaller size
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # 🆕 Position within dashboard boundaries
        self.parent.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Form dimensions
        form_width = 450
        form_height = 550
        
        # Calculate position to keep form within parent bounds
        # Position near the top-right area of the dashboard
        x = parent_x + parent_width - form_width - 20  # 20px from right edge
        y = parent_y + 100  # 100px from top
        
        # Ensure form doesn't go outside screen
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        # Check if form would go outside right edge
        if x + form_width > screen_width:
            x = screen_width - form_width - 20
        
        # Check if form would go outside bottom edge
        if y + form_height > screen_height:
            y = screen_height - form_height - 20
        
        dialog.geometry(f"{form_width}x{form_height}+{x}+{y}")
        
        # Create scrollable form
        canvas = tk.Canvas(dialog, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Form Title
        tk.Label(
            scrollable_frame,
            text="Edit Roof Sheet Product",
            font=('Arial', 18, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 20))
        
        # Image Upload Section
        image_frame = tk.Frame(scrollable_frame, bg='white')
        image_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            image_frame,
            text="Product Image:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        image_path_var = tk.StringVar(value=product_data['image_path'])
        image_entry = tk.Entry(
            image_frame, 
            textvariable=image_path_var,
            font=('Arial', 11), 
            relief='solid', 
            bd=1,
            state='readonly'
        )
        image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(0, 10))
        
        def browse_image():
            file_path = filedialog.askopenfilename(
                title="Select Product Image",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
            )
            if file_path:
                image_path_var.set(file_path)
        
        browse_btn = tk.Button(
            image_frame,
            text="Browse",
            font=('Arial', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=browse_image
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # 🏗️ Roof Sheet Specific Fields (NO PACKING FIELD)
        fields = [
            ("Company", "text", product_data['company']),
            ("Type", "text", product_data['type']),
            ("Color", "text", product_data['color']),
            ("Volume", "text", product_data.get('volume', '')),  # 🆕 Volume instead of Packing
            ("Purchase Price", "number", product_data['purchase_price']),
            ("Sale Price", "number", product_data['sale_price']),
            ("Stock", "number", product_data['current_stock'])
        ]
        
        entries = {}
        
        for field_name, field_type, default_value in fields:
            frame = tk.Frame(scrollable_frame, bg='white')
            frame.pack(fill=tk.X, pady=8)
            
            tk.Label(
                frame,
                text=f"{field_name}:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white',
                width=15,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            if field_type == 'number':
                entry = tk.Entry(frame, font=('Arial', 11), relief='solid', bd=1, validate='key')
                entry.config(validatecommand=(entry.register(self.validate_number), '%P'))
            else:
                entry = tk.Entry(frame, font=('Arial', 11), relief='solid', bd=1)
            
            # Set default value
            entry.insert(0, str(default_value))
            
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
            entries[field_name] = entry
        
        # Buttons
        button_frame = tk.Frame(scrollable_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=20)
        
        def update_product():
            try:
                updated_data = {
                    'category_id': product_data['category_id'],
                    'company': entries['Company'].get().strip(),
                    'type': entries['Type'].get().strip(),
                    'color': entries['Color'].get().strip(),
                    'sale_price': float(entries['Sale Price'].get() or 0),
                    'purchase_price': float(entries['Purchase Price'].get() or 0),
                    'packing': "",  # 🆕 Empty for roof sheets
                    'volume': entries['Volume'].get().strip(),  # 🆕 Using 'volume' column for size
                    'current_stock': int(entries['Stock'].get() or 0),
                    'image_path': image_path_var.get()
                }
                
                # Validate required fields - Volume instead of Packing
                required_fields = ['Company', 'Type', 'Color', 'Volume']
                for field in required_fields:
                    if not entries[field].get().strip():
                        messagebox.showerror("Error", f"{field} is required!")
                        return
                
                # Use UPDATE for roof sheet
                updated_count = self.db.update_product(product_id, updated_data)
                
                if updated_count > 0:
                    messagebox.showinfo("Success", "Roof Sheet updated successfully!")
                    dialog.destroy()
                    self.load_products(self.current_category)
                else:
                    messagebox.showerror("Error", "Failed to update roof sheet!")
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for price and stock!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update roof sheet: {str(e)}")
        
        update_btn = tk.Button(
            button_frame,
            text="Update Roof Sheet",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=update_product
        )
        update_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 12),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=dialog.destroy
        )
        cancel_btn.pack(side=tk.RIGHT)
        
        # Set focus to first field
        entries['Company'].focus()

    def open_edit_dialog(self, product_id, product_data):
        """Open edit dialog with existing product data"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Edit Product")
        dialog.geometry("450x550")  # Smaller size
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # 🆕 Position within dashboard boundaries
        self.parent.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Form dimensions
        form_width = 450
        form_height = 550
        
        # Calculate position to keep form within parent bounds
        # Position near the top-right area of the dashboard
        x = parent_x + parent_width - form_width - 20  # 20px from right edge
        y = parent_y + 100  # 100px from top
        
        # Ensure form doesn't go outside screen
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        # Check if form would go outside right edge
        if x + form_width > screen_width:
            x = screen_width - form_width - 20
        
        # Check if form would go outside bottom edge
        if y + form_height > screen_height:
            y = screen_height - form_height - 20
        
        dialog.geometry(f"{form_width}x{form_height}+{x}+{y}")
        
        # Create scrollable form
        canvas = tk.Canvas(dialog, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Form Title
        tk.Label(
            scrollable_frame,
            text="Edit Product",
            font=('Arial', 18, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 20))
        
        # Image Upload Section
        image_frame = tk.Frame(scrollable_frame, bg='white')
        image_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            image_frame,
            text="Product Image:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        image_path_var = tk.StringVar(value=product_data['image_path'])
        image_entry = tk.Entry(
            image_frame, 
            textvariable=image_path_var,
            font=('Arial', 11), 
            relief='solid', 
            bd=1,
            state='readonly'
        )
        image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(0, 10))
        
        def browse_image():
            file_path = filedialog.askopenfilename(
                title="Select Product Image",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
            )
            if file_path:
                image_path_var.set(file_path)
        
        browse_btn = tk.Button(
            image_frame,
            text="Browse",
            font=('Arial', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=browse_image
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Form fields
        fields = [
            ("Company", "text", product_data['company']),
            ("Type", "text", product_data['type']),
            ("Color", "text", product_data['color']),
            ("Packing", "text", product_data['packing']),
            ("Volume", "text", product_data['volume']),
            ("Purchase Price", "number", product_data['purchase_price']),
            ("Sale Price", "number", product_data['sale_price']),
            ("Stock", "number", product_data['current_stock'])
        ]
        
        entries = {}
        
        for field_name, field_type, default_value in fields:
            frame = tk.Frame(scrollable_frame, bg='white')
            frame.pack(fill=tk.X, pady=8)
            
            tk.Label(
                frame,
                text=f"{field_name}:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white',
                width=15,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            if field_type == 'number':
                entry = tk.Entry(frame, font=('Arial', 11), relief='solid', bd=1, validate='key')
                entry.config(validatecommand=(entry.register(self.validate_number), '%P'))
            else:
                entry = tk.Entry(frame, font=('Arial', 11), relief='solid', bd=1)
            
            # Set default value
            entry.insert(0, str(default_value))
            
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
            entries[field_name] = entry
        
        # Buttons
        button_frame = tk.Frame(scrollable_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=20)
    
        def update_product():
            try:
                updated_data = {
                    'category_id': product_data['category_id'],
                    'company': entries['Company'].get().strip(),
                    'type': entries['Type'].get().strip(),
                    'color': entries['Color'].get().strip(),
                    'sale_price': float(entries['Sale Price'].get() or 0),
                    'purchase_price': float(entries['Purchase Price'].get() or 0),
                    'packing': entries['Packing'].get().strip(),
                    'volume': entries['Volume'].get().strip(),
                    'current_stock': int(entries['Stock'].get() or 0),
                    'image_path': image_path_var.get()
                }
                
                # Validate required fields
                required_fields = ['Company', 'Type', 'Color', 'Packing']
                for field in required_fields:
                    if not entries[field].get().strip():
                        messagebox.showerror("Error", f"{field} is required!")
                        return
                
                # Use UPDATE instead of DELETE+ADD
                updated_count = self.db.update_product(product_id, updated_data)
                
                if updated_count > 0:
                    messagebox.showinfo("Success", "Product updated successfully!")
                    dialog.destroy()
                    self.load_products(self.current_category)
                else:
                    messagebox.showerror("Error", "Failed to update product!")
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for price and stock!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update product: {str(e)}")
        
        update_btn = tk.Button(
            button_frame,
            text="Update Product",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=update_product
        )
        update_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 12),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=dialog.destroy
        )
        cancel_btn.pack(side=tk.RIGHT)
        
        # Set focus to first field
        entries['Company'].focus()

    def delete_product(self, product_id):
        """Delete product functionality"""
        result = messagebox.askyesno(
            "Confirm Delete", 
            "Are you sure you want to delete this product?\nThis action cannot be undone."
        )
        if result:
            try:
                deleted_count = self.db.delete_product(product_id)
                if deleted_count > 0:
                    messagebox.showinfo("Success", "Product deleted successfully!")
                    self.load_products(self.current_category)
                else:
                    messagebox.showerror("Error", "Failed to delete product!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product: {str(e)}")

    def add_category(self):
        """Add new category"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add New Category")
        dialog.geometry("400x200")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        tk.Label(
            dialog,
            text="Add New Category",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(pady=20)
        
        # Category Name
        name_frame = tk.Frame(dialog, bg='white')
        name_frame.pack(fill=tk.X, padx=30, pady=10)
        
        tk.Label(
            name_frame,
            text="Category Name:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w')
        
        name_entry = tk.Entry(
            name_frame,
            font=('Arial', 12),
            relief='solid',
            bd=1
        )
        name_entry.pack(fill=tk.X, pady=(5, 0), ipady=5)
        
        # Description
        desc_frame = tk.Frame(dialog, bg='white')
        desc_frame.pack(fill=tk.X, padx=30, pady=10)
        
        tk.Label(
            desc_frame,
            text="Description (Optional):",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w')
        
        desc_entry = tk.Entry(
            desc_frame,
            font=('Arial', 12),
            relief='solid',
            bd=1
        )
        desc_entry.pack(fill=tk.X, pady=(5, 0), ipady=5)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.pack(fill=tk.X, padx=30, pady=20)
        
        def save_category():
            name = name_entry.get().strip()
            description = desc_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Category name is required!")
                return
            
            try:
                self.db.add_category(name, description)
                messagebox.showinfo("Success", f"Category '{name}' added successfully!")
                dialog.destroy()
                
                # Auto-select the newly added category
                self.selected_category_name = name
                self.load_categories()  # This will now select the new category
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add category: {str(e)}")
        
        save_btn = tk.Button(
            button_frame,
            text="Save Category",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=save_category
        )
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 11),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=dialog.destroy
        )
        cancel_btn.pack(side=tk.RIGHT)
        
        name_entry.focus()
    
    def open_paint_form(self):
        """Open paint product form"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add Paint Product")
        dialog.geometry("450x550")  # Smaller size
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # 🆕 Position within dashboard boundaries
        self.parent.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Form dimensions
        form_width = 450
        form_height = 550
        
        # Calculate position to keep form within parent bounds
        # Position near the top-right area of the dashboard
        x = parent_x + parent_width - form_width - 20  # 20px from right edge
        y = parent_y + 100  # 100px from top
        
        # Ensure form doesn't go outside screen
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        # Check if form would go outside right edge
        if x + form_width > screen_width:
            x = screen_width - form_width - 20
        
        # Check if form would go outside bottom edge
        if y + form_height > screen_height:
            y = screen_height - form_height - 20
        
        dialog.geometry(f"{form_width}x{form_height}+{x}+{y}")
        
        # Create scrollable form
        canvas = tk.Canvas(dialog, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)  # 🆕 Smaller padding
        scrollbar.pack(side="right", fill="y")
        
        # Form Title
        tk.Label(
            scrollable_frame,
            text="Add Paint Product",
            font=('Arial', 16, 'bold'),  # 🆕 Smaller font
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 15))  # 🆕 Smaller padding
        
        # Image Upload Section
        image_frame = tk.Frame(scrollable_frame, bg='white')
        image_frame.pack(fill=tk.X, pady=8)  # 🆕 Smaller padding
        
        tk.Label(
            image_frame,
            text="Product Image:",
            font=('Arial', 10, 'bold'),  # 🆕 Smaller font
            fg='#2c3e50',
            bg='white',
            width=12,  # 🆕 Smaller width
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.image_path_var = tk.StringVar()
        image_entry = tk.Entry(
            image_frame, 
            textvariable=self.image_path_var,
            font=('Arial', 10),  # 🆕 Smaller font
            relief='solid', 
            bd=1,
            state='readonly'
        )
        image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(0, 8))  # 🆕 Smaller padding
        
        def browse_image():
            file_path = filedialog.askopenfilename(
                title="Select Product Image",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
            )
            if file_path:
                self.image_path_var.set(file_path)
        
        browse_btn = tk.Button(
            image_frame,
            text="Browse",
            font=('Arial', 9),  # 🆕 Smaller font
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=browse_image
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Form fields for paint
        fields = [
            ("Company", "text"),
            ("Type", "text"),
            ("Color", "text"),
            ("Packing", "text"),
            ("Volume", "text"),
            ("Purchase Price", "number"),
            ("Sale Price", "number"),
            ("Stock", "number")
        ]
        
        entries = {}
        
        for field_name, field_type in fields:
            frame = tk.Frame(scrollable_frame, bg='white')
            frame.pack(fill=tk.X, pady=6)  # 🆕 Smaller padding
            
            tk.Label(
                frame,
                text=f"{field_name}:",
                font=('Arial', 10, 'bold'),  # 🆕 Smaller font
                fg='#2c3e50',
                bg='white',
                width=12,  # 🆕 Smaller width
                anchor='w'
            ).pack(side=tk.LEFT)
            
            if field_type == 'number':
                entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1, validate='key')  # 🆕 Smaller font
                entry.config(validatecommand=(entry.register(self.validate_number), '%P'))
            else:
                entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1)  # 🆕 Smaller font
            
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)  # 🆕 Smaller padding
            entries[field_name] = entry
        
        # Buttons
        button_frame = tk.Frame(scrollable_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=15)  # 🆕 Smaller padding
        
        def save_product():
            try:
                product_data = {
                    'category_id': self.current_category,
                    'company': entries['Company'].get().strip(),
                    'type': entries['Type'].get().strip(),
                    'color': entries['Color'].get().strip(),
                    'sale_price': float(entries['Sale Price'].get() or 0),
                    'purchase_price': float(entries['Purchase Price'].get() or 0),
                    'packing': entries['Packing'].get().strip(),
                    'volume': entries['Volume'].get().strip(),
                    'current_stock': int(entries['Stock'].get() or 0),
                    'image_path': self.image_path_var.get()
                }
                
                # Validate required fields
                required_fields = ['Company', 'Type', 'Color', 'Packing']
                for field in required_fields:
                    if not entries[field].get().strip():
                        messagebox.showerror("Error", f"{field} is required!")
                        return
                
                self.db.add_product(product_data)
                messagebox.showinfo("Success", "Product added successfully!")
                dialog.destroy()
                self.load_products(self.current_category)
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for price and stock!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add product: {str(e)}")
        
        save_btn = tk.Button(
            button_frame,
            text="Save Product",
            font=('Arial', 11, 'bold'),  # 🆕 Smaller font
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=save_product
        )
        save_btn.pack(side=tk.RIGHT, padx=(8, 0))  # 🆕 Smaller padding
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 11),  # 🆕 Smaller font
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=dialog.destroy
        )
        cancel_btn.pack(side=tk.RIGHT)
        
        # Set focus to first field
        entries['Company'].focus()
    
    def open_generic_form(self, category_name):
        """Open product form for other categories"""
        if category_name.lower() == 'roof sheet':
            # This shouldn't happen now, but keep as fallback
            RoofSheetForm(
                parent=self.parent,
                db=self.db,
                current_category=self.current_category,
                refresh_callback=lambda: self.load_products(self.current_category)
            )
        else:
            messagebox.showinfo("Info", f"Add product form for {category_name} category")
    
    def validate_number(self, value):
        """Validate number input"""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False