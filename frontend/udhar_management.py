import tkinter as tk
from tkinter import ttk, messagebox
from backend.udhar_service import UdharService

class UdharManagement:
    def __init__(self, parent):
        self.parent = parent
        self.udhar_service = UdharService()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        self.main_frame = tk.Frame(self.parent, bg='white')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_header()
        self.create_tabs()
        
    def create_header(self):
        """Create header section"""
        header_frame = tk.Frame(self.main_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            header_frame,
            text="💰 Complete Udhar Management",
            font=('Arial', 18, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(side=tk.LEFT)
        
    def create_tabs(self):
        """Create tabbed interface"""
        # Create notebook (tab container)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.customer_tab = tk.Frame(self.notebook, bg='white')
        self.supplier_tab = tk.Frame(self.notebook, bg='white')
        
        self.notebook.add(self.customer_tab, text='👥 Customer Udhar')
        self.notebook.add(self.supplier_tab, text='🏭 Supplier Udhar')
        
        # Initialize tabs
        self.create_customer_tab()
        self.create_supplier_tab()
        
    # CUSTOMER TAB
    def create_customer_tab(self):
        """Create customer udhar tab"""
        # Controls frame
        controls_frame = tk.Frame(self.customer_tab, bg='white')
        controls_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Search section
        search_frame = tk.Frame(controls_frame, bg='white')
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            search_frame,
            text="🔍 Search Customer:",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side=tk.LEFT, padx=(0, 8))
        
        self.customer_search_var = tk.StringVar()
        self.customer_search_entry = tk.Entry(
            search_frame,
            textvariable=self.customer_search_var,
            font=('Arial', 11),
            width=25,
            relief='solid',
            bd=1
        )
        self.customer_search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.customer_search_entry.bind('<KeyRelease>', self.on_customer_search)
        
        # Buttons section
        button_frame = tk.Frame(controls_frame, bg='white')
        button_frame.pack(side=tk.RIGHT)
        
        self.add_customer_btn = tk.Button(
            button_frame,
            text="➕ Add Customer",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.show_add_customer_form,
            cursor='hand2'
        )
        self.add_customer_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.refresh_customer_btn = tk.Button(
            button_frame,
            text="🔄 Refresh",
            font=('Arial', 10),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.load_customers,
            cursor='hand2'
        )
        self.refresh_customer_btn.pack(side=tk.LEFT)
        
        # Customer summary
        self.create_customer_summary()
        
        # Customer table
        self.create_customer_table()
        
        # Load initial data
        self.load_customers()
        
    def create_customer_summary(self):
        """Create customer summary section"""
        summary_frame = tk.Frame(self.customer_tab, bg='#ecf0f1', relief='solid', bd=1)
        summary_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Create summary variables
        self.total_customers_var = tk.StringVar(value="Total Customers: 0")
        self.customer_total_udhar_var = tk.StringVar(value="Total Udhar: PKR 0")
        self.customer_total_paid_var = tk.StringVar(value="Total Received: PKR 0") 
        self.customer_total_balance_var = tk.StringVar(value="Remaining: PKR 0")
        
        # Summary labels
        tk.Label(
            summary_frame,
            textvariable=self.total_customers_var,
            font=('Arial', 11, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(
            summary_frame,
            textvariable=self.customer_total_udhar_var,
            font=('Arial', 11, 'bold'),
            bg='#ecf0f1',
            fg='#e74c3c'
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(
            summary_frame,
            textvariable=self.customer_total_paid_var,
            font=('Arial', 11, 'bold'),
            bg='#ecf0f1',
            fg='#27ae60'
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(
            summary_frame,
            textvariable=self.customer_total_balance_var,
            font=('Arial', 11, 'bold'),
            bg='#ecf0f1',
            fg='#f39c12'
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
    def create_customer_table(self):
        """Create customers table with date column"""
        table_frame = tk.Frame(self.customer_tab, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with columns - ADDED DATE COLUMN
        columns = ('ID', 'Customer Name', 'Phone', 'Date', 'Total Amount', 'Paid Amount', 'Balance', 'Status', 'Action')
        self.customer_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns - UPDATED WIDTHS
        column_widths = {
            'ID': 60,
            'Customer Name': 150,
            'Phone': 120,
            'Date': 120,  # NEW COLUMN
            'Total Amount': 120,
            'Paid Amount': 120,
            'Balance': 120,
            'Status': 100,
            'Action': 100
        }
        
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=column_widths[col], anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.customer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click for payment
        self.customer_tree.bind('<Double-1>', self.on_customer_double_click)

    
    # SUPPLIER TAB
    def create_supplier_tab(self):
        """Create supplier udhar tab"""
        # Controls frame
        controls_frame = tk.Frame(self.supplier_tab, bg='white')
        controls_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Search section
        search_frame = tk.Frame(controls_frame, bg='white')
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            search_frame,
            text="🔍 Search Supplier:",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side=tk.LEFT, padx=(0, 8))
        
        self.supplier_search_var = tk.StringVar()
        self.supplier_search_entry = tk.Entry(
            search_frame,
            textvariable=self.supplier_search_var,
            font=('Arial', 11),
            width=25,
            relief='solid',
            bd=1
        )
        self.supplier_search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.supplier_search_entry.bind('<KeyRelease>', self.on_supplier_search)
        
        # Buttons section
        button_frame = tk.Frame(controls_frame, bg='white')
        button_frame.pack(side=tk.RIGHT)
        
        self.add_supplier_btn = tk.Button(
            button_frame,
            text="➕ Add Supplier",
            font=('Arial', 10, 'bold'),
            bg='#e67e22',
            fg='white',
            relief='flat',
            command=self.show_add_supplier_form,
            cursor='hand2'
        )
        self.add_supplier_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.refresh_supplier_btn = tk.Button(
            button_frame,
            text="🔄 Refresh",
            font=('Arial', 10),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.load_suppliers,
            cursor='hand2'
        )
        self.refresh_supplier_btn.pack(side=tk.LEFT)
        
        # Supplier summary
        self.create_supplier_summary()
        
        # Supplier table
        self.create_supplier_table()
        
        # Load initial data
        self.load_suppliers()
        
    def create_supplier_summary(self):
        """Create supplier summary section"""
        summary_frame = tk.Frame(self.supplier_tab, bg='#fef9e7', relief='solid', bd=1)
        summary_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Create summary variables
        self.total_suppliers_var = tk.StringVar(value="Total Suppliers: 0")
        self.supplier_total_udhar_var = tk.StringVar(value="Total Udhar: PKR 0")
        self.supplier_total_paid_var = tk.StringVar(value="Total Paid: PKR 0") 
        self.supplier_total_balance_var = tk.StringVar(value="Remaining: PKR 0")
        
        # Summary labels
        tk.Label(
            summary_frame,
            textvariable=self.total_suppliers_var,
            font=('Arial', 11, 'bold'),
            bg='#fef9e7',
            fg='#2c3e50'
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(
            summary_frame,
            textvariable=self.supplier_total_udhar_var,
            font=('Arial', 11, 'bold'),
            bg='#fef9e7',
            fg='#e74c3c'
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(
            summary_frame,
            textvariable=self.supplier_total_paid_var,
            font=('Arial', 11, 'bold'),
            bg='#fef9e7',
            fg='#27ae60'
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(
            summary_frame,
            textvariable=self.supplier_total_balance_var,
            font=('Arial', 11, 'bold'),
            bg='#fef9e7',
            fg='#f39c12'
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
    def create_supplier_table(self):
        """Create suppliers table with date column"""
        table_frame = tk.Frame(self.supplier_tab, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with columns - ADDED DATE COLUMN
        columns = ('ID', 'Supplier Name', 'Phone', 'Type', 'Date', 'Total Amount', 'Paid Amount', 'Balance', 'Status', 'Action')
        self.supplier_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns - UPDATED WIDTHS
        column_widths = {
            'ID': 60,
            'Supplier Name': 150,
            'Phone': 120,
            'Type': 100,
            'Date': 120,  # NEW COLUMN
            'Total Amount': 120,
            'Paid Amount': 120,
            'Balance': 120,
            'Status': 100,
            'Action': 100
        }
        
        for col in columns:
            self.supplier_tree.heading(col, text=col)
            self.supplier_tree.column(col, width=column_widths[col], anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.supplier_tree.yview)
        self.supplier_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.supplier_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click for payment
        self.supplier_tree.bind('<Double-1>', self.on_supplier_double_click)
    
    # CUSTOMER METHODS
    def load_customers(self):
        """Load customers into table with better error handling"""
        try:
            # Clear existing data
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)
            
            # Get customers from service with safety check
            customers = self.udhar_service.get_all_customers()
            
            # Ensure customers is a list (not None)
            if customers is None:
                customers = []
                print("Warning: get_all_customers returned None, using empty list")
            
            # Add customers to table
            for customer in customers:
                self.add_customer_to_table(customer)
            
            # Update summary
            self.update_customer_summary()
            
        except Exception as e:
            error_msg = f"Failed to load customers: {str(e)}"
            print(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def add_customer_to_table(self, customer):
        """Add single customer to table with date"""
        try:
            # Unpack customer data - now includes date
            customer_id, name, phone, total, paid, balance, created_date, status = customer
            
            # Format date (remove time part if present)
            date_display = str(created_date).split()[0] if created_date else "N/A"
            
            # Format values safely with PKR
            total_formatted = f"PKR {float(total):,.0f}" if total else "PKR 0"
            paid_formatted = f"PKR {float(paid):,.0f}" if paid else "PKR 0"
            balance_formatted = f"PKR {float(balance):,.0f}" if balance else "PKR 0"
            
            # Status with emoji
            status_display = "🟢 PAID" if status == 'PAID' else "🔴 UNPAID"
            
            # Action button text
            action_text = "❌ Delete" if status == 'PAID' else "💰 Pay"
            
            # Insert into table - INCLUDING DATE
            self.customer_tree.insert('', 'end', values=(
                customer_id,
                name,
                phone or '-',
                date_display,  # NEW DATE COLUMN
                total_formatted,
                paid_formatted,
                balance_formatted,
                status_display,
                action_text
            ))
            
        except Exception as e:
            print(f"Error adding customer to table: {e}")
    
    def update_customer_summary(self):
        """Update customer summary information"""
        try:
            summary = self.udhar_service.get_customer_summary()
            total_customers, total_udhar, total_paid, total_balance = summary
            
            # Format summary values with PKR
            self.total_customers_var.set(f"Total Customers: {total_customers}")
            self.customer_total_udhar_var.set(f"Total Udhar: PKR {float(total_udhar):,.0f}")
            self.customer_total_paid_var.set(f"Total Received: PKR {float(total_paid):,.0f}")
            self.customer_total_balance_var.set(f"Remaining: PKR {float(total_balance):,.0f}")
            
        except Exception as e:
            print(f"Error updating customer summary: {e}")
    
    def on_customer_search(self, event):
        """Handle customer search functionality"""
        search_term = self.customer_search_var.get().strip()
        
        if not search_term:
            self.load_customers()
            return
            
        try:
            # Clear table
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)
            
            # Search customers
            customers = self.udhar_service.search_customers(search_term)
            
            # Add search results to table
            for customer in customers:
                self.add_customer_to_table(customer)
                
        except Exception as e:
            messagebox.showerror("Error", f"Customer search failed: {str(e)}")
    
    def on_customer_double_click(self, event):
        """Handle customer double click for payment or delete - UPDATED FOR NEW COLUMNS"""
        selection = self.customer_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        values = self.customer_tree.item(item, 'values')
        
        if not values or len(values) < 9:  # Changed from 8 to 9
            return
            
        try:
            customer_id = values[0]
            customer_name = values[1]
            balance_str = values[6]  # Balance column - changed from 5 to 6
            status = values[7]  # Status column - changed from 6 to 7
            action = values[8]  # Action column - changed from 7 to 8
            
            # Extract numeric value from balance string
            balance = float(balance_str.replace('PKR', '').replace(',', '').strip())
            
            if action == "💰 Pay":
                # Show payment dialog
                self.show_customer_payment_dialog(customer_id, customer_name, balance)
            elif action == "❌ Delete":
                # Show delete confirmation
                self.confirm_customer_delete(customer_id, customer_name)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process customer action: {str(e)}")
    
    # SUPPLIER METHODS
    def load_suppliers(self):
        """Load suppliers into table with better error handling"""
        try:
            # Clear existing data
            for item in self.supplier_tree.get_children():
                self.supplier_tree.delete(item)
            
            # Get suppliers from service with safety check
            suppliers = self.udhar_service.get_all_suppliers()
            
            # Ensure suppliers is a list (not None)
            if suppliers is None:
                suppliers = []
                print("Warning: get_all_suppliers returned None, using empty list")
            
            # Add suppliers to table
            for supplier in suppliers:
                self.add_supplier_to_table(supplier)
            
            # Update summary
            self.update_supplier_summary()
            
        except Exception as e:
            error_msg = f"Failed to load suppliers: {str(e)}"
            print(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def add_supplier_to_table(self, supplier):
        """Add single supplier to table with date"""
        try:
            # Unpack supplier data - now includes date
            supplier_id, name, phone, total, paid, balance, created_date, status, supplier_type = supplier
            
            # Format date (remove time part if present)
            date_display = str(created_date).split()[0] if created_date else "N/A"
            
            # Format values safely with PKR
            total_formatted = f"PKR {float(total):,.0f}" if total else "PKR 0"
            paid_formatted = f"PKR {float(paid):,.0f}" if paid else "PKR 0"
            balance_formatted = f"PKR {float(balance):,.0f}" if balance else "PKR 0"
            
            # Status with emoji
            status_display = "🟢 PAID" if status == 'PAID' else "🔴 UNPAID"
            
            # Action button text
            action_text = "❌ Delete" if status == 'PAID' else "💳 Pay"
            
            # Insert into table - INCLUDING DATE
            self.supplier_tree.insert('', 'end', values=(
                supplier_id,
                name,
                phone or '-',
                supplier_type,
                date_display,  # NEW DATE COLUMN
                total_formatted,
                paid_formatted,
                balance_formatted,
                status_display,
                action_text
            ))
            
        except Exception as e:
            print(f"Error adding supplier to table: {e}")
    
    def update_supplier_summary(self):
        """Update supplier summary information"""
        try:
            summary = self.udhar_service.get_supplier_summary()
            total_suppliers, total_udhar, total_paid, total_balance = summary
            
            # Format summary values with PKR
            self.total_suppliers_var.set(f"Total Suppliers: {total_suppliers}")
            self.supplier_total_udhar_var.set(f"Total Udhar: PKR {float(total_udhar):,.0f}")
            self.supplier_total_paid_var.set(f"Total Paid: PKR {float(total_paid):,.0f}")
            self.supplier_total_balance_var.set(f"Remaining: PKR {float(total_balance):,.0f}")
            
        except Exception as e:
            print(f"Error updating supplier summary: {e}")
    
    def on_supplier_search(self, event):
        """Handle supplier search functionality"""
        search_term = self.supplier_search_var.get().strip()
        
        if not search_term:
            self.load_suppliers()
            return
            
        try:
            # Clear table
            for item in self.supplier_tree.get_children():
                self.supplier_tree.delete(item)
            
            # Search suppliers
            suppliers = self.udhar_service.search_suppliers(search_term)
            
            # Add search results to table
            for supplier in suppliers:
                self.add_supplier_to_table(supplier)
                
        except Exception as e:
            messagebox.showerror("Error", f"Supplier search failed: {str(e)}")
    
    def on_supplier_double_click(self, event):
        """Handle supplier double click for payment or delete - UPDATED FOR NEW COLUMNS"""
        selection = self.supplier_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        values = self.supplier_tree.item(item, 'values')
        
        if not values or len(values) < 10:  # Changed from 9 to 10
            return
            
        try:
            supplier_id = values[0]
            supplier_name = values[1]
            balance_str = values[7]  # Balance column - changed from 6 to 7
            status = values[8]  # Status column - changed from 7 to 8
            action = values[9]  # Action column - changed from 8 to 9
            
            # Extract numeric value from balance string
            balance = float(balance_str.replace('PKR', '').replace(',', '').strip())
            
            if action == "💳 Pay":
                # Show payment dialog
                self.show_supplier_payment_dialog(supplier_id, supplier_name, balance)
            elif action == "❌ Delete":
                # Show delete confirmation
                self.confirm_supplier_delete(supplier_id, supplier_name)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process supplier action: {str(e)}")
    
    # CUSTOMER FORM METHODS
    def show_add_customer_form(self):
        """Show add customer form"""
        self.customer_window = tk.Toplevel(self.parent)
        self.customer_window.title("Add Customer Udhar")
        self.customer_window.geometry("500x350")
        self.customer_window.configure(bg='white')
        self.customer_window.resizable(False, False)
        self.customer_window.transient(self.parent)
        self.customer_window.grab_set()
        
        self.center_window(self.customer_window)
        self.create_customer_form()
    
    def create_customer_form(self):
        """Create add customer form"""
        # Header
        header_frame = tk.Frame(self.customer_window, bg='white')
        header_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(
            header_frame,
            text="➕ Add New Customer Udhar",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack()
        
        # Form container
        form_frame = tk.Frame(self.customer_window, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40)
        
        # Customer Name
        name_frame = tk.Frame(form_frame, bg='white')
        name_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(
            name_frame,
            text="Customer Name:",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.customer_name_var = tk.StringVar()
        name_entry = tk.Entry(
            name_frame,
            textvariable=self.customer_name_var,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            width=25
        )
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Phone
        phone_frame = tk.Frame(form_frame, bg='white')
        phone_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(
            phone_frame,
            text="Phone:",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.customer_phone_var = tk.StringVar()
        phone_entry = tk.Entry(
            phone_frame,
            textvariable=self.customer_phone_var,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            width=25
        )
        phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Amount
        amount_frame = tk.Frame(form_frame, bg='white')
        amount_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(
            amount_frame,
            text="Udhar Amount (PKR):",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.customer_amount_var = tk.StringVar()
        amount_entry = tk.Entry(
            amount_frame,
            textvariable=self.customer_amount_var,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            width=25
        )
        amount_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=30)
        
        save_btn = tk.Button(
            button_frame,
            text="💾 Save Customer",
            font=('Arial', 13, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.save_customer,
            width=15,
            height=1
        )
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="❌ Cancel",
            font=('Arial', 13),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=self.customer_window.destroy,
            width=10,
            height=1
        )
        cancel_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key to save
        self.customer_window.bind('<Return>', lambda e: self.save_customer())
        
        # Set focus to name field
        name_entry.focus()
    
    def save_customer(self):
        """Save new customer"""
        try:
            # Get form values
            name = self.customer_name_var.get().strip()
            phone = self.customer_phone_var.get().strip()
            amount_str = self.customer_amount_var.get().strip()
            
            # Validate inputs
            if not name:
                messagebox.showerror("Error", "Please enter customer name!")
                return
                
            if not amount_str:
                messagebox.showerror("Error", "Please enter udhar amount!")
                return
                
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than 0!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount!")
                return
            
            # Save customer
            success, message = self.udhar_service.add_customer(name, phone, amount)
            
            if success:
                messagebox.showinfo("Success", message)
                self.customer_window.destroy()
                self.load_customers()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save customer: {str(e)}")
    
    # SUPPLIER FORM METHODS
    def show_add_supplier_form(self):
        """Show add supplier form"""
        self.supplier_window = tk.Toplevel(self.parent)
        self.supplier_window.title("Add Supplier Udhar")
        self.supplier_window.geometry("500x400")
        self.supplier_window.configure(bg='white')
        self.supplier_window.resizable(False, False)
        self.supplier_window.transient(self.parent)
        self.supplier_window.grab_set()
        
        self.center_window(self.supplier_window)
        self.create_supplier_form()
    
    def create_supplier_form(self):
        """Create add supplier form"""
        # Header
        header_frame = tk.Frame(self.supplier_window, bg='white')
        header_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(
            header_frame,
            text="➕ Add New Supplier Udhar",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack()
        
        # Form container
        form_frame = tk.Frame(self.supplier_window, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40)
        
        # Supplier Name
        name_frame = tk.Frame(form_frame, bg='white')
        name_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(
            name_frame,
            text="Supplier Name:",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.supplier_name_var = tk.StringVar()
        name_entry = tk.Entry(
            name_frame,
            textvariable=self.supplier_name_var,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            width=25
        )
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Phone
        phone_frame = tk.Frame(form_frame, bg='white')
        phone_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(
            phone_frame,
            text="Phone:",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.supplier_phone_var = tk.StringVar()
        phone_entry = tk.Entry(
            phone_frame,
            textvariable=self.supplier_phone_var,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            width=25
        )
        phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Amount
        amount_frame = tk.Frame(form_frame, bg='white')
        amount_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(
            amount_frame,
            text="Udhar Amount (PKR):",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.supplier_amount_var = tk.StringVar()
        amount_entry = tk.Entry(
            amount_frame,
            textvariable=self.supplier_amount_var,
            font=('Arial', 12),
            relief='solid',
            bd=1,
            width=25
        )
        amount_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Supplier Type
        type_frame = tk.Frame(form_frame, bg='white')
        type_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(
            type_frame,
            text="Type:",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.supplier_type_var = tk.StringVar(value="Supplier")
        type_dropdown = ttk.Combobox(
            type_frame,
            textvariable=self.supplier_type_var,
            values=["Supplier", "Vendor", "Dakandar", "Company"],
            state="readonly",
            font=('Arial', 12),
            width=23
        )
        type_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=30)
        
        save_btn = tk.Button(
            button_frame,
            text="💾 Save Supplier",
            font=('Arial', 13, 'bold'),
            bg='#e67e22',
            fg='white',
            relief='flat',
            command=self.save_supplier,
            width=15,
            height=1
        )
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="❌ Cancel",
            font=('Arial', 13),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=self.supplier_window.destroy,
            width=10,
            height=1
        )
        cancel_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key to save
        self.supplier_window.bind('<Return>', lambda e: self.save_supplier())
        
        # Set focus to name field
        name_entry.focus()
    
    def save_supplier(self):
        """Save new supplier"""
        try:
            # Get form values
            name = self.supplier_name_var.get().strip()
            phone = self.supplier_phone_var.get().strip()
            amount_str = self.supplier_amount_var.get().strip()
            supplier_type = self.supplier_type_var.get()
            
            # Validate inputs
            if not name:
                messagebox.showerror("Error", "Please enter supplier name!")
                return
                
            if not amount_str:
                messagebox.showerror("Error", "Please enter udhar amount!")
                return
                
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than 0!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount!")
                return
            
            # Save supplier
            success, message = self.udhar_service.add_supplier(name, phone, amount, supplier_type)
            
            if success:
                messagebox.showinfo("Success", message)
                self.supplier_window.destroy()
                self.load_suppliers()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save supplier: {str(e)}")
    
    # PAYMENT AND DELETE METHODS
    def show_customer_payment_dialog(self, customer_id, customer_name, current_balance):
        """Show customer payment dialog"""
        self.customer_payment_window = tk.Toplevel(self.parent)
        self.customer_payment_window.title("Receive Payment from Customer")
        self.customer_payment_window.geometry("450x300")
        self.customer_payment_window.configure(bg='white')
        self.customer_payment_window.resizable(False, False)
        self.customer_payment_window.transient(self.parent)
        self.customer_payment_window.grab_set()
        
        self.center_window(self.customer_payment_window)
        self.create_customer_payment_form(customer_id, customer_name, current_balance)
    
    def create_customer_payment_form(self, customer_id, customer_name, current_balance):
        """Create customer payment form"""
        # Header
        header_frame = tk.Frame(self.customer_payment_window, bg='white')
        header_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(
            header_frame,
            text="💰 Receive Payment from Customer",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack()
        
        # Form container
        form_frame = tk.Frame(self.customer_payment_window, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40)
        
        # Customer info
        info_frame = tk.Frame(form_frame, bg='white')
        info_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            info_frame,
            text=f"Customer: {customer_name}",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w')
        
        tk.Label(
            info_frame,
            text=f"Current Balance: PKR {current_balance:,.0f}",
            font=('Arial', 12, 'bold'),
            fg='#e74c3c',
            bg='white'
        ).pack(anchor='w', pady=(5, 0))
        
        # Payment amount
        amount_frame = tk.Frame(form_frame, bg='white')
        amount_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(
            amount_frame,
            text="Payment Amount (PKR):",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w')
        
        self.customer_payment_amount_var = tk.StringVar()
        payment_entry = tk.Entry(
            amount_frame,
            textvariable=self.customer_payment_amount_var,
            font=('Arial', 14),
            relief='solid',
            bd=1
        )
        payment_entry.pack(fill=tk.X, pady=(8, 0), ipady=6)
        
        # Info text
        info_text = tk.Label(
            form_frame,
            text="💡 Note: Customer will be automatically removed when fully paid",
            font=('Arial', 10),
            fg='#7f8c8d',
            bg='white',
            wraplength=350
        )
        info_text.pack(anchor='w', pady=(10, 0))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=20)
        
        receive_btn = tk.Button(
            button_frame,
            text="✅ Receive Payment",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=lambda: self.process_customer_payment(customer_id),
            width=15
        )
        receive_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="❌ Cancel",
            font=('Arial', 12),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=self.customer_payment_window.destroy,
            width=10
        )
        cancel_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key
        self.customer_payment_window.bind('<Return>', lambda e: self.process_customer_payment(customer_id))
        
        # Set focus to payment field
        payment_entry.focus()
    
    def show_supplier_payment_dialog(self, supplier_id, supplier_name, current_balance):
        """Show supplier payment dialog"""
        self.supplier_payment_window = tk.Toplevel(self.parent)
        self.supplier_payment_window.title("Make Payment to Supplier")
        self.supplier_payment_window.geometry("450x300")
        self.supplier_payment_window.configure(bg='white')
        self.supplier_payment_window.resizable(False, False)
        self.supplier_payment_window.transient(self.parent)
        self.supplier_payment_window.grab_set()
        
        self.center_window(self.supplier_payment_window)
        self.create_supplier_payment_form(supplier_id, supplier_name, current_balance)
    
    def create_supplier_payment_form(self, supplier_id, supplier_name, current_balance):
        """Create supplier payment form"""
        # Header
        header_frame = tk.Frame(self.supplier_payment_window, bg='white')
        header_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(
            header_frame,
            text="💳 Make Payment to Supplier",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack()
        
        # Form container
        form_frame = tk.Frame(self.supplier_payment_window, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40)
        
        # Supplier info
        info_frame = tk.Frame(form_frame, bg='white')
        info_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            info_frame,
            text=f"Supplier: {supplier_name}",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w')
        
        tk.Label(
            info_frame,
            text=f"Current Balance: PKR {current_balance:,.0f}",
            font=('Arial', 12, 'bold'),
            fg='#e74c3c',
            bg='white'
        ).pack(anchor='w', pady=(5, 0))
        
        # Payment amount
        amount_frame = tk.Frame(form_frame, bg='white')
        amount_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(
            amount_frame,
            text="Payment Amount (PKR):",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w')
        
        self.supplier_payment_amount_var = tk.StringVar()
        payment_entry = tk.Entry(
            amount_frame,
            textvariable=self.supplier_payment_amount_var,
            font=('Arial', 14),
            relief='solid',
            bd=1
        )
        payment_entry.pack(fill=tk.X, pady=(8, 0), ipady=6)
        
        # Info text
        info_text = tk.Label(
            form_frame,
            text="💡 Note: Supplier will be automatically removed when fully paid",
            font=('Arial', 10),
            fg='#7f8c8d',
            bg='white',
            wraplength=350
        )
        info_text.pack(anchor='w', pady=(10, 0))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=20)
        
        pay_btn = tk.Button(
            button_frame,
            text="✅ Make Payment",
            font=('Arial', 12, 'bold'),
            bg='#e67e22',
            fg='white',
            relief='flat',
            command=lambda: self.process_supplier_payment(supplier_id),
            width=15
        )
        pay_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="❌ Cancel",
            font=('Arial', 12),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=self.supplier_payment_window.destroy,
            width=10
        )
        cancel_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key
        self.supplier_payment_window.bind('<Return>', lambda e: self.process_supplier_payment(supplier_id))
        
        # Set focus to payment field
        payment_entry.focus()
    
    def process_customer_payment(self, customer_id):
        """Process customer payment"""
        try:
            amount_str = self.customer_payment_amount_var.get().strip()
            
            if not amount_str:
                messagebox.showerror("Error", "Please enter payment amount!")
                return
                
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than 0!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount!")
                return
            
            # Process payment
            success, message = self.udhar_service.receive_payment(customer_id, amount)
            
            if success:
                messagebox.showinfo("Success", message)
                self.customer_payment_window.destroy()
                self.load_customers()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process payment: {str(e)}")
    
    def process_supplier_payment(self, supplier_id):
        """Process supplier payment"""
        try:
            amount_str = self.supplier_payment_amount_var.get().strip()
            
            if not amount_str:
                messagebox.showerror("Error", "Please enter payment amount!")
                return
                
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than 0!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount!")
                return
            
            # Process payment
            success, message = self.udhar_service.make_payment(supplier_id, amount)
            
            if success:
                messagebox.showinfo("Success", message)
                self.supplier_payment_window.destroy()
                self.load_suppliers()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process payment: {str(e)}")
    
    def confirm_customer_delete(self, customer_id, customer_name):
        """Confirm customer deletion"""
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete customer '{customer_name}'?\n\nThis action cannot be undone."
        )
        
        if result:
            self.delete_customer(customer_id)
    
    def confirm_supplier_delete(self, supplier_id, supplier_name):
        """Confirm supplier deletion"""
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete supplier '{supplier_name}'?\n\nThis action cannot be undone."
        )
        
        if result:
            self.delete_supplier(supplier_id)
    
    def delete_customer(self, customer_id):
        """Delete customer"""
        try:
            success, message = self.udhar_service.force_delete_customer(customer_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.load_customers()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete customer: {str(e)}")
    
    def delete_supplier(self, supplier_id):
        """Delete supplier"""
        try:
            success, message = self.udhar_service.force_delete_supplier(supplier_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.load_suppliers()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete supplier: {str(e)}")
    
    def center_window(self, window):
        """Center window on screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')