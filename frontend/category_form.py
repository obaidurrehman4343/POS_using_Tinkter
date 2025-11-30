
# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# from backend.product_service import ProductService
# from backend.measurement_service import MeasurementService
# from PIL import Image, ImageTk
# import os

# class UniversalProductForm:
#     def __init__(self, parent, product_service, current_category, refresh_callback, category_name, product_id=None, product_data=None):
#         self.parent = parent
#         self.product_service = product_service
#         self.measurement_service = MeasurementService()
#         self.current_category = current_category
#         self.refresh_callback = refresh_callback
#         self.category_name = category_name
#         self.product_id = product_id
#         self.product_data = product_data
#         self.is_edit_mode = product_id is not None
        
#         # Get measurements for this category
#         self.measurements = self.get_measurements_for_category()
#         self.selected_measurement = None
        
#         # Measurement selection variables
#         self.measurement_var = None
#         self.measurement_combo = None
        
#         self.field_config = self.get_field_config()
#         self.setup_form()
    
#     def get_measurements_for_category(self):
#         """Get appropriate measurements based on category - FIXED: All measurements for all non-Paint categories"""
#         if self.category_name == 'Paint':
#             return []  # No measurements for Paint
        
#         # For ALL other categories (Sanitary, Roof Sheet, Limination Sheet, Hardware), return ALL measurements
#         measurements = []
#         seen_names = set()
        
#         # Get ALL measurements from all types
#         all_measurements = []
#         all_measurements.extend(self.measurement_service.get_measurements_by_type('Length'))
#         all_measurements.extend(self.measurement_service.get_measurements_by_type('Weight'))
#         all_measurements.extend(self.measurement_service.get_measurements_by_type('Volume'))
#         all_measurements.extend(self.measurement_service.get_measurements_by_type('Count'))
        
#         # Remove duplicates by name
#         for measurement in all_measurements:
#             if len(measurement) >= 2:  # Ensure measurement has at least name
#                 measurement_name = measurement[1]  # Name is at index 1
#                 if measurement_name not in seen_names:
#                     seen_names.add(measurement_name)
#                     measurements.append(measurement)
        
#         return measurements
    
#     def get_field_config(self):
#         """Define fields for each category with specific measurement requirements"""
#         configs = {
#             'Paint': {
#                 'title': 'Edit Paint Product' if self.is_edit_mode else 'Add Paint Product',
#                 'fields': [
#                     ("Company", "text", "e.g., Berger, Nippon, Jenson"),
#                     ("Type", "text", "e.g., Emulsion, Enamel, Primer"),
#                     ("Color", "text", "e.g., White, Cream, Sky Blue"),
#                     ("Packing", "text", "e.g., 1L, 4L, 10L, 20L"),
#                     ("Purchase Price", "number", "0"),
#                     ("Sale Price", "number", "0"),
#                     ("Stock", "number", "0")  # Stock field for Paint
#                 ],
#                 'mappings': {
#                     'company': 'Company',
#                     'type': 'Type', 
#                     'color': 'Color',
#                     'packing': 'Packing',
#                     'purchase_price': 'Purchase Price',
#                     'sale_price': 'Sale Price',
#                     'current_stock': 'Stock'
#                 },
#                 'placeholder_texts': {
#                     'Company': 'e.g., Berger, Nippon, Jenson',
#                     'Type': 'e.g., Emulsion, Enamel, Primer',
#                     'Color': 'e.g., White, Cream, Sky Blue',
#                     'Packing': 'e.g., 1L, 4L, 10L, 20L'
#                 },
#                 'has_measurement': False  # No measurement for Paint
#             },
#             'Sanitary': {
#                 'title': 'Edit Sanitary Product' if self.is_edit_mode else 'Add Sanitary Product',
#                 'fields': [
#                     ("Company", "text", "e.g., Swiss, Dura, Standard"),
#                     ("Type", "text", "e.g., Wash Basin, Toilet, Tap"),
#                     ("Color", "text", "e.g., White, Red, Blue"),
#                     ("Size", "text", "e.g., Small, Medium, Large"),
#                     ("Purchase Price", "number", "0"),
#                     ("Sale Price", "number", "0")
#                 ],
#                 'mappings': {
#                     'company': 'Company',
#                     'type': 'Type',
#                     'color': 'Color',
#                     'volume': 'Size',
#                     'purchase_price': 'Purchase Price',
#                     'sale_price': 'Sale Price',
#                     'current_stock': 'Stock'
#                 },
#                 'placeholder_texts': {
#                     'Company': 'e.g., Swiss, Dura, Standard',
#                     'Type': 'e.g., Wash Basin, Toilet, Tap',
#                     'Color': 'e.g., White, Red, Blue',
#                     'Size': 'e.g., Small, Medium, Large'
#                 },
#                 'has_measurement': True,  # Now has ALL measurements
#                 'measurement_label': 'Unit:'
#             },
#             'Roof Sheet': {
#                 'title': 'Edit Roof Sheet Product' if self.is_edit_mode else 'Add Roof Sheet Product',
#                 'fields': [
#                     ("Company", "text", "e.g., Diamond, Metro, Sapphire"),
#                     ("Type", "text", "e.g., Corrugated, Plain, Color Coated"),
#                     ("Color", "text", "e.g., Silver, Red, Blue"),
#                     ("Size", "text", "e.g., 8x4, 10x3, 12x4"),
#                     ("Purchase Price", "number", "0"),
#                     ("Sale Price", "number", "0")
#                 ],
#                 'mappings': {
#                     'company': 'Company',
#                     'type': 'Type',
#                     'color': 'Color',
#                     'volume': 'Size',
#                     'purchase_price': 'Purchase Price',
#                     'sale_price': 'Sale Price',
#                     'current_stock': 'Stock'
#                 },
#                 'placeholder_texts': {
#                     'Company': 'e.g., Diamond, Metro, Sapphire',
#                     'Type': 'e.g., Corrugated, Plain, Color Coated',
#                     'Color': 'e.g., Silver, Red, Blue',
#                     'Size': 'e.g., 8x4, 10x3, 12x4'
#                 },
#                 'has_measurement': True,  # Now has ALL measurements
#                 'measurement_label': 'Unit:'
#             },
#             'Limination Sheet': {
#                 'title': 'Edit Limination Sheet Product' if self.is_edit_mode else 'Add Limination Sheet Product',
#                 'fields': [
#                     ("Company", "text", "e.g., Diamond, Metro, Sapphire"),
#                     ("Color", "text", "e.g., Silver, Golden, Wooden"),
#                     ("Color Code", "text", "e.g., #FF0000, RGB255, Code123"),
#                     ("Size", "text", "e.g., 8x4, 10x3, 12x4"),
#                     ("Type", "text", "e.g., Glossy, Matte, Textured"),
#                     ("Purchase Price", "number", "0"),
#                     ("Sale Price", "number", "0")
#                 ],
#                 'mappings': {
#                     'company': 'Company',
#                     'type': 'Type',
#                     'color': 'Color',
#                     'packing': 'Color Code',
#                     'volume': 'Size',
#                     'purchase_price': 'Purchase Price',
#                     'sale_price': 'Sale Price',
#                     'current_stock': 'Stock'
#                 },
#                 'placeholder_texts': {
#                     'Company': 'e.g., Diamond, Metro, Sapphire',
#                     'Color': 'e.g., Silver, Golden, Wooden',
#                     'Color Code': 'e.g., #FF0000, RGB255, Code123',
#                     'Size': 'e.g., 8x4, 10x3, 12x4',
#                     'Type': 'e.g., Glossy, Matte, Textured'
#                 },
#                 'has_measurement': True,  # Now has ALL measurements
#                 'measurement_label': 'Unit:'
#             },
#             'Hardware': {
#                 'title': 'Edit Hardware Product' if self.is_edit_mode else 'Add Hardware Product',
#                 'fields': [
#                     ("Company", "text", "e.g., Bosch, Stanley, Makita"),
#                     ("Type", "text", "e.g., Hammer, Screwdriver, Wrench"),
#                     ("Color", "text", "e.g., Black, Silver, Red"),
#                     ("Purchase Price", "number", "0"),
#                     ("Sale Price", "number", "0")
#                 ],
#                 'mappings': {
#                     'company': 'Company',
#                     'type': 'Type',
#                     'color': 'Color',
#                     'purchase_price': 'Purchase Price',
#                     'sale_price': 'Sale Price',
#                     'current_stock': 'Stock'
#                 },
#                 'placeholder_texts': {
#                     'Company': 'e.g., Bosch, Stanley, Makita',
#                     'Type': 'e.g., Hammer, Screwdriver, Wrench',
#                     'Color': 'e.g., Black, Silver, Red'
#                 },
#                 'has_measurement': True,  # Has ALL measurements
#                 'measurement_label': 'Unit Type:'
#             }
#         }
        
#         return configs.get(self.category_name, configs['Paint'])
    
#     def setup_form(self):
#         """Setup form"""
#         self.dialog = tk.Toplevel(self.parent)
#         self.dialog.title(self.field_config['title'])
        
#         # Calculate height based on content - ADJUSTED FOR PAINT
#         base_height = 550  # Reduced base height
#         if self.field_config.get('has_measurement', False):
#             base_height += 40  # Add space for measurement section
        
#         # Adjust height based on number of fields (Paint has fewer fields)
#         if self.category_name == 'Paint':
#             base_height -= 40  # Further reduce for Paint
        
#         self.dialog.geometry(f"400x{base_height}")
#         self.dialog.configure(bg='white')
#         self.dialog.transient(self.parent)
#         self.dialog.grab_set()
        
#         self.position_form()
#         self.create_form_content()
        
#         # Load existing data if in edit mode
#         if self.is_edit_mode and self.product_data:
#             self.load_existing_data()
    
#     def position_form(self):
#         """Position form within dashboard - ADJUSTED FOR PAINT"""
#         self.parent.update_idletasks()
#         parent_x = self.parent.winfo_x()
#         parent_y = self.parent.winfo_y()
#         parent_width = self.parent.winfo_width()
#         parent_height = self.parent.winfo_height()
        
#         form_width = 350
#         form_height = 500  # Reduced base height
#         if self.field_config.get('has_measurement', False):
#             form_height += 40
        
#         # Further adjust for Paint
#         if self.category_name == 'Paint':
#             form_height -= 40
        
#         x = parent_x + parent_width - form_width - 20
#         y = parent_y + 100
        
#         screen_width = self.parent.winfo_screenwidth()
#         screen_height = self.parent.winfo_screenheight()
        
#         if x + form_width > screen_width:
#             x = screen_width - form_width - 20
        
#         if y + form_height > screen_height:
#             y = screen_height - form_height - 20
        
#         self.dialog.geometry(f"{form_width}x{form_height}+{x}+{y}")
    
#     def create_form_content(self):
#         """Create form content with measurement support"""
#         # Create scrollable form
#         canvas = tk.Canvas(self.dialog, bg='white', highlightthickness=0)
#         scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
#         self.scrollable_frame = tk.Frame(canvas, bg='white')
        
#         self.scrollable_frame.bind(
#             "<Configure>",
#             lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
#         )
        
#         canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
#         canvas.configure(yscrollcommand=scrollbar.set)
        
#         canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
#         scrollbar.pack(side="right", fill="y")
        
#         # Form Title
#         tk.Label(
#             self.scrollable_frame,
#             text=self.field_config['title'],
#             font=('Arial', 16, 'bold'),
#             fg='#2c3e50',
#             bg='white'
#         ).pack(anchor='w', pady=(0, 15))
        
#         # Image Upload Section
#         self.image_path_var = tk.StringVar(value=self.product_data.get('image_path', '') if self.product_data else '')
#         self.create_image_section(self.scrollable_frame)
        
#         # Dynamic fields based on category
#         self.entries = {}
#         self.create_dynamic_fields(self.scrollable_frame)
        
#         # Measurement selection section for categories with measurement support
#         if self.field_config.get('has_measurement', False) and self.measurements:
#             self.create_measurement_section(self.scrollable_frame)
        
#         # Stock input section - ONLY for non-Paint categories
#         if self.category_name != 'Paint':
#             self.create_stock_section(self.scrollable_frame)
        
#         # Buttons
#         self.create_buttons(self.scrollable_frame)
        
#         # Set focus to first field
#         first_field = list(self.entries.keys())[0] if self.entries else None
#         if first_field:
#             self.entries[first_field].focus()
        
#         self.dialog.bind('<Return>', lambda e: self.save_product())
    
#     def create_image_section(self, parent):
#         """Create image upload section"""
#         image_frame = tk.Frame(parent, bg='white')
#         image_frame.pack(fill=tk.X, pady=8)
        
#         tk.Label(
#             image_frame,
#             text="Product Image:",
#             font=('Arial', 10, 'bold'),
#             fg='#2c3e50',
#             bg='white',
#             width=12,
#             anchor='w'
#         ).pack(side=tk.LEFT)
        
#         image_entry = tk.Entry(
#             image_frame, 
#             textvariable=self.image_path_var,
#             font=('Arial', 10),
#             relief='solid', 
#             bd=1,
#             state='readonly'
#         )
#         image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(0, 8))
        
#         browse_btn = tk.Button(
#             image_frame,
#             text="Browse",
#             font=('Arial', 9),
#             bg='#95a5a6',
#             fg='white',
#             relief='flat',
#             command=self.browse_image
#         )
#         browse_btn.pack(side=tk.RIGHT)
    
#     def create_dynamic_fields(self, parent):
#         """Create fields based on configuration"""
#         for field_name, field_type, placeholder in self.field_config['fields']:
#             frame = tk.Frame(parent, bg='white')
#             frame.pack(fill=tk.X, pady=6)
            
#             tk.Label(
#                 frame,
#                 text=f"{field_name}:",
#                 font=('Arial', 10, 'bold'),
#                 fg='#2c3e50',
#                 bg='white',
#                 width=12,
#                 anchor='w'
#             ).pack(side=tk.LEFT)
            
#             if field_type == 'number':
#                 entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1, validate='key')
#                 entry.config(validatecommand=(entry.register(self.validate_number), '%P'))
#             else:
#                 entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1)
            
#             # Add placeholder text (only in add mode, not edit mode)
#             if placeholder and not self.is_edit_mode:
#                 entry.insert(0, placeholder)
#                 entry.bind('<FocusIn>', lambda e, entry=entry, placeholder=placeholder: self.clear_placeholder(entry, placeholder))
            
#             entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
#             self.entries[field_name] = entry
    
#     def create_measurement_section(self, parent):
#         """Create measurement unit selection section"""
#         measurement_frame = tk.Frame(parent, bg='white')
#         measurement_frame.pack(fill=tk.X, pady=8)
        
#         tk.Label(
#             measurement_frame,
#             text=self.field_config.get('measurement_label', 'Unit:'),
#             font=('Arial', 10, 'bold'),
#             fg='#2c3e50',
#             bg='white',
#             width=12,
#             anchor='w'
#         ).pack(side=tk.LEFT)
        
#         # Create dropdown with available measurements
#         self.measurement_var = tk.StringVar()
        
#         # Format measurements for display: "Feet (ft)" - FIXED: No duplicates
#         measurement_options = [f"{m[1]} ({m[2]})" for m in self.measurements]
        
#         self.measurement_combo = ttk.Combobox(
#             measurement_frame,
#             textvariable=self.measurement_var,
#             values=measurement_options,
#             state="readonly",
#             font=('Arial', 10)
#         )
#         self.measurement_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        
#         # Set default selection - first option for all non-Paint categories
#         if measurement_options:
#             self.measurement_combo.set(measurement_options[0])
#             self.selected_measurement = self.measurements[0]
    
#     def create_stock_section(self, parent):
#         """Create stock input section - ONLY for non-Paint categories"""
#         stock_frame = tk.Frame(parent, bg='white')
#         stock_frame.pack(fill=tk.X, pady=8)
        
#         tk.Label(
#             stock_frame,
#             text="Stock Quantity:",
#             font=('Arial', 10, 'bold'),
#             fg='#2c3e50',
#             bg='white',
#             width=12,
#             anchor='w'
#         ).pack(side=tk.LEFT)
        
#         self.stock_entry = tk.Entry(
#             stock_frame,
#             font=('Arial', 10),
#             relief='solid',
#             bd=1,
#             validate='key'
#         )
#         self.stock_entry.config(validatecommand=(self.stock_entry.register(self.validate_number), '%P'))
#         self.stock_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
#         self.stock_entry.insert(0, "0")
    
#     def create_buttons(self, parent):
#         """Create action buttons"""
#         button_frame = tk.Frame(parent, bg='white')
#         button_frame.pack(fill=tk.X, pady=15)
        
#         if self.is_edit_mode:
#             button_text = "Update Product"
#             button_command = self.update_product
#         else:
#             button_text = "Save Product"
#             button_command = self.save_product
        
#         save_btn = tk.Button(
#             button_frame,
#             text=button_text,
#             font=('Arial', 11, 'bold'),
#             bg='#27ae60',
#             fg='white',
#             relief='flat',
#             command=button_command
#         )
#         save_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
#         cancel_btn = tk.Button(
#             button_frame,
#             text="Cancel",
#             font=('Arial', 11),
#             bg='#95a5a6',
#             fg='white',
#             relief='flat',
#             command=self.dialog.destroy
#         )
#         cancel_btn.pack(side=tk.RIGHT)
    
#     def browse_image(self):
#         """Browse for image file"""
#         file_path = filedialog.askopenfilename(
#             title="Select Product Image",
#             filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
#         )
#         if file_path:
#             self.image_path_var.set(file_path)
    
#     def clear_placeholder(self, entry, placeholder):
#         """Clear placeholder text on focus"""
#         if entry.get() == placeholder:
#             entry.delete(0, tk.END)
    
#     def validate_number(self, value):
#         """Validate number input"""
#         if value == "":
#             return True
#         try:
#             float(value)
#             return True
#         except ValueError:
#             return False
    
#     def load_existing_data(self):
#         """Load existing product data into form fields for editing"""
#         if not self.product_data:
#             return
        
#         mappings = self.field_config['mappings']
#         placeholder_texts = self.field_config['placeholder_texts']
        
#         # Map existing data to form fields
#         for db_field, form_field in mappings.items():
#             if form_field and form_field in self.entries:
#                 value = self.product_data.get(db_field, '')
#                 if value is None:
#                     value = ''
                
#                 # Clear existing text and insert actual value
#                 self.entries[form_field].delete(0, tk.END)
#                 self.entries[form_field].insert(0, str(value))
        
#         # Set image path
#         image_path = self.product_data.get('image_path', '')
#         if image_path:
#             self.image_path_var.set(image_path)
        
#         # Load stock data - ONLY for non-Paint categories
#         if self.category_name != 'Paint' and hasattr(self, 'stock_entry'):
#             stock_value = self.product_data.get('current_stock', 0)
#             self.stock_entry.delete(0, tk.END)
#             self.stock_entry.insert(0, str(stock_value))
        
#         # Load measurement data if available
#         if self.field_config.get('has_measurement', False) and self.measurement_combo:
#             packing = self.product_data.get('packing', '')
#             if packing and packing.startswith("Unit: "):
#                 measurement_name = packing.replace("Unit: ", "")
#                 # Find and select the corresponding measurement
#                 for i, measurement in enumerate(self.measurements):
#                     if measurement[1] == measurement_name:
#                         measurement_options = [f"{m[1]} ({m[2]})" for m in self.measurements]
#                         self.measurement_combo.set(measurement_options[i])
#                         self.selected_measurement = measurement
#                         break
    
#     def get_form_data(self):
#         """Extract data from form fields based on category mapping"""
#         mappings = self.field_config['mappings']
#         form_data = {
#             'category_id': self.current_category,
#             'image_path': self.image_path_var.get()
#         }
        
#         # Map form fields to database fields
#         for db_field, form_field in mappings.items():
#             if form_field and form_field in self.entries:
#                 value = self.entries[form_field].get().strip()
                
#                 # Handle numeric fields
#                 if db_field in ['purchase_price', 'sale_price']:
#                     try:
#                         form_data[db_field] = float(value) if value else 0.0
#                     except ValueError:
#                         form_data[db_field] = 0.0
#                 else:
#                     form_data[db_field] = value
        
#         # Handle stock data - DIFFERENT FOR PAINT vs OTHER CATEGORIES
#         if self.category_name == 'Paint':
#             # For Paint, stock is in the main form fields
#             try:
#                 form_data['current_stock'] = int(self.entries['Stock'].get() or 0)
#             except ValueError:
#                 form_data['current_stock'] = 0
#         else:
#             # For other categories, stock is in the separate stock entry
#             try:
#                 if hasattr(self, 'stock_entry'):
#                     form_data['current_stock'] = int(self.stock_entry.get() or 0)
#                 else:
#                     form_data['current_stock'] = 0
#             except ValueError:
#                 form_data['current_stock'] = 0
        
#         # Handle measurement data for non-Paint categories
#         if self.field_config.get('has_measurement', False) and self.measurements:
#             # Get selected measurement
#             selected_display = self.measurement_var.get()
#             if selected_display:
#                 # Extract measurement name from display text "Feet (ft)"
#                 measurement_name = selected_display.split(' (')[0]
#                 # Store measurement info in packing field
#                 form_data['packing'] = f"Unit: {measurement_name}"
#             else:
#                 form_data['packing'] = ""
#         else:
#             # For Paint category, use existing packing
#             if 'packing' not in form_data:
#                 form_data['packing'] = ""
        
#         return form_data
    
#     def validate_required_fields(self):
#         """Validate all required fields"""
#         # Get category-specific required fields
#         required_fields = []
#         placeholder_texts = self.field_config['placeholder_texts']
        
#         for field_name in self.entries.keys():
#             if field_name in ['Purchase Price', 'Sale Price', 'Stock']:
#                 continue  # These are validated separately
#             required_fields.append(field_name)
        
#         # Validate text fields
#         for field in required_fields:
#             value = self.entries[field].get().strip()
#             placeholder = placeholder_texts.get(field, '')
            
#             if not value or (placeholder and value == placeholder):
#                 messagebox.showerror("Error", f"Please enter a valid {field}!")
#                 self.entries[field].focus()
#                 return False
        
#         # Validate measurement selection for measurement-based categories
#         if self.field_config.get('has_measurement', False) and self.measurements:
#             if not self.measurement_var.get():
#                 messagebox.showerror("Error", "Please select a measurement unit!")
#                 if self.measurement_combo:
#                     self.measurement_combo.focus()
#                 return False
        
#         # Validate stock - DIFFERENT LOGIC FOR PAINT vs OTHER CATEGORIES
#         if self.category_name == 'Paint':
#             # For Paint, validate stock from main form fields
#             try:
#                 stock = int(self.entries['Stock'].get() or 0)
#                 if stock < 0:
#                     messagebox.showerror("Error", "Stock cannot be negative!")
#                     self.entries['Stock'].focus()
#                     return False
#             except ValueError:
#                 messagebox.showerror("Error", "Please enter a valid stock number!")
#                 self.entries['Stock'].focus()
#                 return False
#         else:
#             # For other categories, validate stock from separate stock entry
#             if hasattr(self, 'stock_entry'):
#                 try:
#                     stock = int(self.stock_entry.get() or 0)
#                     if stock < 0:
#                         messagebox.showerror("Error", "Stock cannot be negative!")
#                         self.stock_entry.focus()
#                         return False
#                 except ValueError:
#                     messagebox.showerror("Error", "Please enter a valid stock number!")
#                     self.stock_entry.focus()
#                     return False
        
#         # Validate prices
#         try:
#             purchase_price = float(self.entries['Purchase Price'].get() or 0)
#             sale_price = float(self.entries['Sale Price'].get() or 0)
            
#             if purchase_price <= 0:
#                 messagebox.showerror("Error", "Purchase price must be greater than 0!")
#                 self.entries['Purchase Price'].focus()
#                 return False
            
#             if sale_price <= 0:
#                 messagebox.showerror("Error", "Sale price must be greater than 0!")
#                 self.entries['Sale Price'].focus()
#                 return False
            
#         except ValueError:
#             messagebox.showerror("Error", "Please enter valid numbers for price!")
#             return False
        
#         return True
    
#     def save_product(self):
#         """Save new product"""
#         try:
#             if not self.validate_required_fields():
#                 return
            
#             product_data = self.get_form_data()
            
#             # Use product_service to add product
#             result = self.product_service.add_product(product_data)
            
#             if result:
#                 messagebox.showinfo("Success", f"{self.category_name} product added successfully!")
#                 self.dialog.destroy()
                
#                 if self.refresh_callback:
#                     self.refresh_callback()
#             else:
#                 messagebox.showerror("Error", f"Failed to add {self.category_name} product!")
            
#         except ValueError as e:
#             messagebox.showerror("Error", str(e))
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to add product: {str(e)}")
    
#     def update_product(self):
#         """Update existing product"""
#         try:
#             if not self.validate_required_fields():
#                 return
            
#             product_data = self.get_form_data()
            
#             # Use product_service to update product
#             updated_count = self.product_service.update_product(self.product_id, product_data)
            
#             if updated_count > 0:
#                 messagebox.showinfo("Success", f"{self.category_name} product updated successfully!")
#                 self.dialog.destroy()
                
#                 if self.refresh_callback:
#                     self.refresh_callback()
#             else:
#                 messagebox.showerror("Error", f"Failed to update {self.category_name.lower()} product!")
                
#         except ValueError as e:
#             messagebox.showerror("Error", str(e))
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to update product: {str(e)}")
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.product_service import ProductService
from backend.measurement_service import MeasurementService
from PIL import Image, ImageTk
import os

class UniversalProductForm:
    def __init__(self, parent, product_service, current_category, refresh_callback, category_name, product_id=None, product_data=None):
        self.parent = parent
        self.product_service = product_service
        self.measurement_service = MeasurementService()
        self.current_category = current_category
        self.refresh_callback = refresh_callback
        self.category_name = category_name
        self.product_id = product_id
        self.product_data = product_data
        self.is_edit_mode = product_id is not None
        
        # Get measurements for this category
        self.measurements = self.get_measurements_for_category()
        self.selected_measurement = None
        
        # Measurement selection variables
        self.measurement_var = None
        self.measurement_combo = None
        
        self.field_config = self.get_field_config()
        self.setup_form()
    
    def get_measurements_for_category(self):
        """Get appropriate measurements based on category - FIXED: All measurements for all non-Paint categories"""
        if self.category_name == 'Paint':
            return []  # No measurements for Paint
        
        # For ALL other categories (Sanitary, Roof Sheet, Limination Sheet, Hardware), return ALL measurements
        measurements = []
        seen_names = set()
        
        # Get ALL measurements from all types
        all_measurements = []
        all_measurements.extend(self.measurement_service.get_measurements_by_type('Length'))
        all_measurements.extend(self.measurement_service.get_measurements_by_type('Weight'))
        all_measurements.extend(self.measurement_service.get_measurements_by_type('Volume'))
        all_measurements.extend(self.measurement_service.get_measurements_by_type('Count'))
        
        # Remove duplicates by name
        for measurement in all_measurements:
            if len(measurement) >= 2:  # Ensure measurement has at least name
                measurement_name = measurement[1]  # Name is at index 1
                if measurement_name not in seen_names:
                    seen_names.add(measurement_name)
                    measurements.append(measurement)
        
        return measurements
    
    def get_field_config(self):
        """Define fields for each category with specific measurement requirements"""
        configs = {
            'Paint': {
                'title': 'Edit Paint Product' if self.is_edit_mode else 'Add Paint Product',
                'fields': [
                    ("Company", "text", "e.g., Berger, Nippon, Jenson"),
                    ("Type", "text", "e.g., Emulsion, Enamel, Primer"),
                    ("Color", "text", "e.g., White, Cream, Sky Blue"),
                    ("Packing", "text", "e.g., 1L, 4L, 10L, 20L"),
                    ("Purchase Price", "number", "0"),
                    ("Sale Price", "number", "0"),
                    ("Stock", "number", "0")  # Stock field for Paint
                ],
                'mappings': {
                    'company': 'Company',
                    'type': 'Type', 
                    'color': 'Color',
                    'packing': 'Packing',
                    'purchase_price': 'Purchase Price',
                    'sale_price': 'Sale Price',
                    'current_stock': 'Stock'
                },
                'placeholder_texts': {
                    'Company': 'e.g., Berger, Nippon, Jenson',
                    'Type': 'e.g., Emulsion, Enamel, Primer',
                    'Color': 'e.g., White, Cream, Sky Blue',
                    'Packing': 'e.g., 1L, 4L, 10L, 20L'
                },
                'has_measurement': False  # No measurement for Paint
            },
            'Sanitary': {
                'title': 'Edit Sanitary Product' if self.is_edit_mode else 'Add Sanitary Product',
                'fields': [
                    ("Company", "text", "e.g., Swiss, Dura, Standard"),
                    ("Type", "text", "e.g., Wash Basin, Toilet, Tap"),
                    ("Color", "text", "e.g., White, Red, Blue"),
                    ("Size", "text", "e.g., Small, Medium, Large"),
                    ("Purchase Price", "number", "0"),
                    ("Sale Price", "number", "0")
                ],
                'mappings': {
                    'company': 'Company',
                    'type': 'Type',
                    'color': 'Color',
                    'volume': 'Size',
                    'purchase_price': 'Purchase Price',
                    'sale_price': 'Sale Price',
                    'current_stock': 'Stock'
                },
                'placeholder_texts': {
                    'Company': 'e.g., Swiss, Dura, Standard',
                    'Type': 'e.g., Wash Basin, Toilet, Tap',
                    'Color': 'e.g., White, Red, Blue',
                    'Size': 'e.g., Small, Medium, Large'
                },
                'has_measurement': True,  # Now has ALL measurements
                'measurement_label': 'Unit:'
            },
            'Roof Sheet': {
                'title': 'Edit Roof Sheet Product' if self.is_edit_mode else 'Add Roof Sheet Product',
                'fields': [
                    ("Company", "text", "e.g., Diamond, Metro, Sapphire"),
                    ("Type", "text", "e.g., Corrugated, Plain, Color Coated"),
                    ("Color", "text", "e.g., Silver, Red, Blue"),
                    ("Size", "text", "e.g., 8x4, 10x3, 12x4"),
                    ("Purchase Price", "number", "0"),
                    ("Sale Price", "number", "0")
                ],
                'mappings': {
                    'company': 'Company',
                    'type': 'Type',
                    'color': 'Color',
                    'volume': 'Size',
                    'purchase_price': 'Purchase Price',
                    'sale_price': 'Sale Price',
                    'current_stock': 'Stock'
                },
                'placeholder_texts': {
                    'Company': 'e.g., Diamond, Metro, Sapphire',
                    'Type': 'e.g., Corrugated, Plain, Color Coated',
                    'Color': 'e.g., Silver, Red, Blue',
                    'Size': 'e.g., 8x4, 10x3, 12x4'
                },
                'has_measurement': True,  # Now has ALL measurements
                'measurement_label': 'Unit:'
            },
            'Limination Sheet': {
                'title': 'Edit Limination Sheet Product' if self.is_edit_mode else 'Add Limination Sheet Product',
                'fields': [
                    ("Company", "text", "e.g., Diamond, Metro, Sapphire"),
                    ("Color", "text", "e.g., Silver, Golden, Wooden"),
                    ("Color Code", "text", "e.g., #FF0000, RGB255, Code123"),
                    ("Size", "text", "e.g., 8x4, 10x3, 12x4"),
                    ("Type", "text", "e.g., Glossy, Matte, Textured"),
                    ("Purchase Price", "number", "0"),
                    ("Sale Price", "number", "0")
                ],
                'mappings': {
                    'company': 'Company',
                    'type': 'Type',
                    'color': 'Color',
                    'packing': 'Color Code',
                    'volume': 'Size',
                    'purchase_price': 'Purchase Price',
                    'sale_price': 'Sale Price',
                    'current_stock': 'Stock'
                },
                'placeholder_texts': {
                    'Company': 'e.g., Diamond, Metro, Sapphire',
                    'Color': 'e.g., Silver, Golden, Wooden',
                    'Color Code': 'e.g., #FF0000, RGB255, Code123',
                    'Size': 'e.g., 8x4, 10x3, 12x4',
                    'Type': 'e.g., Glossy, Matte, Textured'
                },
                'has_measurement': True,  # Now has ALL measurements
                'measurement_label': 'Unit:'
            },
            'Hardware': {
                'title': 'Edit Hardware Product' if self.is_edit_mode else 'Add Hardware Product',
                'fields': [
                    ("Company", "text", "e.g., Bosch, Stanley, Makita"),
                    ("Type", "text", "e.g., Hammer, Screwdriver, Wrench"),
                    ("Color", "text", "e.g., Black, Silver, Red"),
                    ("Size", "text", "e.g., Small, Medium, Large, 10mm, 1/2 inch"),  # ADDED: Size field for Hardware
                    ("Purchase Price", "number", "0"),
                    ("Sale Price", "number", "0")
                ],
                'mappings': {
                    'company': 'Company',
                    'type': 'Type',
                    'color': 'Color',
                    'volume': 'Size',  # ADDED: Map Size to volume field
                    'purchase_price': 'Purchase Price',
                    'sale_price': 'Sale Price',
                    'current_stock': 'Stock'
                },
                'placeholder_texts': {
                    'Company': 'e.g., Bosch, Stanley, Makita',
                    'Type': 'e.g., Hammer, Screwdriver, Wrench',
                    'Color': 'e.g., Black, Silver, Red',
                    'Size': 'e.g., Small, Medium, Large, 10mm, 1/2 inch'  # ADDED: Placeholder for Size
                },
                'has_measurement': True,  # Has ALL measurements
                'measurement_label': 'Unit Type:'
            }
        }
        
        return configs.get(self.category_name, configs['Paint'])
    
    def setup_form(self):
        """Setup form"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.field_config['title'])
        
        # Calculate height based on content - ADJUSTED FOR PAINT
        base_height = 550  # Reduced base height
        if self.field_config.get('has_measurement', False):
            base_height += 40  # Add space for measurement section
        
        # Adjust height based on number of fields (Paint has fewer fields)
        if self.category_name == 'Paint':
            base_height -= 40  # Further reduce for Paint
        
        self.dialog.geometry(f"400x{base_height}")
        self.dialog.configure(bg='white')
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        self.position_form()
        self.create_form_content()
        
        # Load existing data if in edit mode
        if self.is_edit_mode and self.product_data:
            self.load_existing_data()
    
    def position_form(self):
        """Position form within dashboard - ADJUSTED FOR PAINT"""
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        form_width = 350
        form_height = 500  # Reduced base height
        if self.field_config.get('has_measurement', False):
            form_height += 40
        
        # Further adjust for Paint
        if self.category_name == 'Paint':
            form_height -= 40
        
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
        """Create form content with measurement support"""
        # Create scrollable form
        canvas = tk.Canvas(self.dialog, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Form Title
        tk.Label(
            self.scrollable_frame,
            text=self.field_config['title'],
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 15))
        
        # Image Upload Section
        self.image_path_var = tk.StringVar(value=self.product_data.get('image_path', '') if self.product_data else '')
        self.create_image_section(self.scrollable_frame)
        
        # Dynamic fields based on category
        self.entries = {}
        self.create_dynamic_fields(self.scrollable_frame)
        
        # Measurement selection section for categories with measurement support
        if self.field_config.get('has_measurement', False) and self.measurements:
            self.create_measurement_section(self.scrollable_frame)
        
        # Stock input section - ONLY for non-Paint categories
        if self.category_name != 'Paint':
            self.create_stock_section(self.scrollable_frame)
        
        # Buttons
        self.create_buttons(self.scrollable_frame)
        
        # Set focus to first field
        first_field = list(self.entries.keys())[0] if self.entries else None
        if first_field:
            self.entries[first_field].focus()
        
        self.dialog.bind('<Return>', lambda e: self.save_product())
    
    def create_image_section(self, parent):
        """Create image upload section"""
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
        """Create fields based on configuration"""
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
    
    def create_measurement_section(self, parent):
        """Create measurement unit selection section"""
        measurement_frame = tk.Frame(parent, bg='white')
        measurement_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            measurement_frame,
            text=self.field_config.get('measurement_label', 'Unit:'),
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        # Create dropdown with available measurements
        self.measurement_var = tk.StringVar()
        
        # Format measurements for display: "Feet (ft)" - FIXED: No duplicates
        measurement_options = [f"{m[1]} ({m[2]})" for m in self.measurements]
        
        self.measurement_combo = ttk.Combobox(
            measurement_frame,
            textvariable=self.measurement_var,
            values=measurement_options,
            state="readonly",
            font=('Arial', 10)
        )
        self.measurement_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        
        # Set default selection - first option for all non-Paint categories
        if measurement_options:
            self.measurement_combo.set(measurement_options[0])
            self.selected_measurement = self.measurements[0]
    
    def create_stock_section(self, parent):
        """Create stock input section - ONLY for non-Paint categories"""
        stock_frame = tk.Frame(parent, bg='white')
        stock_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            stock_frame,
            text="Stock Quantity:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.stock_entry = tk.Entry(
            stock_frame,
            font=('Arial', 10),
            relief='solid',
            bd=1,
            validate='key'
        )
        self.stock_entry.config(validatecommand=(self.stock_entry.register(self.validate_number), '%P'))
        self.stock_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        self.stock_entry.insert(0, "0")
    
    def create_buttons(self, parent):
        """Create action buttons"""
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
        """Browse for image file"""
        file_path = filedialog.askopenfilename(
            title="Select Product Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if file_path:
            self.image_path_var.set(file_path)
    
    def clear_placeholder(self, entry, placeholder):
        """Clear placeholder text on focus"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
    
    def validate_number(self, value):
        """Validate number input"""
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
        
        # Load stock data - ONLY for non-Paint categories
        if self.category_name != 'Paint' and hasattr(self, 'stock_entry'):
            stock_value = self.product_data.get('current_stock', 0)
            self.stock_entry.delete(0, tk.END)
            self.stock_entry.insert(0, str(stock_value))
        
        # Load measurement data if available
        if self.field_config.get('has_measurement', False) and self.measurement_combo:
            packing = self.product_data.get('packing', '')
            if packing and packing.startswith("Unit: "):
                measurement_name = packing.replace("Unit: ", "")
                # Find and select the corresponding measurement
                for i, measurement in enumerate(self.measurements):
                    if measurement[1] == measurement_name:
                        measurement_options = [f"{m[1]} ({m[2]})" for m in self.measurements]
                        self.measurement_combo.set(measurement_options[i])
                        self.selected_measurement = measurement
                        break
    
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
                else:
                    form_data[db_field] = value
        
        # Handle stock data - DIFFERENT FOR PAINT vs OTHER CATEGORIES
        if self.category_name == 'Paint':
            # For Paint, stock is in the main form fields
            try:
                form_data['current_stock'] = int(self.entries['Stock'].get() or 0)
            except ValueError:
                form_data['current_stock'] = 0
        else:
            # For other categories, stock is in the separate stock entry
            try:
                if hasattr(self, 'stock_entry'):
                    form_data['current_stock'] = int(self.stock_entry.get() or 0)
                else:
                    form_data['current_stock'] = 0
            except ValueError:
                form_data['current_stock'] = 0
        
        # Handle measurement data for non-Paint categories
        if self.field_config.get('has_measurement', False) and self.measurements:
            # Get selected measurement
            selected_display = self.measurement_var.get()
            if selected_display:
                # Extract measurement name from display text "Feet (ft)"
                measurement_name = selected_display.split(' (')[0]
                # Store measurement info in packing field
                form_data['packing'] = f"Unit: {measurement_name}"
            else:
                form_data['packing'] = ""
        else:
            # For Paint category, use existing packing
            if 'packing' not in form_data:
                form_data['packing'] = ""
        
        return form_data
    
    def validate_required_fields(self):
        """Validate all required fields"""
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
        
        # Validate measurement selection for measurement-based categories
        if self.field_config.get('has_measurement', False) and self.measurements:
            if not self.measurement_var.get():
                messagebox.showerror("Error", "Please select a measurement unit!")
                if self.measurement_combo:
                    self.measurement_combo.focus()
                return False
        
        # Validate stock - DIFFERENT LOGIC FOR PAINT vs OTHER CATEGORIES
        if self.category_name == 'Paint':
            # For Paint, validate stock from main form fields
            try:
                stock = int(self.entries['Stock'].get() or 0)
                if stock < 0:
                    messagebox.showerror("Error", "Stock cannot be negative!")
                    self.entries['Stock'].focus()
                    return False
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid stock number!")
                self.entries['Stock'].focus()
                return False
        else:
            # For other categories, validate stock from separate stock entry
            if hasattr(self, 'stock_entry'):
                try:
                    stock = int(self.stock_entry.get() or 0)
                    if stock < 0:
                        messagebox.showerror("Error", "Stock cannot be negative!")
                        self.stock_entry.focus()
                        return False
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid stock number!")
                    self.stock_entry.focus()
                    return False
        
        # Validate prices
        try:
            purchase_price = float(self.entries['Purchase Price'].get() or 0)
            sale_price = float(self.entries['Sale Price'].get() or 0)
            
            if purchase_price <= 0:
                messagebox.showerror("Error", "Purchase price must be greater than 0!")
                self.entries['Purchase Price'].focus()
                return False
            
            if sale_price <= 0:
                messagebox.showerror("Error", "Sale price must be greater than 0!")
                self.entries['Sale Price'].focus()
                return False
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for price!")
            return False
        
        return True
    
    def save_product(self):
        """Save new product"""
        try:
            if not self.validate_required_fields():
                return
            
            product_data = self.get_form_data()
            
            # Use product_service to add product
            result = self.product_service.add_product(product_data)
            
            if result:
                messagebox.showinfo("Success", f"{self.category_name} product added successfully!")
                self.dialog.destroy()
                
                if self.refresh_callback:
                    self.refresh_callback()
            else:
                messagebox.showerror("Error", f"Failed to add {self.category_name} product!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {str(e)}")
    
    def update_product(self):
        """Update existing product"""
        try:
            if not self.validate_required_fields():
                return
            
            product_data = self.get_form_data()
            
            # Use product_service to update product
            updated_count = self.product_service.update_product(self.product_id, product_data)
            
            if updated_count > 0:
                messagebox.showinfo("Success", f"{self.category_name} product updated successfully!")
                self.dialog.destroy()
                
                if self.refresh_callback:
                    self.refresh_callback()
            else:
                messagebox.showerror("Error", f"Failed to update {self.category_name.lower()} product!")
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update product: {str(e)}")