import tkinter as tk
from tkinter import ttk, messagebox
from backend.sale_service import SaleService
from backend.product_service import ProductService
from datetime import datetime, timedelta

class SaleManagement:
    def __init__(self, parent):
        self.parent = parent
        self.sale_service = SaleService()
        self.product_service = ProductService()
        self.setup_ui()
        self.load_sales()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title and Refresh Button
        title_frame = tk.Frame(main_frame, bg='white')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="💰 SALE MANAGEMENT",
            font=('Arial', 20, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(side=tk.LEFT)
        
        # Add Refresh Button
        refresh_btn = tk.Button(
            title_frame,
            text="🔄 Refresh",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.load_sales,
            cursor='hand2'
        )
        refresh_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Category filter
        filter_frame = tk.Frame(main_frame, bg='white')
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            filter_frame,
            text="Filter by Category:",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.category_var = tk.StringVar(value="All Categories")
        categories = ["All Categories", "Paint", "Sanitary", "Roof Sheet", "Hardware", "Limination Sheet"]
        self.category_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.category_var,
            values=categories,
            state='readonly',
            font=('Arial', 12),
            width=20
        )
        self.category_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.category_combo.bind('<<ComboboxSelected>>', lambda e: self.load_sales())
        
        # 🆕 CATEGORY SUMMARY FRAME
        self.setup_category_summary(main_frame)
        
        # Sales table
        table_frame = tk.Frame(main_frame, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create treeview with essential columns
        columns = ('ID', 'Date', 'Customer', 'Category', 'Items', 'Total', 'Discount', 'Final Amount')
        self.sales_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.sales_tree.heading(col, text=col)
        
        # Define columns
        self.sales_tree.column('ID', width=60)
        self.sales_tree.column('Date', width=120)
        self.sales_tree.column('Customer', width=150)
        self.sales_tree.column('Category', width=120)
        self.sales_tree.column('Items', width=80)
        self.sales_tree.column('Total', width=100)
        self.sales_tree.column('Discount', width=100)
        self.sales_tree.column('Final Amount', width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        
        self.sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click to view details
        self.sales_tree.bind('<Double-1>', self.view_sale_details)
    
    def setup_category_summary(self, parent):
        """Setup category-wise sales summary"""
        # Summary header
        summary_header = tk.Frame(parent, bg='#34495e')
        summary_header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            summary_header,
            text="📊 CATEGORY SALES SUMMARY",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#34495e'
        ).pack(pady=8)
        
        # Summary cards container
        self.summary_container = tk.Frame(parent, bg='#f8f9fa', relief='solid', bd=1)
        self.summary_container.pack(fill=tk.X, pady=(0, 10))
        
        # Initialize summary labels (will be updated in load_sales)
        self.summary_labels = {}
        categories = ["All", "Paint", "Sanitary", "Roof Sheet", "Hardware", "Limination Sheet"]
        
        summary_frame = tk.Frame(self.summary_container, bg='#f8f9fa')
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        for i, category in enumerate(categories):
            card = tk.Frame(summary_frame, bg='white', relief='solid', bd=1, width=150, height=80)
            card.pack(side=tk.LEFT, padx=5)
            card.pack_propagate(False)
            
            # Category name
            tk.Label(
                card,
                text=category,
                font=('Arial', 10, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(pady=(8, 2))
            
            # Amount (will be updated)
            amount_label = tk.Label(
                card,
                text="₨0",
                font=('Arial', 12, 'bold'),
                fg='#27ae60',
                bg='white'
            )
            amount_label.pack(pady=2)
            
            # Count (will be updated)
            count_label = tk.Label(
                card,
                text="0 sales",
                font=('Arial', 9),
                fg='#7f8c8d',
                bg='white'
            )
            count_label.pack(pady=2)
            
            self.summary_labels[category] = {
                'amount': amount_label,
                'count': count_label
            }
    
    def safe_get(self, data, index, default=None):
        """Safely get item from tuple/list by index"""
        try:
            return data[index] if data and len(data) > index else default
        except (IndexError, TypeError):
            return default
    
    def detect_category_from_product(self, company, product_type):
        """Direct category detection from product names"""
        # Convert to lowercase for easier matching
        company_lower = company.lower() if company else ""
        product_lower = product_type.lower() if product_type else ""
        
        # Combine for search
        search_text = f"{company_lower} {product_lower}"
        
        # Paint category
        paint_keywords = ['paint', 'color', 'coating', 'emulsion', 'enamel', 'primer', 'brush', 'roller', 'berger', 'nippon']
        if any(word in search_text for word in paint_keywords):
            return "Paint"
        
        # Sanitary category  
        sanitary_keywords = ['sanitary', 'washbasin', 'basin', 'toilet', 'commode', 'bathroom', 'tap', 'shower', 'sink', 'swiss', 'dura']
        if any(word in search_text for word in sanitary_keywords):
            return "Sanitary"
        
        # Roof Sheet category
        roof_keywords = ['roof', 'sheet', 'metal', 'galvanized', 'iron', 'steel', 'corrugated', 'diamond', 'metro']
        if any(word in search_text for word in roof_keywords):
            return "Roof Sheet"
        
        # Hardware category
        hardware_keywords = ['hardware', 'tool', 'nail', 'screw', 'hammer', 'plier', 'wrench', 'drill', 'cutter', 'bolt', 'nut']
        if any(word in search_text for word in hardware_keywords):
            return "Hardware"
        
        # Limination Sheet category
        limination_keywords = ['limination', 'lamination', 'board', 'plywood', 'wood', 'sheet', 'glossy', 'matte', 'textured']
        if any(word in search_text for word in limination_keywords):
            return "Limination Sheet"
        
        return "General"
    
    def get_sale_category(self, sale_id):
        """Get category for a sale by checking all its items"""
        try:
            sale_items = self.sale_service.get_sale_items(sale_id)
            
            if not sale_items:
                return "General"
            
            categories_found = []
            
            for item in sale_items:
                # Try to get category_name from different indices
                category_name = None
                
                # Try index 9 (if JOIN query returns category_name)
                if len(item) > 9:
                    category_name = self.safe_get(item, 9, '')
                
                # If not found, try index 8
                if not category_name and len(item) > 8:
                    category_name = self.safe_get(item, 8, '')
                
                # If we found a specific category, add it to our list
                if category_name and category_name not in ['', 'N/A', 'General']:
                    categories_found.append(category_name)
                
                # Fallback: detect from product info
                if not category_name or category_name == 'General':
                    company = self.safe_get(item, 6, '') if len(item) > 6 else ''
                    product_type = self.safe_get(item, 7, '') if len(item) > 7 else ''
                    
                    detected_category = self.detect_category_from_product(company, product_type)
                    if detected_category != "General":
                        categories_found.append(detected_category)
            
            # Return the most common category, or first found, or "General"
            if categories_found:
                from collections import Counter
                category_counts = Counter(categories_found)
                most_common_category = category_counts.most_common(1)[0][0]
                return most_common_category
            else:
                return "General"
                
        except Exception as e:
            return "General"
    
    def get_customer_name(self, sale_data):
        """Extract customer name from sale data"""
        try:
            # Check if customer_name is available in the result (index 7)
            if len(sale_data) > 7 and sale_data[7]:
                customer_name = sale_data[7]
                if customer_name and customer_name not in ['', 'N/A', None, 'Walk-in Customer']:
                    name = str(customer_name).strip()
                    if name and name != 'None':
                        return name
            
            # Fallback: Try to get customer by ID
            customer_id = self.safe_get(sale_data, 1, None)
            if customer_id:
                try:
                    customers = self.sale_service.get_all_customers()
                    for customer in customers:
                        if customer[0] == customer_id:
                            return customer[1]
                except:
                    pass
            
            return "Walk-in Customer"
        except Exception as e:
            return "Walk-in Customer"
    
    def calculate_category_totals(self, sales):
        """Calculate total sales amount for each category"""
        category_totals = {
            "All": {"amount": 0, "count": 0},
            "Paint": {"amount": 0, "count": 0},
            "Sanitary": {"amount": 0, "count": 0},
            "Roof Sheet": {"amount": 0, "count": 0},
            "Hardware": {"amount": 0, "count": 0},
            "Limination Sheet": {"amount": 0, "count": 0},
            "General": {"amount": 0, "count": 0}
        }
        
        for sale in sales:
            sale_id = self.safe_get(sale, 0, 'N/A')
            final_amount = self.safe_get(sale, 4, 0)
            
            # Get category for this sale
            sale_category = self.get_sale_category(sale_id)
            
            # Update category totals
            if sale_category in category_totals:
                category_totals[sale_category]["amount"] += float(final_amount)
                category_totals[sale_category]["count"] += 1
            
            # Update "All" category
            category_totals["All"]["amount"] += float(final_amount)
            category_totals["All"]["count"] += 1
        
        return category_totals
    
    def update_category_summary(self, category_totals):
        """Update the category summary display with calculated totals"""
        for category, data in category_totals.items():
            if category in self.summary_labels:
                amount = data["amount"]
                count = data["count"]
                
                # Update amount label
                self.summary_labels[category]['amount'].config(
                    text=f"₨{amount:,.0f}",
                    fg='#27ae60' if amount > 0 else '#7f8c8d'
                )
                
                # Update count label
                self.summary_labels[category]['count'].config(
                    text=f"{count} sale{'s' if count != 1 else ''}",
                    fg='#3498db' if count > 0 else '#bdc3c7'
                )
    
    def load_sales(self):
        """Load all sales with category filtering and update summary"""
        try:
            selected_category = self.category_var.get()
            
            # Get all sales
            sales = self.sale_service.get_sales_report()
            
            # Clear the treeview
            for item in self.sales_tree.get_children():
                self.sales_tree.delete(item)
                
            if not sales:
                self.sales_tree.insert('', 'end', values=("No sales", "found", "", "", "", "", "", ""))
                return
            
            filtered_count = 0
            
            for sale in sales:
                sale_id = self.safe_get(sale, 0, 'N/A')
                
                # Get the category for this sale
                sale_category = self.get_sale_category(sale_id)
                
                # Apply category filter
                if selected_category != "All Categories":
                    if sale_category != selected_category:
                        continue
                
                filtered_count += 1
                
                # Get sale details
                customer_name = self.safe_get(sale, 7, 'Walk-in Customer')
                sale_date = self.safe_get(sale, 6, 'N/A')
                total_amount = self.safe_get(sale, 2, 0)
                discount = self.safe_get(sale, 3, 0)
                final_amount = self.safe_get(sale, 4, 0)
                
                # Get item count for this sale
                try:
                    items = self.sale_service.get_sale_items(sale_id)
                    item_count = len(items) if items else 0
                except:
                    item_count = 0
                
                # Format date
                if sale_date and isinstance(sale_date, str):
                    try:
                        sale_date = sale_date[:19]
                    except:
                        pass
                
                self.sales_tree.insert('', 'end', values=(
                    sale_id,
                    sale_date,
                    customer_name,
                    sale_category,
                    item_count,
                    f"₨{float(total_amount):,.0f}",
                    f"₨{float(discount):,.0f}",
                    f"₨{float(final_amount):,.0f}"
                ))
            
            # Update category summary
            category_totals = self.calculate_category_totals(sales)
            self.update_category_summary(category_totals)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sales: {str(e)}")
    
    def view_sale_details(self, event):
        """View detailed sale information"""
        selected = self.sales_tree.selection()
        if not selected:
            return
            
        try:
            selected_item = self.sales_tree.item(selected[0])
            values = selected_item['values']
            
            if not values or values[0] == "No sales":
                messagebox.showinfo("Info", "No sale selected")
                return
                
            sale_id = values[0]
            
            # Create details window
            details_window = tk.Toplevel(self.parent)
            details_window.title(f"Sale Details # {sale_id}")
            details_window.geometry("700x600")
            details_window.configure(bg='white')
            details_window.transient(self.parent)
            details_window.grab_set()
            
            # Center the window
            details_window.update_idletasks()
            x = (details_window.winfo_screenwidth() // 2) - (700 // 2)
            y = (details_window.winfo_screenheight() // 2) - (600 // 2)
            details_window.geometry(f"700x600+{x}+{y}")
            
            # Get sale details
            sale_details = self.sale_service.get_sale_details(sale_id)
            sale_items = self.sale_service.get_sale_items(sale_id)
            
            # Display sale details
            details_frame = tk.Frame(details_window, bg='white')
            details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Sale header
            tk.Label(
                details_frame,
                text=f"SALE # {sale_id}",
                font=('Arial', 16, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(anchor='w', pady=(0, 10))
            
            # Customer info
            if sale_details:
                customer_name = self.get_customer_name(sale_details)
                sale_date = self.safe_get(sale_details, 6, 'Unknown Date')
                
                customer_info = f"Customer: {customer_name}"
                tk.Label(
                    details_frame,
                    text=customer_info,
                    font=('Arial', 12),
                    fg='#34495e',
                    bg='white'
                ).pack(anchor='w', pady=(0, 5))
                
                date_info = f"Date: {sale_date}"
                tk.Label(
                    details_frame,
                    text=date_info,
                    font=('Arial', 12),
                    fg='#34495e',
                    bg='white'
                ).pack(anchor='w', pady=(0, 10))
            else:
                tk.Label(
                    details_frame,
                    text="Sale details not found",
                    font=('Arial', 12),
                    fg='#e74c3c',
                    bg='white'
                ).pack(anchor='w', pady=(0, 10))
            
            # Items table
            items_frame = tk.Frame(details_frame, bg='white')
            items_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            # Create treeview for items
            columns = ('Product', 'Qty', 'Price', 'Total')
            items_tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=12)
            
            for col in columns:
                items_tree.heading(col, text=col)
                
            items_tree.column('Product', width=350)
            items_tree.column('Qty', width=60)
            items_tree.column('Price', width=90)
            items_tree.column('Total', width=90)
            
            # Add items
            if sale_items:
                for item in sale_items:
                    company = self.safe_get(item, 6, 'Unknown')
                    product_type = self.safe_get(item, 7, 'Unknown')
                    color = self.safe_get(item, 8, '')
                    category_name = self.safe_get(item, 9, '')
                    
                    quantity = self.safe_get(item, 3, 0)
                    unit_price = self.safe_get(item, 4, 0)
                    total_price = self.safe_get(item, 5, 0)
                    
                    product_text = f"{company} - {product_type}"
                    if color and color != 'N/A':
                        product_text += f" ({color})"
                    if category_name:
                        product_text += f" [{category_name}]"
                        
                    items_tree.insert('', 'end', values=(
                        product_text,
                        quantity,
                        f"₨{float(unit_price):,.0f}",
                        f"₨{float(total_price):,.0f}"
                    ))
            else:
                items_tree.insert('', 'end', values=("No items found", "", "", ""))
                
            items_tree.pack(fill=tk.BOTH, expand=True)
            
            # Totals
            if sale_details:
                totals_frame = tk.Frame(details_frame, bg='white')
                totals_frame.pack(fill=tk.X, pady=10)
                
                subtotal = self.safe_get(sale_details, 2, 0)
                discount = self.safe_get(sale_details, 3, 0)
                final_amount = self.safe_get(sale_details, 4, 0)
                
                tk.Label(
                    totals_frame,
                    text=f"Subtotal: ₨{float(subtotal):,.0f}",
                    font=('Arial', 12),
                    fg='#2c3e50',
                    bg='white'
                ).pack(anchor='e')
                
                tk.Label(
                    totals_frame,
                    text=f"Discount: -₨{float(discount):,.0f}",
                    font=('Arial', 12),
                    fg='#e74c3c',
                    bg='white'
                ).pack(anchor='e')
                
                tk.Label(
                    totals_frame,
                    text=f"Final Amount: ₨{float(final_amount):,.0f}",
                    font=('Arial', 14, 'bold'),
                    fg='#27ae60',
                    bg='white'
                ).pack(anchor='e', pady=5)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sale details: {str(e)}")