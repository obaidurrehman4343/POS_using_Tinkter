import tkinter as tk
from tkinter import ttk, messagebox
from backend.measurement_service import MeasurementService

class MeasurementForm:
    def __init__(self, parent, refresh_callback=None):
        self.parent = parent
        self.measurement_service = MeasurementService()
        self.refresh_callback = refresh_callback
        
        self.setup_dialog()
        self.create_form()
    
    def setup_dialog(self):
        """Setup compact dialog window"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add Measurement Unit")
        self.dialog.geometry("400x500")  # Slightly taller to fit buttons
        self.dialog.configure(bg='white')
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"400x500+{x}+{y}")
        
        # Make dialog modal
        self.dialog.focus_set()
    
    def create_form(self):
        """Create compact measurement form"""
        # Create main container with scrollbar to ensure everything fits
        main_frame = tk.Frame(self.dialog, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Add Measurement Unit",
            font=('Arial', 14, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(anchor='w', pady=(0, 15))
        
        # Form fields
        self.create_form_fields(main_frame)
        
        # Example section
        self.create_example_section(main_frame)
        
        # Buttons section - ENSURED TO BE AT BOTTOM
        self.create_action_buttons(main_frame)
    
    def create_form_fields(self, parent):
        """Create compact form input fields"""
        # Measurement Name
        name_frame = tk.Frame(parent, bg='white')
        name_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            name_frame,
            text="Name:",
            font=('Arial', 9, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=8,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(
            name_frame,
            textvariable=self.name_var,
            font=('Arial', 9),
            relief='solid',
            bd=1
        )
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2, padx=(5, 0))
        self.name_entry.insert(0, "Feet")
        self.name_entry.focus()
        
        # Unit Code
        code_frame = tk.Frame(parent, bg='white')
        code_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            code_frame,
            text="Code:",
            font=('Arial', 9, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=8,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.code_var = tk.StringVar()
        self.code_entry = tk.Entry(
            code_frame,
            textvariable=self.code_var,
            font=('Arial', 9),
            relief='solid',
            bd=1
        )
        self.code_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2, padx=(5, 0))
        self.code_entry.insert(0, "ft")
        
        # Measurement Type
        type_frame = tk.Frame(parent, bg='white')
        type_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            type_frame,
            text="Type:",
            font=('Arial', 9, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=8,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.type_var = tk.StringVar(value="Length")
        type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.type_var,
            values=["Length", "Weight", "Volume", "Count"],
            state="readonly",
            font=('Arial', 9)
        )
        type_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2, padx=(5, 0))
        
        # Base Unit
        base_unit_frame = tk.Frame(parent, bg='white')
        base_unit_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            base_unit_frame,
            text="Base Unit:",
            font=('Arial', 9, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=8,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.base_unit_var = tk.StringVar()
        self.base_unit_entry = tk.Entry(
            base_unit_frame,
            textvariable=self.base_unit_var,
            font=('Arial', 9),
            relief='solid',
            bd=1
        )
        self.base_unit_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2, padx=(5, 0))
        self.base_unit_entry.insert(0, "meter")
        
        # Conversion Factor
        conversion_frame = tk.Frame(parent, bg='white')
        conversion_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            conversion_frame,
            text="Conversion:",
            font=('Arial', 9, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=8,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.conversion_var = tk.StringVar(value="0.3048")
        self.conversion_entry = tk.Entry(
            conversion_frame,
            textvariable=self.conversion_var,
            font=('Arial', 9),
            relief='solid',
            bd=1,
            validate='key'
        )
        self.conversion_entry.config(validatecommand=(self.conversion_entry.register(self.validate_float), '%P'))
        self.conversion_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2, padx=(5, 0))
        
        # Description
        desc_frame = tk.Frame(parent, bg='white')
        desc_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            desc_frame,
            text="Description:",
            font=('Arial', 9, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=8,
            anchor='w'
        ).pack(side=tk.LEFT, anchor='n')
        
        self.desc_text = tk.Text(
            desc_frame,
            font=('Arial', 9),
            relief='solid',
            bd=1,
            height=2
        )
        self.desc_text.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2, padx=(5, 0))
        self.desc_text.insert('1.0', "1 foot = 0.3048 meters")
    
    def create_example_section(self, parent):
        """Create compact example section"""
        example_frame = tk.Frame(parent, bg='#f8f9fa', relief='solid', bd=1)
        example_frame.pack(fill=tk.X, pady=10)
        
        # Example title
        example_title = tk.Label(
            example_frame,
            text="📋 Quick Examples:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        )
        example_title.pack(anchor='w', padx=8, pady=(8, 5))
        
        # Example buttons container
        examples_container = tk.Frame(example_frame, bg='#f8f9fa')
        examples_container.pack(fill=tk.X, padx=8, pady=(0, 8))
        
        # Example buttons
        examples = [
            ("📏 Feet", self.load_example_feet, '#3498db'),
            ("⚖️ Kg", self.load_example_kilogram, '#e74c3c'),
            ("⚖️ Lb", self.load_example_pounds, '#d35400'),
            ("💧 Liter", self.load_example_liter, '#2980b9'),
            ("🔢 Pcs", self.load_example_piece, '#9b59b6'),
            ("🔢 Doz", self.load_example_dozen, '#8e44ad')
        ]
        
        # Create buttons in a 3x2 grid
        for i, (text, command, color) in enumerate(examples):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                examples_container,
                text=text,
                font=('Arial', 8),
                bg=color,
                fg='white',
                relief='flat',
                cursor='hand2',
                command=command,
                width=6,
                height=1
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='ew')
        
        # Configure grid
        for i in range(3):
            examples_container.grid_columnconfigure(i, weight=1)
    
    def create_action_buttons(self, parent):
        """Create action buttons - ENSURED VISIBLE"""
        # Create a separate frame for buttons at the bottom
        button_container = tk.Frame(parent, bg='white')
        button_container.pack(fill=tk.X, side=tk.BOTTOM, pady=(20, 0))  # Force to bottom
        
        button_frame = tk.Frame(button_container, bg='white')
        button_frame.pack(fill=tk.X, pady=10)
        
        # Cancel button - LEFT side
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 10, 'bold'),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            width=8,
            command=self.cancel_form,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save button - RIGHT side  
        save_btn = tk.Button(
            button_frame,
            text="Save",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            width=10,
            command=self.save_measurement,
            cursor='hand2'
        )
        save_btn.pack(side=tk.RIGHT)
    
    # KEEP ALL THE LOAD EXAMPLE METHODS THE SAME AS BEFORE
    def load_example_feet(self):
        self.clear_form()
        self.name_var.set("Feet")
        self.code_var.set("ft")
        self.type_var.set("Length")
        self.base_unit_var.set("meter")
        self.conversion_var.set("0.3048")
        self.desc_text.delete('1.0', tk.END)
        self.desc_text.insert('1.0', "1 foot = 0.3048 meters")
        self.name_entry.focus()
    
    def load_example_kilogram(self):
        self.clear_form()
        self.name_var.set("Kilogram")
        self.code_var.set("kg")
        self.type_var.set("Weight")
        self.base_unit_var.set("gram")
        self.conversion_var.set("1000.0")
        self.desc_text.delete('1.0', tk.END)
        self.desc_text.insert('1.0', "1 kg = 1000 grams")
        self.name_entry.focus()
    
    def load_example_pounds(self):
        self.clear_form()
        self.name_var.set("Pounds")
        self.code_var.set("lb")
        self.type_var.set("Weight")
        self.base_unit_var.set("gram")
        self.conversion_var.set("453.592")
        self.desc_text.delete('1.0', tk.END)
        self.desc_text.insert('1.0', "1 lb = 453.592 grams")
        self.name_entry.focus()
    
    def load_example_liter(self):
        self.clear_form()
        self.name_var.set("Liter")
        self.code_var.set("L")
        self.type_var.set("Volume")
        self.base_unit_var.set("liter")
        self.conversion_var.set("1.0")
        self.desc_text.delete('1.0', tk.END)
        self.desc_text.insert('1.0', "Base volume unit")
        self.name_entry.focus()
    
    def load_example_piece(self):
        self.clear_form()
        self.name_var.set("Piece")
        self.code_var.set("pcs")
        self.type_var.set("Count")
        self.base_unit_var.set("piece")
        self.conversion_var.set("1.0")
        self.desc_text.delete('1.0', tk.END)
        self.desc_text.insert('1.0', "Base counting unit")
        self.name_entry.focus()
    
    def load_example_dozen(self):
        self.clear_form()
        self.name_var.set("Dozen")
        self.code_var.set("doz")
        self.type_var.set("Count")
        self.base_unit_var.set("piece")
        self.conversion_var.set("12.0")
        self.desc_text.delete('1.0', tk.END)
        self.desc_text.insert('1.0', "1 dozen = 12 pieces")
        self.name_entry.focus()
    
    def clear_form(self):
        self.name_var.set("")
        self.code_var.set("")
        self.type_var.set("Length")
        self.base_unit_var.set("")
        self.conversion_var.set("1.0")
        self.desc_text.delete('1.0', tk.END)
    
    def cancel_form(self):
        result = messagebox.askyesno("Confirm Cancel", "Are you sure you want to cancel?")
        if result:
            self.dialog.destroy()
    
    def validate_float(self, value):
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def validate_form(self):
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Please enter measurement name!")
            self.name_entry.focus()
            return False
        
        if not self.code_var.get().strip():
            messagebox.showerror("Error", "Please enter unit code!")
            self.code_entry.focus()
            return False
        
        if not self.type_var.get().strip():
            messagebox.showerror("Error", "Please select measurement type!")
            return False
        
        if not self.base_unit_var.get().strip():
            messagebox.showerror("Error", "Please enter base unit!")
            self.base_unit_entry.focus()
            return False
        
        try:
            conversion_factor = float(self.conversion_var.get())
            if conversion_factor <= 0:
                messagebox.showerror("Error", "Conversion factor must be greater than 0!")
                self.conversion_entry.focus()
                return False
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid conversion factor!")
            self.conversion_entry.focus()
            return False
        
        return True
    
    def save_measurement(self):
        try:
            if not self.validate_form():
                return
            
            name = self.name_var.get().strip()
            code = self.code_var.get().strip()
            measurement_type = self.type_var.get().strip()
            base_unit = self.base_unit_var.get().strip()
            conversion_factor = float(self.conversion_var.get())
            description = self.desc_text.get("1.0", tk.END).strip()
            
            measurement_id = self.measurement_service.add_measurement(
                name, code, measurement_type, base_unit, conversion_factor, description
            )
            
            if measurement_id:
                messagebox.showinfo("Success", f"Measurement '{name}' added successfully!")
                self.dialog.destroy()
                
                if self.refresh_callback:
                    self.refresh_callback()
            else:
                messagebox.showerror("Error", "Failed to save measurement!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save measurement: {str(e)}")

# import tkinter as tk
# from tkinter import ttk, messagebox
# from backend.measurement_service import MeasurementService

# class MeasurementForm:
#     def __init__(self, parent, refresh_callback=None):
#         self.parent = parent
#         self.measurement_service = MeasurementService()
#         self.refresh_callback = refresh_callback
        
#         self.setup_dialog()
#         self.create_form()
    
#     def setup_dialog(self):
#         """Setup the dialog window"""
#         self.dialog = tk.Toplevel(self.parent)
#         self.dialog.title("Add Measurement Unit")
#         self.dialog.geometry("500x500")
#         self.dialog.configure(bg='white')
#         self.dialog.transient(self.parent)
#         self.dialog.grab_set()
        
#         # Center the dialog
#         self.dialog.update_idletasks()
#         x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
#         y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
#         self.dialog.geometry(f"600x600+{x}+{y}")
        
#         # Make dialog modal
#         self.dialog.focus_set()
    
#     def create_form(self):
#         """Create the measurement form"""
#         # Create main container with scrollbar
#         main_frame = tk.Frame(self.dialog, bg='white')
#         main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
#         # Title
#         title_label = tk.Label(
#             main_frame,
#             text="Add New Measurement Unit",
#             font=('Arial', 16, 'bold'),
#             fg='#2c3e50',
#             bg='white'
#         )
#         title_label.pack(anchor='w', pady=(0, 20))
        
#         # Form fields
#         self.create_form_fields(main_frame)
        
#         # Example section
#         self.create_example_section(main_frame)
        
#         # Buttons section - FIXED: Proper Save and Cancel buttons
#         self.create_action_buttons(main_frame)
    
#     def create_form_fields(self, parent):
#         """Create form input fields"""
#         # Measurement Name
#         name_frame = tk.Frame(parent, bg='white')
#         name_frame.pack(fill=tk.X, pady=8)
        
#         tk.Label(
#             name_frame,
#             text="Measurement Name:",
#             font=('Arial', 10, 'bold'),
#             fg='#2c3e50',
#             bg='white',
#             width=15,
#             anchor='w'
#         ).pack(side=tk.LEFT)
        
#         self.name_var = tk.StringVar()
#         self.name_entry = tk.Entry(
#             name_frame,
#             textvariable=self.name_var,
#             font=('Arial', 10),
#             relief='solid',
#             bd=1
#         )
#         self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(10, 0))
#         self.name_entry.insert(0, "Feet")  # Example entry
#         self.name_entry.focus()
        
#         # Unit Code
#         code_frame = tk.Frame(parent, bg='white')
#         code_frame.pack(fill=tk.X, pady=8)
        
#         tk.Label(
#             code_frame,
#             text="Unit Code:",
#             font=('Arial', 10, 'bold'),
#             fg='#2c3e50',
#             bg='white',
#             width=15,
#             anchor='w'
#         ).pack(side=tk.LEFT)
        
#         self.code_var = tk.StringVar()
#         self.code_entry = tk.Entry(
#             code_frame,
#             textvariable=self.code_var,
#             font=('Arial', 10),
#             relief='solid',
#             bd=1
#         )
#         self.code_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(10, 0))
#         self.code_entry.insert(0, "ft")  # Example entry
        
#         # Measurement Type
#         type_frame = tk.Frame(parent, bg='white')
#         type_frame.pack(fill=tk.X, pady=8)
        
#         tk.Label(
#             type_frame,
#             text="Measurement Type:",
#             font=('Arial', 10, 'bold'),
#             fg='#2c3e50',
#             bg='white',
#             width=15,
#             anchor='w'
#         ).pack(side=tk.LEFT)
        
#         self.type_var = tk.StringVar(value="Length")
#         type_combo = ttk.Combobox(
#             type_frame,
#             textvariable=self.type_var,
#             values=["Length", "Weight", "Volume", "Count"],
#             state="readonly",
#             font=('Arial', 10)
#         )
#         type_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(10, 0))
        
#         # Base Unit
#         base_unit_frame = tk.Frame(parent, bg='white')
#         base_unit_frame.pack(fill=tk.X, pady=8)
        
#         tk.Label(
#             base_unit_frame,
#             text="Base Unit:",
#             font=('Arial', 10, 'bold'),
#             fg='#2c3e50',
#             bg='white',
#             width=15,
#             anchor='w'
#         ).pack(side=tk.LEFT)
        
#         self.base_unit_var = tk.StringVar()
#         self.base_unit_entry = tk.Entry(
#             base_unit_frame,
#             textvariable=self.base_unit_var,
#             font=('Arial', 10),
#             relief='solid',
#             bd=1
#         )
#         self.base_unit_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(10, 0))
#         self.base_unit_entry.insert(0, "meter")  # Example entry
        
#         # Conversion Factor
#         conversion_frame = tk.Frame(parent, bg='white')
#         conversion_frame.pack(fill=tk.X, pady=8)
        
#         tk.Label(
#             conversion_frame,
#             text="Conversion Factor:",
#             font=('Arial', 10, 'bold'),
#             fg='#2c3e50',
#             bg='white',
#             width=15,
#             anchor='w'
#         ).pack(side=tk.LEFT)
        
#         self.conversion_var = tk.StringVar(value="0.3048")
#         self.conversion_entry = tk.Entry(
#             conversion_frame,
#             textvariable=self.conversion_var,
#             font=('Arial', 10),
#             relief='solid',
#             bd=1,
#             validate='key'
#         )
#         self.conversion_entry.config(validatecommand=(self.conversion_entry.register(self.validate_float), '%P'))
#         self.conversion_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(10, 0))
        
#         # Description
#         desc_frame = tk.Frame(parent, bg='white')
#         desc_frame.pack(fill=tk.X, pady=8)
        
#         tk.Label(
#             desc_frame,
#             text="Description:",
#             font=('Arial', 10, 'bold'),
#             fg='#2c3e50',
#             bg='white',
#             width=15,
#             anchor='w'
#         ).pack(side=tk.LEFT, anchor='n')
        
#         self.desc_text = tk.Text(
#             desc_frame,
#             font=('Arial', 10),
#             relief='solid',
#             bd=1,
#             height=3
#         )
#         self.desc_text.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(10, 0))
#         self.desc_text.insert('1.0', "1 foot = 0.3048 meters\nUsed for measuring length of materials")  # Example entry
    
#     def create_example_section(self, parent):
#         """Create example section with quick fill buttons"""
#         example_frame = tk.Frame(parent, bg='#f8f9fa', relief='solid', bd=1)
#         example_frame.pack(fill=tk.X, pady=15)
        
#         # Example title
#         example_title = tk.Label(
#             example_frame,
#             text="📋 Quick Fill Examples:",
#             font=('Arial', 11, 'bold'),
#             fg='#2c3e50',
#             bg='#f8f9fa'
#         )
#         example_title.pack(anchor='w', padx=10, pady=(10, 5))
        
#         # Example buttons container
#         examples_container = tk.Frame(example_frame, bg='#f8f9fa')
#         examples_container.pack(fill=tk.X, padx=10, pady=(0, 10))
        
#         # Example buttons
#         examples = [
#             ("📏 Feet (Length)", self.load_example_feet, '#3498db'),
#             ("⚖️ Kilogram (Weight)", self.load_example_kilogram, '#e74c3c'),
#             ("💧 Liter (Volume)", self.load_example_liter, '#2980b9'),
#             ("🔢 Piece (Count)", self.load_example_piece, '#9b59b6')
            
#         ]
        
#         for text, command, color in examples:
#             btn = tk.Button(
#                 examples_container,
#                 text=text,
#                 font=('Arial', 9),
#                 bg=color,
#                 fg='white',
#                 relief='flat',
#                 cursor='hand2',
#                 command=command
#             )
#             btn.pack(side=tk.LEFT, padx=(0, 5), pady=2)
    
#     def create_action_buttons(self, parent):
#         """Create Save and Cancel buttons"""
#         button_frame = tk.Frame(parent, bg='white')
#         button_frame.pack(fill=tk.X, pady=20)
        
#         # Cancel button (left side)
#         cancel_btn = tk.Button(
#             button_frame,
#             text="Cancel",
#             font=('Arial', 11, 'bold'),
#             bg='#95a5a6',
#             fg='white',
#             relief='flat',
#             width=10,
#             command=self.cancel_form,
#             cursor='hand2'
#         )
#         cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
#         # Save button (right side)
#         save_btn = tk.Button(
#             button_frame,
#             text="Save Measurement",
#             font=('Arial', 11, 'bold'),
#             bg='#27ae60',
#             fg='white',
#             relief='flat',
#             width=15,
#             command=self.save_measurement,
#             cursor='hand2'
#         )
#         save_btn.pack(side=tk.RIGHT)
    
#     def load_example_feet(self):
#         """Load feet example"""
#         self.clear_form()
#         self.name_var.set("Feet")
#         self.code_var.set("ft")
#         self.type_var.set("Length")
#         self.base_unit_var.set("meter")
#         self.conversion_var.set("0.3048")
#         self.desc_text.delete('1.0', tk.END)
#         self.desc_text.insert('1.0', "1 foot = 0.3048 meters\nCommonly used for roofing sheets, pipes, lumber")
#         self.name_entry.focus()
    
#     def load_example_kilogram(self):
#         """Load kilogram example"""
#         self.clear_form()
#         self.name_var.set("Kilogram")
#         self.code_var.set("kg")
#         self.type_var.set("Weight")
#         self.base_unit_var.set("gram")
#         self.conversion_var.set("1000.0")
#         self.desc_text.delete('1.0', tk.END)
#         self.desc_text.insert('1.0', "1 kilogram = 1000 grams\nUsed for nails, screws, bolts, hardware items")
#         self.name_entry.focus()
    
#     def load_example_liter(self):
#         """Load liter example"""
#         self.clear_form()
#         self.name_var.set("Liter")
#         self.code_var.set("L")
#         self.type_var.set("Volume")
#         self.base_unit_var.set("liter")
#         self.conversion_var.set("1.0")
#         self.desc_text.delete('1.0', tk.END)
#         self.desc_text.insert('1.0', "Base unit for volume\nUsed for paints, chemicals, lubricants")
#         self.name_entry.focus()
    
#     def load_example_piece(self):
#         """Load piece example"""
#         self.clear_form()
#         self.name_var.set("Piece")
#         self.code_var.set("pcs")
#         self.type_var.set("Count")
#         self.base_unit_var.set("piece")
#         self.conversion_var.set("1.0")
#         self.desc_text.delete('1.0', tk.END)
#         self.desc_text.insert('1.0', "Base unit for counting items\nUsed for tools, fixtures, individual items")
#         self.name_entry.focus()
    
#     def clear_form(self):
#         """Clear all form fields"""
#         self.name_var.set("")
#         self.code_var.set("")
#         self.type_var.set("Length")
#         self.base_unit_var.set("")
#         self.conversion_var.set("1.0")
#         self.desc_text.delete('1.0', tk.END)
    
#     def cancel_form(self):
#         """Cancel and close the form"""
#         result = messagebox.askyesno(
#             "Confirm Cancel", 
#             "Are you sure you want to cancel? Any unsaved data will be lost."
#         )
#         if result:
#             self.dialog.destroy()
    
#     def validate_float(self, value):
#         """Validate float input"""
#         if value == "":
#             return True
#         try:
#             float(value)
#             return True
#         except ValueError:
#             return False
    
#     def validate_form(self):
#         """Validate form inputs"""
#         if not self.name_var.get().strip():
#             messagebox.showerror("Error", "Please enter measurement name!")
#             self.name_entry.focus()
#             return False
        
#         if not self.code_var.get().strip():
#             messagebox.showerror("Error", "Please enter unit code!")
#             self.code_entry.focus()
#             return False
        
#         if not self.type_var.get().strip():
#             messagebox.showerror("Error", "Please select measurement type!")
#             return False
        
#         if not self.base_unit_var.get().strip():
#             messagebox.showerror("Error", "Please enter base unit!")
#             self.base_unit_entry.focus()
#             return False
        
#         try:
#             conversion_factor = float(self.conversion_var.get())
#             if conversion_factor <= 0:
#                 messagebox.showerror("Error", "Conversion factor must be greater than 0!")
#                 self.conversion_entry.focus()
#                 return False
#         except ValueError:
#             messagebox.showerror("Error", "Please enter a valid conversion factor!")
#             self.conversion_entry.focus()
#             return False
        
#         return True
    
#     def save_measurement(self):
#         """Save measurement to database"""
#         try:
#             if not self.validate_form():
#                 return
            
#             # Get form data
#             name = self.name_var.get().strip()
#             code = self.code_var.get().strip()
#             measurement_type = self.type_var.get().strip()
#             base_unit = self.base_unit_var.get().strip()
#             conversion_factor = float(self.conversion_var.get())
#             description = self.desc_text.get("1.0", tk.END).strip()
            
#             # Save to database
#             measurement_id = self.measurement_service.add_measurement(
#                 name, code, measurement_type, base_unit, conversion_factor, description
#             )
            
#             if measurement_id:
#                 messagebox.showinfo("Success", f"Measurement '{name}' added successfully!")
#                 self.dialog.destroy()
                
#                 # Refresh callback if provided
#                 if self.refresh_callback:
#                     self.refresh_callback()
#             else:
#                 messagebox.showerror("Error", "Failed to save measurement!")
                
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to save measurement: {str(e)}")