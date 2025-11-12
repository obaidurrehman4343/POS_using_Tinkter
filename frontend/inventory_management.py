
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.product_service import ProductService
from backend.category_service import CategoryService
from PIL import Image, ImageTk
import os
from frontend.roof_sheet import RoofSheetForm
from frontend.limination_sheet import LiminationSheetForm
from frontend.sanitary import SanitaryForm
from frontend.paint_form import PaintForm

class InventoryManagement:
    def __init__(self, parent):
        self.parent = parent
        self.product_service = ProductService()
        self.category_service = CategoryService()
        self.current_category = None
        self.selected_category_name = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the complete UI for inventory management"""
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
        """Load categories from backend service"""
        try:
            categories = self.category_service.get_all_categories()
            category_names = [category[1] for category in categories]
            self.category_dropdown['values'] = category_names
            
            if category_names:
                if self.selected_category_name and self.selected_category_name in category_names:
                    self.category_var.set(self.selected_category_name)
                    self.on_category_select()
                else:
                    self.category_var.set('')
                    self.add_product_btn.config(state='disabled')
                    self.show_select_category_message()
            else:
                self.category_var.set('')
                self.add_product_btn.config(state='disabled')
                self.show_no_categories_message()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load categories: {str(e)}")

    def on_category_select(self, event=None):
        """Handle category selection"""
        category_name = self.category_var.get()
        if category_name:
            self.selected_category_name = category_name
            
            try:
                category_id = self.category_service.get_category_by_name(category_name)
                
                if category_id:
                    self.current_category = category_id
                    self.add_product_btn.config(state='normal')
                    self.load_products(category_id)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load category: {str(e)}")
        else:
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

    def add_category(self):
        """Add new category dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add New Category")
        dialog.geometry("400x200")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center dialog
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
        
        def save_category():
            name = name_entry.get().strip()
            description = desc_entry.get().strip()
            
            try:
                self.category_service.add_category(name, description)
                messagebox.showinfo("Success", f"Category '{name}' added successfully!")
                dialog.destroy()
                
                # Auto-select the newly added category
                self.selected_category_name = name
                self.load_categories()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add category: {str(e)}")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.pack(fill=tk.X, padx=30, pady=20)
        
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

    def add_product(self):
        """Add new product based on category"""
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
            
            # Open product form based on category
            if category_name.lower() == 'paint':
                PaintForm(
                    parent=self.parent,
                    product_service=self.product_service,
                    current_category=self.current_category,
                    refresh_callback=lambda: self.load_products(self.current_category)
                )
            elif category_name.lower() == 'roof sheet':
                RoofSheetForm(
                    parent=self.parent,
                    product_service=self.product_service,
                    current_category=self.current_category,
                    refresh_callback=lambda: self.load_products(self.current_category)
                )
            elif category_name.lower() == 'limination sheet':
                LiminationSheetForm(
                    parent=self.parent,
                    product_service=self.product_service,
                    current_category=self.current_category,
                    refresh_callback=lambda: self.load_products(self.current_category)
                )
            elif category_name.lower() == 'sanitary':
                SanitaryForm(
                    parent=self.parent,
                    product_service=self.product_service,
                    current_category=self.current_category,
                    refresh_callback=lambda: self.load_products(self.current_category)
                )
            else:
                self.open_generic_form(category_name)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {str(e)}")
    
    def load_products(self, category_id):
        """Load products for selected category"""
        # Clear existing content
        for widget in self.products_container.winfo_children():
            widget.destroy()
        
        try:
            products = self.product_service.get_products_by_category(category_id)
            
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
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {str(e)}")
    
    def create_grid_card_view(self, products):
        """Create grid layout with product cards"""
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
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create cards in grid layout with proper spacing
        row = 0
        col = 0
        max_cols = 5
        
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
        """Create individual product card"""
        # Handle different database schemas
        try:
            # Check if it's the old schema (13 columns without color)
            if len(product) == 13:
                (product_id, category_id, company, product_type, 
                 sale_price, purchase_price, packing, volume, current_stock, 
                 image_path, created_at, updated_at, category_name) = product
                color = "N/A"
            # Check if it's the new schema (14 columns with color)
            elif len(product) == 14:
                (product_id, category_id, company, product_type, color,
                 sale_price, purchase_price, packing, volume, current_stock, 
                 image_path, created_at, updated_at, category_name) = product
            else:
                # Default for other schemas
                (product_id, category_id, company, product_type, product_name,
                 sale_price, purchase_price, packing, volume, current_stock, 
                 image_path, created_at, updated_at, category_name) = product
                color = "N/A"
        except ValueError as e:
            print(f"Error unpacking product: {e}")
            print(f"Product tuple: {product}")
            return tk.Frame(parent, width=220, height=350, bg='red')
        
        # Create card frame
        card_frame = tk.Frame(
            parent,
            bg='#f8f9fa',
            relief='solid',
            bd=0,
            width=220,
            height=350
        )
        card_frame.pack_propagate(False)
        card_frame.grid_propagate(False)
        
        # Configure grid weights
        card_frame.grid_rowconfigure(0, weight=0)  # Image
        card_frame.grid_rowconfigure(1, weight=1)  # Details
        card_frame.grid_rowconfigure(2, weight=0)  # Buttons
        
        # 1. Product Image - TOP
        image_frame = tk.Frame(card_frame, bg='#e0e0e0', height=130)
        image_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=(10, 5))
        
        try:
            if image_path and os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((190, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(image_frame, image=photo, bg='#e0e0e0')
                img_label.image = photo
                img_label.pack(expand=True, fill='both')
            else:
                # Category-specific placeholder icons
                if category_name and category_name.lower() == 'roof sheet':
                    placeholder_text = "🏗️ Roof Sheet"
                elif category_name and category_name.lower() == 'limination sheet':
                    placeholder_text = "📄 Limination Sheet"
                elif category_name and category_name.lower() == 'paint':
                    placeholder_text = "🎨 Paint"
                elif category_name and category_name.lower() == 'sanitary':
                    placeholder_text = "🚿 Sanitary"
                else:
                    placeholder_text = "📦 No Image"
                    
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
        
        # DIFFERENT DETAILS FOR DIFFERENT CATEGORIES
        if category_name and category_name.lower() == 'roof sheet':
            # Roof Sheet specific details - SHOW SIZE INSTEAD OF PACKING
            details = [
                ("Company", company),
                ("Type", product_type),
                ("Color", color),
                ("Size", volume or "N/A"),
                ("Purchase", format_price(purchase_price)),
                ("Sale", format_price(sale_price)),
                ("Stock", f"{current_stock} sheets")
            ]
        elif category_name and category_name.lower() == 'limination sheet':
            # Limination Sheet specific details - SHOW SIZE INSTEAD OF PACKING
            details = [
                ("Company", company),
                ("Type", product_type),
                ("Color", color),
                ("Size", volume or "N/A"),
                ("Purchase", format_price(purchase_price)),
                ("Sale", format_price(sale_price)),
                ("Stock", f"{current_stock} sheets")
            ]
        elif category_name and category_name.lower() == 'paint':
            # Paint specific details - KEEP PACKING FOR PAINT
            details = [
                ("Company", company),
                ("Type", product_type),
                ("Color", color),
                ("Packing", packing or "N/A"),
                ("Purchase", format_price(purchase_price)),
                ("Sale", format_price(sale_price)),
                ("Stock", f"{current_stock} units")
            ]
        elif category_name and category_name.lower() == 'sanitary':
            # Sanitary specific details - SHOW SIZE INSTEAD OF PACKING
            details = [
                ("Company", company),
                ("Type", product_type),
                ("Color", color),
                ("Size", volume or "N/A"),
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
                text=str(value)[:15] + ("..." if len(str(value)) > 15 else ""),
                font=('Arial', 9),
                fg='#34495e',
                bg='#f8f9fa',
                anchor='w'
            )
            val.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 3. Action buttons - BOTTOM (ALWAYS VISIBLE)
        button_frame = tk.Frame(card_frame, bg='#f8f9fa', height=40)
        button_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=(5, 10))
        button_frame.grid_propagate(False)
        
        # Configure button frame grid
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        # Single Edit Button
        edit_btn = tk.Button(
            button_frame,
            text="✏️ Edit",
            font=('Arial', 7, 'bold'),
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
            font=('Arial', 7, 'bold'),
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
        try:
            # Get product data from database
            products = self.product_service.get_all_products()
            product_data = None
            category_name = ""
            
            for product in products:
                if product[0] == product_id:
                    product_data = product
                    category_name = product[-1] if len(product) > 13 else ""
                    break
            
            if not product_data:
                messagebox.showerror("Error", "Product not found!")
                return
            
            # Unpack product data based on schema
            if len(product_data) == 14:  # New schema with color
                (pid, category_id, company, ptype, color,
                 sale_price, purchase_price, packing, volume, current_stock, 
                 image_path, created_at, updated_at, category_name) = product_data
            elif len(product_data) == 13:  # Schema without color
                (pid, category_id, company, ptype, 
                 sale_price, purchase_price, packing, volume, current_stock, 
                 image_path, created_at, updated_at, category_name) = product_data
                color = "N/A"
            else:
                messagebox.showerror("Error", "Cannot edit this product format")
                return
            
            # Prepare product data dictionary
            product_dict = {
                'category_id': category_id,
                'company': company,
                'type': ptype,
                'color': color,
                'sale_price': sale_price,
                'purchase_price': purchase_price,
                'packing': packing,
                'volume': volume,
                'current_stock': current_stock,
                'image_path': image_path,
                'category_id': category_id
            }
            
            # Open appropriate edit dialog based on category
            if category_name and category_name.lower() == 'paint':
                self.open_paint_edit_dialog(product_id, product_dict)
            elif category_name and category_name.lower() == 'roof sheet':
                self.open_roof_sheet_edit_dialog(product_id, product_dict)
            elif category_name and category_name.lower() == 'limination sheet':
                self.open_limination_sheet_edit_dialog(product_id, product_dict)
            elif category_name and category_name.lower() == 'sanitary':
                self.open_sanitary_edit_dialog(product_id, product_dict)
            else:
                self.open_generic_edit_dialog(product_id, product_dict)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit product: {str(e)}")

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
                    self.load_products(self.current_category)
                else:
                    messagebox.showerror("Error", "Failed to delete product!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product: {str(e)}")

    def open_generic_form(self, category_name):
        """Open product form for other categories"""
        messagebox.showinfo("Info", f"Add product form for {category_name} category")

    def open_paint_edit_dialog(self, product_id, product_data):
        """Open paint specific edit dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Edit Paint Product")
        dialog.geometry("450x550")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Position within dashboard boundaries
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        form_width = 450
        form_height = 550
        x = parent_x + parent_width - form_width - 20
        y = parent_y + 100
        
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        if x + form_width > screen_width:
            x = screen_width - form_width - 20
        
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
        
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar.pack(side="right", fill="y")
        
        # Form Title
        tk.Label(
            scrollable_frame,
            text="Edit Paint Product",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 15))
        
        # Image Upload Section
        image_frame = tk.Frame(scrollable_frame, bg='white')
        image_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            image_frame,
            text="Product Image:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        image_path_var = tk.StringVar(value=product_data.get('image_path', ''))
        image_entry = tk.Entry(
            image_frame, 
            textvariable=image_path_var,
            font=('Arial', 10),
            relief='solid', 
            bd=1,
            state='readonly'
        )
        image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(0, 8))
        
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
            font=('Arial', 9),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=browse_image
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Paint Specific Fields
        fields = [
            ("Company", "text", product_data.get('company', '')),
            ("Type", "text", product_data.get('type', '')),
            ("Color", "text", product_data.get('color', '')),
            ("Packing", "text", product_data.get('packing', '')),
            ("Volume", "text", product_data.get('volume', '')),
            ("Purchase Price", "number", product_data.get('purchase_price', 0)),
            ("Sale Price", "number", product_data.get('sale_price', 0)),
            ("Stock", "number", product_data.get('current_stock', 0))
        ]
        
        entries = {}
        
        for field_name, field_type, default_value in fields:
            frame = tk.Frame(scrollable_frame, bg='white')
            frame.pack(fill=tk.X, pady=6)
            
            tk.Label(
                frame,
                text=f"{field_name}:",
                font=('Arial', 10, 'bold'),
                fg='#2c3e50',
                bg='white',
                width=12,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            if field_type == 'number':
                entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1, validate='key')
                entry.config(validatecommand=(entry.register(self.validate_number), '%P'))
            else:
                entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1)
            
            # Set default value
            entry.insert(0, str(default_value))
            
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
            entries[field_name] = entry
        
        # Buttons
        button_frame = tk.Frame(scrollable_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=15)
        
        def update_product():
            try:
                updated_data = {
                    'category_id': product_data.get('category_id'),
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
                
                # Validate prices and stock
                if updated_data['purchase_price'] <= 0:
                    messagebox.showerror("Error", "Purchase price must be greater than 0!")
                    entries['Purchase Price'].focus()
                    return
                
                if updated_data['sale_price'] <= 0:
                    messagebox.showerror("Error", "Sale price must be greater than 0!")
                    entries['Sale Price'].focus()
                    return
                
                if updated_data['current_stock'] < 0:
                    messagebox.showerror("Error", "Stock quantity cannot be negative!")
                    entries['Stock'].focus()
                    return
                
                # Use product service to update
                updated_count = self.product_service.update_product(product_id, updated_data)
                
                if updated_count > 0:
                    messagebox.showinfo("Success", "Paint product updated successfully!")
                    dialog.destroy()
                    self.load_products(self.current_category)
                else:
                    messagebox.showerror("Error", "Failed to update paint product!")
                    
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update paint product: {str(e)}")
        
        update_btn = tk.Button(
            button_frame,
            text="Update Paint",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=update_product
        )
        update_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
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
        
        # Set focus to first field
        entries['Company'].focus()
        dialog.bind('<Return>', lambda e: update_product())

    def open_roof_sheet_edit_dialog(self, product_id, product_data):
        """Open roof sheet specific edit dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Edit Roof Sheet Product")
        dialog.geometry("450x550")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Position within dashboard boundaries
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        form_width = 450
        form_height = 550
        x = parent_x + parent_width - form_width - 20
        y = parent_y + 100
        
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        if x + form_width > screen_width:
            x = screen_width - form_width - 20
        
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
        
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar.pack(side="right", fill="y")
        
        # Form Title
        tk.Label(
            scrollable_frame,
            text="Edit Roof Sheet Product",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 15))
        
        # Image Upload Section
        image_frame = tk.Frame(scrollable_frame, bg='white')
        image_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            image_frame,
            text="Product Image:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        image_path_var = tk.StringVar(value=product_data.get('image_path', ''))
        image_entry = tk.Entry(
            image_frame, 
            textvariable=image_path_var,
            font=('Arial', 10),
            relief='solid', 
            bd=1,
            state='readonly'
        )
        image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(0, 8))
        
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
            font=('Arial', 9),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=browse_image
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Roof Sheet Specific Fields - WITH SIZE FIELD
        fields = [
            ("Company", "text", product_data.get('company', '')),
            ("Type", "text", product_data.get('type', '')),
            ("Color", "text", product_data.get('color', '')),
            ("Size", "text", product_data.get('volume', '')),
            ("Purchase Price", "number", product_data.get('purchase_price', 0)),
            ("Sale Price", "number", product_data.get('sale_price', 0)),
            ("Stock", "number", product_data.get('current_stock', 0))
        ]
        
        entries = {}
        
        for field_name, field_type, default_value in fields:
            frame = tk.Frame(scrollable_frame, bg='white')
            frame.pack(fill=tk.X, pady=6)
            
            tk.Label(
                frame,
                text=f"{field_name}:",
                font=('Arial', 10, 'bold'),
                fg='#2c3e50',
                bg='white',
                width=12,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            if field_type == 'number':
                entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1, validate='key')
                entry.config(validatecommand=(entry.register(self.validate_number), '%P'))
            else:
                entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1)
            
            # Set default value
            entry.insert(0, str(default_value))
            
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
            entries[field_name] = entry
        
        # Buttons
        button_frame = tk.Frame(scrollable_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=15)
        
        def update_product():
            try:
                updated_data = {
                    'category_id': product_data.get('category_id'),
                    'company': entries['Company'].get().strip(),
                    'type': entries['Type'].get().strip(),
                    'color': entries['Color'].get().strip(),
                    'sale_price': float(entries['Sale Price'].get() or 0),
                    'purchase_price': float(entries['Purchase Price'].get() or 0),
                    'packing': "",
                    'volume': entries['Size'].get().strip(),
                    'current_stock': int(entries['Stock'].get() or 0),
                    'image_path': image_path_var.get()
                }
                
                # Validate required fields
                required_fields = ['Company', 'Type', 'Color', 'Size']
                for field in required_fields:
                    if not entries[field].get().strip():
                        messagebox.showerror("Error", f"{field} is required!")
                        return
                
                # Validate prices and stock
                if updated_data['purchase_price'] <= 0:
                    messagebox.showerror("Error", "Purchase price must be greater than 0!")
                    entries['Purchase Price'].focus()
                    return
                
                if updated_data['sale_price'] <= 0:
                    messagebox.showerror("Error", "Sale price must be greater than 0!")
                    entries['Sale Price'].focus()
                    return
                
                if updated_data['current_stock'] < 0:
                    messagebox.showerror("Error", "Stock quantity cannot be negative!")
                    entries['Stock'].focus()
                    return
                
                # Use product service to update
                updated_count = self.product_service.update_product(product_id, updated_data)
                
                if updated_count > 0:
                    messagebox.showinfo("Success", "Roof Sheet updated successfully!")
                    dialog.destroy()
                    self.load_products(self.current_category)
                else:
                    messagebox.showerror("Error", "Failed to update roof sheet!")
                    
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update roof sheet: {str(e)}")
        
        update_btn = tk.Button(
            button_frame,
            text="Update Roof Sheet",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=update_product
        )
        update_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
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
        
        # Set focus to first field
        entries['Company'].focus()
        dialog.bind('<Return>', lambda e: update_product())

    def open_limination_sheet_edit_dialog(self, product_id, product_data):
        """Open limination sheet specific edit dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Edit Limination Sheet Product")
        dialog.geometry("450x550")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Position within dashboard boundaries
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        form_width = 450
        form_height = 550
        x = parent_x + parent_width - form_width - 20
        y = parent_y + 100
        
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        if x + form_width > screen_width:
            x = screen_width - form_width - 20
        
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
        
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar.pack(side="right", fill="y")
        
        # Form Title
        tk.Label(
            scrollable_frame,
            text="Edit Limination Sheet Product",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 15))
        
        # Image Upload Section
        image_frame = tk.Frame(scrollable_frame, bg='white')
        image_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            image_frame,
            text="Product Image:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        image_path_var = tk.StringVar(value=product_data.get('image_path', ''))
        image_entry = tk.Entry(
            image_frame, 
            textvariable=image_path_var,
            font=('Arial', 10),
            relief='solid', 
            bd=1,
            state='readonly'
        )
        image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(0, 8))
        
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
            font=('Arial', 9),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=browse_image
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Limination Sheet Specific Fields
        fields = [
            ("Company", "text", product_data.get('company', '')),
            ("Color", "text", product_data.get('color', '')),
            ("Size", "text", product_data.get('volume', '')),
            ("Type", "text", product_data.get('type', '')),
            ("Purchase Price", "number", product_data.get('purchase_price', 0)),
            ("Sale Price", "number", product_data.get('sale_price', 0)),
            ("Stock", "number", product_data.get('current_stock', 0))
        ]
        
        entries = {}
        
        for field_name, field_type, default_value in fields:
            frame = tk.Frame(scrollable_frame, bg='white')
            frame.pack(fill=tk.X, pady=6)
            
            tk.Label(
                frame,
                text=f"{field_name}:",
                font=('Arial', 10, 'bold'),
                fg='#2c3e50',
                bg='white',
                width=12,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            if field_type == 'number':
                entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1, validate='key')
                entry.config(validatecommand=(entry.register(self.validate_number), '%P'))
            else:
                entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1)
            
            # Set default value
            entry.insert(0, str(default_value))
            
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
            entries[field_name] = entry
        
        # Buttons
        button_frame = tk.Frame(scrollable_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=15)
        
        def update_product():
            try:
                updated_data = {
                    'category_id': product_data.get('category_id'),
                    'company': entries['Company'].get().strip(),
                    'type': entries['Type'].get().strip(),
                    'color': entries['Color'].get().strip(),
                    'sale_price': float(entries['Sale Price'].get() or 0),
                    'purchase_price': float(entries['Purchase Price'].get() or 0),
                    'packing': "",
                    'volume': entries['Size'].get().strip(),
                    'current_stock': int(entries['Stock'].get() or 0),
                    'image_path': image_path_var.get()
                }
                
                # Validate required fields
                required_fields = ['Company', 'Color', 'Size', 'Type']
                for field in required_fields:
                    if not entries[field].get().strip():
                        messagebox.showerror("Error", f"{field} is required!")
                        return
                
                # Validate prices and stock
                if updated_data['purchase_price'] <= 0:
                    messagebox.showerror("Error", "Purchase price must be greater than 0!")
                    entries['Purchase Price'].focus()
                    return
                
                if updated_data['sale_price'] <= 0:
                    messagebox.showerror("Error", "Sale price must be greater than 0!")
                    entries['Sale Price'].focus()
                    return
                
                if updated_data['current_stock'] < 0:
                    messagebox.showerror("Error", "Stock quantity cannot be negative!")
                    entries['Stock'].focus()
                    return
                
                # Use product service to update
                updated_count = self.product_service.update_product(product_id, updated_data)
                
                if updated_count > 0:
                    messagebox.showinfo("Success", "Limination Sheet updated successfully!")
                    dialog.destroy()
                    self.load_products(self.current_category)
                else:
                    messagebox.showerror("Error", "Failed to update limination sheet!")
                    
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update limination sheet: {str(e)}")
        
        update_btn = tk.Button(
            button_frame,
            text="Update Limination Sheet",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=update_product
        )
        update_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
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
        
        # Set focus to first field
        entries['Company'].focus()
        dialog.bind('<Return>', lambda e: update_product())

    def open_sanitary_edit_dialog(self, product_id, product_data):
        """Open sanitary specific edit dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Edit Sanitary Product")
        dialog.geometry("450x550")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Position within dashboard boundaries
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        form_width = 450
        form_height = 550
        x = parent_x + parent_width - form_width - 20
        y = parent_y + 100
        
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        if x + form_width > screen_width:
            x = screen_width - form_width - 20
        
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
        
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar.pack(side="right", fill="y")
        
        # Form Title
        tk.Label(
            scrollable_frame,
            text="Edit Sanitary Product",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 15))
        
        # Image Upload Section
        image_frame = tk.Frame(scrollable_frame, bg='white')
        image_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            image_frame,
            text="Product Image:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        image_path_var = tk.StringVar(value=product_data.get('image_path', ''))
        image_entry = tk.Entry(
            image_frame, 
            textvariable=image_path_var,
            font=('Arial', 10),
            relief='solid', 
            bd=1,
            state='readonly'
        )
        image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(0, 8))
        
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
            font=('Arial', 9),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=browse_image
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Sanitary Specific Fields
        fields = [
            ("Company", "text", product_data.get('company', '')),
            ("Color", "text", product_data.get('color', '')),
            ("Size", "text", product_data.get('volume', '')),
            ("Type", "text", product_data.get('type', '')),
            ("Purchase Price", "number", product_data.get('purchase_price', 0)),
            ("Sale Price", "number", product_data.get('sale_price', 0)),
            ("Stock", "number", product_data.get('current_stock', 0))
        ]
        
        entries = {}
        
        for field_name, field_type, default_value in fields:
            frame = tk.Frame(scrollable_frame, bg='white')
            frame.pack(fill=tk.X, pady=6)
            
            tk.Label(
                frame,
                text=f"{field_name}:",
                font=('Arial', 10, 'bold'),
                fg='#2c3e50',
                bg='white',
                width=12,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            if field_type == 'number':
                entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1, validate='key')
                entry.config(validatecommand=(entry.register(self.validate_number), '%P'))
            else:
                entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1)
            
            # Set default value
            entry.insert(0, str(default_value))
            
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
            entries[field_name] = entry
        
        # Buttons
        button_frame = tk.Frame(scrollable_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=15)
        
        def update_product():
            try:
                updated_data = {
                    'category_id': product_data.get('category_id'),
                    'company': entries['Company'].get().strip(),
                    'type': entries['Type'].get().strip(),
                    'color': entries['Color'].get().strip(),
                    'sale_price': float(entries['Sale Price'].get() or 0),
                    'purchase_price': float(entries['Purchase Price'].get() or 0),
                    'packing': "",
                    'volume': entries['Size'].get().strip(),
                    'current_stock': int(entries['Stock'].get() or 0),
                    'image_path': image_path_var.get()
                }
                
                # Validate required fields
                required_fields = ['Company', 'Color', 'Size', 'Type']
                for field in required_fields:
                    if not entries[field].get().strip():
                        messagebox.showerror("Error", f"{field} is required!")
                        return
                
                # Validate prices and stock
                if updated_data['purchase_price'] <= 0:
                    messagebox.showerror("Error", "Purchase price must be greater than 0!")
                    entries['Purchase Price'].focus()
                    return
                
                if updated_data['sale_price'] <= 0:
                    messagebox.showerror("Error", "Sale price must be greater than 0!")
                    entries['Sale Price'].focus()
                    return
                
                if updated_data['current_stock'] < 0:
                    messagebox.showerror("Error", "Stock quantity cannot be negative!")
                    entries['Stock'].focus()
                    return
                
                # Use product service to update
                updated_count = self.product_service.update_product(product_id, updated_data)
                
                if updated_count > 0:
                    messagebox.showinfo("Success", "Sanitary product updated successfully!")
                    dialog.destroy()
                    self.load_products(self.current_category)
                else:
                    messagebox.showerror("Error", "Failed to update sanitary product!")
                    
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update sanitary product: {str(e)}")
        
        update_btn = tk.Button(
            button_frame,
            text="Update Sanitary",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=update_product
        )
        update_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
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
        
        # Set focus to first field
        entries['Company'].focus()
        dialog.bind('<Return>', lambda e: update_product())

    def open_generic_edit_dialog(self, product_id, product_data):
        """Open generic edit dialog for other categories"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Edit Product")
        dialog.geometry("450x550")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Position within dashboard boundaries
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        form_width = 450
        form_height = 550
        x = parent_x + parent_width - form_width - 20
        y = parent_y + 100
        
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        if x + form_width > screen_width:
            x = screen_width - form_width - 20
        
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
        
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar.pack(side="right", fill="y")
        
        # Form Title
        tk.Label(
            scrollable_frame,
            text="Edit Product",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 15))
        
        # Image Upload Section
        image_frame = tk.Frame(scrollable_frame, bg='white')
        image_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            image_frame,
            text="Product Image:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        image_path_var = tk.StringVar(value=product_data.get('image_path', ''))
        image_entry = tk.Entry(
            image_frame, 
            textvariable=image_path_var,
            font=('Arial', 10),
            relief='solid', 
            bd=1,
            state='readonly'
        )
        image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(0, 8))
        
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
            font=('Arial', 9),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=browse_image
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Generic Fields
        fields = [
            ("Company", "text", product_data.get('company', '')),
            ("Type", "text", product_data.get('type', '')),
            ("Color", "text", product_data.get('color', '')),
            ("Packing", "text", product_data.get('packing', '')),
            ("Volume", "text", product_data.get('volume', '')),
            ("Purchase Price", "number", product_data.get('purchase_price', 0)),
            ("Sale Price", "number", product_data.get('sale_price', 0)),
            ("Stock", "number", product_data.get('current_stock', 0))
        ]
        
        entries = {}
        
        for field_name, field_type, default_value in fields:
            frame = tk.Frame(scrollable_frame, bg='white')
            frame.pack(fill=tk.X, pady=6)
            
            tk.Label(
                frame,
                text=f"{field_name}:",
                font=('Arial', 10, 'bold'),
                fg='#2c3e50',
                bg='white',
                width=12,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            if field_type == 'number':
                entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1, validate='key')
                entry.config(validatecommand=(entry.register(self.validate_number), '%P'))
            else:
                entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1)
            
            # Set default value
            entry.insert(0, str(default_value))
            
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
            entries[field_name] = entry
        
        # Buttons
        button_frame = tk.Frame(scrollable_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=15)
        
        def update_product():
            try:
                updated_data = {
                    'category_id': product_data.get('category_id'),
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
                
                # Validate prices and stock
                if updated_data['purchase_price'] <= 0:
                    messagebox.showerror("Error", "Purchase price must be greater than 0!")
                    entries['Purchase Price'].focus()
                    return
                
                if updated_data['sale_price'] <= 0:
                    messagebox.showerror("Error", "Sale price must be greater than 0!")
                    entries['Sale Price'].focus()
                    return
                
                if updated_data['current_stock'] < 0:
                    messagebox.showerror("Error", "Stock quantity cannot be negative!")
                    entries['Stock'].focus()
                    return
                
                # Use product service to update
                updated_count = self.product_service.update_product(product_id, updated_data)
                
                if updated_count > 0:
                    messagebox.showinfo("Success", "Product updated successfully!")
                    dialog.destroy()
                    self.load_products(self.current_category)
                else:
                    messagebox.showerror("Error", "Failed to update product!")
                    
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update product: {str(e)}")
        
        update_btn = tk.Button(
            button_frame,
            text="Update Product",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=update_product
        )
        update_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
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
        
        # Set focus to first field
        entries['Company'].focus()
        dialog.bind('<Return>', lambda e: update_product())

    def validate_number(self, value):
        """Validate number input"""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
