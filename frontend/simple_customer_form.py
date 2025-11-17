import tkinter as tk
from tkinter import ttk, messagebox
from backend.udhar_service import UdharService

class SimpleCustomerForm:
    def __init__(self, parent):
        self.parent = parent
        self.udhar_service = UdharService()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        tk.Label(
            header_frame,
            text="➕ Add Customer Udhar",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack()
        
        # Form frame
        form_frame = tk.Frame(main_frame, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Customer Name
        name_frame = tk.Frame(form_frame, bg='white')
        name_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            name_frame,
            text="Customer Name:",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(
            name_frame,
            textvariable=self.name_var,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            width=30
        )
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Phone Number
        phone_frame = tk.Frame(form_frame, bg='white')
        phone_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            phone_frame,
            text="Phone Number:",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.phone_var = tk.StringVar()
        phone_entry = tk.Entry(
            phone_frame,
            textvariable=self.phone_var,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            width=30
        )
        phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Amount
        amount_frame = tk.Frame(form_frame, bg='white')
        amount_frame.pack(fill=tk.X, pady=(0, 30))
        
        tk.Label(
            amount_frame,
            text="Udhar Amount:",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.amount_var = tk.StringVar()
        amount_entry = tk.Entry(
            amount_frame,
            textvariable=self.amount_var,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            width=30
        )
        amount_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Save Button
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        save_btn = tk.Button(
            button_frame,
            text="💾 Save Customer",
            font=('Arial', 14, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.save_customer,
            width=20,
            height=2
        )
        save_btn.pack(pady=10)
        
        # Bind Enter key to save
        self.parent.bind('<Return>', lambda e: self.save_customer())
        
        # Set focus to name field
        name_entry.focus()
    
    def save_customer(self):
        """Save customer data"""
        try:
            # Get values from form
            name = self.name_var.get().strip()
            phone = self.phone_var.get().strip()
            amount_str = self.amount_var.get().strip()
            
            # Validation
            if not name:
                messagebox.showerror("Error", "Please enter customer name!")
                return
            
            if not amount_str:
                messagebox.showerror("Error", "Please enter udhar amount!")
                return
            
            # Validate amount
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than 0!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount!")
                return
            
            # Save to database
            customer_id = self.udhar_service.add_customer(name, phone, amount)
            
            if customer_id:
                messagebox.showinfo("Success", f"Customer '{name}' added successfully!")
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to save customer!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save customer: {str(e)}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.name_var.set("")
        self.phone_var.set("")
        self.amount_var.set("")
        
        # Set focus back to name field
        for widget in self.parent.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for entry in child.winfo_children():
                            if isinstance(entry, tk.Entry):
                                entry.focus()
                                return