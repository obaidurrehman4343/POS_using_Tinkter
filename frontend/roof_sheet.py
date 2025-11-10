# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# from backend.database import Database
# from PIL import Image, ImageTk
# import os

# class RoofSheetForm:
#     def __init__(self, parent, db, current_category, refresh_callback):
#         self.parent = parent
#         self.db = db
#         self.current_category = current_category
#         self.refresh_callback = refresh_callback
#         self.setup_form()
    
#     def setup_form(self):
#         """Setup the roof sheet form - SAME UI as Paint"""
#         self.dialog = tk.Toplevel(self.parent)
#         self.dialog.title("Add Roof Sheet Product")
#         self.dialog.geometry("500x650")
#         self.dialog.configure(bg='white')
#         self.dialog.transient(self.parent)
#         self.dialog.grab_set()
        
#         # Center the dialog
#         self.dialog.update_idletasks()
#         x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
#         y = (self.dialog.winfo_screenheight() // 2) - (650 // 2)
#         self.dialog.geometry(f"500x650+{x}+{y}")
        
#         # Create scrollable form - SAME as Paint
#         canvas = tk.Canvas(self.dialog, bg='white', highlightthickness=0)
#         scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
#         self.scrollable_frame = tk.Frame(canvas, bg='white')
        
#         self.scrollable_frame.bind(
#             "<Configure>",
#             lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
#         )
        
#         canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
#         canvas.configure(yscrollcommand=scrollbar.set)
        
#         canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
#         scrollbar.pack(side="right", fill="y")
        
#         # Form Title
#         tk.Label(
#             self.scrollable_frame,
#             text="Add Roof Sheet Product",
#             font=('Arial', 18, 'bold'),
#             fg='#2c3e50',
#             bg='white'
#         ).pack(anchor='w', pady=(0, 20))
        
#         # Image Upload Section - SAME as Paint
#         image_frame = tk.Frame(self.scrollable_frame, bg='white')
#         image_frame.pack(fill=tk.X, pady=10)
        
#         tk.Label(
#             image_frame,
#             text="Product Image:",
#             font=('Arial', 11, 'bold'),
#             fg='#2c3e50',
#             bg='white',
#             width=15,
#             anchor='w'
#         ).pack(side=tk.LEFT)
        
#         self.image_path_var = tk.StringVar()
#         image_entry = tk.Entry(
#             image_frame, 
#             textvariable=self.image_path_var,
#             font=('Arial', 11), 
#             relief='solid', 
#             bd=1,
#             state='readonly'
#         )
#         image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(0, 10))
        
#         def browse_image():
#             file_path = filedialog.askopenfilename(
#                 title="Select Product Image",
#                 filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
#             )
#             if file_path:
#                 self.image_path_var.set(file_path)
        
#         browse_btn = tk.Button(
#             image_frame,
#             text="Browse",
#             font=('Arial', 10),
#             bg='#95a5a6',
#             fg='white',
#             relief='flat',
#             command=browse_image
#         )
#         browse_btn.pack(side=tk.RIGHT)
        
#         # 🏗️ Roof Sheet Specific Fields (same layout as Paint but different fields)
#         fields = [
#             ("Company", "text"),
#             ("Type", "text"),
#             ("Color", "text"),
#             ("Volume", "text"),  # 🆕 Volume instead of Packing
#             ("Purchase Price", "number"),
#             ("Sale Price", "number"),
#             ("Stock", "number")
#         ]
        
#         self.entries = {}
        
#         for field_name, field_type in fields:
#             frame = tk.Frame(self.scrollable_frame, bg='white')
#             frame.pack(fill=tk.X, pady=8)
            
#             tk.Label(
#                 frame,
#                 text=f"{field_name}:",
#                 font=('Arial', 11, 'bold'),
#                 fg='#2c3e50',
#                 bg='white',
#                 width=15,
#                 anchor='w'
#             ).pack(side=tk.LEFT)
            
#             if field_type == 'number':
#                 entry = tk.Entry(frame, font=('Arial', 11), relief='solid', bd=1, validate='key')
#                 entry.config(validatecommand=(entry.register(self.validate_number), '%P'))
#             else:
#                 entry = tk.Entry(frame, font=('Arial', 11), relief='solid', bd=1)
            
#             entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
#             self.entries[field_name] = entry
        
#         # Buttons - SAME as Paint
#         button_frame = tk.Frame(self.scrollable_frame, bg='white')
#         button_frame.pack(fill=tk.X, pady=20)
        
#         def save_product():
#             try:
#                 # 🏗️ Map roof sheet fields to database columns
#                 product_data = {
#                     'category_id': self.current_category,
#                     'company': self.entries['Company'].get().strip(),
#                     'type': self.entries['Type'].get().strip(),
#                     'color': self.entries['Color'].get().strip(),
#                     'sale_price': float(self.entries['Sale Price'].get() or 0),
#                     'purchase_price': float(self.entries['Purchase Price'].get() or 0),
#                     'packing': "",  # Not used for roof sheets
#                     'volume': self.entries['Volume'].get().strip(),  # Using 'volume' column for size
#                     'current_stock': int(self.entries['Stock'].get() or 0),
#                     'image_path': self.image_path_var.get()
#                 }
                
#                 # Validate required fields - SAME validation as Paint
#                 required_fields = ['Company', 'Type', 'Color', 'Volume']
#                 for field in required_fields:
#                     if not self.entries[field].get().strip():
#                         messagebox.showerror("Error", f"{field} is required!")
#                         return
                
#                 self.db.add_product(product_data)
#                 messagebox.showinfo("Success", "Roof Sheet product added successfully!")
#                 self.dialog.destroy()
#                 self.refresh_callback()
                
#             except ValueError:
#                 messagebox.showerror("Error", "Please enter valid numbers for price and stock!")
#             except Exception as e:
#                 messagebox.showerror("Error", f"Failed to add product: {str(e)}")
        
#         save_btn = tk.Button(
#             button_frame,
#             text="Save Product",
#             font=('Arial', 12, 'bold'),
#             bg='#27ae60',
#             fg='white',
#             relief='flat',
#             command=save_product
#         )
#         save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
#         cancel_btn = tk.Button(
#             button_frame,
#             text="Cancel",
#             font=('Arial', 12),
#             bg='#95a5a6',
#             fg='white',
#             relief='flat',
#             command=self.dialog.destroy
#         )
#         cancel_btn.pack(side=tk.RIGHT)
        
#         # Set focus to first field - SAME as Paint
#         self.entries['Company'].focus()
    
#     def validate_number(self, value):
#         """Validate number input - SAME as Paint"""
#         if value == "":
#             return True
#         try:
#             float(value)
#             return True
#         except ValueError:
#             return False
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.database import Database
from PIL import Image, ImageTk
import os

class RoofSheetForm:
    def __init__(self, parent, db, current_category, refresh_callback):
        self.parent = parent
        self.db = db
        self.current_category = current_category
        self.refresh_callback = refresh_callback
        self.setup_form()
    
    def setup_form(self):
        """Setup the roof sheet form - Smaller size and positioned below button"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add Roof Sheet Product")
        self.dialog.geometry("450x550")  # 🆕 Smaller size
        self.dialog.configure(bg='white')
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # 🆕 Position below Add Product button
        self.position_form_below_button()
        
        self.create_form_content()
    
    def position_form_below_button(self):
        """Position the form within dashboard boundaries"""
        # Wait for the parent window to update its geometry
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
        
        self.dialog.geometry(f"{form_width}x{form_height}+{x}+{y}")
    
    def create_form_content(self):
        """Create form content with smaller size"""
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
        
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)  # 🆕 Smaller padding
        scrollbar.pack(side="right", fill="y")
        
        # Form Title
        tk.Label(
            self.scrollable_frame,
            text="Add Roof Sheet Product",
            font=('Arial', 16, 'bold'),  # 🆕 Smaller font
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 15))  # 🆕 Smaller padding
        
        # Image Upload Section
        image_frame = tk.Frame(self.scrollable_frame, bg='white')
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
        
        # 🏗️ Roof Sheet Specific Fields
        fields = [
            ("Company", "text"),
            ("Type", "text"),
            ("Color", "text"),
            ("Volume", "text"),  # 🆕 Volume instead of Packing
            ("Purchase Price", "number"),
            ("Sale Price", "number"),
            ("Stock", "number")
        ]
        
        self.entries = {}
        
        for field_name, field_type in fields:
            frame = tk.Frame(self.scrollable_frame, bg='white')
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
            self.entries[field_name] = entry
        
        # Buttons
        button_frame = tk.Frame(self.scrollable_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=15)  # 🆕 Smaller padding
        
        def save_product():
            try:
                # 🏗️ Map roof sheet fields to database columns
                product_data = {
                    'category_id': self.current_category,
                    'company': self.entries['Company'].get().strip(),
                    'type': self.entries['Type'].get().strip(),
                    'color': self.entries['Color'].get().strip(),
                    'sale_price': float(self.entries['Sale Price'].get() or 0),
                    'purchase_price': float(self.entries['Purchase Price'].get() or 0),
                    'packing': "",  # Not used for roof sheets
                    'volume': self.entries['Volume'].get().strip(),  # Using 'volume' column for size
                    'current_stock': int(self.entries['Stock'].get() or 0),
                    'image_path': self.image_path_var.get()
                }
                
                # Validate required fields
                required_fields = ['Company', 'Type', 'Color', 'Volume']
                for field in required_fields:
                    if not self.entries[field].get().strip():
                        messagebox.showerror("Error", f"{field} is required!")
                        return
                
                self.db.add_product(product_data)
                messagebox.showinfo("Success", "Roof Sheet product added successfully!")
                self.dialog.destroy()
                self.refresh_callback()
                
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
            command=self.dialog.destroy
        )
        cancel_btn.pack(side=tk.RIGHT)
        
        # Set focus to first field
        self.entries['Company'].focus()
        
        # 🆕 Bind Enter key to save
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