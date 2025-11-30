import tkinter as tk
from tkinter import ttk, messagebox
from backend.udhar_service import UdharService
from datetime import datetime
from tkcalendar import DateEntry

class UdharManagement:
    def __init__(self, parent):
        self.parent = parent
        self.udhar_service = UdharService()
        
        # Colors for clean UI
        self.colors = {
            'primary': '#2c3e50',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'info': '#3498db',
            'light': '#ecf0f1',
            'background': '#f8f9fa',
            'dark': '#2c3e50'
        }
        
        # Measurement units for dropdown
        self.measurement_units = [
            'feet', 'kilogram', 'meter', 'pieces', 'centimeter', 
            'dozen', 'pounds', 'liter', 'gram'
        ]
        
        self.setup_ui()
        self.bind_events()
        
    def setup_ui(self):
        # Main container
        self.main_frame = tk.Frame(self.parent, bg=self.colors['background'], padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_header()
        self.create_tabs()
        
    def create_header(self):
        """Create simplified header section with summary totals"""
        header_frame = tk.Frame(self.main_frame, bg=self.colors['primary'])
        header_frame.pack(fill=tk.X, pady=10)
        
        # Main title
        tk.Label(
            header_frame,
            text="💰 UDHAR MANAGEMENT",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg=self.colors['primary']
        ).pack(pady=5)
        
        # Get summary data
        try:
            summary = self.udhar_service.get_overall_summary()
            customers = summary['customers']
            suppliers = summary['suppliers']
            overall = summary['overall']
            
            # Create summary text
            summary_text = f"👥 Customers: {customers['count']} | PKR {customers['total_balance']:,.0f} | 🏭 Suppliers: {suppliers['count']} | PKR {suppliers['total_balance']:,.0f} | 💰 Total: PKR {overall['total_balance']:,.0f}"
            
            tk.Label(
                header_frame,
                text=summary_text,
                font=('Arial', 11, 'bold'),
                fg='white',
                bg=self.colors['primary'],
                pady=5
            ).pack()
            
        except Exception as e:
            print(f"Error loading header summary: {e}")
            # Fallback if there's an error
            tk.Label(
                header_frame,
                text="👥 Customers: 0 | 🏭 Suppliers: 0 | 💰 Total: PKR 0",
                font=('Arial', 11, 'bold'),
                fg='white',
                bg=self.colors['primary'],
                pady=5
            ).pack()
    def refresh_header(self):
        """Refresh header summary data"""
        # This method will be called when data changes
        # For now, we'll recreate the header
        # In a more advanced version, you could update the labels directly
        
        # Remove existing header
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_height() == 120:
                widget.destroy()
                break
        
        # Create new header
        self.create_header()
        
        # Re-pack the notebook below the new header
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
    def create_tabs(self):
        """Create tabbed interface"""
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.customer_tab = tk.Frame(self.notebook, bg=self.colors['background'])
        self.supplier_tab = tk.Frame(self.notebook, bg=self.colors['background'])
        
        self.notebook.add(self.customer_tab, text='👥 CUSTOMER UDHAR')
        self.notebook.add(self.supplier_tab, text='🏭 SUPPLIER UDHAR')
        
        # Initialize tabs
        self.create_customer_tab()
        self.create_supplier_tab()
        
        # Load initial data
        self.load_customers()
        self.load_suppliers()

    # CUSTOMER TAB
    def create_customer_tab(self):
        """Create customer udhar tab"""
        # Main container
        main_frame = tk.Frame(self.customer_tab, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Controls frame
        controls_frame = tk.Frame(main_frame, bg=self.colors['background'])
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search
        search_frame = tk.Frame(controls_frame, bg=self.colors['background'])
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            search_frame,
            text="Search (Name/Phone):",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.customer_search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.customer_search_var,
            font=('Arial', 10),
            width=25
        )
        search_entry.pack(side=tk.LEFT, padx=(0, 20))
        search_entry.bind('<KeyRelease>', self.on_customer_search)
        
        # Buttons
        button_frame = tk.Frame(controls_frame, bg=self.colors['background'])
        button_frame.pack(side=tk.RIGHT)
        
        tk.Button(
            button_frame,
            text="➕ Add Customer",
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self.show_add_customer_form,
            padx=15,
            pady=8,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="🔄 Refresh",
            bg=self.colors['info'],
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self.load_customers,
            padx=15,
            pady=8,
            cursor='hand2'
        ).pack(side=tk.LEFT)
        
        # Customer table
        self.create_customer_table(main_frame)
        
    def create_customer_table(self, parent):
        """Create customer table with Bill column"""
        table_frame = tk.Frame(parent, bg=self.colors['background'])
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with Bill column
        columns = ('ID', 'Name', 'Phone', 'Total', 'Paid', 'Balance', 'Status', 'Last Payment', 'Bill', 'Actions')
        self.customer_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        # Configure columns
        column_config = {
            'ID': 50, 'Name': 120, 'Phone': 100, 'Total': 80, 
            'Paid': 80, 'Balance': 80, 'Status': 80, 'Last Payment': 100, 
            'Bill': 80, 'Actions': 120
        }
        
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=column_config[col], anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.customer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # SUPPLIER TAB
    def create_supplier_tab(self):
        """Create supplier udhar tab"""
        # Main container
        main_frame = tk.Frame(self.supplier_tab, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Controls frame
        controls_frame = tk.Frame(main_frame, bg=self.colors['background'])
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search
        search_frame = tk.Frame(controls_frame, bg=self.colors['background'])
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            search_frame,
            text="Search (Name/Phone):",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.supplier_search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.supplier_search_var,
            font=('Arial', 10),
            width=25
        )
        search_entry.pack(side=tk.LEFT, padx=(0, 20))
        search_entry.bind('<KeyRelease>', self.on_supplier_search)
        
        # Buttons
        button_frame = tk.Frame(controls_frame, bg=self.colors['background'])
        button_frame.pack(side=tk.RIGHT)
        
        tk.Button(
            button_frame,
            text="➕ Add Supplier",
            bg=self.colors['warning'],
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self.show_add_supplier_form,
            padx=15,
            pady=8,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="🔄 Refresh",
            bg=self.colors['info'],
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self.load_suppliers,
            padx=15,
            pady=8,
            cursor='hand2'
        ).pack(side=tk.LEFT)
        
        # Supplier table
        self.create_supplier_table(main_frame)
        
    def create_supplier_table(self, parent):
        """Create supplier table with Bill column"""
        table_frame = tk.Frame(parent, bg=self.colors['background'])
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with Bill column
        columns = ('ID', 'Name', 'Phone', 'Type', 'Total', 'Paid', 'Balance', 'Status', 'Last Payment', 'Bill', 'Actions')
        self.supplier_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        # Configure columns
        column_config = {
            'ID': 50, 'Name': 120, 'Phone': 100, 'Type': 80, 'Total': 80, 
            'Paid': 80, 'Balance': 80, 'Status': 80, 'Last Payment': 100, 
            'Bill': 80, 'Actions': 120
        }
        
        for col in columns:
            self.supplier_tree.heading(col, text=col)
            self.supplier_tree.column(col, width=column_config[col], anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.supplier_tree.yview)
        self.supplier_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.supplier_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # DATA LOADING METHODS
    def load_customers(self):
        """Load customers into table"""
        try:
            # Clear existing data
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)
            
            customers = self.udhar_service.get_all_customers()
            
            if not customers:
                return
                
            for customer in customers:
                self.add_customer_to_table(customer)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers: {str(e)}")
    
    def add_customer_to_table(self, customer):
        """Add customer to table with Bill button"""
        try:
            customer_id = customer[0]
            name = customer[1]
            phone = customer[2]
            total = customer[3]
            paid = customer[4]
            balance = customer[5]
            created_date = customer[6]
            status = customer[7]
            last_payment_date = customer[8]
            
            # Format dates
            last_payment_display = "Never"
            if last_payment_date and str(last_payment_date).strip() and str(last_payment_date).lower() != 'none':
                last_payment_display = str(last_payment_date).split()[0]
            
            # Format currency
            total_formatted = f"PKR {float(total):,.0f}" if total else "PKR 0"
            paid_formatted = f"PKR {float(paid):,.0f}" if paid else "PKR 0"
            balance_formatted = f"PKR {float(balance):,.0f}" if balance else "PKR 0"
            
            # Status
            status_display = "🟢 PAID" if status == 'PAID' else "🔴 UNPAID"
            
            # Insert into table WITH BILL COLUMN
            self.customer_tree.insert('', 'end', values=(
                customer_id, name, phone or '-', total_formatted, paid_formatted, 
                balance_formatted, status_display, last_payment_display,
                "📄 View Bill",  # BILL BUTTON
                "💰 Payment | ❌ Delete"
            ))
            
        except Exception as e:
            print(f"Error adding customer: {e}")
    
    def load_suppliers(self):
        """Load suppliers into table"""
        try:
            # Clear existing data
            for item in self.supplier_tree.get_children():
                self.supplier_tree.delete(item)
            
            suppliers = self.udhar_service.get_all_suppliers()
            
            if not suppliers:
                return
                
            for supplier in suppliers:
                self.add_supplier_to_table(supplier)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load suppliers: {str(e)}")
    
    def add_supplier_to_table(self, supplier):
        """Add supplier to table with Bill button"""
        try:
            supplier_id = supplier[0]
            name = supplier[1]
            phone = supplier[2]
            total = supplier[3]
            paid = supplier[4]
            balance = supplier[5]
            created_date = supplier[6]
            status = supplier[7]
            last_payment_date = supplier[8]
            supplier_type = supplier[9] if len(supplier) > 9 else "Supplier"
            
            # Format dates
            last_payment_display = "Never"
            if last_payment_date and str(last_payment_date).strip() and str(last_payment_date).lower() != 'none':
                last_payment_display = str(last_payment_date).split()[0]
            
            # Handle supplier type
            type_display = supplier_type if supplier_type and str(supplier_type).lower() != 'none' else "Supplier"
            
            # Format currency
            total_formatted = f"PKR {float(total):,.0f}" if total else "PKR 0"
            paid_formatted = f"PKR {float(paid):,.0f}" if paid else "PKR 0"
            balance_formatted = f"PKR {float(balance):,.0f}" if balance else "PKR 0"
            
            # Status
            status_display = "🟢 PAID" if status == 'PAID' else "🔴 UNPAID"
            
            # Insert into table WITH BILL COLUMN
            self.supplier_tree.insert('', 'end', values=(
                supplier_id, name, phone or '-', type_display, total_formatted, 
                paid_formatted, balance_formatted, status_display, last_payment_display,
                "📄 View Bill",  # BILL BUTTON
                "💳 Payment | ❌ Delete"
            ))
            
        except Exception as e:
            print(f"Error adding supplier: {e}")

    # SEARCH FUNCTIONALITY
    def on_customer_search(self, event):
        """Handle customer search - ENHANCED WITH PHONE SEARCH"""
        search_term = self.customer_search_var.get().strip()
        
        if not search_term:
            self.load_customers()
            return
            
        try:
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)
            
            # Use enhanced search that searches both name and phone
            customers = self.udhar_service.search_customers_enhanced(search_term)
            for customer in customers:
                self.add_customer_to_table(customer)
                
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
    
    def on_supplier_search(self, event):
        """Handle supplier search - ENHANCED WITH PHONE SEARCH"""
        search_term = self.supplier_search_var.get().strip()
        
        if not search_term:
            self.load_suppliers()
            return
            
        try:
            for item in self.supplier_tree.get_children():
                self.supplier_tree.delete(item)
            
            # Use enhanced search that searches both name and phone
            suppliers = self.udhar_service.search_suppliers_enhanced(search_term)
            for supplier in suppliers:
                self.add_supplier_to_table(supplier)
                
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")

    # ACTION HANDLERS
    def handle_customer_action(self, event):
        """Handle customer row action - UPDATED FOR BILL COLUMN"""
        item = self.customer_tree.selection()
        if not item:
            return
            
        item = item[0]
        values = self.customer_tree.item(item, 'values')
        
        if not values:
            return
            
        try:
            customer_id = values[0]
            customer_name = values[1]
            balance_str = values[5]
            
            # Get click position
            x, y = event.x, event.y
            column = self.customer_tree.identify_column(x)
            column_index = int(column.replace('#', '')) - 1
            
            # Check which column was clicked
            if column_index == 8:  # Bill column
                self.show_customer_bill(customer_id, customer_name)
                
            elif column_index == 9:  # Actions column
                # Get the exact click position within the actions column
                col_x = self.customer_tree.bbox(item, column_index)[0]
                
                # Simple approach: Payment is first half, Delete is second half
                if x < col_x + 60:  # Payment button area
                    balance = float(balance_str.replace('PKR', '').replace(',', '').strip())
                    self.show_customer_payment_dialog(customer_id, customer_name, balance)
                else:  # Delete button area
                    self.confirm_customer_delete(customer_id, customer_name)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Action failed: {str(e)}")
    
    def handle_supplier_action(self, event):
        """Handle supplier row action - UPDATED FOR BILL COLUMN"""
        item = self.supplier_tree.selection()
        if not item:
            return
            
        item = item[0]
        values = self.supplier_tree.item(item, 'values')
        
        if not values:
            return
            
        try:
            supplier_id = values[0]
            supplier_name = values[1]
            balance_str = values[6]
            
            # Get click position
            x, y = event.x, event.y
            column = self.supplier_tree.identify_column(x)
            column_index = int(column.replace('#', '')) - 1
            
            # Check which column was clicked
            if column_index == 9:  # Bill column
                self.show_supplier_bill(supplier_id, supplier_name)
                
            elif column_index == 10:  # Actions column (index changed due to Bill column)
                # Get the exact click position within the actions column
                col_x = self.supplier_tree.bbox(item, column_index)[0]
                
                # Simple approach: Payment is first half, Delete is second half
                if x < col_x + 60:  # Payment button area
                    balance = float(balance_str.replace('PKR', '').replace(',', '').strip())
                    self.show_supplier_payment_dialog(supplier_id, supplier_name, balance)
                else:  # Delete button area
                    self.confirm_supplier_delete(supplier_id, supplier_name)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Action failed: {str(e)}")

    # BILL VIEWING FUNCTIONALITY
    def show_customer_bill(self, customer_id, customer_name):
        """Show customer bill with items and transactions - FIXED VERSION"""
        try:
            # Get customer details using the new method
            customer = self.udhar_service.get_customer_by_id(customer_id)
            
            if not customer:
                messagebox.showerror("Error", f"Customer with ID {customer_id} not found!")
                return
            
            # Get items and transactions
            items = self.udhar_service.get_customer_udhar_items(customer_id)
            transactions = self.udhar_service.get_customer_transactions(customer_id)
            
            # Create bill window
            bill_window = tk.Toplevel(self.parent)
            bill_window.title(f"Bill - {customer_name}")
            bill_window.geometry("900x600")
            bill_window.configure(bg='white')
            bill_window.resizable(True, True)
            bill_window.transient(self.parent)
            bill_window.grab_set()
            
            self.center_window(bill_window)
            
            # Header
            header_frame = tk.Frame(bill_window, bg=self.colors['primary'])
            header_frame.pack(fill=tk.X, pady=(0, 10))
            
            tk.Label(
                header_frame,
                text="📄 CUSTOMER BILL / UDHAR DETAIL",
                font=('Arial', 16, 'bold'),
                fg='white',
                bg=self.colors['primary'],
                pady=15
            ).pack()
            
            # Customer Info Frame
            info_frame = tk.Frame(bill_window, bg='white', padx=20, pady=10)
            info_frame.pack(fill=tk.X)
            
            # Customer details - FIXED INDICES
            customer_id = customer[0]
            name = customer[1]
            phone = customer[2]
            address = customer[3] if len(customer) > 3 else 'N/A'
            total_amount = customer[4] if len(customer) > 4 else 0
            paid_amount = customer[5] if len(customer) > 5 else 0
            remaining_balance = customer[6] if len(customer) > 6 else 0
            created_date = customer[7] if len(customer) > 7 else 'N/A'
            status = customer[8] if len(customer) > 8 else 'UNPAID'
            last_payment_date = customer[9] if len(customer) > 9 else 'Never'
            
            details_text = f"""
    Customer Name: {name}
    Phone: {phone or 'N/A'}
    Address: {address or 'N/A'}
    Total Amount: PKR {float(total_amount):,.0f}
    Paid Amount: PKR {float(paid_amount):,.0f}
    Remaining Balance: PKR {float(remaining_balance):,.0f}
    Status: {status}
    Created Date: {created_date}
    Last Payment: {last_payment_date if last_payment_date and str(last_payment_date).lower() != 'none' else 'Never'}
            """
            
            tk.Label(
                info_frame,
                text=details_text.strip(),
                font=('Arial', 11),
                bg='white',
                justify=tk.LEFT,
                anchor='w'
            ).pack(fill=tk.X)
            
            # Notebook for Items and Transactions
            notebook = ttk.Notebook(bill_window)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Items Tab
            items_frame = tk.Frame(notebook, bg='white')
            notebook.add(items_frame, text='📦 Udhar Items')
            
            # Items Treeview
            items_columns = ('Product Name', 'Quantity', 'Unit', 'Unit Price', 'Total Price', 'Date')
            items_tree = ttk.Treeview(items_frame, columns=items_columns, show='headings', height=8)
            
            # Configure columns
            column_widths = {
                'Product Name': 150, 'Quantity': 80, 'Unit': 80, 
                'Unit Price': 100, 'Total Price': 100, 'Date': 100
            }
            
            for col in items_columns:
                items_tree.heading(col, text=col)
                items_tree.column(col, width=column_widths[col], anchor='center')
            
            # Add scrollbar for items
            items_scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=items_tree.yview)
            items_tree.configure(yscrollcommand=items_scrollbar.set)
            
            items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            items_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Populate items
            total_items_value = 0
            for item in items:
                # Item structure: (id, product_name, quantity, unit, unit_price, total_price, created_date)
                product_name = item[1] if len(item) > 1 else 'N/A'
                quantity = item[2] if len(item) > 2 else 0
                unit = item[3] if len(item) > 3 else 'pcs'
                unit_price = item[4] if len(item) > 4 else 0
                total_price = item[5] if len(item) > 5 else 0
                created_date = item[6] if len(item) > 6 else 'N/A'
                
                items_tree.insert('', 'end', values=(
                    product_name,
                    quantity,
                    unit,
                    f"PKR {float(unit_price):,.0f}",
                    f"PKR {float(total_price):,.0f}",
                    created_date.split()[0] if created_date and str(created_date).lower() != 'none' else 'N/A'
                ))
                total_items_value += float(total_price)
            
            # Transactions Tab
            transactions_frame = tk.Frame(notebook, bg='white')
            notebook.add(transactions_frame, text='💳 Transactions')
            
            # Transactions Treeview
            trans_columns = ('Type', 'Amount', 'Description', 'Date')
            trans_tree = ttk.Treeview(transactions_frame, columns=trans_columns, show='headings', height=8)
            
            for col in trans_columns:
                trans_tree.heading(col, text=col)
                trans_tree.column(col, width=150, anchor='center')
            
            # Add scrollbar for transactions
            trans_scrollbar = ttk.Scrollbar(transactions_frame, orient="vertical", command=trans_tree.yview)
            trans_tree.configure(yscrollcommand=trans_scrollbar.set)
            
            trans_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            trans_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Populate transactions
            for transaction in transactions:
                # Transaction structure: (transaction_type, amount, description, transaction_date)
                trans_type = "➕ CREDIT" if transaction[0] == 'credit' else "💵 PAYMENT"
                amount = transaction[1] if len(transaction) > 1 else 0
                description = transaction[2] if len(transaction) > 2 else 'N/A'
                trans_date = transaction[3] if len(transaction) > 3 else 'N/A'
                
                trans_tree.insert('', 'end', values=(
                    trans_type,
                    f"PKR {float(amount):,.0f}",
                    description,
                    trans_date.split()[0] if trans_date and str(trans_date).lower() != 'none' else 'N/A'
                ))
            
            # Summary Frame
            summary_frame = tk.Frame(bill_window, bg='lightgray', padx=10, pady=5)
            summary_frame.pack(fill=tk.X, padx=10, pady=5)
            
            summary_text = f"Total Items: {len(items)} | Items Total: PKR {total_items_value:,.0f} | Verified Total: PKR {float(total_amount):,.0f}"
            tk.Label(
                summary_frame,
                text=summary_text,
                font=('Arial', 10, 'bold'),
                bg='lightgray',
                fg='black'
            ).pack()
            
            # Close button
            button_frame = tk.Frame(bill_window, bg='white', pady=10)
            button_frame.pack(fill=tk.X)
            
            tk.Button(
                button_frame,
                text="🖨️ Print Bill",
                bg=self.colors['info'],
                fg='white',
                font=('Arial', 11, 'bold'),
                command=lambda: self.print_bill(customer_id, customer_name, 'customer'),
                cursor='hand2'
            ).pack(side=tk.LEFT, padx=20)
            
            tk.Button(
                button_frame,
                text="❌ Close",
                bg=self.colors['danger'],
                fg='white',
                font=('Arial', 11, 'bold'),
                command=bill_window.destroy,
                cursor='hand2'
            ).pack(side=tk.RIGHT, padx=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show bill: {str(e)}")
            print(f"Debug - Error details: {e}")

    def show_supplier_bill(self, supplier_id, supplier_name):
        """Show supplier bill with items and transactions - FIXED VERSION"""
        try:
            # Get supplier details using the new method
            supplier = self.udhar_service.get_supplier_by_id(supplier_id)
            
            if not supplier:
                messagebox.showerror("Error", f"Supplier with ID {supplier_id} not found!")
                return
            
            # Get items and transactions
            items = self.udhar_service.get_supplier_udhar_items(supplier_id)
            transactions = self.udhar_service.get_supplier_transactions(supplier_id)
            
            # Create bill window
            bill_window = tk.Toplevel(self.parent)
            bill_window.title(f"Bill - {supplier_name}")
            bill_window.geometry("900x600")
            bill_window.configure(bg='white')
            bill_window.resizable(True, True)
            bill_window.transient(self.parent)
            bill_window.grab_set()
            
            self.center_window(bill_window)
            
            # Header
            header_frame = tk.Frame(bill_window, bg=self.colors['warning'])
            header_frame.pack(fill=tk.X, pady=(0, 10))
            
            tk.Label(
                header_frame,
                text="📄 SUPPLIER BILL / UDHAR DETAIL",
                font=('Arial', 16, 'bold'),
                fg='white',
                bg=self.colors['warning'],
                pady=15
            ).pack()
            
            # Supplier Info Frame
            info_frame = tk.Frame(bill_window, bg='white', padx=20, pady=10)
            info_frame.pack(fill=tk.X)
            
            # Supplier details - FIXED INDICES
            supplier_id = supplier[0]
            name = supplier[1]
            phone = supplier[2]
            address = supplier[3] if len(supplier) > 3 else 'N/A'
            total_amount = supplier[4] if len(supplier) > 4 else 0
            paid_amount = supplier[5] if len(supplier) > 5 else 0
            remaining_balance = supplier[6] if len(supplier) > 6 else 0
            created_date = supplier[7] if len(supplier) > 7 else 'N/A'
            status = supplier[8] if len(supplier) > 8 else 'UNPAID'
            last_payment_date = supplier[9] if len(supplier) > 9 else 'Never'
            supplier_type = supplier[10] if len(supplier) > 10 else 'Supplier'
            
            details_text = f"""
    Supplier Name: {name}
    Type: {supplier_type}
    Phone: {phone or 'N/A'}
    Address: {address or 'N/A'}
    Total Amount: PKR {float(total_amount):,.0f}
    Paid Amount: PKR {float(paid_amount):,.0f}
    Remaining Balance: PKR {float(remaining_balance):,.0f}
    Status: {status}
    Created Date: {created_date}
    Last Payment: {last_payment_date if last_payment_date and str(last_payment_date).lower() != 'none' else 'Never'}
            """
            
            tk.Label(
                info_frame,
                text=details_text.strip(),
                font=('Arial', 11),
                bg='white',
                justify=tk.LEFT,
                anchor='w'
            ).pack(fill=tk.X)
            
            # Notebook for Items and Transactions
            notebook = ttk.Notebook(bill_window)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Items Tab
            items_frame = tk.Frame(notebook, bg='white')
            notebook.add(items_frame, text='📦 Udhar Items')
            
            # Items Treeview
            items_columns = ('Product Name', 'Quantity', 'Unit', 'Unit Price', 'Total Price', 'Date')
            items_tree = ttk.Treeview(items_frame, columns=items_columns, show='headings', height=8)
            
            # Configure columns
            column_widths = {
                'Product Name': 150, 'Quantity': 80, 'Unit': 80, 
                'Unit Price': 100, 'Total Price': 100, 'Date': 100
            }
            
            for col in items_columns:
                items_tree.heading(col, text=col)
                items_tree.column(col, width=column_widths[col], anchor='center')
            
            # Add scrollbar for items
            items_scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=items_tree.yview)
            items_tree.configure(yscrollcommand=items_scrollbar.set)
            
            items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            items_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Populate items
            total_items_value = 0
            for item in items:
                # Item structure: (id, product_name, quantity, unit, unit_price, total_price, created_date)
                product_name = item[1] if len(item) > 1 else 'N/A'
                quantity = item[2] if len(item) > 2 else 0
                unit = item[3] if len(item) > 3 else 'pcs'
                unit_price = item[4] if len(item) > 4 else 0
                total_price = item[5] if len(item) > 5 else 0
                created_date = item[6] if len(item) > 6 else 'N/A'
                
                items_tree.insert('', 'end', values=(
                    product_name,
                    quantity,
                    unit,
                    f"PKR {float(unit_price):,.0f}",
                    f"PKR {float(total_price):,.0f}",
                    created_date.split()[0] if created_date and str(created_date).lower() != 'none' else 'N/A'
                ))
                total_items_value += float(total_price)
            
            # Transactions Tab
            transactions_frame = tk.Frame(notebook, bg='white')
            notebook.add(transactions_frame, text='💳 Transactions')
            
            # Transactions Treeview
            trans_columns = ('Type', 'Amount', 'Description', 'Date')
            trans_tree = ttk.Treeview(transactions_frame, columns=trans_columns, show='headings', height=8)
            
            for col in trans_columns:
                trans_tree.heading(col, text=col)
                trans_tree.column(col, width=150, anchor='center')
            
            # Add scrollbar for transactions
            trans_scrollbar = ttk.Scrollbar(transactions_frame, orient="vertical", command=trans_tree.yview)
            trans_tree.configure(yscrollcommand=trans_scrollbar.set)
            
            trans_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            trans_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Populate transactions
            for transaction in transactions:
                # Transaction structure: (transaction_type, amount, description, transaction_date)
                trans_type = "➕ CREDIT" if transaction[0] == 'credit' else "💵 PAYMENT"
                amount = transaction[1] if len(transaction) > 1 else 0
                description = transaction[2] if len(transaction) > 2 else 'N/A'
                trans_date = transaction[3] if len(transaction) > 3 else 'N/A'
                
                trans_tree.insert('', 'end', values=(
                    trans_type,
                    f"PKR {float(amount):,.0f}",
                    description,
                    trans_date.split()[0] if trans_date and str(trans_date).lower() != 'none' else 'N/A'
                ))
            
            # Summary Frame
            summary_frame = tk.Frame(bill_window, bg='lightgray', padx=10, pady=5)
            summary_frame.pack(fill=tk.X, padx=10, pady=5)
            
            summary_text = f"Total Items: {len(items)} | Items Total: PKR {total_items_value:,.0f} | Verified Total: PKR {float(total_amount):,.0f}"
            tk.Label(
                summary_frame,
                text=summary_text,
                font=('Arial', 10, 'bold'),
                bg='lightgray',
                fg='black'
            ).pack()
            
            # Close button
            button_frame = tk.Frame(bill_window, bg='white', pady=10)
            button_frame.pack(fill=tk.X)
            
            tk.Button(
                button_frame,
                text="🖨️ Print Bill",
                bg=self.colors['info'],
                fg='white',
                font=('Arial', 11, 'bold'),
                command=lambda: self.print_bill(supplier_id, supplier_name, 'supplier'),
                cursor='hand2'
            ).pack(side=tk.LEFT, padx=20)
            
            tk.Button(
                button_frame,
                text="❌ Close",
                bg=self.colors['danger'],
                fg='white',
                font=('Arial', 11, 'bold'),
                command=bill_window.destroy,
                cursor='hand2'
            ).pack(side=tk.RIGHT, padx=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show bill: {str(e)}")
            print(f"Debug - Error details: {e}")

    def print_bill(self, udhar_id, name, udhar_type):
        """Print bill functionality"""
        messagebox.showinfo("Print", f"Bill for {name} would be printed here!")

    # ENHANCED CUSTOMER FORM WITH BILL ITEMS AND MEASUREMENT UNITS
    def show_add_customer_form(self):
        """Show enhanced add customer form with bill items and measurement units"""
        self.customer_window = tk.Toplevel(self.parent)
        self.customer_window.title("Add Customer Udhar with Bill Details")
        self.customer_window.geometry("750x600")
        self.customer_window.configure(bg='white')
        self.customer_window.resizable(True, True)
        self.customer_window.transient(self.parent)
        self.customer_window.grab_set()
        
        self.center_window(self.customer_window)
        
        # Store items
        self.customer_items = []
        
        # Header
        header_frame = tk.Frame(self.customer_window, bg=self.colors['primary'])
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            header_frame,
            text="➕ ADD CUSTOMER UDHAR WITH BILL",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg=self.colors['primary'],
            pady=15
        ).pack()
        
        # Main form container with scrollbar
        main_container = tk.Frame(self.customer_window, bg='white')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Customer Information Frame
        info_frame = tk.LabelFrame(main_container, text="👤 Customer Information", font=('Arial', 12, 'bold'), 
                                 bg='white', fg=self.colors['primary'], padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Customer Name
        name_frame = tk.Frame(info_frame, bg='white')
        name_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            name_frame,
            text="Customer Name:",
            font=('Arial', 11, 'bold'),
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.customer_name_var = tk.StringVar()
        name_entry = tk.Entry(
            name_frame,
            textvariable=self.customer_name_var,
            font=('Arial', 11),
            width=30,
            relief='solid',
            bd=1
        )
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Phone
        phone_frame = tk.Frame(info_frame, bg='white')
        phone_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            phone_frame,
            text="Phone:",
            font=('Arial', 11, 'bold'),
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.customer_phone_var = tk.StringVar()
        phone_entry = tk.Entry(
            phone_frame,
            textvariable=self.customer_phone_var,
            font=('Arial', 11),
            width=30,
            relief='solid',
            bd=1
        )
        phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Address
        address_frame = tk.Frame(info_frame, bg='white')
        address_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            address_frame,
            text="Address:",
            font=('Arial', 11, 'bold'),
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.customer_address_var = tk.StringVar()
        address_entry = tk.Entry(
            address_frame,
            textvariable=self.customer_address_var,
            font=('Arial', 11),
            width=30,
            relief='solid',
            bd=1
        )
        address_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Bill Items Frame
        items_frame = tk.LabelFrame(main_container, text="📦 Bill Items", font=('Arial', 12, 'bold'), 
                                  bg='white', fg=self.colors['primary'], padx=10, pady=10)
        items_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Item Entry Frame
        item_entry_frame = tk.Frame(items_frame, bg='white')
        item_entry_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Product Name
        tk.Label(
            item_entry_frame,
            text="Product:",
            font=('Arial', 10, 'bold'),
            bg='white'
        ).grid(row=0, column=0, padx=(0, 5), pady=5, sticky='w')
        
        self.item_product_var = tk.StringVar()
        product_entry = tk.Entry(
            item_entry_frame,
            textvariable=self.item_product_var,
            font=('Arial', 10),
            width=15,
            relief='solid',
            bd=1
        )
        product_entry.grid(row=0, column=1, padx=(0, 10), pady=5, sticky='w')
        
        # Quantity
        tk.Label(
            item_entry_frame,
            text="Qty:",
            font=('Arial', 10, 'bold'),
            bg='white'
        ).grid(row=0, column=2, padx=(0, 5), pady=5, sticky='w')
        
        self.item_quantity_var = tk.StringVar()
        quantity_entry = tk.Entry(
            item_entry_frame,
            textvariable=self.item_quantity_var,
            font=('Arial', 10),
            width=8,
            relief='solid',
            bd=1
        )
        quantity_entry.grid(row=0, column=3, padx=(0, 10), pady=5, sticky='w')
        
        # Unit (Measurement Dropdown)
        tk.Label(
            item_entry_frame,
            text="Unit:",
            font=('Arial', 10, 'bold'),
            bg='white'
        ).grid(row=0, column=4, padx=(0, 5), pady=5, sticky='w')
        
        self.item_unit_var = tk.StringVar(value="pieces")
        unit_combo = ttk.Combobox(
            item_entry_frame,
            textvariable=self.item_unit_var,
            values=self.measurement_units,
            state="readonly",
            font=('Arial', 10),
            width=10
        )
        unit_combo.grid(row=0, column=5, padx=(0, 10), pady=5, sticky='w')
        
        # Unit Price
        tk.Label(
            item_entry_frame,
            text="Unit Price:",
            font=('Arial', 10, 'bold'),
            bg='white'
        ).grid(row=0, column=6, padx=(0, 5), pady=5, sticky='w')
        
        self.item_price_var = tk.StringVar()
        price_entry = tk.Entry(
            item_entry_frame,
            textvariable=self.item_price_var,
            font=('Arial', 10),
            width=10,
            relief='solid',
            bd=1
        )
        price_entry.grid(row=0, column=7, padx=(0, 10), pady=5, sticky='w')
        
        # Add Item Button
        add_item_btn = tk.Button(
            item_entry_frame,
            text="➕ Add Item",
            bg=self.colors['info'],
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self.add_customer_item,
            cursor='hand2'
        )
        add_item_btn.grid(row=0, column=8, padx=(10, 0), pady=5, sticky='w')
        
        # Items Table
        table_frame = tk.Frame(items_frame, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create items treeview
        columns = ('Product', 'Quantity', 'Unit', 'Unit Price', 'Total', 'Actions')
        self.customer_items_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=6)
        
        # Configure columns
        column_widths = {
            'Product': 120, 'Quantity': 60, 'Unit': 80, 
            'Unit Price': 90, 'Total': 90, 'Actions': 80
        }
        
        for col in columns:
            self.customer_items_tree.heading(col, text=col)
            self.customer_items_tree.column(col, width=column_widths[col], anchor='center')
        
        # Add scrollbar for items
        items_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.customer_items_tree.yview)
        self.customer_items_tree.configure(yscrollcommand=items_scrollbar.set)
        
        self.customer_items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        items_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click to remove item
        self.customer_items_tree.bind('<Double-1>', self.remove_customer_item)
        
        # Summary Frame
        summary_frame = tk.Frame(main_container, bg='lightgray', padx=10, pady=5)
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.customer_total_var = tk.StringVar(value="Total: PKR 0")
        tk.Label(
            summary_frame,
            textvariable=self.customer_total_var,
            font=('Arial', 12, 'bold'),
            bg='lightgray',
            fg='black'
        ).pack()
        
        # Buttons Frame
        button_frame = tk.Frame(main_container, bg='white', pady=10)
        button_frame.pack(fill=tk.X)
        
        # Save button (Green)
        save_btn = tk.Button(
            button_frame,
            text="💾 SAVE CUSTOMER & BILL",
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 12, 'bold'),
            command=self.save_customer_with_items,
            width=20,
            height=1,
            cursor='hand2',
            relief='raised',
            bd=2
        )
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Cancel button (Red)
        cancel_btn = tk.Button(
            button_frame,
            text="❌ CANCEL",
            bg=self.colors['danger'],
            fg='white',
            font=('Arial', 12, 'bold'),
            command=self.customer_window.destroy,
            width=10,
            height=1,
            cursor='hand2',
            relief='raised',
            bd=2
        )
        cancel_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Clear Items button
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear Items",
            bg=self.colors['warning'],
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self.clear_customer_items,
            cursor='hand2'
        )
        clear_btn.pack(side=tk.LEFT)
        
        # Bind Enter key to add item
        self.customer_window.bind('<Return>', lambda e: self.add_customer_item())
        
        # Set focus to name field
        name_entry.focus()
    
    def add_customer_item(self):
        """Add item to customer bill"""
        try:
            product = self.item_product_var.get().strip()
            quantity_str = self.item_quantity_var.get().strip()
            unit = self.item_unit_var.get()
            price_str = self.item_price_var.get().strip()
            
            if not product:
                messagebox.showerror("Error", "Please enter product name!")
                return
                
            if not quantity_str:
                messagebox.showerror("Error", "Please enter quantity!")
                return
                
            if not price_str:
                messagebox.showerror("Error", "Please enter unit price!")
                return
            
            try:
                quantity = float(quantity_str)
                price = float(price_str)
                
                if quantity <= 0:
                    messagebox.showerror("Error", "Quantity must be greater than 0!")
                    return
                    
                if price <= 0:
                    messagebox.showerror("Error", "Price must be greater than 0!")
                    return
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for quantity and price!")
                return
            
            # Calculate total
            total = quantity * price
            
            # Add to items list
            item_data = {
                'product_name': product,
                'quantity': quantity,
                'unit': unit,
                'unit_price': price,
                'total_price': total
            }
            self.customer_items.append(item_data)
            
            # Add to treeview
            self.customer_items_tree.insert('', 'end', values=(
                product,
                quantity,
                unit,
                f"PKR {price:,.0f}",
                f"PKR {total:,.0f}",
                "❌ Remove"
            ))
            
            # Update total
            self.update_customer_total()
            
            # Clear entry fields
            self.item_product_var.set("")
            self.item_quantity_var.set("")
            self.item_price_var.set("")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {str(e)}")
    
    def remove_customer_item(self, event):
        """Remove item from customer bill"""
        item = self.customer_items_tree.selection()
        if not item:
            return
            
        item = item[0]
        index = self.customer_items_tree.index(item)
        
        # Remove from list and treeview
        if 0 <= index < len(self.customer_items):
            self.customer_items.pop(index)
            self.customer_items_tree.delete(item)
            self.update_customer_total()
    
    def clear_customer_items(self):
        """Clear all customer items"""
        if self.customer_items:
            result = messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all items?")
            if result:
                self.customer_items.clear()
                for item in self.customer_items_tree.get_children():
                    self.customer_items_tree.delete(item)
                self.update_customer_total()
    
    def update_customer_total(self):
        """Update customer total amount"""
        total = sum(item['total_price'] for item in self.customer_items)
        self.customer_total_var.set(f"Total: PKR {total:,.0f}")
    
    def save_supplier_with_items(self):
        """Save supplier with bill items"""
        try:
            # Get form values
            name = self.supplier_name_var.get().strip()
            phone = self.supplier_phone_var.get().strip()
            address = self.supplier_address_var.get().strip()
            supplier_type = self.supplier_type_var.get()
            
            # Validate inputs
            if not name:
                messagebox.showerror("Error", "Please enter supplier name!")
                return
                
            if not self.supplier_items:
                messagebox.showerror("Error", "Please add at least one bill item!")
                return
            
            # Save supplier with items
            success, message = self.udhar_service.add_supplier_with_items(name, phone, address, self.supplier_items, supplier_type)
            
            if success:
                messagebox.showinfo("Success", message)
                self.supplier_window.destroy()
                self.load_suppliers()
                self.refresh_header()  # Refresh header summary
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save supplier: {str(e)}")

    # ENHANCED SUPPLIER FORM WITH BILL ITEMS AND MEASUREMENT UNITS
    def show_add_supplier_form(self):
        """Show enhanced add supplier form with bill items and measurement units"""
        self.supplier_window = tk.Toplevel(self.parent)
        self.supplier_window.title("Add Supplier Udhar with Bill Details")
        self.supplier_window.geometry("750x650")
        self.supplier_window.configure(bg='white')
        self.supplier_window.resizable(True, True)
        self.supplier_window.transient(self.parent)
        self.supplier_window.grab_set()
        
        self.center_window(self.supplier_window)
        
        # Store items
        self.supplier_items = []
        
        # Header
        header_frame = tk.Frame(self.supplier_window, bg=self.colors['primary'])
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            header_frame,
            text="➕ ADD SUPPLIER UDHAR WITH BILL",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg=self.colors['primary'],
            pady=15
        ).pack()
        
        # Main form container
        main_container = tk.Frame(self.supplier_window, bg='white')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Supplier Information Frame
        info_frame = tk.LabelFrame(main_container, text="🏭 Supplier Information", font=('Arial', 12, 'bold'), 
                                 bg='white', fg=self.colors['primary'], padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Supplier Name
        name_frame = tk.Frame(info_frame, bg='white')
        name_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            name_frame,
            text="Supplier Name:",
            font=('Arial', 11, 'bold'),
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.supplier_name_var = tk.StringVar()
        name_entry = tk.Entry(
            name_frame,
            textvariable=self.supplier_name_var,
            font=('Arial', 11),
            width=30,
            relief='solid',
            bd=1
        )
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Phone
        phone_frame = tk.Frame(info_frame, bg='white')
        phone_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            phone_frame,
            text="Phone:",
            font=('Arial', 11, 'bold'),
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.supplier_phone_var = tk.StringVar()
        phone_entry = tk.Entry(
            phone_frame,
            textvariable=self.supplier_phone_var,
            font=('Arial', 11),
            width=30,
            relief='solid',
            bd=1
        )
        phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Address
        address_frame = tk.Frame(info_frame, bg='white')
        address_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            address_frame,
            text="Address:",
            font=('Arial', 11, 'bold'),
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.supplier_address_var = tk.StringVar()
        address_entry = tk.Entry(
            address_frame,
            textvariable=self.supplier_address_var,
            font=('Arial', 11),
            width=30,
            relief='solid',
            bd=1
        )
        address_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Supplier Type
        type_frame = tk.Frame(info_frame, bg='white')
        type_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            type_frame,
            text="Type:",
            font=('Arial', 11, 'bold'),
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.supplier_type_var = tk.StringVar(value="Supplier")
        type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.supplier_type_var,
            values=["Supplier", "Vendor", "Dakandar", "Company"],
            state="readonly",
            font=('Arial', 11),
            width=28
        )
        type_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # Bill Items Frame (similar to customer form)
        items_frame = tk.LabelFrame(main_container, text="📦 Bill Items", font=('Arial', 12, 'bold'), 
                                  bg='white', fg=self.colors['primary'], padx=10, pady=10)
        items_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Item Entry Frame
        item_entry_frame = tk.Frame(items_frame, bg='white')
        item_entry_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Product Name
        tk.Label(
            item_entry_frame,
            text="Product:",
            font=('Arial', 10, 'bold'),
            bg='white'
        ).grid(row=0, column=0, padx=(0, 5), pady=5, sticky='w')
        
        self.supplier_item_product_var = tk.StringVar()
        product_entry = tk.Entry(
            item_entry_frame,
            textvariable=self.supplier_item_product_var,
            font=('Arial', 10),
            width=15,
            relief='solid',
            bd=1
        )
        product_entry.grid(row=0, column=1, padx=(0, 10), pady=5, sticky='w')
        
        # Quantity
        tk.Label(
            item_entry_frame,
            text="Qty:",
            font=('Arial', 10, 'bold'),
            bg='white'
        ).grid(row=0, column=2, padx=(0, 5), pady=5, sticky='w')
        
        self.supplier_item_quantity_var = tk.StringVar()
        quantity_entry = tk.Entry(
            item_entry_frame,
            textvariable=self.supplier_item_quantity_var,
            font=('Arial', 10),
            width=8,
            relief='solid',
            bd=1
        )
        quantity_entry.grid(row=0, column=3, padx=(0, 10), pady=5, sticky='w')
        
        # Unit (Measurement Dropdown)
        tk.Label(
            item_entry_frame,
            text="Unit:",
            font=('Arial', 10, 'bold'),
            bg='white'
        ).grid(row=0, column=4, padx=(0, 5), pady=5, sticky='w')
        
        self.supplier_item_unit_var = tk.StringVar(value="pieces")
        unit_combo = ttk.Combobox(
            item_entry_frame,
            textvariable=self.supplier_item_unit_var,
            values=self.measurement_units,
            state="readonly",
            font=('Arial', 10),
            width=10
        )
        unit_combo.grid(row=0, column=5, padx=(0, 10), pady=5, sticky='w')
        
        # Unit Price
        tk.Label(
            item_entry_frame,
            text="Unit Price:",
            font=('Arial', 10, 'bold'),
            bg='white'
        ).grid(row=0, column=6, padx=(0, 5), pady=5, sticky='w')
        
        self.supplier_item_price_var = tk.StringVar()
        price_entry = tk.Entry(
            item_entry_frame,
            textvariable=self.supplier_item_price_var,
            font=('Arial', 10),
            width=10,
            relief='solid',
            bd=1
        )
        price_entry.grid(row=0, column=7, padx=(0, 10), pady=5, sticky='w')
        
        # Add Item Button
        add_item_btn = tk.Button(
            item_entry_frame,
            text="➕ Add Item",
            bg=self.colors['info'],
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self.add_supplier_item,
            cursor='hand2'
        )
        add_item_btn.grid(row=0, column=8, padx=(10, 0), pady=5, sticky='w')
        
        # Items Table
        table_frame = tk.Frame(items_frame, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create items treeview
        columns = ('Product', 'Quantity', 'Unit', 'Unit Price', 'Total', 'Actions')
        self.supplier_items_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=6)
        
        # Configure columns
        column_widths = {
            'Product': 120, 'Quantity': 60, 'Unit': 80, 
            'Unit Price': 90, 'Total': 90, 'Actions': 80
        }
        
        for col in columns:
            self.supplier_items_tree.heading(col, text=col)
            self.supplier_items_tree.column(col, width=column_widths[col], anchor='center')
        
        # Add scrollbar for items
        items_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.supplier_items_tree.yview)
        self.supplier_items_tree.configure(yscrollcommand=items_scrollbar.set)
        
        self.supplier_items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        items_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click to remove item
        self.supplier_items_tree.bind('<Double-1>', self.remove_supplier_item)
        
        # Summary Frame
        summary_frame = tk.Frame(main_container, bg='lightgray', padx=10, pady=5)
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.supplier_total_var = tk.StringVar(value="Total: PKR 0")
        tk.Label(
            summary_frame,
            textvariable=self.supplier_total_var,
            font=('Arial', 12, 'bold'),
            bg='lightgray',
            fg='black'
        ).pack()
        
        # Buttons Frame
        button_frame = tk.Frame(main_container, bg='white', pady=10)
        button_frame.pack(fill=tk.X)
        
        # Save button (Orange)
        save_btn = tk.Button(
            button_frame,
            text="💾 SAVE SUPPLIER & BILL",
            bg=self.colors['warning'],
            fg='white',
            font=('Arial', 12, 'bold'),
            command=self.save_supplier_with_items,
            width=20,
            height=1,
            cursor='hand2',
            relief='raised',
            bd=2
        )
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Cancel button (Red)
        cancel_btn = tk.Button(
            button_frame,
            text="❌ CANCEL",
            bg=self.colors['danger'],
            fg='white',
            font=('Arial', 12, 'bold'),
            command=self.supplier_window.destroy,
            width=10,
            height=1,
            cursor='hand2',
            relief='raised',
            bd=2
        )
        cancel_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Clear Items button
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear Items",
            bg=self.colors['warning'],
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self.clear_supplier_items,
            cursor='hand2'
        )
        clear_btn.pack(side=tk.LEFT)
        
        # Bind Enter key to add item
        self.supplier_window.bind('<Return>', lambda e: self.add_supplier_item())
        
        # Set focus to name field
        name_entry.focus()
    
    def add_supplier_item(self):
        """Add item to supplier bill"""
        try:
            product = self.supplier_item_product_var.get().strip()
            quantity_str = self.supplier_item_quantity_var.get().strip()
            unit = self.supplier_item_unit_var.get()
            price_str = self.supplier_item_price_var.get().strip()
            
            if not product:
                messagebox.showerror("Error", "Please enter product name!")
                return
                
            if not quantity_str:
                messagebox.showerror("Error", "Please enter quantity!")
                return
                
            if not price_str:
                messagebox.showerror("Error", "Please enter unit price!")
                return
            
            try:
                quantity = float(quantity_str)
                price = float(price_str)
                
                if quantity <= 0:
                    messagebox.showerror("Error", "Quantity must be greater than 0!")
                    return
                    
                if price <= 0:
                    messagebox.showerror("Error", "Price must be greater than 0!")
                    return
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for quantity and price!")
                return
            
            # Calculate total
            total = quantity * price
            
            # Add to items list
            item_data = {
                'product_name': product,
                'quantity': quantity,
                'unit': unit,
                'unit_price': price,
                'total_price': total
            }
            self.supplier_items.append(item_data)
            
            # Add to treeview
            self.supplier_items_tree.insert('', 'end', values=(
                product,
                quantity,
                unit,
                f"PKR {price:,.0f}",
                f"PKR {total:,.0f}",
                "❌ Remove"
            ))
            
            # Update total
            self.update_supplier_total()
            
            # Clear entry fields
            self.supplier_item_product_var.set("")
            self.supplier_item_quantity_var.set("")
            self.supplier_item_price_var.set("")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {str(e)}")
    
    def remove_supplier_item(self, event):
        """Remove item from supplier bill"""
        item = self.supplier_items_tree.selection()
        if not item:
            return
            
        item = item[0]
        index = self.supplier_items_tree.index(item)
        
        # Remove from list and treeview
        if 0 <= index < len(self.supplier_items):
            self.supplier_items.pop(index)
            self.supplier_items_tree.delete(item)
            self.update_supplier_total()
    
    def clear_supplier_items(self):
        """Clear all supplier items"""
        if self.supplier_items:
            result = messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all items?")
            if result:
                self.supplier_items.clear()
                for item in self.supplier_items_tree.get_children():
                    self.supplier_items_tree.delete(item)
                self.update_supplier_total()
    
    def update_supplier_total(self):
        """Update supplier total amount"""
        total = sum(item['total_price'] for item in self.supplier_items)
        self.supplier_total_var.set(f"Total: PKR {total:,.0f}")
    
    def save_supplier_with_items(self):
        """Save supplier with bill items"""
        try:
            # Get form values
            name = self.supplier_name_var.get().strip()
            phone = self.supplier_phone_var.get().strip()
            address = self.supplier_address_var.get().strip()
            supplier_type = self.supplier_type_var.get()
            
            # Validate inputs
            if not name:
                messagebox.showerror("Error", "Please enter supplier name!")
                return
                
            if not self.supplier_items:
                messagebox.showerror("Error", "Please add at least one bill item!")
                return
            
            # Save supplier with items
            success, message = self.udhar_service.add_supplier_with_items(name, phone, address, self.supplier_items, supplier_type)
            
            if success:
                messagebox.showinfo("Success", message)
                self.supplier_window.destroy()
                self.load_suppliers()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save supplier: {str(e)}")
   
    # PAYMENT DIALOGS
    def show_customer_payment_dialog(self, customer_id, customer_name, current_balance):
        """Show customer payment dialog - FIXED VERSION"""
        try:
            self.customer_payment_window = tk.Toplevel(self.parent)
            self.customer_payment_window.title("Receive Payment from Customer")
            self.customer_payment_window.geometry("600x500")  # Increased height
            self.customer_payment_window.configure(bg='white')
            self.customer_payment_window.resizable(False, False)
            self.customer_payment_window.transient(self.parent)
            self.customer_payment_window.grab_set()
            
            self.center_window(self.customer_payment_window)
            
            # Header
            header_frame = tk.Frame(self.customer_payment_window, bg=self.colors['primary'])
            header_frame.pack(fill=tk.X, pady=(0, 15))
            
            tk.Label(
                header_frame,
                text="💰 RECEIVE PAYMENT",
                font=('Arial', 16, 'bold'),
                fg='white',
                bg=self.colors['primary'],
                pady=15
            ).pack()
            
            # Main content frame
            main_frame = tk.Frame(self.customer_payment_window, bg='white', padx=20, pady=10)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Customer info
            info_frame = tk.Frame(main_frame, bg='white')
            info_frame.pack(fill=tk.X, pady=10)
            
            tk.Label(
                info_frame,
                text=f"Customer: {customer_name}",
                font=('Arial', 12, 'bold'),
                fg=self.colors['primary'],
                bg='white'
            ).pack(anchor='w')
            
            tk.Label(
                info_frame,
                text=f"Current Balance: PKR {current_balance:,.0f}",
                font=('Arial', 12, 'bold'),
                fg=self.colors['danger'],
                bg='white'
            ).pack(anchor='w', pady=5)
            
            # Payment amount
            amount_frame = tk.Frame(main_frame, bg='white')
            amount_frame.pack(fill=tk.X, pady=15)
            
            tk.Label(
                amount_frame,
                text="Payment Amount (PKR):",
                font=('Arial', 11, 'bold'),
                fg=self.colors['primary'],
                bg='white'
            ).pack(anchor='w')
            
            self.customer_payment_amount_var = tk.StringVar()
            payment_entry = tk.Entry(
                amount_frame,
                textvariable=self.customer_payment_amount_var,
                font=('Arial', 14),
                relief='solid',
                bd=1,
                width=20
            )
            payment_entry.pack(fill=tk.X, pady=8, ipady=6)
            
            # Payment date
            date_frame = tk.Frame(main_frame, bg='white')
            date_frame.pack(fill=tk.X, pady=15)
            
            tk.Label(
                date_frame,
                text="Payment Date:",
                font=('Arial', 11, 'bold'),
                fg=self.colors['primary'],
                bg='white'
            ).pack(anchor='w')
            
            self.customer_payment_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
            date_entry = DateEntry(
                date_frame,
                textvariable=self.customer_payment_date_var,
                font=('Arial', 12),
                date_pattern='yyyy-mm-dd',
                background='darkblue',
                foreground='white',
                borderwidth=2,
                width=18
            )
            date_entry.pack(fill=tk.X, pady=8, ipady=6)
            
            # Buttons Frame - FIXED: Made more prominent
            button_frame = tk.Frame(main_frame, bg='white')
            button_frame.pack(fill=tk.X, pady=25)
            
            # Button container to center the buttons
            button_container = tk.Frame(button_frame, bg='white')
            button_container.pack(expand=True)
            
            # Save Payment button - Made larger and more visible
            save_btn = tk.Button(
                button_container,
                text="💾 SAVE PAYMENT",
                bg=self.colors['success'],
                fg='white',
                font=('Arial', 13, 'bold'),
                command=lambda: self.process_customer_payment(customer_id),
                width=15,
                height=12,
                cursor='hand2',
                relief='raised',
                bd=3
            )
            save_btn.pack(side=tk.LEFT, padx=10)
            
            # Cancel button - Made larger and more visible
            cancel_btn = tk.Button(
                button_container,
                text="❌ CANCEL",
                bg=self.colors['danger'],
                fg='white',
                font=('Arial', 13, 'bold'),
                command=self.customer_payment_window.destroy,
                width=15,
                height=12,
                cursor='hand2',
                relief='raised',
                bd=3
            )
            cancel_btn.pack(side=tk.LEFT, padx=10)
            
            # Bind Enter key to save payment
            self.customer_payment_window.bind('<Return>', lambda e: self.process_customer_payment(customer_id))
            
            # Set focus to payment field
            payment_entry.focus()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open payment dialog: {str(e)}")
    
    def show_supplier_payment_dialog(self, supplier_id, supplier_name, current_balance):
        """Show supplier payment dialog - FIXED VERSION"""
        try:
            self.supplier_payment_window = tk.Toplevel(self.parent)
            self.supplier_payment_window.title("Make Payment to Supplier")
            self.supplier_payment_window.geometry("600x500")  # Increased height
            self.supplier_payment_window.configure(bg='white')
            self.supplier_payment_window.resizable(False, False)
            self.supplier_payment_window.transient(self.parent)
            self.supplier_payment_window.grab_set()
            
            self.center_window(self.supplier_payment_window)
            
            # Header
            header_frame = tk.Frame(self.supplier_payment_window, bg=self.colors['primary'])
            header_frame.pack(fill=tk.X, pady=(0, 15))
            
            tk.Label(
                header_frame,
                text="💳 MAKE PAYMENT",
                font=('Arial', 16, 'bold'),
                fg='white',
                bg=self.colors['primary'],
                pady=15
            ).pack()
            
            # Main content frame
            main_frame = tk.Frame(self.supplier_payment_window, bg='white', padx=20, pady=10)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Supplier info
            info_frame = tk.Frame(main_frame, bg='white')
            info_frame.pack(fill=tk.X, pady=10)
            
            tk.Label(
                info_frame,
                text=f"Supplier: {supplier_name}",
                font=('Arial', 12, 'bold'),
                fg=self.colors['primary'],
                bg='white'
            ).pack(anchor='w')
            
            tk.Label(
                info_frame,
                text=f"Current Balance: PKR {current_balance:,.0f}",
                font=('Arial', 12, 'bold'),
                fg=self.colors['danger'],
                bg='white'
            ).pack(anchor='w', pady=5)
            
            # Payment amount
            amount_frame = tk.Frame(main_frame, bg='white')
            amount_frame.pack(fill=tk.X, pady=15)
            
            tk.Label(
                amount_frame,
                text="Payment Amount (PKR):",
                font=('Arial', 11, 'bold'),
                fg=self.colors['primary'],
                bg='white'
            ).pack(anchor='w')
            
            self.supplier_payment_amount_var = tk.StringVar()
            payment_entry = tk.Entry(
                amount_frame,
                textvariable=self.supplier_payment_amount_var,
                font=('Arial', 14),
                relief='solid',
                bd=1,
                width=20
            )
            payment_entry.pack(fill=tk.X, pady=8, ipady=6)
            
            # Payment date
            date_frame = tk.Frame(main_frame, bg='white')
            date_frame.pack(fill=tk.X, pady=15)
            
            tk.Label(
                date_frame,
                text="Payment Date:",
                font=('Arial', 11, 'bold'),
                fg=self.colors['primary'],
                bg='white'
            ).pack(anchor='w')
            
            self.supplier_payment_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
            date_entry = DateEntry(
                date_frame,
                textvariable=self.supplier_payment_date_var,
                font=('Arial', 12),
                date_pattern='yyyy-mm-dd',
                background='darkblue',
                foreground='white',
                borderwidth=2,
                width=18
            )
            date_entry.pack(fill=tk.X, pady=8, ipady=6)
            
            # Buttons Frame - FIXED: Made more prominent
            button_frame = tk.Frame(main_frame, bg='white')
            button_frame.pack(fill=tk.X, pady=25)
            
            # Button container to center the buttons
            button_container = tk.Frame(button_frame, bg='white')
            button_container.pack(expand=True)
            
            # Save Payment button - Made larger and more visible
            save_btn = tk.Button(
                button_container,
                text="💾 SAVE PAYMENT",
                bg=self.colors['warning'],
                fg='white',
                font=('Arial', 13, 'bold'),
                command=lambda: self.process_supplier_payment(supplier_id),
                width=18,
                height=6,
                cursor='hand2',
                relief='raised',
                bd=3
            )
            save_btn.pack(side=tk.LEFT, padx=10)
            
            # Cancel button - Made larger and more visible
            cancel_btn = tk.Button(
                button_container,
                text="❌ CANCEL",
                bg=self.colors['danger'],
                fg='white',
                font=('Arial', 13, 'bold'),
                command=self.supplier_payment_window.destroy,
                width=12,
                height=6,
                cursor='hand2',
                relief='raised',
                bd=3
            )
            cancel_btn.pack(side=tk.LEFT, padx=10)
            
            # Bind Enter key to save payment
            self.supplier_payment_window.bind('<Return>', lambda e: self.process_supplier_payment(supplier_id))
            
            # Set focus to payment field
            payment_entry.focus()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open payment dialog: {str(e)}")

    def process_customer_payment(self, customer_id):
        """Process customer payment"""
        try:
            amount_str = self.customer_payment_amount_var.get().strip()
            payment_date = self.customer_payment_date_var.get().strip()
            
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
            
            # Validate date
            try:
                datetime.strptime(payment_date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format!")
                return
            
            # Process payment with date
            success, message = self.udhar_service.receive_payment(customer_id, amount, payment_date)
            
            if success:
                messagebox.showinfo("Success", message)
                self.customer_payment_window.destroy()
                self.load_customers()
                self.refresh_header()  # Refresh header summary
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process payment: {str(e)}")
    
    def process_supplier_payment(self, supplier_id):
        """Process supplier payment"""
        try:
            amount_str = self.supplier_payment_amount_var.get().strip()
            payment_date = self.supplier_payment_date_var.get().strip()
            
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
            
            # Validate date
            try:
                datetime.strptime(payment_date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format!")
                return
            
            # Process payment with date
            success, message = self.udhar_service.make_payment(supplier_id, amount, payment_date)
            
            if success:
                messagebox.showinfo("Success", message)
                self.supplier_payment_window.destroy()
                self.load_suppliers()
                self.refresh_header()  # Refresh header summary
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process payment: {str(e)}")


    # DELETE FUNCTIONALITY
    def confirm_customer_delete(self, customer_id, customer_name):
        """Confirm customer deletion"""
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete customer '{customer_name}'?\n\nThis action cannot be undone!",
            icon='warning'
        )
        
        if result:
            self.delete_customer(customer_id)
    
    def confirm_supplier_delete(self, supplier_id, supplier_name):
        """Confirm supplier deletion"""
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete supplier '{supplier_name}'?\n\nThis action cannot be undone!",
            icon='warning'
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
                self.refresh_header()  # Refresh header summary
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed: {str(e)}")
    
    def delete_supplier(self, supplier_id):
        """Delete supplier"""
        try:
            success, message = self.udhar_service.force_delete_supplier(supplier_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.load_suppliers()
                self.refresh_header()  # Refresh header summary
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed: {str(e)}")

    # UTILITY METHODS
    def center_window(self, window):
        """Center window on screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def bind_events(self):
        """Bind click events to the tables"""
        self.customer_tree.bind('<Button-1>', self.handle_customer_action)
        self.supplier_tree.bind('<Button-1>', self.handle_supplier_action)