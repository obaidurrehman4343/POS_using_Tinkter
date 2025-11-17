import tkinter as tk
from tkinter import ttk, messagebox
from backend.sale_service import SaleService
from backend.product_service import ProductService
from datetime import datetime, timedelta
import time
from collections import Counter

class SaleManagement:
    def __init__(self, parent):
        self.parent = parent
        self.sale_service = SaleService()
        self.product_service = ProductService()
        self.auto_refresh_id = None
        
        # Compact color palette
        self.colors = {
            'primary': '#2563eb', 'secondary': '#475569', 'success': '#16a34a',
            'warning': '#d97706', 'danger': '#dc2626', 'dark': '#1e293b',
            'light': '#f8fafc', 'white': '#ffffff', 'border': '#e2e8f0',
            'text_primary': '#1e293b', 'text_secondary': '#64748b',
            'background': '#f1f5f9', 'profit_green': '#059669', 'card_bg': '#ffffff'
        }
        
        self.setup_ui()
        self.load_sales()
        self.start_auto_refresh()
        
    def start_auto_refresh(self):
        """Start auto refresh sales data every 30 seconds"""
        self.auto_refresh()
        
    def auto_refresh(self):
        """Auto refresh sales data every 30 seconds - WITH SAFETY CHECKS"""
        try:
            # Check if parent window and all main widgets still exist
            if (self.parent.winfo_exists() and 
                hasattr(self, 'sales_tree') and 
                self.sales_tree.winfo_exists()):
                
                self.load_sales()
                # Schedule next refresh only if still valid
                if self.parent.winfo_exists():
                    self.auto_refresh_id = self.parent.after(30000, self.auto_refresh)
            else:
                # Stop refreshing if widgets are destroyed
                if self.auto_refresh_id:
                    self.parent.after_cancel(self.auto_refresh_id)
                    self.auto_refresh_id = None
        except tk.TclError:
            # Widget destroyed, stop refreshing
            if self.auto_refresh_id:
                try:
                    self.parent.after_cancel(self.auto_refresh_id)
                except:
                    pass
                self.auto_refresh_id = None
        except Exception as e:
            # Stop on any other error
            if self.auto_refresh_id:
                try:
                    self.parent.after_cancel(self.auto_refresh_id)
                except:
                    pass
                self.auto_refresh_id = None
    
    def stop_auto_refresh(self):
        """Stop auto-refresh when leaving the sales management page"""
        if self.auto_refresh_id:
            try:
                self.parent.after_cancel(self.auto_refresh_id)
            except tk.TclError:
                pass
            self.auto_refresh_id = None
        
    def destroy(self):
        """Clean up auto-refresh when window is destroyed"""
        self.stop_auto_refresh()
        
    def setup_ui(self):
        # Main container
        self.main_container = tk.Frame(self.parent, bg=self.colors['background'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.create_compact_header()
        self.create_quick_stats()
        self.create_category_sales_section()
        self.create_sales_table_section()
    
    def create_compact_header(self):
        """Create compact header"""
        header = tk.Frame(self.main_container, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X, pady=(0, 15))
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg=self.colors['primary'])
        header_content.pack(fill=tk.X, padx=20, pady=12)
        
        tk.Label(
            header_content,
            text="📊 Sales Management",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['white'],
            bg=self.colors['primary']
        ).pack(side=tk.LEFT)
        
        self.last_update_label = tk.Label(
            header_content,
            text="",
            font=('Segoe UI', 9),
            fg=self.colors['light'],
            bg=self.colors['primary']
        )
        self.last_update_label.pack(side=tk.RIGHT)
    
    def create_quick_stats(self):
        """Create quick stats row"""
        stats_frame = tk.Frame(self.main_container, bg=self.colors['background'])
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.profit_card = self.create_stat_card(stats_frame, "Total Profit", "₨0", self.colors['profit_green'])
        self.profit_card.pack(side=tk.LEFT, padx=(0, 10))
        
        self.count_card = self.create_stat_card(stats_frame, "Total Sales", "0", self.colors['primary'])
        self.count_card.pack(side=tk.LEFT)
        
        self.profit_label = self.profit_card.nametowidget(self.profit_card.winfo_children()[0].winfo_children()[1])
        self.sales_count_label = self.count_card.nametowidget(self.count_card.winfo_children()[0].winfo_children()[1])
    
    def create_stat_card(self, parent, title, value, color):
        """Create compact stat card"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1, width=140, height=70)
        card.pack_propagate(False)
        
        content = tk.Frame(card, bg='white')
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        
        tk.Label(
            content,
            text=title,
            font=('Segoe UI', 10),
            fg=self.colors['text_secondary'],
            bg='white'
        ).pack(anchor='w')
        
        value_label = tk.Label(
            content,
            text=value,
            font=('Segoe UI', 16, 'bold'),
            fg=color,
            bg='white'
        )
        value_label.pack(anchor='w', pady=(3, 0))
        
        return card
    
    def create_category_sales_section(self):
        """Create category-wise sales breakdown"""
        category_header = tk.Frame(self.main_container, bg=self.colors['background'])
        category_header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            category_header,
            text="Category-wise Sales",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['background']
        ).pack(anchor='w')
        
        self.category_cards_frame = tk.Frame(self.main_container, bg=self.colors['background'])
        self.category_cards_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.category_cards = {}
        categories = ["Paint", "Sanitary", "Roof Sheet", "Hardware", "Limination Sheet"]
        
        for i, category in enumerate(categories):
            card = self.create_category_card(self.category_cards_frame, category)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10) if i < len(categories)-1 else (0, 0))
            self.category_cards[category] = card
    
    def create_category_card(self, parent, category):
        """Create category sales card"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1, width=110, height=80)
        card.pack_propagate(False)
        
        content = tk.Frame(card, bg='white')
        content.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
        
        icons = {"Paint": "🎨", "Sanitary": "🚿", "Roof Sheet": "🏗️", "Hardware": "🔧", "Limination Sheet": "📄"}
        icon = icons.get(category, "📦")
        
        icon_frame = tk.Frame(content, bg='white')
        icon_frame.pack(fill=tk.X)
        
        tk.Label(icon_frame, text=icon, font=('Segoe UI', 12), bg='white').pack(side=tk.LEFT)
        tk.Label(icon_frame, text=category, font=('Segoe UI', 8, 'bold'), fg=self.colors['text_secondary'], bg='white').pack(side=tk.RIGHT)
        
        amount_label = tk.Label(content, text="₨0", font=('Segoe UI', 12, 'bold'), fg=self.colors['primary'], bg='white')
        amount_label.pack(anchor='w', pady=(3, 0))
        
        count_label = tk.Label(content, text="0 sales", font=('Segoe UI', 7), fg=self.colors['text_secondary'], bg='white')
        count_label.pack(anchor='w')
        
        card.amount_label = amount_label
        card.count_label = count_label
        return card
    
    def create_sales_table_section(self):
        """Create compact sales table section"""
        table_container = tk.Frame(self.main_container, bg=self.colors['card_bg'])
        table_container.pack(fill=tk.BOTH, expand=True)
        
        table_header = tk.Frame(table_container, bg=self.colors['card_bg'])
        table_header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            table_header,
            text="Recent Sales",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['card_bg']
        ).pack(side=tk.LEFT)
        
        columns = ('ID', 'Date', 'Customer', 'Category', 'Items', 'Amount', 'Profit')
        self.sales_tree = ttk.Treeview(table_container, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.sales_tree.heading(col, text=col)
        
        self.sales_tree.column('ID', width=50)
        self.sales_tree.column('Date', width=160)  # Increased width for longer date format
        self.sales_tree.column('Customer', width=100)
        self.sales_tree.column('Category', width=80)
        self.sales_tree.column('Items', width=50)
        self.sales_tree.column('Amount', width=80)
        self.sales_tree.column('Profit', width=70)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=self.colors['white'], foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['white'], borderwidth=0, font=('Segoe UI', 9), rowheight=25)
        style.configure("Treeview.Heading", background=self.colors['light'], foreground=self.colors['text_primary'],
                       relief='flat', font=('Segoe UI', 9, 'bold'))
        style.map("Treeview", background=[('selected', self.colors['primary'])], foreground=[('selected', self.colors['white'])])
        
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        self.sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sales_tree.bind('<Double-1>', self.view_sale_details)
    
    def safe_get(self, data, index, default=None):
        """Safely get item from tuple/list by index"""
        try:
            return data[index] if data and len(data) > index else default
        except (IndexError, TypeError):
            return default

    def get_pakistan_time(self):
        """Get current Pakistan time (UTC+5)"""
        try:
            # Pakistan is UTC+5
            utc_now = datetime.utcnow()
            pakistan_time = utc_now + timedelta(hours=5)
            return pakistan_time
        except Exception:
            return datetime.now()

    def format_display_time(self, date_string):
        """Format time for display - FIXED FORMAT TO YYYY-MM-DD HH:MM:SS"""
        try:
            if not date_string or date_string == 'N/A':
                return 'N/A'
            
            # If it's already a datetime object
            if isinstance(date_string, datetime):
                return date_string.strftime('%Y-%m-%d %H:%M:%S')
            
            # Handle string date from database (ALREADY IN PAKISTAN TIME)
            date_string = str(date_string).split('+')[0].strip()
            
            # Try different date formats
            formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(date_string, fmt)
                    # ✅ FIXED FORMAT: YYYY-MM-DD HH:MM:SS
                    return dt.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    continue
            
            return str(date_string)[:19]  # Return first 19 chars: "YYYY-MM-DD HH:MM:SS"
        except Exception as e:
            return str(date_string)[:19] if date_string else 'N/A'

    def get_sale_category(self, sale_id):
        """Get category for a sale by checking all its items - FIXED"""
        try:
            sale_items = self.sale_service.get_sale_items(sale_id)
            if not sale_items:
                return "General"
            
            categories_found = []
            for item in sale_items:
                # FIXED: Check all possible indices for category name
                category_name = None
                
                # Try different index positions based on possible database schema
                if len(item) > 9:
                    # Schema: [id, sale_id, product_id, quantity, unit_price, total_price, purchase_price, company, type, color, category_name]
                    category_name = self.safe_get(item, 10, '')
                elif len(item) > 8:
                    # Schema: [id, sale_id, product_id, quantity, unit_price, total_price, company, type, color, category_name]
                    category_name = self.safe_get(item, 8, '')
                
                # If still not found, try to get from product table
                if not category_name or category_name in ['', 'N/A', 'General']:
                    product_id = self.safe_get(item, 2)
                    if product_id:
                        product = self.product_service.get_product_by_id(product_id)
                        if product and len(product) >= 14:
                            # Product schema: [id, category_id, company, type, color, sale_price, purchase_price, packing, volume, current_stock, image_path, created_at, updated_at, category_name]
                            category_name = self.safe_get(product, 13, '')
                
                if category_name and category_name not in ['', 'N/A', 'General']:
                    categories_found.append(category_name)
            
            if categories_found:
                category_counts = Counter(categories_found)
                return category_counts.most_common(1)[0][0]
            return "General"
        except Exception as e:
            print(f"Error getting sale category: {e}")
            return "General"
    
    def calculate_sale_profit(self, sale_id):
        """Calculate profit for a sale - USING HISTORICAL PRICES FROM sale_items"""
        try:
            sale_items = self.sale_service.get_sale_items(sale_id)
            total_profit = 0
            
            for item in sale_items:
                # Use historical prices stored in sale_items table
                quantity = self.safe_get(item, 3, 0)        # Index 3: quantity
                unit_sale_price = self.safe_get(item, 4, 0) # Index 4: sale price at time of sale
                historical_purchase_price = self.safe_get(item, 6, 0) # Index 6: purchase price at time of sale
                
                try:
                    # Convert to proper numeric values
                    sale_price = float(unit_sale_price) if unit_sale_price else 0
                    cost_price = float(historical_purchase_price) if historical_purchase_price else 0
                    qty = int(quantity) if quantity else 0
                    
                    # Calculate actual profit using historical prices
                    profit_per_unit = sale_price - cost_price
                    item_profit = profit_per_unit * qty
                    
                    # Add to total
                    total_profit += item_profit
                    
                except (ValueError, TypeError):
                    continue
            
            return total_profit
        except Exception as e:
            print(f"Error calculating profit for sale {sale_id}: {e}")
            return 0
    
    def calculate_total_items_sold(self, sale_id):
        """Calculate total quantity of items sold in a sale - FIXED"""
        try:
            sale_items = self.sale_service.get_sale_items(sale_id)
            total_quantity = 0
            
            for item in sale_items:
                quantity = self.safe_get(item, 3, 0)  # quantity at index 3
                try:
                    total_quantity += int(quantity) if quantity else 0
                except (ValueError, TypeError):
                    continue
            
            return total_quantity
        except Exception as e:
            print(f"Error in calculate_total_items_sold: {e}")
            return 0
    
    def calculate_category_totals(self, sales):
        """Calculate total sales and count for each category - FIXED"""
        category_totals = {}
        
        for sale in sales:
            sale_id = self.safe_get(sale, 0)
            final_amount = self.safe_get(sale, 4, 0)
            category = self.get_sale_category(sale_id)
            
            if category not in category_totals:
                category_totals[category] = {"amount": 0, "count": 0}
            
            try:
                category_totals[category]["amount"] += float(final_amount) if final_amount else 0
                category_totals[category]["count"] += 1
            except (ValueError, TypeError):
                pass
        
        return category_totals
    
    def calculate_total_profit(self, sales):
        """Calculate total profit from all sales"""
        total_profit = 0
        for sale in sales:
            sale_id = self.safe_get(sale, 0)
            sale_profit = self.calculate_sale_profit(sale_id)
            total_profit += sale_profit
        return total_profit

    def safe_widget_update(self, widget, **kwargs):
        """Safely update widget if it exists"""
        try:
            if (widget and 
                hasattr(widget, 'winfo_exists') and 
                widget.winfo_exists() and 
                self.parent.winfo_exists()):
                widget.config(**kwargs)
        except tk.TclError:
            pass  # Widget destroyed, safely ignore

    def update_category_cards(self, category_totals):
        """Update category cards with calculated totals - FIXED"""
        try:
            for category, card in self.category_cards.items():
                if hasattr(card, 'amount_label') and hasattr(card, 'count_label'):
                    if category in category_totals:
                        data = category_totals[category]
                        amount = data["amount"]
                        count = data["count"]
                        
                        self.safe_widget_update(card.amount_label, text=f"₨{amount:,.0f}")
                        self.safe_widget_update(card.count_label, text=f"{count} sale{'s' if count != 1 else ''}")
                    else:
                        self.safe_widget_update(card.amount_label, text="₨0")
                        self.safe_widget_update(card.count_label, text="0 sales")
        except Exception as e:
            print(f"Error updating category cards: {e}")

    def load_sales(self):
        """Load all sales with profit calculation and category breakdown - FIXED DATE FORMAT"""
        try:
            # ✅ ENHANCED SAFETY CHECK: Check if all required widgets exist
            if (not self.parent.winfo_exists() or 
                not hasattr(self, 'sales_tree') or 
                not self.sales_tree.winfo_exists()):
                return

            # Update last refresh time with Pakistan time - FIXED FORMAT
            current_time = self.get_pakistan_time().strftime('%Y-%m-%d %H:%M:%S')
            self.safe_widget_update(self.last_update_label, text=f"Last update: {current_time}")
            
            sales = self.sale_service.get_sales_report()
            
            # Clear treeview with safety check
            try:
                for item in self.sales_tree.get_children():
                    self.sales_tree.delete(item)
            except tk.TclError:
                return  # Treeview destroyed, stop loading
                
            if not sales:
                try:
                    self.sales_tree.insert('', 'end', values=("No", "sales", "found", "", "", "", ""))
                    self.safe_widget_update(self.profit_label, text="₨0")
                    self.safe_widget_update(self.sales_count_label, text="0")
                except tk.TclError:
                    return
                return
            
            # Calculate category totals
            category_totals = self.calculate_category_totals(sales)
            self.update_category_cards(category_totals)
            
            # Update quick stats
            total_profit = self.calculate_total_profit(sales)
            total_sales_count = len(sales)
            
            self.safe_widget_update(self.profit_label, text=f"₨{total_profit:,.0f}")
            self.safe_widget_update(self.sales_count_label, text=f"{total_sales_count}")
            
            # Show sales in chronological order
            recent_sales = sales[:20]
            
            for sale in recent_sales:
                sale_id = self.safe_get(sale, 0, 'N/A')
                customer_name = self.safe_get(sale, 7, 'Walk-in Customer')
                final_amount = self.safe_get(sale, 4, 0)
                sale_date = self.safe_get(sale, 6, 'N/A')
                
                # Format time with CORRECT Pakistan time (no double adjustment) - FIXED FORMAT
                sale_date_display = self.format_display_time(sale_date)
                
                # Get category
                sale_category = self.get_sale_category(sale_id)
                
                # Calculate profit for this sale USING HISTORICAL PRICES
                sale_profit = self.calculate_sale_profit(sale_id)
                
                # Get CORRECT total quantity of items sold
                total_items = self.calculate_total_items_sold(sale_id)
                
                # Format values
                try:
                    final_amount_float = float(final_amount) if final_amount else 0
                except (ValueError, TypeError):
                    final_amount_float = 0
                
                # Insert into treeview with safety check
                try:
                    self.sales_tree.insert('', 'end', values=(
                        sale_id,
                        sale_date_display,  # Fixed format: YYYY-MM-DD HH:MM:SS
                        customer_name[:12] + ('...' if len(customer_name) > 12 else ''),
                        sale_category[:10] + ('...' if len(sale_category) > 10 else ''),
                        total_items,  # CORRECT total quantity of items sold
                        f"₨{final_amount_float:,.0f}",
                        f"₨{sale_profit:,.0f}"  # Accurate profit using historical prices
                    ))
                except tk.TclError:
                    return  # Treeview destroyed, stop loading
                
        except Exception as e:
            print(f"Error loading sales: {e}")

    def view_sale_details(self, event):
        """View detailed sale information with profit breakdown - FIXED DATE FORMAT"""
        selected = self.sales_tree.selection()
        if not selected:
            return
            
        try:
            selected_item = self.sales_tree.item(selected[0])
            values = selected_item['values']
            
            if not values or values[0] == "No":
                messagebox.showinfo("Info", "No sale selected")
                return
                
            sale_id = values[0]
            
            details_window = tk.Toplevel(self.parent)
            details_window.title(f"Sale #{sale_id} Details")
            details_window.geometry("500x500")
            details_window.configure(bg='white')
            details_window.transient(self.parent)
            details_window.grab_set()
            
            details_window.update_idletasks()
            x = (details_window.winfo_screenwidth() // 2) - (500 // 2)
            y = (details_window.winfo_screenheight() // 2) - (500 // 2)
            details_window.geometry(f"500x500+{x}+{y}")
            
            sale_details = self.sale_service.get_sale_details(sale_id)
            sale_items = self.sale_service.get_sale_items(sale_id)
            
            details_frame = tk.Frame(details_window, bg='white')
            details_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
            tk.Label(details_frame, text=f"Sale #{sale_id}", font=('Segoe UI', 14, 'bold'),
                    fg=self.colors['text_primary'], bg='white').pack(anchor='w', pady=(0, 8))
            
            if sale_details:
                customer_name = self.safe_get(sale_details, 7, 'Walk-in Customer')
                sale_date = self.safe_get(sale_details, 6, 'Unknown Date')
                # FIXED FORMAT: YYYY-MM-DD HH:MM:SS
                sale_date_display = self.format_display_time(sale_date)
                
                tk.Label(details_frame, text=f"Customer: {customer_name}", font=('Segoe UI', 10),
                        fg=self.colors['text_primary'], bg='white').pack(anchor='w', pady=(0, 2))
                tk.Label(details_frame, text=f"Date: {sale_date_display}", font=('Segoe UI', 10),
                        fg=self.colors['text_secondary'], bg='white').pack(anchor='w', pady=(0, 10))
            
            items_frame = tk.Frame(details_frame, bg='white')
            items_frame.pack(fill=tk.BOTH, expand=True, pady=8)
            
            columns = ('Product', 'Qty', 'Price', 'Cost', 'Profit')
            items_tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=8)
            
            for col in columns:
                items_tree.heading(col, text=col)
                
            items_tree.column('Product', width=200)
            items_tree.column('Qty', width=40)
            items_tree.column('Price', width=70)
            items_tree.column('Cost', width=70)
            items_tree.column('Profit', width=70)
            
            total_sale_profit = 0
            if sale_items:
                for item in sale_items:
                    company = self.safe_get(item, 6, 'Unknown')
                    product_type = self.safe_get(item, 7, 'Unknown')
                    quantity = self.safe_get(item, 3, 0)
                    unit_price = self.safe_get(item, 4, 0)
                    historical_purchase_price = self.safe_get(item, 6, 0)
                    product_id = self.safe_get(item, 2)
                    
                    # ✅ FIXED: Use current product price if historical is 0
                    if historical_purchase_price == 0:
                        # Get current purchase price from products table
                        product = self.product_service.get_product_by_id(product_id)
                        if product and len(product) >= 7:
                            current_purchase_price = self.safe_get(product, 6, 0)
                            cost_price_val = float(current_purchase_price) if current_purchase_price else 0
                            display_cost = current_purchase_price
                        else:
                            cost_price_val = 0
                            display_cost = 0
                    else:
                        cost_price_val = float(historical_purchase_price) if historical_purchase_price else 0
                        display_cost = historical_purchase_price
                    
                    try:
                        sale_price_val = float(unit_price) if unit_price else 0
                        qty_val = int(quantity) if quantity else 0
                        
                        item_profit = (sale_price_val - cost_price_val) * qty_val
                        total_sale_profit += item_profit
                    except (ValueError, TypeError):
                        item_profit = 0
                    
                    product_text = f"{company} - {product_type}"[:25] + ('...' if len(f"{company} - {product_type}") > 25 else '')
                    items_tree.insert('', 'end', values=(
                        product_text, quantity, f"₨{float(unit_price):,.0f}", 
                        f"₨{float(display_cost):,.0f}", f"₨{item_profit:,.0f}"
                    ))
            else:
                items_tree.insert('', 'end', values=("No items", "", "", "", ""))
                
            items_tree.pack(fill=tk.BOTH, expand=True)
            
            if sale_details:
                totals_frame = tk.Frame(details_frame, bg='white')
                totals_frame.pack(fill=tk.X, pady=8)
                
                subtotal = self.safe_get(sale_details, 2, 0)
                discount = self.safe_get(sale_details, 3, 0)
                final_amount = self.safe_get(sale_details, 4, 0)
                
                profit_percentage = (total_sale_profit / float(final_amount)) * 100 if float(final_amount) > 0 else 0
                
                tk.Label(totals_frame, text=f"Subtotal: ₨{float(subtotal):,.0f}", font=('Segoe UI', 10),
                        fg=self.colors['text_primary'], bg='white').pack(anchor='e')
                tk.Label(totals_frame, text=f"Discount: -₨{float(discount):,.0f}", font=('Segoe UI', 10),
                        fg=self.colors['danger'], bg='white').pack(anchor='e')
                tk.Label(totals_frame, text=f"Final Amount: ₨{float(final_amount):,.0f}", font=('Segoe UI', 11, 'bold'),
                        fg=self.colors['primary'], bg='white').pack(anchor='e', pady=(2, 0))
                
                profit_frame = tk.Frame(details_frame, bg='white')
                profit_frame.pack(fill=tk.X, pady=(5, 0))
                
                tk.Label(profit_frame, text=f"Total Profit: ₨{total_sale_profit:,.0f}", font=('Segoe UI', 11, 'bold'),
                        fg=self.colors['profit_green'], bg='white').pack(anchor='e')
                tk.Label(profit_frame, text=f"Profit Margin: {profit_percentage:.1f}%", font=('Segoe UI', 9),
                        fg=self.colors['text_secondary'], bg='white').pack(anchor='e')
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sale details: {str(e)}")

# import tkinter as tk
# from tkinter import ttk, messagebox
# from backend.sale_service import SaleService
# from backend.product_service import ProductService
# from datetime import datetime, timedelta
# import time

# class SaleManagement:
#     def __init__(self, parent):
#         self.parent = parent
#         self.sale_service = SaleService()
#         self.product_service = ProductService()
#         self.auto_refresh_id = None
        
#         # Compact color palette
#         self.colors = {
#             'primary': '#2563eb', 'secondary': '#475569', 'success': '#16a34a',
#             'warning': '#d97706', 'danger': '#dc2626', 'dark': '#1e293b',
#             'light': '#f8fafc', 'white': '#ffffff', 'border': '#e2e8f0',
#             'text_primary': '#1e293b', 'text_secondary': '#64748b',
#             'background': '#f1f5f9', 'profit_green': '#059669', 'card_bg': '#ffffff'
#         }
        
#         self.setup_ui()
#         self.load_sales()
#         self.start_auto_refresh()
        
#     def start_auto_refresh(self):
#         """Start auto refresh sales data every 30 seconds"""
#         self.auto_refresh()
        
#     def auto_refresh(self):
#         """Auto refresh sales data every 30 seconds - WITH SAFETY CHECKS"""
#         try:
#             # Check if parent window and all main widgets still exist
#             if (self.parent.winfo_exists() and 
#                 hasattr(self, 'sales_tree') and 
#                 self.sales_tree.winfo_exists()):
                
#                 self.load_sales()
#                 # Schedule next refresh only if still valid
#                 if self.parent.winfo_exists():
#                     self.auto_refresh_id = self.parent.after(30000, self.auto_refresh)
#             else:
#                 # Stop refreshing if widgets are destroyed
#                 if self.auto_refresh_id:
#                     self.parent.after_cancel(self.auto_refresh_id)
#                     self.auto_refresh_id = None
#         except tk.TclError:
#             # Widget destroyed, stop refreshing
#             if self.auto_refresh_id:
#                 try:
#                     self.parent.after_cancel(self.auto_refresh_id)
#                 except:
#                     pass
#                 self.auto_refresh_id = None
#         except Exception as e:
#             # Stop on any other error
#             if self.auto_refresh_id:
#                 try:
#                     self.parent.after_cancel(self.auto_refresh_id)
#                 except:
#                     pass
#                 self.auto_refresh_id = None
    
#     def stop_auto_refresh(self):
#         """Stop auto-refresh when leaving the sales management page"""
#         if self.auto_refresh_id:
#             try:
#                 self.parent.after_cancel(self.auto_refresh_id)
#                 self.auto_refresh_id = None
#             except tk.TclError:
#                 self.auto_refresh_id = None
        
#     def destroy(self):
#         """Clean up auto-refresh when window is destroyed"""
#         self.stop_auto_refresh()
        
#     def setup_ui(self):
#         # Main container
#         self.main_container = tk.Frame(self.parent, bg=self.colors['background'])
#         self.main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
#         self.create_compact_header()
#         self.create_quick_stats()
#         self.create_category_sales_section()
#         self.create_sales_table_section()
    
#     def create_compact_header(self):
#         """Create compact header"""
#         header = tk.Frame(self.main_container, bg=self.colors['primary'], height=60)
#         header.pack(fill=tk.X, pady=(0, 15))
#         header.pack_propagate(False)
        
#         header_content = tk.Frame(header, bg=self.colors['primary'])
#         header_content.pack(fill=tk.X, padx=20, pady=12)
        
#         tk.Label(
#             header_content,
#             text="📊 Sales Management",
#             font=('Segoe UI', 16, 'bold'),
#             fg=self.colors['white'],
#             bg=self.colors['primary']
#         ).pack(side=tk.LEFT)
        
#         self.last_update_label = tk.Label(
#             header_content,
#             text="",
#             font=('Segoe UI', 9),
#             fg=self.colors['light'],
#             bg=self.colors['primary']
#         )
#         self.last_update_label.pack(side=tk.RIGHT)
    
#     def create_quick_stats(self):
#         """Create quick stats row"""
#         stats_frame = tk.Frame(self.main_container, bg=self.colors['background'])
#         stats_frame.pack(fill=tk.X, pady=(0, 15))
        
#         self.profit_card = self.create_stat_card(stats_frame, "Total Profit", "₨0", self.colors['profit_green'])
#         self.profit_card.pack(side=tk.LEFT, padx=(0, 10))
        
#         self.count_card = self.create_stat_card(stats_frame, "Total Sales", "0", self.colors['primary'])
#         self.count_card.pack(side=tk.LEFT)
        
#         self.profit_label = self.profit_card.nametowidget(self.profit_card.winfo_children()[0].winfo_children()[1])
#         self.sales_count_label = self.count_card.nametowidget(self.count_card.winfo_children()[0].winfo_children()[1])
    
#     def create_stat_card(self, parent, title, value, color):
#         """Create compact stat card"""
#         card = tk.Frame(parent, bg='white', relief='solid', bd=1, width=140, height=70)
#         card.pack_propagate(False)
        
#         content = tk.Frame(card, bg='white')
#         content.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        
#         tk.Label(
#             content,
#             text=title,
#             font=('Segoe UI', 10),
#             fg=self.colors['text_secondary'],
#             bg='white'
#         ).pack(anchor='w')
        
#         value_label = tk.Label(
#             content,
#             text=value,
#             font=('Segoe UI', 16, 'bold'),
#             fg=color,
#             bg='white'
#         )
#         value_label.pack(anchor='w', pady=(3, 0))
        
#         return card
    
#     def create_category_sales_section(self):
#         """Create category-wise sales breakdown"""
#         category_header = tk.Frame(self.main_container, bg=self.colors['background'])
#         category_header.pack(fill=tk.X, pady=(0, 10))
        
#         tk.Label(
#             category_header,
#             text="Category-wise Sales",
#             font=('Segoe UI', 12, 'bold'),
#             fg=self.colors['text_primary'],
#             bg=self.colors['background']
#         ).pack(anchor='w')
        
#         self.category_cards_frame = tk.Frame(self.main_container, bg=self.colors['background'])
#         self.category_cards_frame.pack(fill=tk.X, pady=(0, 15))
        
#         self.category_cards = {}
#         categories = ["Paint", "Sanitary", "Roof Sheet", "Hardware", "Limination Sheet"]
        
#         for i, category in enumerate(categories):
#             card = self.create_category_card(self.category_cards_frame, category)
#             card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10) if i < len(categories)-1 else (0, 0))
#             self.category_cards[category] = card
    
#     def create_category_card(self, parent, category):
#         """Create category sales card"""
#         card = tk.Frame(parent, bg='white', relief='solid', bd=1, width=110, height=80)
#         card.pack_propagate(False)
        
#         content = tk.Frame(card, bg='white')
#         content.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
        
#         icons = {"Paint": "🎨", "Sanitary": "🚿", "Roof Sheet": "🏗️", "Hardware": "🔧", "Limination Sheet": "📄"}
#         icon = icons.get(category, "📦")
        
#         icon_frame = tk.Frame(content, bg='white')
#         icon_frame.pack(fill=tk.X)
        
#         tk.Label(icon_frame, text=icon, font=('Segoe UI', 12), bg='white').pack(side=tk.LEFT)
#         tk.Label(icon_frame, text=category, font=('Segoe UI', 8, 'bold'), fg=self.colors['text_secondary'], bg='white').pack(side=tk.RIGHT)
        
#         amount_label = tk.Label(content, text="₨0", font=('Segoe UI', 12, 'bold'), fg=self.colors['primary'], bg='white')
#         amount_label.pack(anchor='w', pady=(3, 0))
        
#         count_label = tk.Label(content, text="0 sales", font=('Segoe UI', 7), fg=self.colors['text_secondary'], bg='white')
#         count_label.pack(anchor='w')
        
#         card.amount_label = amount_label
#         card.count_label = count_label
#         return card
    
#     def create_sales_table_section(self):
#         """Create compact sales table section"""
#         table_container = tk.Frame(self.main_container, bg=self.colors['card_bg'])
#         table_container.pack(fill=tk.BOTH, expand=True)
        
#         table_header = tk.Frame(table_container, bg=self.colors['card_bg'])
#         table_header.pack(fill=tk.X, pady=(0, 10))
        
#         tk.Label(
#             table_header,
#             text="Recent Sales",
#             font=('Segoe UI', 12, 'bold'),
#             fg=self.colors['text_primary'],
#             bg=self.colors['card_bg']
#         ).pack(side=tk.LEFT)
        
#         columns = ('ID', 'Date', 'Customer', 'Category', 'Items', 'Amount', 'Profit')
#         self.sales_tree = ttk.Treeview(table_container, columns=columns, show='headings', height=12)
        
#         for col in columns:
#             self.sales_tree.heading(col, text=col)
        
#         self.sales_tree.column('ID', width=50)
#         self.sales_tree.column('Date', width=100)
#         self.sales_tree.column('Customer', width=100)
#         self.sales_tree.column('Category', width=80)
#         self.sales_tree.column('Items', width=50)
#         self.sales_tree.column('Amount', width=80)
#         self.sales_tree.column('Profit', width=70)
        
#         style = ttk.Style()
#         style.theme_use("clam")
#         style.configure("Treeview", background=self.colors['white'], foreground=self.colors['text_primary'],
#                        fieldbackground=self.colors['white'], borderwidth=0, font=('Segoe UI', 9), rowheight=25)
#         style.configure("Treeview.Heading", background=self.colors['light'], foreground=self.colors['text_primary'],
#                        relief='flat', font=('Segoe UI', 9, 'bold'))
#         style.map("Treeview", background=[('selected', self.colors['primary'])], foreground=[('selected', self.colors['white'])])
        
#         scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.sales_tree.yview)
#         self.sales_tree.configure(yscrollcommand=scrollbar.set)
#         self.sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#         self.sales_tree.bind('<Double-1>', self.view_sale_details)
    
#     def safe_get(self, data, index, default=None):
#         """Safely get item from tuple/list by index"""
#         try:
#             return data[index] if data and len(data) > index else default
#         except (IndexError, TypeError):
#             return default

#     def get_pakistan_time(self):
#         """Get current Pakistan time (UTC+5)"""
#         try:
#             # Pakistan is UTC+5
#             utc_now = datetime.utcnow()
#             pakistan_time = utc_now + timedelta(hours=5)
#             return pakistan_time
#         except Exception:
#             return datetime.now()

#     def format_display_time(self, date_string):
#         """Format time for display - DATABASE ALREADY HAS PAKISTAN TIME"""
#         try:
#             if not date_string or date_string == 'N/A':
#                 return 'N/A'
            
#             # If it's already a datetime object
#             if isinstance(date_string, datetime):
#                 return date_string.strftime('%m/%d %H:%M')
            
#             # Handle string date from database (ALREADY IN PAKISTAN TIME)
#             date_string = str(date_string).split('+')[0].strip()
            
#             # Try different date formats
#             formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']
            
#             for fmt in formats:
#                 try:
#                     dt = datetime.strptime(date_string, fmt)
#                     # ✅ NO TIMEZONE ADJUSTMENT NEEDED - Database already stores Pakistan time
#                     return dt.strftime('%m/%d %H:%M')
#                 except ValueError:
#                     continue
            
#             return str(date_string)[:16]
#         except Exception as e:
#             return str(date_string)[:16] if date_string else 'N/A'

#     def get_sale_category(self, sale_id):
#         """Get category for a sale by checking all its items"""
#         try:
#             sale_items = self.sale_service.get_sale_items(sale_id)
#             if not sale_items:
#                 return "General"
            
#             categories_found = []
#             for item in sale_items:
#                 category_name = None
#                 if len(item) > 9:
#                     category_name = self.safe_get(item, 9, '')
#                 if not category_name and len(item) > 8:
#                     category_name = self.safe_get(item, 8, '')
#                 if category_name and category_name not in ['', 'N/A', 'General']:
#                     categories_found.append(category_name)
            
#             if categories_found:
#                 from collections import Counter
#                 category_counts = Counter(categories_found)
#                 return category_counts.most_common(1)[0][0]
#             return "General"
#         except Exception:
#             return "General"
    
#     def calculate_sale_profit(self, sale_id):
#         """Calculate profit for a sale - USING HISTORICAL PRICES FROM sale_items"""
#         try:
#             sale_items = self.sale_service.get_sale_items(sale_id)
#             total_profit = 0
            
#             for item in sale_items:
#                 # Use historical prices stored in sale_items table
#                 quantity = self.safe_get(item, 3, 0)        # Index 3: quantity
#                 unit_sale_price = self.safe_get(item, 4, 0) # Index 4: sale price at time of sale
#                 historical_purchase_price = self.safe_get(item, 6, 0) # Index 6: purchase price at time of sale
                
#                 try:
#                     # Convert to proper numeric values
#                     sale_price = float(unit_sale_price) if unit_sale_price else 0
#                     cost_price = float(historical_purchase_price) if historical_purchase_price else 0
#                     qty = int(quantity) if quantity else 0
                    
#                     # Calculate actual profit using historical prices
#                     profit_per_unit = sale_price - cost_price
#                     item_profit = profit_per_unit * qty
                    
#                     # Add to total
#                     total_profit += item_profit
                    
#                 except (ValueError, TypeError):
#                     continue
            
#             return total_profit
#         except Exception as e:
#             return 0
    
#     def calculate_total_items_sold(self, sale_id):
#         """Calculate total quantity of items sold in a sale - FIXED"""
#         try:
#             sale_items = self.sale_service.get_sale_items(sale_id)
#             total_quantity = 0
            
#             for item in sale_items:
#                 quantity = self.safe_get(item, 3, 0)  # quantity at index 3
#                 try:
#                     total_quantity += int(quantity) if quantity else 0
#                 except (ValueError, TypeError):
#                     continue
            
#             return total_quantity
#         except Exception:
#             return 0
    
#     def calculate_category_totals(self, sales):
#         """Calculate total sales and count for each category"""
#         category_totals = {}
        
#         for sale in sales:
#             sale_id = self.safe_get(sale, 0)
#             final_amount = self.safe_get(sale, 4, 0)
#             category = self.get_sale_category(sale_id)
            
#             if category not in category_totals:
#                 category_totals[category] = {"amount": 0, "count": 0}
            
#             try:
#                 category_totals[category]["amount"] += float(final_amount) if final_amount else 0
#                 category_totals[category]["count"] += 1
#             except (ValueError, TypeError):
#                 pass
        
#         return category_totals
    
#     def calculate_total_profit(self, sales):
#         """Calculate total profit from all sales"""
#         total_profit = 0
#         for sale in sales:
#             sale_id = self.safe_get(sale, 0)
#             sale_profit = self.calculate_sale_profit(sale_id)
#             total_profit += sale_profit
#         return total_profit

#     def safe_widget_update(self, widget, **kwargs):
#         """Safely update widget if it exists"""
#         try:
#             if (widget and 
#                 hasattr(widget, 'winfo_exists') and 
#                 widget.winfo_exists() and 
#                 self.parent.winfo_exists()):
#                 widget.config(**kwargs)
#         except tk.TclError:
#             pass  # Widget destroyed, safely ignore

#     def update_category_cards(self, category_totals):
#         """Update category cards with calculated totals"""
#         try:
#             for category, card in self.category_cards.items():
#                 if hasattr(card, 'amount_label') and hasattr(card, 'count_label'):
#                     if category in category_totals:
#                         data = category_totals[category]
#                         amount = data["amount"]
#                         count = data["count"]
                        
#                         self.safe_widget_update(card.amount_label, text=f"₨{amount:,.0f}")
#                         self.safe_widget_update(card.count_label, text=f"{count} sale{'s' if count != 1 else ''}")
#                     else:
#                         self.safe_widget_update(card.amount_label, text="₨0")
#                         self.safe_widget_update(card.count_label, text="0 sales")
#         except Exception as e:
#             pass

#     def load_sales(self):
#         """Load all sales with profit calculation and category breakdown - FIXED"""
#         try:
#             # ✅ ENHANCED SAFETY CHECK: Check if all required widgets exist
#             if (not self.parent.winfo_exists() or 
#                 not hasattr(self, 'sales_tree') or 
#                 not self.sales_tree.winfo_exists()):
#                 return

#             # Update last refresh time with Pakistan time
#             current_time = self.get_pakistan_time().strftime('%H:%M:%S')
#             self.safe_widget_update(self.last_update_label, text=f"Last update: {current_time}")
            
#             sales = self.sale_service.get_sales_report()
            
#             # Clear treeview with safety check
#             try:
#                 for item in self.sales_tree.get_children():
#                     self.sales_tree.delete(item)
#             except tk.TclError:
#                 return  # Treeview destroyed, stop loading
                
#             if not sales:
#                 try:
#                     self.sales_tree.insert('', 'end', values=("No", "sales", "found", "", "", "", ""))
#                     self.safe_widget_update(self.profit_label, text="₨0")
#                     self.safe_widget_update(self.sales_count_label, text="0")
#                 except tk.TclError:
#                     return
#                 return
            
#             # Calculate category totals
#             category_totals = self.calculate_category_totals(sales)
#             self.update_category_cards(category_totals)
            
#             # Update quick stats
#             total_profit = self.calculate_total_profit(sales)
#             total_sales_count = len(sales)
            
#             self.safe_widget_update(self.profit_label, text=f"₨{total_profit:,.0f}")
#             self.safe_widget_update(self.sales_count_label, text=f"{total_sales_count}")
            
#             # Show sales in chronological order
#             recent_sales = sales[:20]
            
#             for sale in recent_sales:
#                 sale_id = self.safe_get(sale, 0, 'N/A')
#                 customer_name = self.safe_get(sale, 7, 'Walk-in Customer')
#                 final_amount = self.safe_get(sale, 4, 0)
#                 sale_date = self.safe_get(sale, 6, 'N/A')
                
#                 # Format time with CORRECT Pakistan time (no double adjustment)
#                 sale_date_display = self.format_display_time(sale_date)
                
#                 # Get category
#                 sale_category = self.get_sale_category(sale_id)
                
#                 # Calculate profit for this sale USING HISTORICAL PRICES
#                 sale_profit = self.calculate_sale_profit(sale_id)
                
#                 # Get total quantity of items sold
#                 total_items = self.calculate_total_items_sold(sale_id)
                
#                 # Format values
#                 try:
#                     final_amount_float = float(final_amount) if final_amount else 0
#                 except (ValueError, TypeError):
#                     final_amount_float = 0
                
#                 # Insert into treeview with safety check
#                 try:
#                     self.sales_tree.insert('', 'end', values=(
#                         sale_id,
#                         sale_date_display,  # Correct Pakistan time now
#                         customer_name[:12] + ('...' if len(customer_name) > 12 else ''),
#                         sale_category[:10] + ('...' if len(sale_category) > 10 else ''),
#                         total_items,  # Total quantity of items sold
#                         f"₨{final_amount_float:,.0f}",
#                         f"₨{sale_profit:,.0f}"  # Accurate profit using historical prices
#                     ))
#                 except tk.TclError:
#                     return  # Treeview destroyed, stop loading
                
#         except Exception as e:
#             # Silently handle errors to avoid console spam
#             pass

#     def view_sale_details(self, event):
#         """View detailed sale information with profit breakdown"""
#         selected = self.sales_tree.selection()
#         if not selected:
#             return
            
#         try:
#             selected_item = self.sales_tree.item(selected[0])
#             values = selected_item['values']
            
#             if not values or values[0] == "No":
#                 messagebox.showinfo("Info", "No sale selected")
#                 return
                
#             sale_id = values[0]
            
#             details_window = tk.Toplevel(self.parent)
#             details_window.title(f"Sale #{sale_id} Details")
#             details_window.geometry("500x500")
#             details_window.configure(bg='white')
#             details_window.transient(self.parent)
#             details_window.grab_set()
            
#             details_window.update_idletasks()
#             x = (details_window.winfo_screenwidth() // 2) - (500 // 2)
#             y = (details_window.winfo_screenheight() // 2) - (500 // 2)
#             details_window.geometry(f"500x500+{x}+{y}")
            
#             sale_details = self.sale_service.get_sale_details(sale_id)
#             sale_items = self.sale_service.get_sale_items(sale_id)
            
#             details_frame = tk.Frame(details_window, bg='white')
#             details_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
#             tk.Label(details_frame, text=f"Sale #{sale_id}", font=('Segoe UI', 14, 'bold'),
#                     fg=self.colors['text_primary'], bg='white').pack(anchor='w', pady=(0, 8))
            
#             if sale_details:
#                 customer_name = self.safe_get(sale_details, 7, 'Walk-in Customer')
#                 sale_date = self.safe_get(sale_details, 6, 'Unknown Date')
#                 sale_date_display = self.format_display_time(sale_date)
                
#                 tk.Label(details_frame, text=f"Customer: {customer_name}", font=('Segoe UI', 10),
#                         fg=self.colors['text_primary'], bg='white').pack(anchor='w', pady=(0, 2))
#                 tk.Label(details_frame, text=f"Date: {sale_date_display}", font=('Segoe UI', 10),
#                         fg=self.colors['text_secondary'], bg='white').pack(anchor='w', pady=(0, 10))
            
#             items_frame = tk.Frame(details_frame, bg='white')
#             items_frame.pack(fill=tk.BOTH, expand=True, pady=8)
            
#             columns = ('Product', 'Qty', 'Price', 'Cost', 'Profit')
#             items_tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=8)
            
#             for col in columns:
#                 items_tree.heading(col, text=col)
                
#             items_tree.column('Product', width=200)
#             items_tree.column('Qty', width=40)
#             items_tree.column('Price', width=70)
#             items_tree.column('Cost', width=70)
#             items_tree.column('Profit', width=70)
            
#             total_sale_profit = 0
#             if sale_items:
#                 for item in sale_items:
#                     company = self.safe_get(item, 6, 'Unknown')
#                     product_type = self.safe_get(item, 7, 'Unknown')
#                     quantity = self.safe_get(item, 3, 0)
#                     unit_price = self.safe_get(item, 4, 0)
#                     historical_purchase_price = self.safe_get(item, 6, 0)
#                     product_id = self.safe_get(item, 2)
                    
#                     # ✅ FIXED: Use current product price if historical is 0
#                     if historical_purchase_price == 0:
#                         # Get current purchase price from products table
#                         product = self.product_service.get_product_by_id(product_id)
#                         if product and len(product) >= 7:
#                             current_purchase_price = self.safe_get(product, 6, 0)
#                             cost_price_val = float(current_purchase_price) if current_purchase_price else 0
#                             display_cost = current_purchase_price
#                         else:
#                             cost_price_val = 0
#                             display_cost = 0
#                     else:
#                         cost_price_val = float(historical_purchase_price) if historical_purchase_price else 0
#                         display_cost = historical_purchase_price
                    
#                     try:
#                         sale_price_val = float(unit_price) if unit_price else 0
#                         qty_val = int(quantity) if quantity else 0
                        
#                         item_profit = (sale_price_val - cost_price_val) * qty_val
#                         total_sale_profit += item_profit
#                     except (ValueError, TypeError):
#                         item_profit = 0
                    
#                     product_text = f"{company} - {product_type}"[:25] + ('...' if len(f"{company} - {product_type}") > 25 else '')
#                     items_tree.insert('', 'end', values=(
#                         product_text, quantity, f"₨{float(unit_price):,.0f}", 
#                         f"₨{float(display_cost):,.0f}", f"₨{item_profit:,.0f}"
#                     ))
#             else:
#                 items_tree.insert('', 'end', values=("No items", "", "", "", ""))
                
#             items_tree.pack(fill=tk.BOTH, expand=True)
            
#             if sale_details:
#                 totals_frame = tk.Frame(details_frame, bg='white')
#                 totals_frame.pack(fill=tk.X, pady=8)
                
#                 subtotal = self.safe_get(sale_details, 2, 0)
#                 discount = self.safe_get(sale_details, 3, 0)
#                 final_amount = self.safe_get(sale_details, 4, 0)
                
#                 profit_percentage = (total_sale_profit / float(final_amount)) * 100 if float(final_amount) > 0 else 0
                
#                 tk.Label(totals_frame, text=f"Subtotal: ₨{float(subtotal):,.0f}", font=('Segoe UI', 10),
#                         fg=self.colors['text_primary'], bg='white').pack(anchor='e')
#                 tk.Label(totals_frame, text=f"Discount: -₨{float(discount):,.0f}", font=('Segoe UI', 10),
#                         fg=self.colors['danger'], bg='white').pack(anchor='e')
#                 tk.Label(totals_frame, text=f"Final Amount: ₨{float(final_amount):,.0f}", font=('Segoe UI', 11, 'bold'),
#                         fg=self.colors['primary'], bg='white').pack(anchor='e', pady=(2, 0))
                
#                 profit_frame = tk.Frame(details_frame, bg='white')
#                 profit_frame.pack(fill=tk.X, pady=(5, 0))
                
#                 tk.Label(profit_frame, text=f"Total Profit: ₨{total_sale_profit:,.0f}", font=('Segoe UI', 11, 'bold'),
#                         fg=self.colors['profit_green'], bg='white').pack(anchor='e')
#                 tk.Label(profit_frame, text=f"Profit Margin: {profit_percentage:.1f}%", font=('Segoe UI', 9),
#                         fg=self.colors['text_secondary'], bg='white').pack(anchor='e')
                
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to load sale details: {str(e)}")

