import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.product_service import ProductService
from backend.category_service import CategoryService
from PIL import Image, ImageTk
import os
from frontend.category_form import UniversalProductForm  # ADD THIS IMPORT

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
        """Handle category selection - FIXED METHOD NAME"""
        category_name = self.category_var.get()
        if category_name:
            self.selected_category_name = category_name
            
            try:
                category_id = self.category_service.get_category_by_name(category_name)
                
                if category_id:
                    self.current_category = category_id
                    self.add_product_btn.config(state='normal')
                    self.load_products(category_id)  # ✅ CORRECT METHOD NAME
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
        """Add new product using universal form - FIXED METHOD"""
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
                refresh_callback=lambda: self.load_products(self.current_category),  # ✅ CORRECT METHOD NAME
                category_name=category_name
            )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {str(e)}")
    
    def load_products(self, category_id):
        """Load products for selected category - FIXED METHOD NAME"""
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
        """Edit product using universal form - FIXED METHOD"""
        try:
            # Get product data from database
            products = self.product_service.get_all_products()
            product_data = None
            category_name = ""
            
            for product in products:
                if product[0] == product_id:
                    product_data = self.unpack_product_data(product)
                    category_name = product[-1] if len(product) > 13 else ""
                    break
            
            if not product_data:
                messagebox.showerror("Error", "Product not found!")
                return
            
            # Use Universal Form for editing ALL categories
            UniversalProductForm(
                parent=self.parent,
                product_service=self.product_service,
                current_category=self.current_category,
                refresh_callback=lambda: self.load_products(self.current_category),  # ✅ CORRECT METHOD NAME
                category_name=category_name,
                product_id=product_id,
                product_data=product_data
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit product: {str(e)}")

    def unpack_product_data(self, product):
        """Helper to unpack product data for editing"""
        try:
            if len(product) == 14:  # New schema with color
                (product_id, category_id, company, ptype, color,
                 sale_price, purchase_price, packing, volume, current_stock, 
                 image_path, created_at, updated_at, category_name) = product
            elif len(product) == 13:  # Schema without color
                (product_id, category_id, company, ptype, 
                 sale_price, purchase_price, packing, volume, current_stock, 
                 image_path, created_at, updated_at, category_name) = product
                color = "N/A"
            else:
                return None
            
            return {
                'category_id': category_id,
                'company': company,
                'type': ptype,
                'color': color,
                'sale_price': sale_price,
                'purchase_price': purchase_price,
                'packing': packing,
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
                    self.load_products(self.current_category)  # ✅ CORRECT METHOD NAME
                else:
                    messagebox.showerror("Error", "Failed to delete product!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product: {str(e)}")

    def validate_number(self, value):
        """Validate number input"""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False