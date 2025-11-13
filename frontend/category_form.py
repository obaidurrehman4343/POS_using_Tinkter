import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.product_service import ProductService
from PIL import Image, ImageTk
import os

class UniversalProductForm:
    def __init__(self, parent, product_service, current_category, refresh_callback, category_name, product_id=None, product_data=None):
        self.parent = parent
        self.product_service = product_service
        self.current_category = current_category
        self.refresh_callback = refresh_callback
        self.category_name = category_name
        self.product_id = product_id
        self.product_data = product_data
        self.is_edit_mode = product_id is not None
        
        self.field_config = self.get_field_config()
        self.setup_form()
    
    def get_field_config(self):
        """Define fields for each category - USING YOUR EXACT FIELD STRUCTURES"""
        configs = {
            'Paint': {
                'title': 'Edit Paint Product' if self.is_edit_mode else 'Add Paint Product',
                'fields': [
                    ("Company", "text", "e.g., Berger, Nippon, Jenson"),
                    ("Type", "text", "e.g., Emulsion, Enamel, Primer"),
                    ("Color", "text", "e.g., White, Cream, Sky Blue"),
                    ("Packing", "text", "e.g., 1L, 4L, 10L, 20L"),
                    ("Volume", "text", "e.g., 1 liter, 4 liters"),
                    ("Purchase Price", "number", "0"),
                    ("Sale Price", "number", "0"),
                    ("Stock", "number", "0")
                ],
                'mappings': {
                    'company': 'Company',
                    'type': 'Type', 
                    'color': 'Color',
                    'packing': 'Packing',
                    'volume': 'Volume',
                    'purchase_price': 'Purchase Price',
                    'sale_price': 'Sale Price',
                    'current_stock': 'Stock'
                },
                'placeholder_texts': {
                    'Company': 'e.g., Berger, Nippon, Jenson',
                    'Type': 'e.g., Emulsion, Enamel, Primer',
                    'Color': 'e.g., White, Cream, Sky Blue',
                    'Packing': 'e.g., 1L, 4L, 10L, 20L',
                    'Volume': 'e.g., 1 liter, 4 liters'
                }
            },
            'Roof Sheet': {
                'title': 'Edit Roof Sheet Product' if self.is_edit_mode else 'Add Roof Sheet Product',
                'fields': [
                    ("Company", "text", "e.g., Diamond, Metro, Sapphire"),
                    ("Type", "text", "e.g., Corrugated, Plain, Color Coated"),
                    ("Color", "text", "e.g., Silver, Red, Blue"),
                    ("Size", "text", "e.g., 8x4, 10x3, 12x4"),
                    ("Purchase Price", "number", "0"),
                    ("Sale Price", "number", "0"),
                    ("Stock", "number", "0")
                ],
                'mappings': {
                    'company': 'Company',
                    'type': 'Type',
                    'color': 'Color',
                    'packing': '',  # Not used for roof sheets
                    'volume': 'Size',  # Using 'volume' column for size
                    'purchase_price': 'Purchase Price',
                    'sale_price': 'Sale Price',
                    'current_stock': 'Stock'
                },
                'placeholder_texts': {
                    'Company': 'e.g., Diamond, Metro, Sapphire',
                    'Type': 'e.g., Corrugated, Plain, Color Coated',
                    'Color': 'e.g., Silver, Red, Blue',
                    'Size': 'e.g., 8x4, 10x3, 12x4'
                }
            },
            'Limination Sheet': {
                'title': 'Edit Limination Sheet Product' if self.is_edit_mode else 'Add Limination Sheet Product',
                'fields': [
                    ("Company", "text", "e.g., Diamond, Metro, Sapphire"),
                    ("Color", "text", "e.g., Silver, Golden, Wooden"),
                    ("Size", "text", "e.g., 8x4, 10x3, 12x4"),
                    ("Type", "text", "e.g., Glossy, Matte, Textured"),
                    ("Purchase Price", "number", "0"),
                    ("Sale Price", "number", "0"),
                    ("Stock", "number", "0")
                ],
                'mappings': {
                    'company': 'Company',
                    'type': 'Type',
                    'color': 'Color',
                    'packing': '',  # Not used for limination sheets
                    'volume': 'Size',  # Using 'volume' column for size
                    'purchase_price': 'Purchase Price',
                    'sale_price': 'Sale Price',
                    'current_stock': 'Stock'
                },
                'placeholder_texts': {
                    'Company': 'e.g., Diamond, Metro, Sapphire',
                    'Color': 'e.g., Silver, Golden, Wooden',
                    'Size': 'e.g., 8x4, 10x3, 12x4',
                    'Type': 'e.g., Glossy, Matte, Textured'
                }
            },
            'Sanitary': {
                'title': 'Edit Sanitary Product' if self.is_edit_mode else 'Add Sanitary Product',
                'fields': [
                    ("Company", "text", "e.g., Swiss, Dura, Standard"),
                    ("Size", "text", "e.g., 8x4, Small, Medium"),
                    ("Type", "text", "e.g., Wash Basin, Toilet, Tap"),
                    ("Color", "text", "e.g., White, Red, Blue"),
                    ("Purchase Price", "number", "0"),
                    ("Sale Price", "number", "0"),
                    ("Stock", "number", "0")
                ],
                'mappings': {
                    'company': 'Company',
                    'type': 'Type',
                    'color': 'Color',
                    'packing': '',  # Not used for sanitary
                    'volume': 'Size',  # Using 'volume' column for size
                    'purchase_price': 'Purchase Price',
                    'sale_price': 'Sale Price',
                    'current_stock': 'Stock'
                },
                'placeholder_texts': {
                    'Company': 'e.g., Swiss, Dura, Standard',
                    'Size': 'e.g., 8x4, Small, Medium',
                    'Type': 'e.g., Wash Basin, Toilet, Tap',
                    'Color': 'e.g., White, Red, Blue'
                }
            }
        }
        
        # Default to Paint if category not found
        return configs.get(self.category_name, configs['Paint'])
    
    def setup_form(self):
        """Setup the form - SINGLE implementation for all categories"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.field_config['title'])
        self.dialog.geometry("450x550")
        self.dialog.configure(bg='white')
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        self.position_form()
        self.create_form_content()
        
        # Load existing data if in edit mode
        if self.is_edit_mode and self.product_data:
            self.load_existing_data()
    
    def position_form(self):
        """Position form within dashboard - SAME AS YOUR ORIGINAL"""
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
        
        self.dialog.geometry(f"{form_width}x{form_height}+{x}+{y}")
    
    def create_form_content(self):
        """Create form content - SINGLE implementation for all categories"""
        # Create scrollable form (SAME AS YOUR ORIGINAL)
        canvas = tk.Canvas(self.dialog, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar.pack(side="right", fill="y")
        
        # Form Title
        tk.Label(
            self.scrollable_frame,
            text=self.field_config['title'],
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 15))
        
        # Image Upload Section (SAME AS YOUR ORIGINAL)
        self.image_path_var = tk.StringVar(value=self.product_data.get('image_path', '') if self.product_data else '')
        self.create_image_section(self.scrollable_frame)
        
        # Dynamic fields based on category
        self.entries = {}
        self.create_dynamic_fields(self.scrollable_frame)
        
        # Buttons
        self.create_buttons(self.scrollable_frame)
        
        # Set focus to first field
        first_field = list(self.entries.keys())[0] if self.entries else None
        if first_field:
            self.entries[first_field].focus()
        
        self.dialog.bind('<Return>', lambda e: self.save_product())
    
    def create_image_section(self, parent):
        """Create image upload section - SAME AS YOUR ORIGINAL"""
        image_frame = tk.Frame(parent, bg='white')
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
        
        image_entry = tk.Entry(
            image_frame, 
            textvariable=self.image_path_var,
            font=('Arial', 10),
            relief='solid', 
            bd=1,
            state='readonly'
        )
        image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(0, 8))
        
        browse_btn = tk.Button(
            image_frame,
            text="Browse",
            font=('Arial', 9),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=self.browse_image
        )
        browse_btn.pack(side=tk.RIGHT)
    
    def create_dynamic_fields(self, parent):
        """Create fields based on configuration - USING YOUR EXACT FIELD STRUCTURES"""
        for field_name, field_type, placeholder in self.field_config['fields']:
            frame = tk.Frame(parent, bg='white')
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
            
            # Add placeholder text (only in add mode, not edit mode)
            if placeholder and not self.is_edit_mode:
                entry.insert(0, placeholder)
                entry.bind('<FocusIn>', lambda e, entry=entry, placeholder=placeholder: self.clear_placeholder(entry, placeholder))
            
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
            self.entries[field_name] = entry
    
    def create_buttons(self, parent):
        """Create action buttons - SAME AS YOUR ORIGINAL"""
        button_frame = tk.Frame(parent, bg='white')
        button_frame.pack(fill=tk.X, pady=15)
        
        if self.is_edit_mode:
            button_text = "Update Product"
            button_command = self.update_product
        else:
            button_text = "Save Product"
            button_command = self.save_product
        
        save_btn = tk.Button(
            button_frame,
            text=button_text,
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=button_command
        )
        save_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 11),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=self.dialog.destroy
        )
        cancel_btn.pack(side=tk.RIGHT)
    
    def browse_image(self):
        """Browse for image file - SAME AS YOUR ORIGINAL"""
        file_path = filedialog.askopenfilename(
            title="Select Product Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if file_path:
            self.image_path_var.set(file_path)
    
    def clear_placeholder(self, entry, placeholder):
        """Clear placeholder text on focus - SAME AS YOUR ORIGINAL"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
    
    def validate_number(self, value):
        """Validate number input - SAME AS YOUR ORIGINAL"""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def load_existing_data(self):
        """Load existing product data into form fields for editing"""
        if not self.product_data:
            return
        
        mappings = self.field_config['mappings']
        placeholder_texts = self.field_config['placeholder_texts']
        
        # Map existing data to form fields
        for db_field, form_field in mappings.items():
            if form_field and form_field in self.entries:
                value = self.product_data.get(db_field, '')
                if value is None:
                    value = ''
                
                # Clear existing text and insert actual value
                self.entries[form_field].delete(0, tk.END)
                self.entries[form_field].insert(0, str(value))
        
        # Set image path
        image_path = self.product_data.get('image_path', '')
        if image_path:
            self.image_path_var.set(image_path)
    
    def get_form_data(self):
        """Extract data from form fields based on category mapping"""
        mappings = self.field_config['mappings']
        form_data = {
            'category_id': self.current_category,
            'image_path': self.image_path_var.get()
        }
        
        # Map form fields to database fields
        for db_field, form_field in mappings.items():
            if form_field and form_field in self.entries:
                value = self.entries[form_field].get().strip()
                
                # Handle numeric fields
                if db_field in ['purchase_price', 'sale_price']:
                    try:
                        form_data[db_field] = float(value) if value else 0.0
                    except ValueError:
                        form_data[db_field] = 0.0
                elif db_field == 'current_stock':
                    try:
                        form_data[db_field] = int(value) if value else 0
                    except ValueError:
                        form_data[db_field] = 0
                else:
                    form_data[db_field] = value
        
        # Handle empty packing for categories that don't use it
        if 'packing' not in form_data:
            form_data['packing'] = ""
        
        return form_data
    
    def validate_required_fields(self):
        """Validate all required fields - SAME VALIDATION AS YOUR ORIGINAL"""
        # Get category-specific required fields
        required_fields = []
        placeholder_texts = self.field_config['placeholder_texts']
        
        for field_name in self.entries.keys():
            if field_name in ['Purchase Price', 'Sale Price', 'Stock']:
                continue  # These are validated separately
            required_fields.append(field_name)
        
        # Validate text fields
        for field in required_fields:
            value = self.entries[field].get().strip()
            placeholder = placeholder_texts.get(field, '')
            
            if not value or (placeholder and value == placeholder):
                messagebox.showerror("Error", f"Please enter a valid {field}!")
                self.entries[field].focus()
                return False
        
        # Validate prices and stock
        try:
            purchase_price = float(self.entries['Purchase Price'].get() or 0)
            sale_price = float(self.entries['Sale Price'].get() or 0)
            stock = int(self.entries['Stock'].get() or 0)
            
            if purchase_price <= 0:
                messagebox.showerror("Error", "Purchase price must be greater than 0!")
                self.entries['Purchase Price'].focus()
                return False
            
            if sale_price <= 0:
                messagebox.showerror("Error", "Sale price must be greater than 0!")
                self.entries['Sale Price'].focus()
                return False
            
            if stock < 0:
                messagebox.showerror("Error", "Stock quantity cannot be negative!")
                self.entries['Stock'].focus()
                return False
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for price and stock!")
            return False
        
        return True
    
    def save_product(self):
        """Save new product - SAME LOGIC AS YOUR ORIGINAL FORMS"""
        try:
            if not self.validate_required_fields():
                return
            
            product_data = self.get_form_data()
            
            # Use product_service to add product
            self.product_service.add_product(product_data)
            messagebox.showinfo("Success", f"{self.category_name} product added successfully!")
            self.dialog.destroy()
            self.refresh_callback()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {str(e)}")
    
    def update_product(self):
        """Update existing product - SAME LOGIC AS YOUR ORIGINAL EDIT DIALOGS"""
        try:
            if not self.validate_required_fields():
                return
            
            product_data = self.get_form_data()
            
            # Use product_service to update product
            updated_count = self.product_service.update_product(self.product_id, product_data)
            
            if updated_count > 0:
                messagebox.showinfo("Success", f"{self.category_name} product updated successfully!")
                self.dialog.destroy()
                self.refresh_callback()
            else:
                messagebox.showerror("Error", f"Failed to update {self.category_name.lower()} product!")
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update product: {str(e)}")