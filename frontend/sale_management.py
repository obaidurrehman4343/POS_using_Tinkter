import tkinter as tk
from tkinter import ttk, messagebox
from backend.sale_service import SaleService
from datetime import datetime, timedelta

class SaleManagement:
    def __init__(self, parent):
        self.parent = parent
        self.sale_service = SaleService()
        self.setup_ui()
        self.load_sales()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame,
            text="💰 SALE MANAGEMENT",
            font=('Arial', 20, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 20))
        
        # Filters frame
        filters_frame = tk.Frame(main_frame, bg='#f8f9fa', relief='solid', bd=1)
        filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Top filters row
        top_filters_frame = tk.Frame(filters_frame, bg='#f8f9fa')
        top_filters_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Date Range
        tk.Label(
            top_filters_frame,
            text="Date Range:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Start date
        tk.Label(top_filters_frame, text="From:", font=('Arial', 10), bg='#f8f9fa').pack(side=tk.LEFT, padx=(0, 5))
        self.start_date = tk.Entry(top_filters_frame, font=('Arial', 10), width=12)
        self.start_date.pack(side=tk.LEFT, padx=(0, 10))
        self.start_date.insert(0, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        
        # End date
        tk.Label(top_filters_frame, text="To:", font=('Arial', 10), bg='#f8f9fa').pack(side=tk.LEFT, padx=(0, 5))
        self.end_date = tk.Entry(top_filters_frame, font=('Arial', 10), width=12)
        self.end_date.pack(side=tk.LEFT, padx=(0, 10))
        self.end_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Category filter
        tk.Label(
            top_filters_frame,
            text="Category:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(side=tk.LEFT, padx=(20, 5))
        
        self.category_var = tk.StringVar(value="All Categories")
        categories = ["All Categories", "Paint", "Sanitary", "Roof Sheet", "Hardware", "Limination Sheet"]
        self.category_combo = ttk.Combobox(
            top_filters_frame,
            textvariable=self.category_var,
            values=categories,
            state='readonly',
            font=('Arial', 10),
            width=15
        )
        self.category_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.category_combo.bind('<<ComboboxSelected>>', lambda e: self.load_sales())
        
        # Bottom filters row
        bottom_filters_frame = tk.Frame(filters_frame, bg='#f8f9fa')
        bottom_filters_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Filter button
        filter_btn = tk.Button(
            bottom_filters_frame,
            text="🔍 Apply Filters",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.load_sales
        )
        filter_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Refresh button
        refresh_btn = tk.Button(
            bottom_filters_frame,
            text="🔄 Refresh All",
            font=('Arial', 10),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.refresh_all
        )
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear filters button
        clear_btn = tk.Button(
            bottom_filters_frame,
            text="🗑️ Clear Filters",
            font=('Arial', 10),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            command=self.clear_filters
        )
        clear_btn.pack(side=tk.LEFT)
        
        # Sales table
        table_frame = tk.Frame(main_frame, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with additional category column
        columns = ('ID', 'Date', 'Customer', 'Category', 'Items', 'Total', 'Discount', 'Final Amount')
        self.sales_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.sales_tree.heading(col, text=col)
        
        # Define columns
        self.sales_tree.column('ID', width=50)
        self.sales_tree.column('Date', width=120)
        self.sales_tree.column('Customer', width=120)
        self.sales_tree.column('Category', width=100)
        self.sales_tree.column('Items', width=60)
        self.sales_tree.column('Total', width=90)
        self.sales_tree.column('Discount', width=80)
        self.sales_tree.column('Final Amount', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        
        self.sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click to view details
        self.sales_tree.bind('<Double-1>', self.view_sale_details)
        
    def safe_get(self, data, index, default=None):
        """Safely get item from tuple/list by index"""
        try:
            return data[index] if data and len(data) > index else default
        except (IndexError, TypeError):
            return default
    
    def get_sale_categories(self, sale_id):
        """Get all categories for a sale based on its items"""
        try:
            sale_items = self.sale_service.get_sale_items(sale_id)
            categories = set()
            
            for item in sale_items:
                # Try different indices where category might be stored
                category_name = None
                for idx in [12, 11, 10, 9]:  # Try different possible indices
                    category_name = self.safe_get(item, idx, '')
                    if category_name and category_name not in ['', 'N/A', None]:
                        break
                
                if category_name and category_name not in ['', 'N/A', None]:
                    # Clean up category name
                    category_name = str(category_name).strip().title()
                    categories.add(category_name)
            
            return list(categories)
        except Exception as e:
            print(f"Error getting categories for sale {sale_id}: {e}")
            return []
    
    def get_primary_category(self, categories):
        """Determine primary category for a sale (most frequent or first)"""
        if not categories:
            return "General"
        
        # Count category occurrences
        category_count = {}
        for category in categories:
            category_count[category] = category_count.get(category, 0) + 1
        
        # Return the most frequent category
        return max(category_count.items(), key=lambda x: x[1])[0]
    
    def sale_contains_category(self, sale_id, target_category):
        """Check if a sale contains items from the target category"""
        if target_category == "All Categories":
            return True
            
        sale_categories = self.get_sale_categories(sale_id)
        
        # Debug print to see what categories are found
        if sale_categories:
            print(f"Sale {sale_id} categories: {sale_categories}")
        
        # Check if target category exists in sale categories
        for category in sale_categories:
            if target_category.lower() in category.lower() or category.lower() in target_category.lower():
                return True
        return False
    
    def get_customer_name(self, sale_data):
        """Extract customer name from sale data"""
        try:
            # Try different indices where customer name might be stored
            for idx in [8, 7, 1]:  # Common indices for customer name
                customer_name = self.safe_get(sale_data, idx, '')
                if customer_name and customer_name not in ['', 'N/A', None, 'Walk-in Customer']:
                    return str(customer_name).strip()
            
            # If no specific customer found, return Walk-in Customer
            return "Walk-in Customer"
        except Exception as e:
            print(f"Error getting customer name: {e}")
            return "Walk-in Customer"
    
    def load_sales(self):
        """Load sales based on date and category filters"""
        try:
            start_date = self.start_date.get()
            end_date = self.end_date.get()
            selected_category = self.category_var.get()
            
            sales = self.sale_service.get_sales_report(start_date, end_date)
            
            # Clear existing data
            for item in self.sales_tree.get_children():
                self.sales_tree.delete(item)
                
            if not sales:
                # Show empty message
                self.sales_tree.insert('', 'end', values=(
                    "No sales", "found in", "selected", "filters", "", "", "", ""
                ))
                return
            
            filtered_count = 0
            total_count = 0
            
            # Add sales to treeview with category filtering
            for sale in sales:
                total_count += 1
                sale_id = self.safe_get(sale, 0, 'N/A')
                
                # Apply category filter
                if not self.sale_contains_category(sale_id, selected_category):
                    continue
                
                filtered_count += 1
                
                sale_date = self.safe_get(sale, 6, 'N/A')
                customer_name = self.get_customer_name(sale)  # Use the new method
                total_amount = self.safe_get(sale, 2, 0)
                discount = self.safe_get(sale, 3, 0)
                final_amount = self.safe_get(sale, 4, 0)
                
                # Get categories for display
                sale_categories = self.get_sale_categories(sale_id)
                primary_category = self.get_primary_category(sale_categories)
                
                # Get item count for this sale
                try:
                    items = self.sale_service.get_sale_items(sale_id)
                    item_count = len(items) if items else 0
                except:
                    item_count = 0
                
                self.sales_tree.insert('', 'end', values=(
                    sale_id,
                    sale_date,
                    customer_name,
                    primary_category,
                    item_count,
                    f"₨{float(total_amount):,.0f}",
                    f"₨{float(discount):,.0f}",
                    f"₨{float(final_amount):,.0f}"
                ))
            
            # Show filter summary
            if filtered_count == 0 and total_count > 0:
                self.sales_tree.insert('', 'end', values=(
                    "No sales", "found for", selected_category, "category", "", "", "", ""
                ))
            elif selected_category != "All Categories":
                messagebox.showinfo("Filter Applied", 
                                  f"Showing {filtered_count} of {total_count} sales\nFilter: {selected_category}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sales: {str(e)}")
            print(f"Error details: {e}")
    
    def refresh_all(self):
        """Refresh all data and reset to default filters"""
        self.start_date.delete(0, tk.END)
        self.start_date.insert(0, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        self.end_date.delete(0, tk.END)
        self.end_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.category_var.set("All Categories")
        self.load_sales()
        messagebox.showinfo("Refreshed", "All filters reset to default")
    
    def clear_filters(self):
        """Clear all filters"""
        self.start_date.delete(0, tk.END)
        self.end_date.delete(0, tk.END)
        self.category_var.set("All Categories")
        self.load_sales()
        messagebox.showinfo("Cleared", "All filters cleared")
            
    def view_sale_details(self, event):
        """View detailed sale information with category breakdown"""
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
                customer_name = self.get_customer_name(sale_details)  # Use the new method
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
                
                # Category breakdown
                categories = self.get_sale_categories(sale_id)
                if categories:
                    category_info = f"Categories: {', '.join(categories)}"
                    tk.Label(
                        details_frame,
                        text=category_info,
                        font=('Arial', 11, 'bold'),
                        fg='#e67e22',
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
            
            # Items table with category column
            items_frame = tk.Frame(details_frame, bg='white')
            items_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            # Create treeview for items with category
            columns = ('Product', 'Category', 'Qty', 'Price', 'Total')
            items_tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=12)
            
            for col in columns:
                items_tree.heading(col, text=col)
                
            items_tree.column('Product', width=250)
            items_tree.column('Category', width=100)
            items_tree.column('Qty', width=60)
            items_tree.column('Price', width=90)
            items_tree.column('Total', width=90)
            
            # Add items
            if sale_items:
                for item in sale_items:
                    company = self.safe_get(item, 6, 'Unknown')
                    ptype = self.safe_get(item, 7, 'Unknown')
                    color = self.safe_get(item, 8, '')
                    
                    # Get category from different possible indices
                    category = "General"
                    for idx in [12, 11, 10, 9]:
                        cat = self.safe_get(item, idx, '')
                        if cat and cat not in ['', 'N/A', None]:
                            category = str(cat).strip().title()
                            break
                    
                    quantity = self.safe_get(item, 3, 0)
                    unit_price = self.safe_get(item, 4, 0)
                    total_price = self.safe_get(item, 5, 0)
                    
                    product_text = f"{company} - {ptype}"
                    if color and color != 'N/A':
                        product_text += f" ({color})"
                        
                    items_tree.insert('', 'end', values=(
                        product_text,
                        category,
                        quantity,
                        f"₨{float(unit_price):,.0f}",
                        f"₨{float(total_price):,.0f}"
                    ))
            else:
                items_tree.insert('', 'end', values=("No items found", "", "", "", ""))
                
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
                
                # Payment method
                payment_method = self.safe_get(sale_details, 5, 'cash')
                tk.Label(
                    totals_frame,
                    text=f"Payment Method: {payment_method.title()}",
                    font=('Arial', 11),
                    fg='#7f8c8d',
                    bg='white'
                ).pack(anchor='e')
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sale details: {str(e)}")
            print(f"Error in view_sale_details: {e}")