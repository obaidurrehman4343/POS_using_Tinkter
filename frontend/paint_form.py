import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.product_service import ProductService
from PIL import Image, ImageTk
import os

class PaintForm:
    def __init__(self, parent, product_service, current_category, refresh_callback):
        self.parent = parent
        self.product_service = product_service
        self.current_category = current_category
        self.refresh_callback = refresh_callback
        self.setup_form()
    
    def setup_form(self):
        """Setup the paint form"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add Paint Product")
        self.dialog.geometry("450x550")
        self.dialog.configure(bg='white')
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Position within dashboard boundaries
        self.position_form_within_dashboard()
        self.create_form_content()
    
    def position_form_within_dashboard(self):
        """Position the form within dashboard boundaries"""
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
        """Create form content"""
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
            text="Add Paint Product",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 15))
        
        # Image Upload Section
        image_frame = tk.Frame(self.scrollable_frame, bg='white')
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
        
        # 🎨 Paint Specific Fields
        fields = [
            ("Company", "text", "e.g., Berger, Nippon, Jenson"),
            ("Type", "text", "e.g., Emulsion, Enamel, Primer"),
            ("Color", "text", "e.g., White, Cream, Sky Blue"),
            ("Packing", "text", "e.g., 1L, 4L, 10L, 20L"),
            ("Volume", "text", "e.g., 1 liter, 4 liters"),
            ("Purchase Price", "number", "0"),
            ("Sale Price", "number", "0"),
            ("Stock", "number", "0")
        ]
        
        self.entries = {}
        
        for field_name, field_type, placeholder in fields:
            frame = tk.Frame(self.scrollable_frame, bg='white')
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
        button_frame = tk.Frame(self.scrollable_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=15)
        
        def save_product():
            try:
                # 🎨 Map paint fields to database columns
                product_data = {
                    'category_id': self.current_category,
                    'company': self.entries['Company'].get().strip(),
                    'type': self.entries['Type'].get().strip(),
                    'color': self.entries['Color'].get().strip(),
                    'sale_price': float(self.entries['Sale Price'].get() or 0),
                    'purchase_price': float(self.entries['Purchase Price'].get() or 0),
                    'packing': self.entries['Packing'].get().strip(),
                    'volume': self.entries['Volume'].get().strip(),
                    'current_stock': int(self.entries['Stock'].get() or 0),
                    'image_path': self.image_path_var.get()
                }
                
                # Validate required fields and check for placeholders
                required_fields = ['Company', 'Type', 'Color', 'Packing']
                placeholder_texts = {
                    'Company': 'e.g., Berger, Nippon, Jenson',
                    'Type': 'e.g., Emulsion, Enamel, Primer',
                    'Color': 'e.g., White, Cream, Sky Blue',
                    'Packing': 'e.g., 1L, 4L, 10L, 20L'
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
                    self.entries['Stock'].focus()
                    return
                
                # Use product_service
                self.product_service.add_product(product_data)
                messagebox.showinfo("Success", "Paint product added successfully!")
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