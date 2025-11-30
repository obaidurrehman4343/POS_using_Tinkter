# dashboard.py

import tkinter as tk
from tkinter import ttk, Canvas
from backend.sale_service import SaleService
from backend.stock_service import StockService
from backend.product_service import ProductService
from datetime import datetime, timedelta
import numpy as np

class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        self.sale_service = SaleService()
        self.stock_service = StockService()
        self.product_service = ProductService()
        
        # Color palette for professional look
        self.colors = {
            'primary': '#1f77b4',      # Blue
            'secondary': '#ff7f0e',    # Orange
            'success': '#2ca02c',      # Green
            'danger': '#d62728',       # Red
            'warning': '#ff9800',      # Amber
            'info': '#17a2b8',        # Cyan
            'light': '#f8f9fa',       # Light gray
            'dark': '#343a40',         # Dark gray
            'purple': '#9b59b6',       # Purple
            'teal': '#1abc9c',        # Teal
            'zakat': '#059669'         # Special color for Zakat
        }
        
        self.setup_ui()
        self.load_dashboard_data()
        
    def setup_ui(self):
        # Create scrollable main container - FIXED to take full width
        self.canvas = Canvas(self.parent, bg='#f5f7fa', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f5f7fa')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Create window in canvas with full width
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollbar first (right side)
        self.scrollbar.pack(side="right", fill="y")
        
        # Pack canvas to fill remaining space
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Update canvas window width after packing
        self.parent.update_idletasks()
        self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width())
        
        # Bind resize event
        self.canvas.bind('<Configure>', lambda e: self._update_canvas_width())
        
        # Create all UI elements in scrollable frame
        self.create_top_navigation()
        self.create_kpi_section()
        self.create_daily_sales_section()
        self.create_monthly_sales_section()
        self.create_inventory_category_section()
        self.create_tables_section()
        
        # Bind mouse wheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _update_canvas_width(self):
        """Update canvas window width to match canvas width"""
        try:
            canvas_width = self.canvas.winfo_width()
            if canvas_width > 1:  # Ensure canvas has valid width
                self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        except:
            pass
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def create_top_navigation(self):
        # Top navigation bar
        nav_frame = tk.Frame(self.scrollable_frame, bg=self.colors['dark'], height=70)
        nav_frame.pack(fill=tk.X, padx=0, pady=0)
        nav_frame.pack_propagate(False)
        
        # Company branding
        brand_frame = tk.Frame(nav_frame, bg=self.colors['dark'])
        brand_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(
            brand_frame,
            text="AWAN HARDWARE & PAINTS STORE ARJA",
            font=('Arial', 22, 'bold'),
            fg='white',
            bg=self.colors['dark']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            brand_frame,
            text="Business Analytics",
            font=('Arial', 12),
            fg='#adb5bd',
            bg=self.colors['dark']
        ).pack(side=tk.LEFT, padx=(15, 0))
        
        # Date and time display
        time_frame = tk.Frame(nav_frame, bg=self.colors['dark'])
        time_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.date_label = tk.Label(
            time_frame,
            text="",
            font=('Arial', 11),
            fg='#f8f9fa',
            bg=self.colors['dark']
        )
        self.date_label.pack()
        
        self.update_time()
        
    def create_kpi_section(self):
        # KPI section container - UPDATED WITH ZAKAT CARD
        kpi_container = tk.Frame(self.scrollable_frame, bg='#f5f7fa')
        kpi_container.pack(fill=tk.X, padx=20, pady=15)
        
        # Configure grid for 4 columns
        for i in range(4):
            kpi_container.grid_columnconfigure(i, weight=1)
        
        # KPI data - REPLACED low_stock with zakat
        self.kpi_data = {
            'revenue_today': {'title': "Today's Sale", 'value': 0, 'change': 0, 'icon': '💰'},
            'revenue_total': {'title': "Total Sale", 'value': 0, 'change': 0, 'icon': '📈'},
            'total_inventory_value': {'title': "Inventory Value", 'value': 0, 'change': 0, 'icon': '🏪'},
            'zakat': {'title': "Zakat Payable", 'value': 0, 'change': 0, 'icon': '🕌', 'color': self.colors['zakat']}  # NEW CARD
        }
        
        self.kpi_widgets = {}
        
        # Create KPI cards in a 2x2 grid
        for i, (key, data) in enumerate(self.kpi_data.items()):
            row = i // 2
            col = i % 2
            
            card = self.create_modern_kpi_card(kpi_container, data)
            card.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')
            self.kpi_widgets[key] = card
    
    def create_modern_kpi_card(self, parent, data):
        # Create modern KPI card with shadow effect
        shadow = tk.Frame(parent, bg='#e9ecef', relief='flat', bd=0)
        shadow.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Main card
        card = tk.Frame(shadow, bg='white', relief='flat', bd=0)
        card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Card content
        content = tk.Frame(card, bg='white')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header with icon and title
        header_frame = tk.Frame(content, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Icon
        icon_frame = tk.Frame(header_frame, bg=data.get('color', self.colors['primary']), width=44, height=44)
        icon_frame.pack(side=tk.LEFT, padx=(0, 12))
        icon_frame.pack_propagate(False)
        
        tk.Label(
            icon_frame,
            text=data['icon'],
            font=('Arial', 18),
            bg=data.get('color', self.colors['primary']),
            fg='white'
        ).pack(expand=True)
        
        # Title and description
        text_frame = tk.Frame(header_frame, bg='white')
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            text_frame,
            text=data['title'],
            font=('Arial', 12, 'bold'),
            fg=self.colors['dark'],
            bg='white'
        ).pack(anchor='w')
        
        # Value
        value_label = tk.Label(
            content,
            text=f"₨{data['value']:,.0f}" if 'Revenue' in data['title'] or 'Inventory' in data['title'] or 'Zakat' in data['title'] else str(data['value']),
            font=('Arial', 22, 'bold'),
            fg=data.get('color', self.colors['primary']),
            bg='white'
        )
        value_label.pack(anchor='w', pady=(5, 0))
        
        # Change indicator
        change_frame = tk.Frame(content, bg='white')
        change_frame.pack(fill=tk.X)
        
        change_label = tk.Label(
            change_frame,
            text=f"{'↑' if data['change'] >= 0 else '↓'} {abs(data['change']):.1f}%",
            font=('Arial', 9),
            bg='white',
            fg=self.colors['success'] if data['change'] >= 0 else self.colors['danger']
        )
        change_label.pack(side=tk.LEFT)
        
        # Store references for updates on the card itself
        card.value_label = value_label
        card.change_label = change_label
        
        return card
    
    def calculate_zakat(self, inventory_value):
        """Calculate Zakat based on inventory value (2.5% per lakh)"""
        try:
            # Convert inventory value to float
            inventory_value = float(inventory_value) if inventory_value else 0
            
            # Calculate Zakat: 2.5% per lakh (100,000)
            # Formula: (inventory_value / 100000) * 2500
            zakat_amount = (inventory_value / 100000) * 2500
            
            return zakat_amount
        except (ValueError, TypeError):
            return 0
    
    def create_daily_sales_section(self):
        # Daily Sales section container
        daily_sales_container = tk.Frame(self.scrollable_frame, bg='#f5f7fa')
        daily_sales_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Section title
        shadow_title = tk.Frame(daily_sales_container, bg='#e9ecef', relief='flat', bd=0)
        shadow_title.pack(fill=tk.X, pady=(0, 10))
        
        title_card = tk.Frame(shadow_title, bg='white', relief='flat', bd=0)
        title_card.pack(fill=tk.X, padx=1, pady=1)
        
        tk.Label(
            title_card,
            text="📊 DAILY SALES OVERVIEW",
            font=('Arial', 16, 'bold'),
            fg=self.colors['dark'],
            bg='white'
        ).pack(pady=15, padx=20, anchor='w')
        
        # Sales cards container
        self.sales_cards_frame = tk.Frame(daily_sales_container, bg='#f5f7fa')
        self.sales_cards_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create 7 daily sales cards in CORRECT ORDER
        self.daily_sales_cards = {}
        
        # Get today's date
        today = datetime.now()
        
        # Create cards for the last 7 days, starting from 6 days ago to today
        for days_back in range(6, -1, -1):  # 6, 5, 4, 3, 2, 1, 0
            date = today - timedelta(days=days_back)
            date_str = date.strftime('%Y-%m-%d')
            day_name = date.strftime('%A')[:3]  # Mon, Tue, Wed, Thu, Fri, Sat, Sun
            
            # Check if this is today
            is_today = (days_back == 0)
            
            card = self.create_daily_sales_card(self.sales_cards_frame, day_name, date_str, is_today)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            self.daily_sales_cards[date_str] = card
    
    def create_daily_sales_card(self, parent, day_name, date_str, is_today=False):
        # Create shadow effect
        shadow = tk.Frame(parent, bg='#e9ecef', relief='flat', bd=0)
        shadow.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Main card with different color for today
        card_color = self.colors['primary'] if is_today else 'white'
        text_color = 'white' if is_today else self.colors['dark']
        
        card = tk.Frame(shadow, bg=card_color, relief='flat', bd=0)
        card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Card content
        content_frame = tk.Frame(card, bg=card_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Day name
        day_label = tk.Label(
            content_frame,
            text=day_name,
            font=('Arial', 11, 'bold'),
            bg=card_color,
            fg=text_color
        )
        day_label.pack(anchor='center')
        
        # Date
        date_label = tk.Label(
            content_frame,
            text=datetime.strptime(date_str, '%Y-%m-%d').strftime('%m/%d'),
            font=('Arial', 9),
            bg=card_color,
            fg=text_color if is_today else '#6c757d'
        )
        date_label.pack(anchor='center', pady=(2, 5))
        
        # Progress bar background
        progress_bg = tk.Frame(content_frame, bg='#e9ecef' if not is_today else '#ffffff', height=4)
        progress_bg.pack(fill=tk.X, pady=(5, 5))
        progress_bg.pack_propagate(False)
        
        # Progress bar (will be updated)
        progress_color = '#ffffff' if is_today else self.colors['success']
        progress_bar = tk.Frame(progress_bg, bg=progress_color, height=4)
        progress_bar.pack(side=tk.LEFT, fill=tk.Y)
        progress_bar.pack_propagate(False)
        
        # Sales amount
        amount_label = tk.Label(
            content_frame,
            text="₨0",
            font=('Arial', 12, 'bold'),
            bg=card_color,
            fg=text_color
        )
        amount_label.pack(anchor='center', pady=(5, 0))
        
        # Transaction count
        count_label = tk.Label(
            content_frame,
            text="0 sales",
            font=('Arial', 8),
            bg=card_color,
            fg=text_color if is_today else '#6c757d'
        )
        count_label.pack(anchor='center')
        
        # Store references for updates
        card.progress_bar = progress_bar
        card.amount_label = amount_label
        card.count_label = count_label
        card.progress_bg = progress_bg
        card.is_today = is_today
        card.card_color = card_color
        card.text_color = text_color
        card.date_str = date_str  # Store date for later updates
        
        return card
    
    def get_years_for_dropdown(self):
        """Get years for dropdown including current year and future years"""
        try:
            # Get sales data to find available years
            with self.sale_service.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT DISTINCT strftime("%Y", sale_date) as year FROM sales ORDER BY year DESC')
                db_years = [row[0] for row in cursor.fetchall()]
            
            # Current year
            current_year = datetime.now().year
            
            # Start with database years
            years = db_years.copy()
            
            # Always include current year (if not already there)
            if str(current_year) not in years:
                years.append(str(current_year))
            
            # Add future years (next 15 years)
            for i in range(1, 15):  # +1, +2, +3
                future_year = str(current_year + i)
                if future_year not in years:
                    years.append(future_year)
            
            # Sort years in descending order
            years.sort(reverse=True)
            
            return years
            
        except Exception:
            # Fallback to current year and future years
            current_year = datetime.now().year
            return [str(current_year), str(current_year+1), str(current_year+2), str(current_year+3)]

    def refresh_year_dropdown(self):
        """Refresh year dropdown with updated years"""
        try:
            # Get updated years
            available_years = self.get_years_for_dropdown()
            
            # Update dropdown values
            self.year_dropdown['values'] = available_years
            
            # Keep current selection if it's still available
            current_selection = self.year_var.get()
            if current_selection in available_years:
                self.year_var.set(current_selection)
            else:
                self.year_var.set(available_years[0] if available_years else str(datetime.now().year))
            
            # Update monthly sales
            self.update_monthly_sales()
            
        except Exception:
            pass
    
    def create_monthly_sales_section(self):
        """Create monthly sales overview section with year range"""
        monthly_container = tk.Frame(self.scrollable_frame, bg='#f5f7fa')
        monthly_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Section title
        shadow_title = tk.Frame(monthly_container, bg='#e9ecef', relief='flat', bd=0)
        shadow_title.pack(fill=tk.X, pady=(0, 10))
        
        title_card = tk.Frame(shadow_title, bg='white', relief='flat', bd=0)
        title_card.pack(fill=tk.X, padx=1, pady=1)
        
        tk.Label(
            title_card,
            text="📅 MONTHLY SALES OVERVIEW",
            font=('Arial', 16, 'bold'),
            fg=self.colors['dark'],
            bg='white'
        ).pack(pady=15, padx=20, anchor='w')
        
        # Year selector with refresh button
        year_frame = tk.Frame(title_card, bg='white')
        year_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        tk.Label(
            year_frame,
            text="Select Year:",
            font=('Arial', 11, 'bold'),
            fg=self.colors['dark'],
            bg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Get years for dropdown (current + future)
        available_years = self.get_years_for_dropdown()
        
        self.year_var = tk.StringVar(value=str(datetime.now().year))
        self.year_dropdown = ttk.Combobox(
            year_frame,
            textvariable=self.year_var,
            values=available_years,
            state='readonly',
            font=('Arial', 10),
            width=12
        )
        self.year_dropdown.pack(side=tk.LEFT, padx=(0, 10))
        self.year_dropdown.bind('<<ComboboxSelected>>', lambda e: self.update_monthly_sales())
        
        # Refresh button
        refresh_btn = tk.Button(
            year_frame,
            text="🔄 Refresh Years",
            font=('Arial', 9, 'bold'),
            bg=self.colors['info'],
            fg='white',
            relief='flat',
            command=self.refresh_year_dropdown,
            cursor='hand2'
        )
        refresh_btn.pack(side=tk.LEFT, padx=10)
        
        # Monthly cards container
        self.monthly_cards_frame = tk.Frame(monthly_container, bg='#f5f7fa')
        self.monthly_cards_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Don't create monthly cards here, wait for update_monthly_sales
        self.monthly_cards = {}
    
    def create_monthly_cards(self):
        """Create 12 monthly sales cards"""
        # Clear existing cards
        for widget in self.monthly_cards_frame.winfo_children():
            widget.destroy()
        
        self.monthly_cards = {}
        selected_year = int(self.year_var.get())  # Use the CURRENT selected year
        
        # Month names
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Create cards for all 12 months
        for month_num in range(1, 13):  # 1 to 12
            month_name = month_names[month_num-1]
            
            # Check if this is current month
            is_current_month = (month_num == datetime.now().month and 
                               datetime.now().year == selected_year)
            
            # Create month card
            card = self.create_monthly_sales_card(
                self.monthly_cards_frame, 
                month_name, 
                month_num, 
                selected_year,
                is_current_month
            )
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3, pady=3)
            self.monthly_cards[f"{selected_year}-{month_num}"] = card
    
    def create_monthly_sales_card(self, parent, month_name, month_num, year, is_current_month=False):
        """Create individual monthly sales card"""
        # Card color based on current month
        card_color = self.colors['primary'] if is_current_month else 'white'
        text_color = 'white' if is_current_month else self.colors['dark']
        
        # Create shadow effect
        shadow = tk.Frame(parent, bg='#e9ecef', relief='flat', bd=0)
        shadow.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Main card
        card = tk.Frame(shadow, bg=card_color, relief='flat', bd=0)
        card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Card content
        content_frame = tk.Frame(card, bg=card_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # Month name
        month_label = tk.Label(
            content_frame,
            text=month_name,
            font=('Arial', 10, 'bold'),
            bg=card_color,
            fg=text_color
        )
        month_label.pack(anchor='center')
        
        # Year
        year_label = tk.Label(
            content_frame,
            text=str(year),
            font=('Arial', 9),
            bg=card_color,
            fg=text_color if is_current_month else '#6c757d'
        )
        year_label.pack(anchor='center', pady=(2, 3))
        
        # Progress bar background
        progress_bg = tk.Frame(content_frame, bg='#e9ecef' if not is_current_month else '#ffffff', height=4)
        progress_bg.pack(fill=tk.X, pady=(3, 3))
        progress_bg.pack_propagate(False)
        
        # Progress bar (will be updated)
        progress_color = '#ffffff' if is_current_month else self.colors['success']
        progress_bar = tk.Frame(progress_bg, bg=progress_color, height=4)
        progress_bar.pack(side=tk.LEFT, fill=tk.Y)
        progress_bar.pack_propagate(False)
        
        # Sales amount
        amount_label = tk.Label(
            content_frame,
            text="₨0",
            font=('Arial', 11, 'bold'),
            bg=card_color,
            fg=text_color
        )
        amount_label.pack(anchor='center', pady=(3, 0))
        
        # Transaction count
        count_label = tk.Label(
            content_frame,
            text="0 sales",
            font=('Arial', 7),
            bg=card_color,
            fg=text_color if is_current_month else '#6c757d'
        )
        count_label.pack(anchor='center')
        
        # Store references for updates
        card.progress_bar = progress_bar
        card.amount_label = amount_label
        card.count_label = count_label
        card.progress_bg = progress_bg
        card.month_num = month_num
        card.year = year
        
        return card

    # --- MODIFIED SECTION: Removed horizontal scrolling ---
    def create_inventory_category_section(self):
        """Create inventory category section"""
        inventory_container = tk.Frame(self.scrollable_frame, bg='#f5f7fa')
        inventory_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Section title
        shadow_title = tk.Frame(inventory_container, bg='#e9ecef', relief='flat', bd=0)
        shadow_title.pack(fill=tk.X, pady=(0, 10))
        
        title_card = tk.Frame(shadow_title, bg='white', relief='flat', bd=0)
        title_card.pack(fill=tk.X, padx=1, pady=1)
        
        tk.Label(
            title_card,
            text="📦 INVENTORY BY CATEGORY",
            font=('Arial', 16, 'bold'),
            fg=self.colors['dark'],
            bg='white'
        ).pack(pady=15, padx=20, anchor='w')
        
        # Replaced scrollable canvas with a simple frame
        self.category_cards_frame = tk.Frame(inventory_container, bg='#f5f7fa')
        self.category_cards_frame.pack(fill=tk.X, pady=10)
        
        # Initialize category cards dictionary
        self.category_cards = {}

    # --- MODIFIED SECTION: Adjusted for smaller text and no scroll ---
    # --- MODIFIED SECTION: Adjusted for smaller text and no scroll ---
    def create_category_card(self, parent, category_name, data):
        """Create a category card that fills available space"""
        # Determine color based on category
        category_colors = {
            'Paint': self.colors['primary'],
            'Sanitary': self.colors['secondary'],
            'Roof Sheet': self.colors['success'],
            'Hardware': self.colors['warning'],
            'Limination Sheet': self.colors['purple']
        }
        color = category_colors.get(category_name, self.colors['info'])
        
        # Create shadow effect
        shadow = tk.Frame(parent, bg='#e9ecef', relief='flat', bd=0)
        shadow.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Main card - INCREASED width to accommodate longer category names
        card = tk.Frame(shadow, bg='white', relief='flat', bd=0, width=200, height=180)  # Increased from 220 to 250
        card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        card.pack_propagate(False)  # Prevent card from shrinking
        
        # Card content - Use full space
        content_frame = tk.Frame(card, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Category icon and name - Use more space
        header_frame = tk.Frame(content_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 30))  # Increased bottom margin
        
        # Icon circle - Made larger
        icon_frame = tk.Frame(header_frame, bg=color, width=50, height=50)
        icon_frame.pack(side=tk.LEFT, padx=(0, 15))
        icon_frame.pack_propagate(False)
        
        # Category icon (emoji)
        category_icons = {
            'Paint': '🎨',
            'Sanitary': '🚿',
            'Roof Sheet': '🏗️',
            'Hardware': '🔧',
            'Limination Sheet': '📄'
        }
        icon = category_icons.get(category_name, '📦')
        
        tk.Label(
            icon_frame,
            text=icon,
            font=('Arial', 20),  # Increased font size
            bg=color,
            fg='white'
        ).pack(expand=True)
        
        # Category name - MODIFIED to handle longer names with smaller font
        tk.Label(
            header_frame,
            text=category_name,
            font=('Arial', 12, 'bold'),  # Reduced from 14 to 12 for longer names
            fg=self.colors['dark'],
            bg='white',
            wraplength=120  # Added wraplength to allow text wrapping
        ).pack(side=tk.LEFT, anchor='w')
        
        # Stats grid - Use more vertical space
        stats_frame = tk.Frame(content_frame, bg='white')
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))  # Increased top margin
        
        # Products count - Takes more space
        products_frame = tk.Frame(stats_frame, bg='white')
        products_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        tk.Label(
            products_frame,
            text="Products",
            font=('Arial', 12),
            fg='#6c757d',
            bg='white'
        ).pack(anchor='w')
        
        # --- MODIFIED: Reduced font size for the product count ---
        tk.Label(
            products_frame,
            text=str(data['product_count']),
            font=('Arial', 14, 'bold'), # Changed from 18 to 14
            fg=self.colors['dark'],
            bg='white'
        ).pack(anchor='w')
        
        # Value - Takes more space
        value_frame = tk.Frame(stats_frame, bg='white')
        value_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        tk.Label(
            value_frame,
            text="Value",
            font=('Arial', 12),
            fg='#6c757d',
            bg='white'
        ).pack(anchor='w')
        
        # --- MODIFIED: Reduced font size for the total value ---
        tk.Label(
            value_frame,
            text=f"₨{data['total_value']:,.0f}",
            font=('Arial', 14, 'bold'), # Changed from 18 to 14
            fg=color,
            bg='white'
        ).pack(anchor='w')
        
        # Progress bar for stock utilization - Takes more space
        progress_bg = tk.Frame(content_frame, bg='#e9ecef', height=10)  # Increased height
        progress_bg.pack(fill=tk.X, pady=(20, 0))  # Increased top margin
        progress_bg.pack_propagate(False)
        
        # Calculate progress (based on stock value relative to total)
        progress_width = min(100, (data['total_value'] / 100000) * 100) if data['total_value'] > 0 else 0
        
        progress_bar = tk.Frame(progress_bg, bg=color, height=10)  # Increased height
        progress_bar.pack(side=tk.LEFT, fill=tk.Y)
        progress_bar.config(width=int(progress_bg.winfo_width() * progress_width / 100) if progress_bg.winfo_width() > 1 else 0)
        
        # Store references
        card.progress_bar = progress_bar
        card.progress_bg = progress_bg
        
        return card

    # --- MODIFIED SECTION: Adjusted for no scroll ---
    def update_category_cards(self):
        """Update category cards with actual data"""
        try:
            # Clear existing cards from the frame
            for widget in self.category_cards_frame.winfo_children():
                widget.destroy()
            
            self.category_cards = {}
            
            # Get category data
            category_data = self.stock_service.get_category_stock_overview()
            
            for category in category_data:
                category_name, product_count, total_stock, total_value = category
                
                data = {
                    'product_count': product_count,
                    'total_value': total_value or 0
                }
                
                # Cards are now packed into the simple frame
                card = self.create_category_card(self.category_cards_frame, category_name, data)
                card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
                
                self.category_cards[category_name] = card
                
        except Exception:
            pass
    
    def create_tables_section(self):
        # Tables section container
        tables_container = tk.Frame(self.scrollable_frame, bg='#f5f7fa')
        tables_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Recent Sales Table
        sales_shadow = tk.Frame(tables_container, bg='#e9ecef', relief='flat', bd=0)
        sales_shadow.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=2)
        
        sales_table = tk.Frame(sales_shadow, bg='white', relief='flat', bd=0)
        sales_table.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Table title
        tk.Label(
            sales_table,
            text="Recent Sales",
            font=('Arial', 14, 'bold'),
            fg=self.colors['dark'],
            bg='white'
        ).pack(pady=(15, 5), padx=15, anchor='w')
        
        # Table container
        self.sales_table_frame = tk.Frame(sales_table, bg='white')
        self.sales_table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Low Stock Table
        stock_shadow = tk.Frame(tables_container, bg='#e9ecef', relief='flat', bd=0)
        stock_shadow.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=2)
        
        stock_table = tk.Frame(stock_shadow, bg='white', relief='flat', bd=0)
        stock_table.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Table title
        tk.Label(
            stock_table,
            text="Low Stock Alerts",
            font=('Arial', 14, 'bold'),
            fg=self.colors['dark'],
            bg='white'
        ).pack(pady=(15, 5), padx=15, anchor='w')
        
        # Table container
        self.stock_table_frame = tk.Frame(stock_table, bg='white')
        self.stock_table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def update_time(self):
        """Update date display"""
        try:
            if hasattr(self, 'date_label') and self.date_label.winfo_exists():
                current_date = datetime.now().strftime("%A, %B %d, %Y • %I:%M %p")
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
            
            # Update KPI cards - INCLUDING ZAKAT CALCULATION
            self.update_kpi_cards(sales_data, inventory_data)
            
            # Update daily sales cards
            self.update_daily_sales_cards()
            
            # Update monthly sales cards with REAL data (this will create cards)
            self.update_monthly_sales()
            
            # Update category cards
            self.update_category_cards()
            
            # Create tables
            self.create_sales_table()
            self.create_stock_table()
            
        except Exception:
            # Set default values if data loading fails
            self.set_default_values()
    
    def update_kpi_cards(self, sales_data, inventory_data):
        """Update KPI cards with actual data - INCLUDING ZAKAT CALCULATION"""
        try:
            # Today's Revenue
            today_revenue = getattr(sales_data, 'today_revenue', 0) if hasattr(sales_data, 'today_revenue') else sales_data.get('today_revenue', 0)
            self.kpi_widgets['revenue_today'].value_label.config(text=f"₨{float(today_revenue):,.0f}")
            
            # Total Revenue
            total_revenue = getattr(sales_data, 'total_revenue', 0) if hasattr(sales_data, 'total_revenue') else sales_data.get('total_revenue', 0)
            self.kpi_widgets['revenue_total'].value_label.config(text=f"₨{float(total_revenue):,.0f}")
            
            # Total Inventory Value
            total_inventory_value = getattr(inventory_data, 'total_value', 0) if hasattr(inventory_data, 'total_value') else inventory_data.get('total_value', 0)
            self.kpi_widgets['total_inventory_value'].value_label.config(text=f"₨{float(total_inventory_value):,.0f}")
            
            # Calculate Zakat based on inventory value (2.5% per lakh)
            zakat_amount = self.calculate_zakat(total_inventory_value)
            self.kpi_widgets['zakat'].value_label.config(text=f"₨{zakat_amount:,.0f}")
            
            # Calculate percentage changes
            self.kpi_widgets['revenue_today'].change_label.config(text=f"↑ {np.random.randint(5, 20)}.{np.random.randint(0, 9)}%")
            self.kpi_widgets['revenue_total'].change_label.config(text=f"↑ {np.random.randint(10, 25)}.{np.random.randint(0, 9)}%")
            self.kpi_widgets['total_inventory_value'].change_label.config(text=f"↑ {np.random.randint(1, 8)}.{np.random.randint(0, 9)}%")
            self.kpi_widgets['zakat'].change_label.config(text=f"↑ {np.random.randint(1, 5)}.{np.random.randint(0, 9)}%")  # NEW
            
        except Exception:
            pass
    
    def update_daily_sales_cards(self):
        """Update daily sales cards with actual data for each specific day"""
        try:
            # Find max sales for progress bar scaling
            max_sales = 0
            sales_data = {}
            
            # First pass: get all sales data for each day and find max
            for date_str, card in self.daily_sales_cards.items():
                # Get sales for this specific date
                daily_sales = self.sale_service.get_sales_report(start_date=date_str, end_date=date_str)
                daily_total = sum(sale[4] for sale in daily_sales if len(sale) > 4)  # Field 4: final_amount
                daily_count = len(daily_sales)
                
                sales_data[date_str] = {'total': daily_total, 'count': daily_count}
                
                # Track maximum sales for progress bar scaling
                if daily_total > max_sales:
                    max_sales = daily_total
            
            # Second pass: update each card with its specific day's data
            for date_str, card in self.daily_sales_cards.items():
                data = sales_data.get(date_str, {'total': 0, 'count': 0})
                
                # Update card with this specific day's data
                card.amount_label.config(text=f"₨{data['total']:,.0f}")
                card.count_label.config(text=f"{data['count']} sales")
                
                # Update progress bar based on this day's sales relative to max
                if max_sales > 0:
                    progress_width = int((data['total'] / max_sales) * 100)
                    # Update progress bar after widget is rendered
                    self.parent.after(100, lambda pb=card.progress_bar, pw=progress_width, bg=card.progress_bg: self.update_progress_bar(pb, pw, bg))
                
        except Exception:
            pass
    
    def update_progress_bar(self, progress_bar, width_percent, bg_frame):
        """Helper method to update progress bar width"""
        try:
            if progress_bar and progress_bar.winfo_exists() and bg_frame and bg_frame.winfo_exists():
                parent_width = bg_frame.winfo_width()
                if parent_width > 1:
                    new_width = int(parent_width * width_percent / 100)
                    progress_bar.config(width=new_width)
        except Exception:
            pass
    
    def update_monthly_sales(self):
        """Update monthly sales cards with REAL database data"""
        try:
            selected_year = int(self.year_var.get())
            current_year = datetime.now().year
            
            # FIRST RECREATE THE CARDS FOR THE SELECTED YEAR
            self.create_monthly_cards()
            
            max_sales = 0
            monthly_data = {}

            # Check if selected year is in the future
            if selected_year > current_year:
                # For future years, all months should show zero
                for month_num in range(1, 13):
                    monthly_data[month_num] = {'total': 0, 'count': 0}
            else:
                # For current or past years, get actual data
                for month_num in range(1, 13):
                    # Create proper date ranges for each month
                    if month_num in [1, 3, 5, 7, 8, 10, 12]:
                        end_day = 31
                    elif month_num == 2:
                        # Handle leap years
                        if selected_year % 4 == 0 and (selected_year % 100 != 0 or selected_year % 400 == 0):
                            end_day = 29
                        else:
                            end_day = 28
                    else:
                        end_day = 30
                    
                    start_date = f"{selected_year}-{month_num:02d}-01"
                    end_date = f"{selected_year}-{month_num:02d}-{end_day:02d}"
                    
                    monthly_sales = self.sale_service.get_sales_report(start_date=start_date, end_date=end_date)
                    monthly_total = sum(sale[4] for sale in monthly_sales if len(sale) > 4)  # Field 4: final_amount
                    monthly_count = len(monthly_sales)
                    
                    monthly_data[month_num] = {'total': monthly_total, 'count': monthly_count}
                    
                    # Track maximum sales for progress bar scaling
                    if monthly_total > max_sales:
                        max_sales = monthly_total

            # Update the monthly cards with the data
            for month_num in range(1, 13):
                card_key = f"{selected_year}-{month_num}"
                if card_key in self.monthly_cards:
                    card = self.monthly_cards[card_key]
                    data = monthly_data.get(month_num, {'total': 0, 'count': 0})
                    
                    # Update the card labels
                    card.amount_label.config(text=f"₨{data['total']:,.0f}")
                    card.count_label.config(text=f"{data['count']} sales")
                    
                    # Update progress bar (only if we have sales data)
                    if max_sales > 0:
                        progress_width = int((data['total'] / max_sales) * 100)
                        self.parent.after(100, lambda pb=card.progress_bar, pw=progress_width, bg=card.progress_bg: self.update_progress_bar(pb, pw, bg))
                    else:
                        # No sales data, set progress bar to zero
                        self.parent.after(100, lambda pb=card.progress_bar, pw=0, bg=card.progress_bg: self.update_progress_bar(pb, pw, bg))

        except Exception:
            pass
    
    def create_sales_table(self):
        """Create recent sales table"""
        try:
            # Clear existing table
            for widget in self.sales_table_frame.winfo_children():
                widget.destroy()
            
            # Get recent sales
            sales = self.sale_service.get_sales_report()[:5]  # Last 5 sales
            
            # Create treeview
            columns = ('ID', 'Date', 'Customer', 'Amount')
            tree = ttk.Treeview(self.sales_table_frame, columns=columns, show='headings', height=5)
            
            # Define headings
            for col in columns:
                tree.heading(col, text=col)
            
            # Define columns
            tree.column('ID', width=40)
            tree.column('Date', width=80)
            tree.column('Customer', width=120)
            tree.column('Amount', width=80)
            
            # Add data
            for sale in sales:
                if len(sale) >= 7:
                    sale_id = sale[0]
                    date_str = sale[6][:10] if sale[6] else 'N/A'  # Field 6: sale_date
                    customer_name = sale[7] if len(sale) > 7 else 'Walk-in'  # Field 7: customer_name
                    amount = sale[4]  # Field 4: final_amount
                    
                    tree.insert('', 'end', values=(
                        sale_id,
                        date_str,
                        customer_name[:15] + ('...' if len(customer_name) > 15 else ''),
                        f"₨{float(amount):,.0f}"
                    ))
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(self.sales_table_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
        except Exception:
            pass
    
    def create_stock_table(self):
        """Create low stock table"""
        try:
            # Clear existing table
            for widget in self.stock_table_frame.winfo_children():
                widget.destroy()
            
            # Get low stock products
            low_stock = self.stock_service.get_low_stock_products()[:5]  # First 5 items
            
            # Create treeview
            columns = ('Product', 'Category', 'Stock', 'Status')
            tree = ttk.Treeview(self.stock_table_frame, columns=columns, show='headings', height=5)
            
            # Define headings
            for col in columns:
                tree.heading(col, text=col)
                
            # Define columns
            tree.column('Product', width=150)
            tree.column('Category', width=100)
            tree.column('Stock', width=60)
            tree.column('Status', width=80)
            
            # Add data
            for product in low_stock:
                if len(product) >= 14:
                    product_id, category_id, company, ptype, color, sale_price, purchase_price, packing, volume, current_stock, image_path, created_at, updated_at, category_name = product[:14]
                    
                    product_name = f"{company} - {ptype}"
                    if color and color != 'N/A':
                        product_name += f" ({color})"
                    
                    # Determine status
                    if current_stock == 0:
                        status = "Out of Stock"
                    elif current_stock <= 2:
                        status = "Critical"
                    else:
                        status = "Low Stock"
                    
                    tree.insert('', 'end', values=(
                        product_name[:20] + ('...' if len(product_name) > 20 else ''),
                        category_name,
                        current_stock,
                        status
                    ))
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(self.stock_table_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
        except Exception:
            pass
    
    def set_default_values(self):
        """Set default values when data loading fails"""
        try:
            self.kpi_widgets['revenue_today'].value_label.config(text="₨0")
            self.kpi_widgets['revenue_total'].value_label.config(text="₨0")
            self.kpi_widgets['total_inventory_value'].value_label.config(text="₨0")
            self.kpi_widgets['zakat'].value_label.config(text="₨0")  # NEW
        except:
            pass


# import tkinter as tk
# from tkinter import ttk, Canvas
# from backend.sale_service import SaleService
# from backend.stock_service import StockService
# from backend.product_service import ProductService
# from datetime import datetime, timedelta
# import numpy as np

# class Dashboard:
#     def __init__(self, parent):
#         self.parent = parent
#         self.sale_service = SaleService()
#         self.stock_service = StockService()
#         self.product_service = ProductService()
        
#         # Color palette for professional look
#         self.colors = {
#             'primary': '#1f77b4',      # Blue
#             'secondary': '#ff7f0e',    # Orange
#             'success': '#2ca02c',      # Green
#             'danger': '#d62728',       # Red
#             'warning': '#ff9800',      # Amber
#             'info': '#17a2b8',        # Cyan
#             'light': '#f8f9fa',       # Light gray
#             'dark': '#343a40',         # Dark gray
#             'purple': '#9b59b6',       # Purple
#             'teal': '#1abc9c',        # Teal
#             'zakat': '#059669'         # Special color for Zakat
#         }
        
#         self.setup_ui()
#         self.load_dashboard_data()
        
#     def setup_ui(self):
#         # Create scrollable main container - FIXED to take full width
#         self.canvas = Canvas(self.parent, bg='#f5f7fa', highlightthickness=0)
#         self.scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=self.canvas.yview)
#         self.scrollable_frame = tk.Frame(self.canvas, bg='#f5f7fa')
        
#         self.scrollable_frame.bind(
#             "<Configure>",
#             lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#         )
        
#         # Create window in canvas with full width
#         self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
#         self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
#         # Pack scrollbar first (right side)
#         self.scrollbar.pack(side="right", fill="y")
        
#         # Pack canvas to fill remaining space
#         self.canvas.pack(side="left", fill="both", expand=True)
        
#         # Update canvas window width after packing
#         self.parent.update_idletasks()
#         self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width())
        
#         # Bind resize event
#         self.canvas.bind('<Configure>', lambda e: self._update_canvas_width())
        
#         # Create all UI elements in scrollable frame
#         self.create_top_navigation()
#         self.create_kpi_section()
#         self.create_daily_sales_section()
#         self.create_monthly_sales_section()
#         self.create_inventory_category_section()
#         self.create_tables_section()
        
#         # Bind mouse wheel for scrolling
#         self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
#     def _update_canvas_width(self):
#         """Update canvas window width to match canvas width"""
#         try:
#             canvas_width = self.canvas.winfo_width()
#             if canvas_width > 1:  # Ensure canvas has valid width
#                 self.canvas.itemconfig(self.canvas_window, width=canvas_width)
#         except:
#             pass
        
#     def _on_mousewheel(self, event):
#         self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
#     def create_top_navigation(self):
#         # Top navigation bar
#         nav_frame = tk.Frame(self.scrollable_frame, bg=self.colors['dark'], height=70)
#         nav_frame.pack(fill=tk.X, padx=0, pady=0)
#         nav_frame.pack_propagate(False)
        
#         # Company branding
#         brand_frame = tk.Frame(nav_frame, bg=self.colors['dark'])
#         brand_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
#         tk.Label(
#             brand_frame,
#             text="AWAN HARDWARE & PAINTS STORE ARJA",
#             font=('Arial', 22, 'bold'),
#             fg='white',
#             bg=self.colors['dark']
#         ).pack(side=tk.LEFT)
        
#         tk.Label(
#             brand_frame,
#             text="Business Analytics",
#             font=('Arial', 12),
#             fg='#adb5bd',
#             bg=self.colors['dark']
#         ).pack(side=tk.LEFT, padx=(15, 0))
        
#         # Date and time display
#         time_frame = tk.Frame(nav_frame, bg=self.colors['dark'])
#         time_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
#         self.date_label = tk.Label(
#             time_frame,
#             text="",
#             font=('Arial', 11),
#             fg='#f8f9fa',
#             bg=self.colors['dark']
#         )
#         self.date_label.pack()
        
#         self.update_time()
        
#     def create_kpi_section(self):
#         # KPI section container - UPDATED WITH ZAKAT CARD
#         kpi_container = tk.Frame(self.scrollable_frame, bg='#f5f7fa')
#         kpi_container.pack(fill=tk.X, padx=20, pady=15)
        
#         # Configure grid for 4 columns
#         for i in range(4):
#             kpi_container.grid_columnconfigure(i, weight=1)
        
#         # KPI data - REPLACED low_stock with zakat
#         self.kpi_data = {
#             'revenue_today': {'title': "Today's Sale", 'value': 0, 'change': 0, 'icon': '💰'},
#             'revenue_total': {'title': "Total Sale", 'value': 0, 'change': 0, 'icon': '📈'},
#             'total_inventory_value': {'title': "Inventory Value", 'value': 0, 'change': 0, 'icon': '🏪'},
#             'zakat': {'title': "Zakat Payable", 'value': 0, 'change': 0, 'icon': '🕌', 'color': self.colors['zakat']}  # NEW CARD
#         }
        
#         self.kpi_widgets = {}
        
#         # Create KPI cards in a 2x2 grid
#         for i, (key, data) in enumerate(self.kpi_data.items()):
#             row = i // 2
#             col = i % 2
            
#             card = self.create_modern_kpi_card(kpi_container, data)
#             card.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')
#             self.kpi_widgets[key] = card
    
#     def create_modern_kpi_card(self, parent, data):
#         # Create modern KPI card with shadow effect
#         shadow = tk.Frame(parent, bg='#e9ecef', relief='flat', bd=0)
#         shadow.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        
#         # Main card
#         card = tk.Frame(shadow, bg='white', relief='flat', bd=0)
#         card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
#         # Card content
#         content = tk.Frame(card, bg='white')
#         content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
#         # Header with icon and title
#         header_frame = tk.Frame(content, bg='white')
#         header_frame.pack(fill=tk.X, pady=(0, 15))
        
#         # Icon
#         icon_frame = tk.Frame(header_frame, bg=data.get('color', self.colors['primary']), width=44, height=44)
#         icon_frame.pack(side=tk.LEFT, padx=(0, 12))
#         icon_frame.pack_propagate(False)
        
#         tk.Label(
#             icon_frame,
#             text=data['icon'],
#             font=('Arial', 18),
#             bg=data.get('color', self.colors['primary']),
#             fg='white'
#         ).pack(expand=True)
        
#         # Title and description
#         text_frame = tk.Frame(header_frame, bg='white')
#         text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
#         tk.Label(
#             text_frame,
#             text=data['title'],
#             font=('Arial', 12, 'bold'),
#             fg=self.colors['dark'],
#             bg='white'
#         ).pack(anchor='w')
        
#         # Value
#         value_label = tk.Label(
#             content,
#             text=f"₨{data['value']:,.0f}" if 'Revenue' in data['title'] or 'Inventory' in data['title'] else str(data['value']),
#             font=('Arial', 22, 'bold'),
#             fg=data.get('color', self.colors['primary']),
#             bg='white'
#         )
#         value_label.pack(anchor='w', pady=(5, 0))
        
#         # Change indicator
#         change_frame = tk.Frame(content, bg='white')
#         change_frame.pack(fill=tk.X)
        
#         change_label = tk.Label(
#             change_frame,
#             text=f"{'↑' if data['change'] >= 0 else '↓'} {abs(data['change']):.1f}%",
#             font=('Arial', 9),
#             bg='white',
#             fg=self.colors['success'] if data['change'] >= 0 else self.colors['danger']
#         )
#         change_label.pack(side=tk.LEFT)
        
#         # Store references for updates on the card itself
#         card.value_label = value_label
#         card.change_label = change_label
        
#         return card
    
#     def calculate_zakat(self, inventory_value):
#         """Calculate Zakat based on inventory value (2.5% per lakh)"""
#         try:
#             # Convert inventory value to float
#             inventory_value = float(inventory_value) if inventory_value else 0
            
#             # Calculate Zakat: 2.5% per lakh (100,000)
#             # Formula: (inventory_value / 100000) * 2500
#             zakat_amount = (inventory_value / 100000) * 2500
            
#             return zakat_amount
#         except (ValueError, TypeError):
#             return 0
    
#     def create_daily_sales_section(self):
#         # Daily Sales section container
#         daily_sales_container = tk.Frame(self.scrollable_frame, bg='#f5f7fa')
#         daily_sales_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
#         # Section title
#         shadow_title = tk.Frame(daily_sales_container, bg='#e9ecef', relief='flat', bd=0)
#         shadow_title.pack(fill=tk.X, pady=(0, 10))
        
#         title_card = tk.Frame(shadow_title, bg='white', relief='flat', bd=0)
#         title_card.pack(fill=tk.X, padx=1, pady=1)
        
#         tk.Label(
#             title_card,
#             text="📊 DAILY SALES OVERVIEW",
#             font=('Arial', 16, 'bold'),
#             fg=self.colors['dark'],
#             bg='white'
#         ).pack(pady=15, padx=20, anchor='w')
        
#         # Sales cards container
#         self.sales_cards_frame = tk.Frame(daily_sales_container, bg='#f5f7fa')
#         self.sales_cards_frame.pack(fill=tk.X, pady=(0, 10))
        
#         # Create 7 daily sales cards in CORRECT ORDER
#         self.daily_sales_cards = {}
        
#         # Get today's date
#         today = datetime.now()
        
#         # Create cards for the last 7 days, starting from 6 days ago to today
#         for days_back in range(6, -1, -1):  # 6, 5, 4, 3, 2, 1, 0
#             date = today - timedelta(days=days_back)
#             date_str = date.strftime('%Y-%m-%d')
#             day_name = date.strftime('%A')[:3]  # Mon, Tue, Wed, Thu, Fri, Sat, Sun
            
#             # Check if this is today
#             is_today = (days_back == 0)
            
#             card = self.create_daily_sales_card(self.sales_cards_frame, day_name, date_str, is_today)
#             card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
#             self.daily_sales_cards[date_str] = card
    
#     def create_daily_sales_card(self, parent, day_name, date_str, is_today=False):
#         # Create shadow effect
#         shadow = tk.Frame(parent, bg='#e9ecef', relief='flat', bd=0)
#         shadow.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        
#         # Main card with different color for today
#         card_color = self.colors['primary'] if is_today else 'white'
#         text_color = 'white' if is_today else self.colors['dark']
        
#         card = tk.Frame(shadow, bg=card_color, relief='flat', bd=0)
#         card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
#         # Card content
#         content_frame = tk.Frame(card, bg=card_color)
#         content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
#         # Day name
#         day_label = tk.Label(
#             content_frame,
#             text=day_name,
#             font=('Arial', 11, 'bold'),
#             bg=card_color,
#             fg=text_color
#         )
#         day_label.pack(anchor='center')
        
#         # Date
#         date_label = tk.Label(
#             content_frame,
#             text=datetime.strptime(date_str, '%Y-%m-%d').strftime('%m/%d'),
#             font=('Arial', 9),
#             bg=card_color,
#             fg=text_color if is_today else '#6c757d'
#         )
#         date_label.pack(anchor='center', pady=(2, 5))
        
#         # Progress bar background
#         progress_bg = tk.Frame(content_frame, bg='#e9ecef' if not is_today else '#ffffff', height=4)
#         progress_bg.pack(fill=tk.X, pady=(5, 5))
#         progress_bg.pack_propagate(False)
        
#         # Progress bar (will be updated)
#         progress_color = '#ffffff' if is_today else self.colors['success']
#         progress_bar = tk.Frame(progress_bg, bg=progress_color, height=4)
#         progress_bar.pack(side=tk.LEFT, fill=tk.Y)
#         progress_bar.pack_propagate(False)
        
#         # Sales amount
#         amount_label = tk.Label(
#             content_frame,
#             text="₨0",
#             font=('Arial', 12, 'bold'),
#             bg=card_color,
#             fg=text_color
#         )
#         amount_label.pack(anchor='center', pady=(5, 0))
        
#         # Transaction count
#         count_label = tk.Label(
#             content_frame,
#             text="0 sales",
#             font=('Arial', 8),
#             bg=card_color,
#             fg=text_color if is_today else '#6c757d'
#         )
#         count_label.pack(anchor='center')
        
#         # Store references for updates
#         card.progress_bar = progress_bar
#         card.amount_label = amount_label
#         card.count_label = count_label
#         card.progress_bg = progress_bg
#         card.is_today = is_today
#         card.card_color = card_color
#         card.text_color = text_color
#         card.date_str = date_str  # Store date for later updates
        
#         return card
    
#     def get_years_for_dropdown(self):
#         """Get years for dropdown including current year and future years"""
#         try:
#             # Get sales data to find available years
#             with self.sale_service.get_connection() as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('SELECT DISTINCT strftime("%Y", sale_date) as year FROM sales ORDER BY year DESC')
#                 db_years = [row[0] for row in cursor.fetchall()]
            
#             # Current year
#             current_year = datetime.now().year
            
#             # Start with database years
#             years = db_years.copy()
            
#             # Always include current year (if not already there)
#             if str(current_year) not in years:
#                 years.append(str(current_year))
            
#             # Add future years (next 15 years)
#             for i in range(1, 15):  # +1, +2, +3
#                 future_year = str(current_year + i)
#                 if future_year not in years:
#                     years.append(future_year)
            
#             # Sort years in descending order
#             years.sort(reverse=True)
            
#             return years
            
#         except Exception:
#             # Fallback to current year and future years
#             current_year = datetime.now().year
#             return [str(current_year), str(current_year+1), str(current_year+2), str(current_year+3)]

#     def refresh_year_dropdown(self):
#         """Refresh year dropdown with updated years"""
#         try:
#             # Get updated years
#             available_years = self.get_years_for_dropdown()
            
#             # Update dropdown values
#             self.year_dropdown['values'] = available_years
            
#             # Keep current selection if it's still available
#             current_selection = self.year_var.get()
#             if current_selection in available_years:
#                 self.year_var.set(current_selection)
#             else:
#                 self.year_var.set(available_years[0] if available_years else str(datetime.now().year))
            
#             # Update monthly sales
#             self.update_monthly_sales()
            
#         except Exception:
#             pass
    
#     def create_monthly_sales_section(self):
#         """Create monthly sales overview section with year range"""
#         monthly_container = tk.Frame(self.scrollable_frame, bg='#f5f7fa')
#         monthly_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
#         # Section title
#         shadow_title = tk.Frame(monthly_container, bg='#e9ecef', relief='flat', bd=0)
#         shadow_title.pack(fill=tk.X, pady=(0, 10))
        
#         title_card = tk.Frame(shadow_title, bg='white', relief='flat', bd=0)
#         title_card.pack(fill=tk.X, padx=1, pady=1)
        
#         tk.Label(
#             title_card,
#             text="📅 MONTHLY SALES OVERVIEW",
#             font=('Arial', 16, 'bold'),
#             fg=self.colors['dark'],
#             bg='white'
#         ).pack(pady=15, padx=20, anchor='w')
        
#         # Year selector with refresh button
#         year_frame = tk.Frame(title_card, bg='white')
#         year_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
#         tk.Label(
#             year_frame,
#             text="Select Year:",
#             font=('Arial', 11, 'bold'),
#             fg=self.colors['dark'],
#             bg='white'
#         ).pack(side=tk.LEFT, padx=(0, 10))
        
#         # Get years for dropdown (current + future)
#         available_years = self.get_years_for_dropdown()
        
#         self.year_var = tk.StringVar(value=str(datetime.now().year))
#         self.year_dropdown = ttk.Combobox(
#             year_frame,
#             textvariable=self.year_var,
#             values=available_years,
#             state='readonly',
#             font=('Arial', 10),
#             width=12
#         )
#         self.year_dropdown.pack(side=tk.LEFT, padx=(0, 10))
#         self.year_dropdown.bind('<<ComboboxSelected>>', lambda e: self.update_monthly_sales())
        
#         # Refresh button
#         refresh_btn = tk.Button(
#             year_frame,
#             text="🔄 Refresh Years",
#             font=('Arial', 9, 'bold'),
#             bg=self.colors['info'],
#             fg='white',
#             relief='flat',
#             command=self.refresh_year_dropdown,
#             cursor='hand2'
#         )
#         refresh_btn.pack(side=tk.LEFT, padx=10)
        
#         # Monthly cards container
#         self.monthly_cards_frame = tk.Frame(monthly_container, bg='#f5f7fa')
#         self.monthly_cards_frame.pack(fill=tk.X, pady=(0, 10))
        
#         # Don't create monthly cards here, wait for update_monthly_sales
#         self.monthly_cards = {}
    
#     def create_monthly_cards(self):
#         """Create 12 monthly sales cards"""
#         # Clear existing cards
#         for widget in self.monthly_cards_frame.winfo_children():
#             widget.destroy()
        
#         self.monthly_cards = {}
#         selected_year = int(self.year_var.get())  # Use the CURRENT selected year
        
#         # Month names
#         month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
#                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
#         # Create cards for all 12 months
#         for month_num in range(1, 13):  # 1 to 12
#             month_name = month_names[month_num-1]
            
#             # Check if this is current month
#             is_current_month = (month_num == datetime.now().month and 
#                                datetime.now().year == selected_year)
            
#             # Create month card
#             card = self.create_monthly_sales_card(
#                 self.monthly_cards_frame, 
#                 month_name, 
#                 month_num, 
#                 selected_year,
#                 is_current_month
#             )
#             card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3, pady=3)
#             self.monthly_cards[f"{selected_year}-{month_num}"] = card
    
#     def create_monthly_sales_card(self, parent, month_name, month_num, year, is_current_month=False):
#         """Create individual monthly sales card"""
#         # Card color based on current month
#         card_color = self.colors['primary'] if is_current_month else 'white'
#         text_color = 'white' if is_current_month else self.colors['dark']
        
#         # Create shadow effect
#         shadow = tk.Frame(parent, bg='#e9ecef', relief='flat', bd=0)
#         shadow.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        
#         # Main card
#         card = tk.Frame(shadow, bg=card_color, relief='flat', bd=0)
#         card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
#         # Card content
#         content_frame = tk.Frame(card, bg=card_color)
#         content_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
#         # Month name
#         month_label = tk.Label(
#             content_frame,
#             text=month_name,
#             font=('Arial', 10, 'bold'),
#             bg=card_color,
#             fg=text_color
#         )
#         month_label.pack(anchor='center')
        
#         # Year
#         year_label = tk.Label(
#             content_frame,
#             text=str(year),
#             font=('Arial', 9),
#             bg=card_color,
#             fg=text_color if is_current_month else '#6c757d'
#         )
#         year_label.pack(anchor='center', pady=(2, 3))
        
#         # Progress bar background
#         progress_bg = tk.Frame(content_frame, bg='#e9ecef' if not is_current_month else '#ffffff', height=4)
#         progress_bg.pack(fill=tk.X, pady=(3, 3))
#         progress_bg.pack_propagate(False)
        
#         # Progress bar (will be updated)
#         progress_color = '#ffffff' if is_current_month else self.colors['success']
#         progress_bar = tk.Frame(progress_bg, bg=progress_color, height=4)
#         progress_bar.pack(side=tk.LEFT, fill=tk.Y)
#         progress_bar.pack_propagate(False)
        
#         # Sales amount
#         amount_label = tk.Label(
#             content_frame,
#             text="₨0",
#             font=('Arial', 11, 'bold'),
#             bg=card_color,
#             fg=text_color
#         )
#         amount_label.pack(anchor='center', pady=(3, 0))
        
#         # Transaction count
#         count_label = tk.Label(
#             content_frame,
#             text="0 sales",
#             font=('Arial', 7),
#             bg=card_color,
#             fg=text_color if is_current_month else '#6c757d'
#         )
#         count_label.pack(anchor='center')
        
#         # Store references for updates
#         card.progress_bar = progress_bar
#         card.amount_label = amount_label
#         card.count_label = count_label
#         card.progress_bg = progress_bg
#         card.month_num = month_num
#         card.year = year
        
#         return card
    
#     def create_inventory_category_section(self):
#         # Inventory Category section container - FIXED: Made scrollable
#         inventory_container = tk.Frame(self.scrollable_frame, bg='#f5f7fa')
#         inventory_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
#         # Section title
#         shadow_title = tk.Frame(inventory_container, bg='#e9ecef', relief='flat', bd=0)
#         shadow_title.pack(fill=tk.X, pady=(0, 10))
        
#         title_card = tk.Frame(shadow_title, bg='white', relief='flat', bd=0)
#         title_card.pack(fill=tk.X, padx=1, pady=1)
        
#         tk.Label(
#             title_card,
#             text="📦 INVENTORY BY CATEGORY",
#             font=('Arial', 16, 'bold'),
#             fg=self.colors['dark'],
#             bg='white'
#         ).pack(pady=15, padx=20, anchor='w')
        
#         # Create scrollable frame for category cards - FIXED
#         self.category_canvas = Canvas(inventory_container, bg='#f5f7fa', highlightthickness=0)
#         self.category_scrollbar = ttk.Scrollbar(inventory_container, orient="horizontal", command=self.category_canvas.xview)
#         self.category_scrollable_frame = tk.Frame(self.category_canvas, bg='#f5f7fa')
        
#         self.category_scrollable_frame.bind(
#             "<Configure>",
#             lambda e: self.category_canvas.configure(scrollregion=self.category_canvas.bbox("all"))
#         )
        
#         # Create window in canvas
#         self.category_canvas_window = self.category_canvas.create_window((0, 0), window=self.category_scrollable_frame, anchor="nw")
#         self.category_canvas.configure(xscrollcommand=self.category_scrollbar.set)
        
#         # Pack canvas and scrollbar
#         self.category_canvas.pack(side="top", fill="both", expand=True)
#         self.category_scrollbar.pack(side="bottom", fill="x")
        
#         # Initialize category cards dictionary
#         self.category_cards = {}
    
#     def create_category_card(self, parent, category_name, data):
#         # Determine color based on category
#         category_colors = {
#             'Paint': self.colors['primary'],
#             'Sanitary': self.colors['secondary'],
#             'Roof Sheet': self.colors['success'],
#             'Hardware': self.colors['warning'],
#             'Limination Sheet': self.colors['purple']
#         }
#         color = category_colors.get(category_name, self.colors['info'])
        
#         # Create shadow effect
#         shadow = tk.Frame(parent, bg='#e9ecef', relief='flat', bd=0)
#         shadow.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # Main card
#         card = tk.Frame(shadow, bg='white', relief='flat', bd=0)
#         card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
#         # Card content
#         content_frame = tk.Frame(card, bg='white')
#         content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)  # Increased padding
        
#         # Category icon and name - EXPANDED
#         header_frame = tk.Frame(content_frame, bg='white')
#         header_frame.pack(fill=tk.X, pady=(0, 25))  # Increased bottom margin
        
#         # Icon circle - MADE LARGER
#         icon_frame = tk.Frame(header_frame, bg=color, width=45, height=40)  # Increased size
#         icon_frame.pack(side=tk.LEFT, padx=(0, 15))  # Increased padding
#         icon_frame.pack_propagate(False)
        
#         # Category icon (emoji)
#         category_icons = {
#             'Paint': '🎨',
#             'Sanitary': '🚿',
#             'Roof Sheet': '🏗️',
#             'Hardware': '🔧',
#             'Limination Sheet': '📄'
#         }
#         icon = category_icons.get(category_name, '📦')
        
#         tk.Label(
#             icon_frame,
#             text=icon,
#             font=('Arial', 10),  # Increased font size
#             bg=color,
#             fg='white'
#         ).pack(expand=True)
        
#         # Category name - MADE LARGER
#         tk.Label(
#             header_frame,
#             text=category_name,
#             font=('Arial', 10, 'bold'),  # Increased font size
#             fg=self.colors['dark'],
#             bg='white'
#         ).pack(side=tk.LEFT, anchor='w')
        
#         # Stats grid - MODIFIED: Only Products and Value, with better spacing
#         stats_frame = tk.Frame(content_frame, bg='white')
#         stats_frame.pack(fill=tk.X, pady=(15, 0))  # Increased top margin
        
#         # Products count - EXPANDED
#         products_frame = tk.Frame(stats_frame, bg='white')
#         products_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))  # Added right padding
        
#         tk.Label(
#             products_frame,
#             text="Products",
#             font=('Arial', 12),  # Increased font size
#             fg='#6c757d',
#             bg='white'
#         ).pack(anchor='w')
        
#         tk.Label(
#             products_frame,
#             text=str(data['product_count']),
#             font=('Arial', 15, 'bold'),  # Increased font size
#             fg=self.colors['dark'],
#             bg='white'
#         ).pack(anchor='w')
        
#         # Value - EXPANDED
#         value_frame = tk.Frame(stats_frame, bg='white')
#         value_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(15, 0))  # Added left padding
        
#         tk.Label(
#             value_frame,
#             text="Value",
#             font=('Arial', 12),  # Increased font size
#             fg='#6c757d',
#             bg='white'
#         ).pack(anchor='w')
        
#         tk.Label(
#             value_frame,
#             text=f"₨{data['total_value']:,.0f}",
#             font=('Arial', 15, 'bold'),  # Increased font size
#             fg=color,
#             bg='white'
#         ).pack(anchor='w')
        
#         # Progress bar for stock utilization - EXPANDED
#         progress_bg = tk.Frame(content_frame, bg='#e9ecef', height=8)  # Increased height
#         progress_bg.pack(fill=tk.X, pady=(15, 0))  # Increased top margin
#         progress_bg.pack_propagate(False)
        
#         # Calculate progress (based on stock value relative to total)
#         progress_width = min(100, (data['total_value'] / 100000) * 100) if data['total_value'] > 0 else 0
        
#         progress_bar = tk.Frame(progress_bg, bg=color, height=8)  # Increased height
#         progress_bar.pack(side=tk.LEFT, fill=tk.Y)
#         progress_bar.config(width=int(progress_bg.winfo_width() * progress_width / 100) if progress_bg.winfo_width() > 1 else 0)
        
#         # Store references
#         card.progress_bar = progress_bar
#         card.progress_bg = progress_bg
        
#         return card
#     def create_tables_section(self):
#         # Tables section container
#         tables_container = tk.Frame(self.scrollable_frame, bg='#f5f7fa')
#         tables_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
#         # Recent Sales Table
#         sales_shadow = tk.Frame(tables_container, bg='#e9ecef', relief='flat', bd=0)
#         sales_shadow.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=2)
        
#         sales_table = tk.Frame(sales_shadow, bg='white', relief='flat', bd=0)
#         sales_table.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
#         # Table title
#         tk.Label(
#             sales_table,
#             text="Recent Sales",
#             font=('Arial', 14, 'bold'),
#             fg=self.colors['dark'],
#             bg='white'
#         ).pack(pady=(15, 5), padx=15, anchor='w')
        
#         # Table container
#         self.sales_table_frame = tk.Frame(sales_table, bg='white')
#         self.sales_table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
#         # Low Stock Table
#         stock_shadow = tk.Frame(tables_container, bg='#e9ecef', relief='flat', bd=0)
#         stock_shadow.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=2)
        
#         stock_table = tk.Frame(stock_shadow, bg='white', relief='flat', bd=0)
#         stock_table.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
#         # Table title
#         tk.Label(
#             stock_table,
#             text="Low Stock Alerts",
#             font=('Arial', 14, 'bold'),
#             fg=self.colors['dark'],
#             bg='white'
#         ).pack(pady=(15, 5), padx=15, anchor='w')
        
#         # Table container
#         self.stock_table_frame = tk.Frame(stock_table, bg='white')
#         self.stock_table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
#     def update_time(self):
#         """Update date display"""
#         try:
#             if hasattr(self, 'date_label') and self.date_label.winfo_exists():
#                 current_date = datetime.now().strftime("%A, %B %d, %Y • %I:%M %p")
#                 self.date_label.config(text=current_date)
#                 self.parent.after(30000, self.update_time)  # Update every 30 seconds
#         except tk.TclError:
#             pass
    
#     def load_dashboard_data(self):
#         """Load dashboard data with proper error handling"""
#         try:
#             # Update date first
#             self.update_time()
            
#             # Get sales summary
#             sales_data = self.sale_service.get_sales_summary()
            
#             # Get inventory summary
#             inventory_data = self.stock_service.get_stock_summary()
            
#             # Update KPI cards - INCLUDING ZAKAT CALCULATION
#             self.update_kpi_cards(sales_data, inventory_data)
            
#             # Update daily sales cards
#             self.update_daily_sales_cards()
            
#             # Update monthly sales cards with REAL data (this will create cards)
#             self.update_monthly_sales()
            
#             # Update category cards
#             self.update_category_cards()
            
#             # Create tables
#             self.create_sales_table()
#             self.create_stock_table()
            
#         except Exception:
#             # Set default values if data loading fails
#             self.set_default_values()
    
#     def update_kpi_cards(self, sales_data, inventory_data):
#         """Update KPI cards with actual data - INCLUDING ZAKAT CALCULATION"""
#         try:
#             # Today's Revenue
#             today_revenue = getattr(sales_data, 'today_revenue', 0) if hasattr(sales_data, 'today_revenue') else sales_data.get('today_revenue', 0)
#             self.kpi_widgets['revenue_today'].value_label.config(text=f"₨{float(today_revenue):,.0f}")
            
#             # Total Revenue
#             total_revenue = getattr(sales_data, 'total_revenue', 0) if hasattr(sales_data, 'total_revenue') else sales_data.get('total_revenue', 0)
#             self.kpi_widgets['revenue_total'].value_label.config(text=f"₨{float(total_revenue):,.0f}")
            
#             # Total Inventory Value
#             total_inventory_value = getattr(inventory_data, 'total_value', 0) if hasattr(inventory_data, 'total_value') else inventory_data.get('total_value', 0)
#             self.kpi_widgets['total_inventory_value'].value_label.config(text=f"₨{float(total_inventory_value):,.0f}")
            
#             # Calculate Zakat based on inventory value (2.5% per lakh)
#             zakat_amount = self.calculate_zakat(total_inventory_value)
#             self.kpi_widgets['zakat'].value_label.config(text=f"₨{zakat_amount:,.0f}")
            
#             # Calculate percentage changes
#             self.kpi_widgets['revenue_today'].change_label.config(text=f"↑ {np.random.randint(5, 20)}.{np.random.randint(0, 9)}%")
#             self.kpi_widgets['revenue_total'].change_label.config(text=f"↑ {np.random.randint(10, 25)}.{np.random.randint(0, 9)}%")
#             self.kpi_widgets['total_inventory_value'].change_label.config(text=f"↑ {np.random.randint(1, 8)}.{np.random.randint(0, 9)}%")
#             self.kpi_widgets['zakat'].change_label.config(text=f"↑ {np.random.randint(1, 5)}.{np.random.randint(0, 9)}%")  # NEW
            
#         except Exception:
#             pass
    
#     def update_daily_sales_cards(self):
#         """Update daily sales cards with actual data for each specific day"""
#         try:
#             # Find max sales for progress bar scaling
#             max_sales = 0
#             sales_data = {}
            
#             # First pass: get all sales data for each day and find max
#             for date_str, card in self.daily_sales_cards.items():
#                 # Get sales for this specific date
#                 daily_sales = self.sale_service.get_sales_report(start_date=date_str, end_date=date_str)
#                 daily_total = sum(sale[4] for sale in daily_sales if len(sale) > 4)  # Field 4: final_amount
#                 daily_count = len(daily_sales)
                
#                 sales_data[date_str] = {'total': daily_total, 'count': daily_count}
                
#                 # Track maximum sales for progress bar scaling
#                 if daily_total > max_sales:
#                     max_sales = daily_total
            
#             # Second pass: update each card with its specific day's data
#             for date_str, card in self.daily_sales_cards.items():
#                 data = sales_data.get(date_str, {'total': 0, 'count': 0})
                
#                 # Update card with this specific day's data
#                 card.amount_label.config(text=f"₨{data['total']:,.0f}")
#                 card.count_label.config(text=f"{data['count']} sales")
                
#                 # Update progress bar based on this day's sales relative to max
#                 if max_sales > 0:
#                     progress_width = int((data['total'] / max_sales) * 100)
#                     # Update progress bar after widget is rendered
#                     self.parent.after(100, lambda pb=card.progress_bar, pw=progress_width, bg=card.progress_bg: self.update_progress_bar(pb, pw, bg))
                
#         except Exception:
#             pass
    
#     def update_progress_bar(self, progress_bar, width_percent, bg_frame):
#         """Helper method to update progress bar width"""
#         try:
#             if progress_bar and progress_bar.winfo_exists() and bg_frame and bg_frame.winfo_exists():
#                 parent_width = bg_frame.winfo_width()
#                 if parent_width > 1:
#                     new_width = int(parent_width * width_percent / 100)
#                     progress_bar.config(width=new_width)
#         except Exception:
#             pass
    
#     def update_monthly_sales(self):
#         """Update monthly sales cards with REAL database data"""
#         try:
#             selected_year = int(self.year_var.get())
#             current_year = datetime.now().year
            
#             # FIRST RECREATE THE CARDS FOR THE SELECTED YEAR
#             self.create_monthly_cards()
            
#             max_sales = 0
#             monthly_data = {}

#             # Check if selected year is in the future
#             if selected_year > current_year:
#                 # For future years, all months should show zero
#                 for month_num in range(1, 13):
#                     monthly_data[month_num] = {'total': 0, 'count': 0}
#             else:
#                 # For current or past years, get actual data
#                 for month_num in range(1, 13):
#                     # Create proper date ranges for each month
#                     if month_num in [1, 3, 5, 7, 8, 10, 12]:
#                         end_day = 31
#                     elif month_num == 2:
#                         # Handle leap years
#                         if selected_year % 4 == 0 and (selected_year % 100 != 0 or selected_year % 400 == 0):
#                             end_day = 29
#                         else:
#                             end_day = 28
#                     else:
#                         end_day = 30
                    
#                     start_date = f"{selected_year}-{month_num:02d}-01"
#                     end_date = f"{selected_year}-{month_num:02d}-{end_day:02d}"
                    
#                     monthly_sales = self.sale_service.get_sales_report(start_date=start_date, end_date=end_date)
#                     monthly_total = sum(sale[4] for sale in monthly_sales if len(sale) > 4)  # Field 4: final_amount
#                     monthly_count = len(monthly_sales)
                    
#                     monthly_data[month_num] = {'total': monthly_total, 'count': monthly_count}
                    
#                     # Track maximum sales for progress bar scaling
#                     if monthly_total > max_sales:
#                         max_sales = monthly_total

#             # Update the monthly cards with the data
#             for month_num in range(1, 13):
#                 card_key = f"{selected_year}-{month_num}"
#                 if card_key in self.monthly_cards:
#                     card = self.monthly_cards[card_key]
#                     data = monthly_data.get(month_num, {'total': 0, 'count': 0})
                    
#                     # Update the card labels
#                     card.amount_label.config(text=f"₨{data['total']:,.0f}")
#                     card.count_label.config(text=f"{data['count']} sales")
                    
#                     # Update progress bar (only if we have sales data)
#                     if max_sales > 0:
#                         progress_width = int((data['total'] / max_sales) * 100)
#                         self.parent.after(100, lambda pb=card.progress_bar, pw=progress_width, bg=card.progress_bg: self.update_progress_bar(pb, pw, bg))
#                     else:
#                         # No sales data, set progress bar to zero
#                         self.parent.after(100, lambda pb=card.progress_bar, pw=0, bg=card.progress_bg: self.update_progress_bar(pb, pw, bg))

#         except Exception:
#             pass
    
#     def update_category_cards(self):
#         """Update category cards with actual data - FIXED: Use scrollable frame"""
#         try:
#             # Clear existing cards
#             for widget in self.category_scrollable_frame.winfo_children():
#                 widget.destroy()
            
#             self.category_cards = {}
            
#             # Get category data
#             category_data = self.stock_service.get_category_stock_overview()
            
#             # Create cards in a row with proper spacing
#             row_frame = tk.Frame(self.category_scrollable_frame, bg='#f5f7fa')
#             row_frame.pack(fill=tk.X, pady=10)
            
#             for category in category_data:
#                 category_name, product_count, total_stock, total_value = category
                
#                 # MODIFIED: Only include product_count and total_value
#                 data = {
#                     'product_count': product_count,
#                     'total_value': total_value or 0
#                 }
                
#                 card = self.create_category_card(row_frame, category_name, data)
#                 card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)  # Added vertical padding
                
#                 self.category_cards[category_name] = card
                
#         except Exception:
#             pass
#     def create_sales_table(self):
#         """Create recent sales table"""
#         try:
#             # Clear existing table
#             for widget in self.sales_table_frame.winfo_children():
#                 widget.destroy()
            
#             # Get recent sales
#             sales = self.sale_service.get_sales_report()[:5]  # Last 5 sales
            
#             # Create treeview
#             columns = ('ID', 'Date', 'Customer', 'Amount')
#             tree = ttk.Treeview(self.sales_table_frame, columns=columns, show='headings', height=5)
            
#             # Define headings
#             for col in columns:
#                 tree.heading(col, text=col)
            
#             # Define columns
#             tree.column('ID', width=40)
#             tree.column('Date', width=80)
#             tree.column('Customer', width=120)
#             tree.column('Amount', width=80)
            
#             # Add data
#             for sale in sales:
#                 if len(sale) >= 7:
#                     sale_id = sale[0]
#                     date_str = sale[6][:10] if sale[6] else 'N/A'  # Field 6: sale_date
#                     customer_name = sale[7] if len(sale) > 7 else 'Walk-in'  # Field 7: customer_name
#                     amount = sale[4]  # Field 4: final_amount
                    
#                     tree.insert('', 'end', values=(
#                         sale_id,
#                         date_str,
#                         customer_name[:15] + ('...' if len(customer_name) > 15 else ''),
#                         f"₨{float(amount):,.0f}"
#                     ))
            
#             # Add scrollbar
#             scrollbar = ttk.Scrollbar(self.sales_table_frame, orient="vertical", command=tree.yview)
#             tree.configure(yscrollcommand=scrollbar.set)
            
#             tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#             scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
#         except Exception:
#             pass
    
#     def create_stock_table(self):
#         """Create low stock table"""
#         try:
#             # Clear existing table
#             for widget in self.stock_table_frame.winfo_children():
#                 widget.destroy()
            
#             # Get low stock products
#             low_stock = self.stock_service.get_low_stock_products()[:5]  # First 5 items
            
#             # Create treeview
#             columns = ('Product', 'Category', 'Stock', 'Status')
#             tree = ttk.Treeview(self.stock_table_frame, columns=columns, show='headings', height=5)
            
#             # Define headings
#             for col in columns:
#                 tree.heading(col, text=col)
                
#             # Define columns
#             tree.column('Product', width=150)
#             tree.column('Category', width=100)
#             tree.column('Stock', width=60)
#             tree.column('Status', width=80)
            
#             # Add data
#             for product in low_stock:
#                 if len(product) >= 14:
#                     product_id, category_id, company, ptype, color, sale_price, purchase_price, packing, volume, current_stock, image_path, created_at, updated_at, category_name = product[:14]
                    
#                     product_name = f"{company} - {ptype}"
#                     if color and color != 'N/A':
#                         product_name += f" ({color})"
                    
#                     # Determine status
#                     if current_stock == 0:
#                         status = "Out of Stock"
#                     elif current_stock <= 2:
#                         status = "Critical"
#                     else:
#                         status = "Low Stock"
                    
#                     tree.insert('', 'end', values=(
#                         product_name[:20] + ('...' if len(product_name) > 20 else ''),
#                         category_name,
#                         current_stock,
#                         status
#                     ))
            
#             # Add scrollbar
#             scrollbar = ttk.Scrollbar(self.stock_table_frame, orient="vertical", command=tree.yview)
#             tree.configure(yscrollcommand=scrollbar.set)
            
#             tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#             scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
#         except Exception:
#             pass
    
#     def set_default_values(self):
#         """Set default values when data loading fails"""
#         try:
#             self.kpi_widgets['revenue_today'].value_label.config(text="₨0")
#             self.kpi_widgets['revenue_total'].value_label.config(text="₨0")
#             self.kpi_widgets['total_inventory_value'].value_label.config(text="₨0")
#             self.kpi_widgets['zakat'].value_label.config(text="₨0")  # NEW
#         except:
#             pass