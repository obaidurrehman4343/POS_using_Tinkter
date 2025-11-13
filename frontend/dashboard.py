# import tkinter as tk
# from tkinter import ttk
# from backend.sale_service import SaleService
# from backend.stock_service import StockService
# from backend.product_service import ProductService
# from datetime import datetime, timedelta

# class Dashboard:
#     def __init__(self, parent):
#         self.parent = parent
#         self.sale_service = SaleService()
#         self.stock_service = StockService()
#         self.product_service = ProductService()
#         self.setup_ui()
#         self.load_dashboard_data()
        
#     def setup_ui(self):
#         # Main container with professional background
#         main_frame = tk.Frame(self.parent, bg='#f8f9fa')
#         main_frame.pack(fill=tk.BOTH, expand=True)
        
#         # Header Section - Professional Business Style
#         header_frame = tk.Frame(main_frame, bg='#ffffff', height=80)
#         header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
#         header_frame.pack_propagate(False)
        
#         # Company branding
#         brand_frame = tk.Frame(header_frame, bg='#ffffff')
#         brand_frame.pack(side=tk.LEFT, padx=20)
        
#         tk.Label(
#             brand_frame,
#             text="AWAN HARDWARE",
#             font=('Arial', 20, 'bold'),
#             fg='#2c3e50',
#             bg='#ffffff'
#         ).pack(anchor='w')
        
#         tk.Label(
#             brand_frame,
#             text="Business Intelligence Dashboard",
#             font=('Arial', 11),
#             fg='#7f8c8d',
#             bg='#ffffff'
#         ).pack(anchor='w')
        
#         # Current date and time - Professional placement
#         time_frame = tk.Frame(header_frame, bg='#ffffff')
#         time_frame.pack(side=tk.RIGHT, padx=20)
        
#         self.time_label = tk.Label(
#             time_frame,
#             text="",
#             font=('Arial', 11, 'bold'),
#             fg='#3498db',
#             bg='#ffffff'
#         )
#         self.time_label.pack(anchor='e')
        
#         self.date_label = tk.Label(
#             time_frame,
#             text="",
#             font=('Arial', 10),
#             fg='#7f8c8d',
#             bg='#ffffff'
#         )
#         self.date_label.pack(anchor='e')
        
#         self.update_time()
        
#         # 🔥 KPI METRICS - Top Row (Business KPIs)
#         kpi_frame = tk.Frame(main_frame, bg='#f8f9fa')
#         kpi_frame.pack(fill=tk.X, padx=20, pady=10)
        
#         # Key Performance Indicators
#         kpis = [
#             {
#                 "title": "Daily Revenue",
#                 "value": "₨0",
#                 "change": "+0%",
#                 "icon": "💰",
#                 "color": "#27ae60",
#                 "bg_color": "#d5f4e6"
#             },
#             {
#                 "title": "Total Inventory",
#                 "value": "0",
#                 "change": "Items",
#                 "icon": "📦",
#                 "color": "#3498db",
#                 "bg_color": "#d6eaf8"
#             },
#             {
#                 "title": "Stock Alerts",
#                 "value": "0",
#                 "change": "Needs Attention",
#                 "icon": "⚠️",
#                 "color": "#e74c3c",
#                 "bg_color": "#fadbd8"
#             },
#             {
#                 "title": "Inventory Value",
#                 "value": "₨0",
#                 "change": "Total Assets",
#                 "icon": "💎",
#                 "color": "#9b59b6",
#                 "bg_color": "#e8daef"
#             }
#         ]
        
#         self.kpi_cards = {}
#         for i, kpi in enumerate(kpis):
#             card = self.create_kpi_card(kpi_frame, kpi, i)
#             card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
#             self.kpi_cards[kpi["title"]] = card
        
#         # 📊 MAIN DASHBOARD GRID - Professional 2-column layout
#         dashboard_frame = tk.Frame(main_frame, bg='#f8f9fa')
#         dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
#         # Left Column - Financial Performance
#         left_column = tk.Frame(dashboard_frame, bg='#f8f9fa')
#         left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
#         # Right Column - Inventory & Operations
#         right_column = tk.Frame(dashboard_frame, bg='#f8f9fa')
#         right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
#         # 🎯 LEFT COLUMN - Financial Metrics
        
#         # Sales Performance Card
#         sales_card = self.create_dashboard_card(left_column, "Sales Performance", "#e74c3c")
#         sales_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
#         sales_content = tk.Frame(sales_card, bg='white')
#         sales_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
#         # Sales metrics in a clean table format
#         self.sales_metrics = {
#             "Today's Revenue": {"value": "₨0", "trend": "↗️"},
#             "Weekly Total": {"value": "₨0", "trend": "↗️"},
#             "Monthly Total": {"value": "₨0", "trend": "↗️"},
#             "YTD Revenue": {"value": "₨0", "trend": "↗️"},
#             "Avg. Transaction": {"value": "₨0", "trend": "→"},
#             "Total Transactions": {"value": "0", "trend": "↗️"}
#         }
        
#         for metric, data in self.sales_metrics.items():
#             metric_row = tk.Frame(sales_content, bg='white')
#             metric_row.pack(fill=tk.X, pady=8)
            
#             tk.Label(
#                 metric_row,
#                 text=metric,
#                 font=('Arial', 10),
#                 fg='#2c3e50',
#                 bg='white',
#                 anchor='w'
#             ).pack(side=tk.LEFT)
            
#             value_frame = tk.Frame(metric_row, bg='white')
#             value_frame.pack(side=tk.RIGHT)
            
#             trend_label = tk.Label(
#                 value_frame,
#                 text=data["trend"],
#                 font=('Arial', 10),
#                 bg='white'
#             )
#             trend_label.pack(side=tk.LEFT, padx=(0, 5))
            
#             value_label = tk.Label(
#                 value_frame,
#                 text=data["value"],
#                 font=('Arial', 10, 'bold'),
#                 fg='#2c3e50',
#                 bg='white'
#             )
#             value_label.pack(side=tk.LEFT)
#             self.sales_metrics[metric] = {"value_label": value_label, "trend_label": trend_label}
        
#         # Recent Activity Card
#         activity_card = self.create_dashboard_card(left_column, "Recent Activity", "#3498db")
#         activity_card.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
#         activity_content = tk.Frame(activity_card, bg='white')
#         activity_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
#         # Recent transactions table
#         columns = ('Time', 'Transaction', 'Amount')
#         self.activity_tree = ttk.Treeview(activity_content, columns=columns, show='headings', height=6)
        
#         self.activity_tree.heading('Time', text='Time')
#         self.activity_tree.heading('Transaction', text='Transaction')
#         self.activity_tree.heading('Amount', text='Amount')
        
#         self.activity_tree.column('Time', width=80)
#         self.activity_tree.column('Transaction', width=120)
#         self.activity_tree.column('Amount', width=80)
        
#         self.activity_tree.pack(fill=tk.BOTH, expand=True)
        
#         # 🎯 RIGHT COLUMN - Inventory & Operations
        
#         # Inventory Overview Card
#         inventory_card = self.create_dashboard_card(right_column, "Inventory Overview", "#27ae60")
#         inventory_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
#         inventory_content = tk.Frame(inventory_card, bg='white')
#         inventory_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
#         self.inventory_metrics = {
#             "Total Products": {"value": "0", "status": "📊"},
#             "Active Categories": {"value": "0", "status": "📁"},
#             "Out of Stock": {"value": "0", "status": "❌"},
#             "Low Stock Items": {"value": "0", "status": "🟡"},
#             "Total Inventory Value": {"value": "₨0", "status": "💎"},
#             "Stock Turnover": {"value": "0", "status": "🔄"}
#         }
        
#         for metric, data in self.inventory_metrics.items():
#             metric_row = tk.Frame(inventory_content, bg='white')
#             metric_row.pack(fill=tk.X, pady=8)
            
#             status_label = tk.Label(
#                 metric_row,
#                 text=data["status"],
#                 font=('Arial', 12),
#                 bg='white'
#             )
#             status_label.pack(side=tk.LEFT, padx=(0, 10))
            
#             tk.Label(
#                 metric_row,
#                 text=metric,
#                 font=('Arial', 10),
#                 fg='#2c3e50',
#                 bg='white',
#                 anchor='w'
#             ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
#             value_label = tk.Label(
#                 metric_row,
#                 text=data["value"],
#                 font=('Arial', 10, 'bold'),
#                 fg='#2c3e50',
#                 bg='white'
#             )
#             value_label.pack(side=tk.RIGHT)
#             self.inventory_metrics[metric] = {"value_label": value_label, "status_label": status_label}
        
#         # Quick Actions Card
#         actions_card = self.create_dashboard_card(right_column, "Quick Actions", "#f39c12")
#         actions_card.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
#         actions_content = tk.Frame(actions_card, bg='white')
#         actions_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
#         # Professional action buttons
#         actions = [
#             ("📊 Generate Report", "#3498db", self.generate_report),
#             ("💰 New Sale", "#27ae60", self.new_sale),
#             ("📦 Manage Inventory", "#e67e22", self.manage_inventory),
#             ("⚠️ View Alerts", "#e74c3c", self.view_alerts)
#         ]
        
#         for action, color, command in actions:
#             btn = tk.Button(
#                 actions_content,
#                 text=action,
#                 font=('Arial', 10, 'bold'),
#                 bg=color,
#                 fg='white',
#                 relief='flat',
#                 height=2,
#                 cursor='hand2',
#                 command=command
#             )
#             btn.pack(fill=tk.X, pady=5)
    
#     def create_kpi_card(self, parent, kpi_data, index):
#         """Create professional KPI card"""
#         card = tk.Frame(
#             parent,
#             bg='white',
#             relief='flat',
#             bd=1,
#             height=120
#         )
#         card.pack_propagate(False)
        
#         # Card content with professional spacing
#         content_frame = tk.Frame(card, bg=kpi_data["bg_color"])
#         content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
#         # Top row: Icon and Title
#         top_frame = tk.Frame(content_frame, bg=kpi_data["bg_color"])
#         top_frame.pack(fill=tk.X, pady=(0, 10))
        
#         tk.Label(
#             top_frame,
#             text=kpi_data["icon"],
#             font=('Arial', 16),
#             bg=kpi_data["bg_color"]
#         ).pack(side=tk.LEFT)
        
#         tk.Label(
#             top_frame,
#             text=kpi_data["title"],
#             font=('Arial', 11, 'bold'),
#             bg=kpi_data["bg_color"],
#             fg='#2c3e50'
#         ).pack(side=tk.LEFT, padx=(8, 0))
        
#         # Middle: Main Value
#         value_label = tk.Label(
#             content_frame,
#             text=kpi_data["value"],
#             font=('Arial', 18, 'bold'),
#             bg=kpi_data["bg_color"],
#             fg=kpi_data["color"]
#         )
#         value_label.pack(anchor='w', pady=(0, 5))
        
#         # Bottom: Change/Status
#         change_label = tk.Label(
#             content_frame,
#             text=kpi_data["change"],
#             font=('Arial', 10),
#             bg=kpi_data["bg_color"],
#             fg='#7f8c8d'
#         )
#         change_label.pack(anchor='w')
        
#         # Store references for updates
#         if kpi_data["title"] == "Daily Revenue":
#             self.daily_revenue_label = value_label
#         elif kpi_data["title"] == "Total Inventory":
#             self.total_inventory_label = value_label
#         elif kpi_data["title"] == "Stock Alerts":
#             self.stock_alerts_label = value_label
#         elif kpi_data["title"] == "Inventory Value":
#             self.inventory_value_label = value_label
        
#         return card
    
#     def create_dashboard_card(self, parent, title, color):
#         """Create professional dashboard card"""
#         card = tk.Frame(
#             parent,
#             bg='white',
#             relief='flat',
#             bd=1
#         )
        
#         # Card header with accent color
#         header = tk.Frame(card, bg=color, height=5)
#         header.pack(fill=tk.X)
        
#         # Title frame
#         title_frame = tk.Frame(card, bg='white', height=40)
#         title_frame.pack(fill=tk.X)
#         title_frame.pack_propagate(False)
        
#         tk.Label(
#             title_frame,
#             text=title,
#             font=('Arial', 12, 'bold'),
#             fg='#2c3e50',
#             bg='white'
#         ).pack(anchor='w', padx=15, pady=10)
        
#         return card
    
#     def update_time(self):
#         """Update current date and time with error handling"""
#         try:
#             if hasattr(self, 'time_label') and self.time_label.winfo_exists():
#                 current_time = datetime.now().strftime("%I:%M:%S %p")
#                 current_date = datetime.now().strftime("%B %d, %Y")
                
#                 self.time_label.config(text=f"🕒 {current_time}")
#                 self.date_label.config(text=current_date)
#                 self.parent.after(1000, self.update_time)
#         except tk.TclError:
#             # Widget destroyed, stop updating
#             pass
    
#     def load_dashboard_data(self):
#         """Load all dashboard data"""
#         try:
#             # Sales data
#             sales_summary = self.sale_service.get_sales_summary()
            
#             # Update KPI cards
#             self.daily_revenue_label.config(text=f"₨{sales_summary['today_revenue']:,.0f}")
            
#             # Inventory data
#             stock_summary = self.stock_service.get_stock_summary()
#             self.total_inventory_label.config(text=str(stock_summary['total_products']))
#             self.stock_alerts_label.config(text=str(stock_summary['low_stock_count']))
#             self.inventory_value_label.config(text=f"₨{stock_summary['total_value']:,.0f}")
            
#             # Update sales metrics
#             self.update_sales_metrics(sales_summary)
            
#             # Update inventory metrics
#             self.update_inventory_metrics(stock_summary)
            
#             # Load recent activity
#             self.load_recent_activity()
            
#         except Exception as e:
#             print(f"Dashboard data loading error: {e}")
    
#     def update_sales_metrics(self, sales_summary):
#         """Update sales performance metrics"""
#         try:
#             # Calculate additional metrics
#             weekly_revenue = sales_summary['total_revenue'] * 0.25  # Simplified
#             monthly_revenue = sales_summary['total_revenue'] * 0.6  # Simplified
#             avg_transaction = sales_summary['today_revenue'] / max(sales_summary['total_sales'], 1)
            
#             metrics_data = {
#                 "Today's Revenue": f"₨{sales_summary['today_revenue']:,.0f}",
#                 "Weekly Total": f"₨{weekly_revenue:,.0f}",
#                 "Monthly Total": f"₨{monthly_revenue:,.0f}",
#                 "YTD Revenue": f"₨{sales_summary['total_revenue']:,.0f}",
#                 "Avg. Transaction": f"₨{avg_transaction:,.0f}",
#                 "Total Transactions": str(sales_summary['total_sales'])
#             }
            
#             for metric, value in metrics_data.items():
#                 if metric in self.sales_metrics:
#                     self.sales_metrics[metric]["value_label"].config(text=value)
                    
#         except Exception as e:
#             print(f"Sales metrics update error: {e}")
    
#     def update_inventory_metrics(self, stock_summary):
#         """Update inventory metrics"""
#         try:
#             metrics_data = {
#                 "Total Products": str(stock_summary['total_products']),
#                 "Active Categories": str(stock_summary['total_categories']),
#                 "Out of Stock": str(stock_summary['out_of_stock_count']),
#                 "Low Stock Items": str(stock_summary['low_stock_count']),
#                 "Total Inventory Value": f"₨{stock_summary['total_value']:,.0f}",
#                 "Stock Turnover": "2.5"  # Placeholder
#             }
            
#             for metric, value in metrics_data.items():
#                 if metric in self.inventory_metrics:
#                     self.inventory_metrics[metric]["value_label"].config(text=value)
                    
#         except Exception as e:
#             print(f"Inventory metrics update error: {e}")
    
#     def load_recent_activity(self):
#         """Load recent sales activity"""
#         try:
#             # Clear existing data
#             for item in self.activity_tree.get_children():
#                 self.activity_tree.delete(item)
            
#             sales = self.sale_service.get_sales_report()[:6]  # Last 6 sales
            
#             for sale in sales:
#                 if len(sale) >= 7:
#                     sale_id = sale[0]
#                     amount = sale[4] if len(sale) > 4 else 0
#                     date_str = sale[6] if len(sale) > 6 else ''
                    
#                     # Format time
#                     try:
#                         if date_str:
#                             sale_time = date_str[11:16] if len(date_str) > 16 else 'N/A'
#                         else:
#                             sale_time = 'N/A'
#                     except:
#                         sale_time = 'N/A'
                    
#                     self.activity_tree.insert('', 'end', values=(
#                         sale_time,
#                         f"Sale #{sale_id}",
#                         f"₨{float(amount):,.0f}"
#                     ))
                    
#         except Exception as e:
#             print(f"Recent activity loading error: {e}")
    
#     # Action methods
#     def generate_report(self):
#         """Generate business report"""
#         from tkinter import messagebox
#         messagebox.showinfo("Report", "Business report generation feature will be implemented here.")
    
#     def new_sale(self):
#         """Start new sale"""
#         from tkinter import messagebox
#         messagebox.showinfo("New Sale", "Redirecting to Point of Sale system...")
    
#     def manage_inventory(self):
#         """Manage inventory"""
#         from tkinter import messagebox
#         messagebox.showinfo("Inventory", "Redirecting to Inventory Management...")
    
#     def view_alerts(self):
#         """View stock alerts"""
#         from tkinter import messagebox
#         messagebox.showinfo("Alerts", "Showing stock alerts and notifications...")
import tkinter as tk
from tkinter import ttk
from backend.sale_service import SaleService
from backend.stock_service import StockService
from backend.product_service import ProductService
from datetime import datetime, timedelta

class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        self.sale_service = SaleService()
        self.stock_service = StockService()
        self.product_service = ProductService()
        self.setup_ui()
        self.load_dashboard_data()
        
    def setup_ui(self):
        # Main container with professional background
        main_frame = tk.Frame(self.parent, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header Section
        header_frame = tk.Frame(main_frame, bg='#ffffff', height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Company branding
        brand_frame = tk.Frame(header_frame, bg='#ffffff')
        brand_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            brand_frame,
            text="AWAN HARDWARE",
            font=('Arial', 20, 'bold'),
            fg='#2c3e50',
            bg='#ffffff'
        ).pack(anchor='w')
        
        tk.Label(
            brand_frame,
            text="Business Intelligence Dashboard",
            font=('Arial', 11),
            fg='#7f8c8d',
            bg='#ffffff'
        ).pack(anchor='w')
        
        # Current date and time
        time_frame = tk.Frame(header_frame, bg='#ffffff')
        time_frame.pack(side=tk.RIGHT, padx=20)
        
        self.date_label = tk.Label(
            time_frame,
            text="",
            font=('Arial', 11, 'bold'),
            fg='#3498db',
            bg='#ffffff'
        )
        self.date_label.pack(anchor='e')
        
        # 🔥 KPI METRICS - Top Row
        kpi_frame = tk.Frame(main_frame, bg='#f8f9fa')
        kpi_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Key Performance Indicators - FIXED REVENUE DISPLAY
        kpis = [
            {
                "title": "TODAY'S REVENUE",
                "value": "₨0",
                "subtitle": "Sales Today",
                "icon": "💰",
                "color": "#27ae60",
                "bg_color": "#d5f4e6"
            },
            {
                "title": "TOTAL REVENUE",  # CHANGED FROM INVENTORY
                "value": "₨0",
                "subtitle": "All Time Sales",
                "icon": "📈",
                "color": "#3498db", 
                "bg_color": "#d6eaf8"
            },
            {
                "title": "TOTAL INVENTORY",
                "value": "0",
                "subtitle": "Products",
                "icon": "📦",
                "color": "#e67e22",
                "bg_color": "#fdebd0"
            },
            {
                "title": "STOCK ALERTS",
                "value": "0",
                "subtitle": "Needs Attention", 
                "icon": "⚠️",
                "color": "#e74c3c",
                "bg_color": "#fadbd8"
            }
        ]
        
        self.kpi_cards = {}
        for kpi in kpis:
            card = self.create_kpi_card(kpi_frame, kpi)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            self.kpi_cards[kpi["title"]] = card
        
        # 📊 MAIN DASHBOARD GRID
        dashboard_frame = tk.Frame(main_frame, bg='#f8f9fa')
        dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left Column - Financial Performance
        left_column = tk.Frame(dashboard_frame, bg='#f8f9fa')
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right Column - Inventory & Operations  
        right_column = tk.Frame(dashboard_frame, bg='#f8f9fa')
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # 🎯 LEFT COLUMN - Financial Metrics
        
        # Sales Performance Card
        sales_card = self.create_dashboard_card(left_column, "💰 SALES PERFORMANCE", "#e74c3c")
        sales_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        sales_content = tk.Frame(sales_card, bg='white')
        sales_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Sales metrics - FOCUS ON REVENUE
        self.sales_metrics = {
            "Today's Revenue": "₨0",
            "This Week": "₨0", 
            "This Month": "₨0",
            "Total Revenue": "₨0",
            "Total Transactions": "0",
            "Avg. Sale Value": "₨0"
        }
        
        for metric, value in self.sales_metrics.items():
            metric_row = tk.Frame(sales_content, bg='white')
            metric_row.pack(fill=tk.X, pady=8)
            
            tk.Label(
                metric_row,
                text=metric,
                font=('Arial', 10),
                fg='#2c3e50',
                bg='white',
                anchor='w'
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            value_label = tk.Label(
                metric_row,
                text=value,
                font=('Arial', 10, 'bold'),
                fg='#2c3e50',
                bg='white'
            )
            value_label.pack(side=tk.RIGHT)
            self.sales_metrics[metric] = value_label
        
        # Recent Sales Card
        recent_card = self.create_dashboard_card(left_column, "🔄 RECENT TRANSACTIONS", "#3498db")
        recent_card.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        recent_content = tk.Frame(recent_card, bg='white')
        recent_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Recent transactions
        self.recent_text = tk.Text(
            recent_content,
            height=6,
            font=('Arial', 9),
            bg='#f8f9fa', 
            fg='#2c3e50',
            relief='flat',
            wrap=tk.WORD
        )
        self.recent_text.pack(fill=tk.BOTH, expand=True)
        self.recent_text.insert('1.0', "Loading recent transactions...")
        self.recent_text.config(state='disabled')
        
        # 🎯 RIGHT COLUMN - Inventory & Operations
        
        # Inventory Overview Card
        inventory_card = self.create_dashboard_card(right_column, "📦 INVENTORY OVERVIEW", "#27ae60")
        inventory_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        inventory_content = tk.Frame(inventory_card, bg='white')
        inventory_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.inventory_metrics = {
            "Total Products": "0",
            "Product Categories": "0", 
            "Out of Stock": "0",
            "Low Stock (<5)": "0",
            "Total Stock Value": "₨0",
            "Inventory Health": "Good"
        }
        
        for metric, value in self.inventory_metrics.items():
            metric_row = tk.Frame(inventory_content, bg='white')
            metric_row.pack(fill=tk.X, pady=8)
            
            tk.Label(
                metric_row,
                text=metric,
                font=('Arial', 10),
                fg='#2c3e50', 
                bg='white',
                anchor='w'
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            value_label = tk.Label(
                metric_row,
                text=value,
                font=('Arial', 10, 'bold'),
                fg='#2c3e50',
                bg='white'
            )
            value_label.pack(side=tk.RIGHT)
            self.inventory_metrics[metric] = value_label
        
        # Quick Actions Card
        actions_card = self.create_dashboard_card(right_column, "⚡ QUICK ACTIONS", "#f39c12")
        actions_card.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        actions_content = tk.Frame(actions_card, bg='white')
        actions_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Action buttons
        actions = [
            ("💰 New Sale", "#27ae60", self.new_sale),
            ("📦 Add Product", "#3498db", self.add_product),
            ("📊 View Reports", "#9b59b6", self.view_reports),
            ("⚠️ Stock Alerts", "#e74c3c", self.stock_alerts)
        ]
        
        for action, color, command in actions:
            btn = tk.Button(
                actions_content,
                text=action,
                font=('Arial', 10, 'bold'),
                bg=color,
                fg='white',
                relief='flat',
                height=2,
                cursor='hand2',
                command=command
            )
            btn.pack(fill=tk.X, pady=5)
    
    def create_kpi_card(self, parent, kpi_data):
        """Create KPI card"""
        card = tk.Frame(
            parent,
            bg='white',
            relief='flat',
            bd=1,
            height=120
        )
        card.pack_propagate(False)
        
        content_frame = tk.Frame(card, bg=kpi_data["bg_color"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Icon and title
        icon_frame = tk.Frame(content_frame, bg=kpi_data["bg_color"])
        icon_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            icon_frame,
            text=kpi_data["icon"],
            font=('Arial', 16),
            bg=kpi_data["bg_color"]
        ).pack(side=tk.LEFT)
        
        tk.Label(
            icon_frame,
            text=kpi_data["title"],
            font=('Arial', 11, 'bold'),
            bg=kpi_data["bg_color"],
            fg='#2c3e50'
        ).pack(side=tk.LEFT, padx=(8, 0))
        
        # Main value
        value_label = tk.Label(
            content_frame,
            text=kpi_data["value"],
            font=('Arial', 18, 'bold'),
            bg=kpi_data["bg_color"],
            fg=kpi_data["color"]
        )
        value_label.pack(anchor='w', pady=(0, 5))
        
        # Subtitle
        tk.Label(
            content_frame,
            text=kpi_data["subtitle"],
            font=('Arial', 10),
            bg=kpi_data["bg_color"],
            fg='#7f8c8d'
        ).pack(anchor='w')
        
        # Store references
        if kpi_data["title"] == "TODAY'S REVENUE":
            self.today_revenue_kpi = value_label
        elif kpi_data["title"] == "TOTAL REVENUE":
            self.total_revenue_kpi = value_label
        elif kpi_data["title"] == "TOTAL INVENTORY":
            self.total_inventory_kpi = value_label
        elif kpi_data["title"] == "STOCK ALERTS":
            self.stock_alerts_kpi = value_label
        
        return card
    
    def create_dashboard_card(self, parent, title, color):
        """Create dashboard card"""
        card = tk.Frame(
            parent,
            bg='white',
            relief='flat',
            bd=1
        )
        
        # Card header
        header = tk.Frame(card, bg=color, height=5)
        header.pack(fill=tk.X)
        
        title_frame = tk.Frame(card, bg='white', height=40)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text=title,
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', padx=15, pady=10)
        
        return card
    
    def update_time(self):
        """Update date display"""
        try:
            if hasattr(self, 'date_label') and self.date_label.winfo_exists():
                current_date = datetime.now().strftime("%B %d, %Y • %I:%M %p")
                self.date_label.config(text=current_date)
                self.parent.after(30000, self.update_time)  # Update every 30 seconds
        except tk.TclError:
            pass
    
    def load_dashboard_data(self):
        """Load dashboard data with proper error handling"""
        try:
            # Update date first
            self.update_time()
            
            # Get sales summary
            sales_data = self.sale_service.get_sales_summary()
            
            # Get inventory summary  
            inventory_data = self.stock_service.get_stock_summary()
            
            # Update KPI cards with ACTUAL REVENUE DATA
            self.update_kpi_cards(sales_data, inventory_data)
            
            # Update detailed metrics
            self.update_sales_metrics(sales_data)
            self.update_inventory_metrics(inventory_data)
            
            # Load recent transactions
            self.load_recent_transactions()
            
        except Exception as e:
            print(f"Dashboard error: {e}")
            # Set default values if data loading fails
            self.set_default_values()
    
    def update_kpi_cards(self, sales_data, inventory_data):
        """Update KPI cards with actual revenue data"""
        try:
            # Today's Revenue
            today_revenue = getattr(sales_data, 'today_revenue', 0) if hasattr(sales_data, 'today_revenue') else sales_data.get('today_revenue', 0)
            self.today_revenue_kpi.config(text=f"₨{float(today_revenue):,.0f}")
            
            # Total Revenue (Sum of all sales final_amount)
            total_revenue = getattr(sales_data, 'total_revenue', 0) if hasattr(sales_data, 'total_revenue') else sales_data.get('total_revenue', 0)
            self.total_revenue_kpi.config(text=f"₨{float(total_revenue):,.0f}")
            
            # Total Inventory
            total_products = getattr(inventory_data, 'total_products', 0) if hasattr(inventory_data, 'total_products') else inventory_data.get('total_products', 0)
            self.total_inventory_kpi.config(text=str(total_products))
            
            # Stock Alerts
            low_stock = getattr(inventory_data, 'low_stock_count', 0) if hasattr(inventory_data, 'low_stock_count') else inventory_data.get('low_stock_count', 0)
            self.stock_alerts_kpi.config(text=str(low_stock))
            
        except Exception as e:
            print(f"KPI update error: {e}")
    
    def update_sales_metrics(self, sales_data):
        """Update sales performance metrics"""
        try:
            # Extract values safely
            today_revenue = getattr(sales_data, 'today_revenue', 0) if hasattr(sales_data, 'today_revenue') else sales_data.get('today_revenue', 0)
            total_revenue = getattr(sales_data, 'total_revenue', 0) if hasattr(sales_data, 'total_revenue') else sales_data.get('total_revenue', 0)
            total_sales = getattr(sales_data, 'total_sales', 0) if hasattr(sales_data, 'total_sales') else sales_data.get('total_sales', 0)
            
            # Calculate additional metrics
            avg_sale = today_revenue / max(total_sales, 1) if today_revenue > 0 else 0
            
            # Update metrics
            self.sales_metrics["Today's Revenue"].config(text=f"₨{float(today_revenue):,.0f}")
            self.sales_metrics["Total Revenue"].config(text=f"₨{float(total_revenue):,.0f}")
            self.sales_metrics["Total Transactions"].config(text=str(total_sales))
            self.sales_metrics["Avg. Sale Value"].config(text=f"₨{avg_sale:,.0f}")
            
            # Placeholder for weekly/monthly (you can implement proper calculations)
            self.sales_metrics["This Week"].config(text=f"₨{float(total_revenue * 0.3):,.0f}")
            self.sales_metrics["This Month"].config(text=f"₨{float(total_revenue * 0.7):,.0f}")
            
        except Exception as e:
            print(f"Sales metrics error: {e}")
    
    def update_inventory_metrics(self, inventory_data):
        """Update inventory metrics"""
        try:
            total_products = getattr(inventory_data, 'total_products', 0) if hasattr(inventory_data, 'total_products') else inventory_data.get('total_products', 0)
            total_categories = getattr(inventory_data, 'total_categories', 0) if hasattr(inventory_data, 'total_categories') else inventory_data.get('total_categories', 0)
            out_of_stock = getattr(inventory_data, 'out_of_stock_count', 0) if hasattr(inventory_data, 'out_of_stock_count') else inventory_data.get('out_of_stock_count', 0)
            low_stock = getattr(inventory_data, 'low_stock_count', 0) if hasattr(inventory_data, 'low_stock_count') else inventory_data.get('low_stock_count', 0)
            total_value = getattr(inventory_data, 'total_value', 0) if hasattr(inventory_data, 'total_value') else inventory_data.get('total_value', 0)
            
            # Update metrics
            self.inventory_metrics["Total Products"].config(text=str(total_products))
            self.inventory_metrics["Product Categories"].config(text=str(total_categories))
            self.inventory_metrics["Out of Stock"].config(text=str(out_of_stock))
            self.inventory_metrics["Low Stock (<5)"].config(text=str(low_stock))
            self.inventory_metrics["Total Stock Value"].config(text=f"₨{float(total_value):,.0f}")
            
            # Inventory health
            health = "Good" if low_stock < 10 else "Attention Needed"
            self.inventory_metrics["Inventory Health"].config(text=health)
            
        except Exception as e:
            print(f"Inventory metrics error: {e}")
    
    def load_recent_transactions(self):
        """Load recent sales transactions"""
        try:
            self.recent_text.config(state='normal')
            self.recent_text.delete('1.0', tk.END)
            
            sales = self.sale_service.get_sales_report()[:8]  # Last 8 sales
            
            if not sales:
                self.recent_text.insert(tk.END, "No recent transactions")
            else:
                for sale in sales:
                    if len(sale) >= 5:
                        sale_id = sale[0]
                        amount = sale[4]  # final_amount
                        date_str = sale[6] if len(sale) > 6 else ''  # sale_date
                        
                        # Format display
                        time_display = date_str[11:16] if date_str and len(date_str) > 16 else 'Today'
                        self.recent_text.insert(tk.END, f"• Sale #{sale_id}: ₨{float(amount):,.0f} ({time_display})\n")
            
            self.recent_text.config(state='disabled')
            
        except Exception as e:
            self.recent_text.config(state='normal')
            self.recent_text.delete('1.0', tk.END)
            self.recent_text.insert(tk.END, "Error loading transactions")  # FIXED: Removed extra quote
            self.recent_text.config(state='disabled')
    
    def set_default_values(self):
        """Set default values when data loading fails"""
        try:
            self.today_revenue_kpi.config(text="₨0")
            self.total_revenue_kpi.config(text="₨0")
            self.total_inventory_kpi.config(text="0")
            self.stock_alerts_kpi.config(text="0")
        except:
            pass
    
    # Action methods
    def new_sale(self):
        from tkinter import messagebox
        messagebox.showinfo("New Sale", "Opening Point of Sale...")
    
    def add_product(self):
        from tkinter import messagebox
        messagebox.showinfo("Add Product", "Opening Inventory Management...")
    
    def view_reports(self):
        from tkinter import messagebox
        messagebox.showinfo("Reports", "Opening Reports Dashboard...")
    
    def stock_alerts(self):
        from tkinter import messagebox
        messagebox.showinfo("Stock Alerts", "Showing low stock items...")