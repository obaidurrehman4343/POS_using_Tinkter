import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.product_service import ProductService
from PIL import Image, ImageTk
import os

class HardwareForm:
    def __init__(self, parent, product_service, current_category, refresh_callback):
        self.parent = parent
        self.product_service = product_service
        self.current_category = current_category
        self.refresh_callback = refresh_callback
        self.entries = {}  # Initialize entries dictionary
        self.setup_form()
    
    def setup_form(self):
        """Setup the hardware form"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add Hardware Product")
        self.dialog.geometry("500x650")
        self.dialog.configure(bg='white')
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        self.position_form_within_dashboard()
        self.create_form_content()
    
    def position_form_within_dashboard(self):
        """Position the form within dashboard boundaries"""
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        form_width = 500
        form_height = 650
        x = parent_x + parent_width - form_width - 20
        y = parent_y + 50
        
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        if x + form_width > screen_width:
            x = screen_width - form_width - 20
        
        if y + form_height > screen_height:
            y = screen_height - form_height - 20
        
        self.dialog.geometry(f"{form_width}x{form_height}+{x}+{y}")
    
    def create_form_content(self):
        """Create form content with hardware specific fields"""
        canvas = tk.Canvas(self.dialog, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
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
            text="Add Hardware Product",
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
        
        self.image_path_var = tk.StringVar()
        image_entry = tk.Entry(
            image_frame, 
            textvariable=self.image_path_var,
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
                self.image_path_var.set(file_path)
        
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
        
        # Product Type Selection
        type_frame = tk.Frame(scrollable_frame, bg='white')
        type_frame.pack(fill=tk.X, pady=6)
        
        tk.Label(
            type_frame,
            text="Product Type:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.product_type_var = tk.StringVar()
        product_type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.product_type_var,
            values=[
                "Screws & Nails",
                "Bolts & Nuts", 
                "Electrical Wires",
                "Pipes & Fittings",
                "Door Locks",
                "Handles & Knobs",
                "Hinges",
                "Tools",
                "Other Hardware"
            ],
            state='readonly',
            font=('Arial', 10)
        )
        product_type_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        
        # Base Unit Selection
        base_unit_frame = tk.Frame(scrollable_frame, bg='white')
        base_unit_frame.pack(fill=tk.X, pady=6)
        
        tk.Label(
            base_unit_frame,
            text="Base Unit:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.base_unit_var = tk.StringVar(value="piece")
        base_unit_combo = ttk.Combobox(
            base_unit_frame,
            textvariable=self.base_unit_var,
            values=["piece", "kilogram", "meter", "set", "box", "packet"],
            state='readonly',
            font=('Arial', 10)
        )
        base_unit_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        
        # Conversion Settings Frame
        conversion_frame = tk.Frame(scrollable_frame, bg='#f8f9fa', relief='solid', bd=1)
        conversion_frame.pack(fill=tk.X, pady=10, padx=5)
        
        tk.Label(
            conversion_frame,
            text="Unit Conversion Settings:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w', pady=(5, 10), padx=10)
        
        # Pieces per KG for weight-based items
        pieces_frame = tk.Frame(conversion_frame, bg='#f8f9fa')
        pieces_frame.pack(fill=tk.X, pady=3, padx=10)
        
        tk.Label(
            pieces_frame,
            text="Pieces per KG:",
            font=('Arial', 9, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.pieces_per_kg_var = tk.StringVar(value="0")
        pieces_entry = tk.Entry(
            pieces_frame,
            textvariable=self.pieces_per_kg_var,
            font=('Arial', 9),
            relief='solid',
            bd=1,
            validate='key'
        )
        pieces_entry.config(validatecommand=(pieces_entry.register(self.validate_number), '%P'))
        pieces_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2)
        
        # Length per Unit for length-based items
        length_frame = tk.Frame(conversion_frame, bg='#f8f9fa')
        length_frame.pack(fill=tk.X, pady=3, padx=10)
        
        tk.Label(
            length_frame,
            text="Length per Unit (m):",
            font=('Arial', 9, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.length_per_unit_var = tk.StringVar(value="0")
        length_entry = tk.Entry(
            length_frame,
            textvariable=self.length_per_unit_var,
            font=('Arial', 9),
            relief='solid',
            bd=1,
            validate='key'
        )
        length_entry.config(validatecommand=(length_entry.register(self.validate_number), '%P'))
        length_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2)
        
        # Width per Unit for area-based items
        width_frame = tk.Frame(conversion_frame, bg='#f8f9fa')
        width_frame.pack(fill=tk.X, pady=3, padx=10)
        
        tk.Label(
            width_frame,
            text="Width per Unit (m):",
            font=('Arial', 9, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.width_per_unit_var = tk.StringVar(value="0")
        width_entry = tk.Entry(
            width_frame,
            textvariable=self.width_per_unit_var,
            font=('Arial', 9),
            relief='solid',
            bd=1,
            validate='key'
        )
        width_entry.config(validatecommand=(width_entry.register(self.validate_number), '%P'))
        width_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2)
        
        # Basic Product Information
        basic_fields = [
            ("Company", "text", "e.g., China, Local, Brand Name"),
            ("Product Name", "text", "e.g., Wood Screw, Door Lock, Cable"),
            ("Color/Material", "text", "e.g., Steel, Brass, Black, Silver"),
            ("Size/Dimensions", "text", "e.g., 2inch, 10mm, 2x4"),
            ("Material Type", "text", "e.g., Metal, Plastic, Wood"),
            ("Specifications", "text", "e.g., Rust Proof, Waterproof"),
            ("Purchase Price", "number", "0"),
            ("Sale Price", "number", "0"),
            ("Stock Quantity", "number", "0")
        ]
        
        for field_name, field_type, placeholder in basic_fields:
            frame = tk.Frame(scrollable_frame, bg='white')
            frame.pack(fill=tk.X, pady=6)
            
            tk.Label(
                frame,
                text=f"{field_name}:",
                font=('Arial', 10, 'bold'),
                fg='#2c3e50',
                bg='white',
                width=15,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            if field_type == 'number':
                entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1, validate='key')
                entry.config(validatecommand=(entry.register(self.validate_number), '%P'))
            else:
                entry = tk.Entry(frame, font=('Arial', 10), relief='solid', bd=1)
            
            # Add placeholder text
            if placeholder:
                entry.insert(0, placeholder)
                def clear_placeholder(event, e=entry, p=placeholder):
                    if e.get() == p:
                        e.delete(0, tk.END)
                entry.bind('<FocusIn>', clear_placeholder)
            
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
            self.entries[field_name] = entry
        
        # Buttons
        button_frame = tk.Frame(scrollable_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=15)
        
        def save_product():
            try:
                # Get conversion values
                pieces_per_kg = float(self.pieces_per_kg_var.get() or 0)
                length_per_unit = float(self.length_per_unit_var.get() or 0)
                width_per_unit = float(self.width_per_unit_var.get() or 0)
                
                # Map hardware fields to database columns
                product_data = {
                    'category_id': self.current_category,
                    'company': self.entries['Company'].get().strip(),
                    'type': self.entries['Product Name'].get().strip(),
                    'color': self.entries['Color/Material'].get().strip(),
                    'sale_price': float(self.entries['Sale Price'].get() or 0),
                    'purchase_price': float(self.entries['Purchase Price'].get() or 0),
                    'packing': self.base_unit_var.get(),
                    'volume': self.entries['Size/Dimensions'].get().strip(),
                    'current_stock': int(self.entries['Stock Quantity'].get() or 0),
                    'image_path': self.image_path_var.get(),
                    'unit_type': self.base_unit_var.get(),
                    'material_type': self.entries['Material Type'].get().strip(),
                    'specifications': self.entries['Specifications'].get().strip(),
                    'base_unit': self.base_unit_var.get(),
                    'pieces_per_kg': pieces_per_kg,
                    'length_per_unit': length_per_unit,
                    'width_per_unit': width_per_unit
                }
                
                # Validate required fields and check for placeholders
                required_fields = ['Company', 'Product Name', 'Color/Material']
                placeholder_texts = {
                    'Company': 'e.g., China, Local, Brand Name',
                    'Product Name': 'e.g., Wood Screw, Door Lock, Cable',
                    'Color/Material': 'e.g., Steel, Brass, Black, Silver'
                }
                
                for field in required_fields:
                    value = self.entries[field].get().strip()
                    if not value or value == placeholder_texts[field]:
                        messagebox.showerror("Error", f"Please enter a valid {field}!")
                        self.entries[field].focus()
                        return
                
                # Validate prices and stock
                if product_data['purchase_price'] <= 0:
                    messagebox.showerror("Error", "Purchase price must be greater than 0!")
                    self.entries['Purchase Price'].focus()
                    return
                
                if product_data['sale_price'] <= 0:
                    messagebox.showerror("Error", "Sale price must be greater than 0!")
                    self.entries['Sale Price'].focus()
                    return
                
                if product_data['current_stock'] < 0:
                    messagebox.showerror("Error", "Stock quantity cannot be negative!")
                    self.entries['Stock Quantity'].focus()
                    return
                
                # Validate conversion settings based on base unit
                if self.base_unit_var.get() == "kilogram" and pieces_per_kg <= 0:
                    messagebox.showerror("Error", "Please enter valid 'Pieces per KG' for kilogram-based items!")
                    return
                
                if self.base_unit_var.get() == "meter" and length_per_unit <= 0:
                    messagebox.showerror("Error", "Please enter valid 'Length per Unit' for meter-based items!")
                    return
                
                # Use product_service
                self.product_service.add_product(product_data)
                messagebox.showinfo("Success", "Hardware product added successfully!")
                self.dialog.destroy()
                self.refresh_callback()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add product: {str(e)}")
        
        save_btn = tk.Button(
            button_frame,
            text="Save Product",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=save_product
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
        
        # Set focus to first field
        self.entries['Company'].focus()
        
        # Bind Enter key to save
        self.dialog.bind('<Return>', lambda e: save_product())
    
    def validate_number(self, value):
        """Validate number input"""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False