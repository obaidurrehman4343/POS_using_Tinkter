from frontend.dashboard import Dashboard
from frontend.inventory_management import InventoryManagement
from frontend.sale_pos import SalePOS
from frontend.sale_management import SaleManagement  # Add this import
from frontend.stock_report import StockReport
from frontend.settings import Settings
import tkinter as tk
from frontend.stock_report import StockReport
class MainWindow:
    def __init__(self, root, login_root=None):
        self.root = root
        self.login_root = login_root
        self.root.title("Awan Hardware POS")
        self.root.state('zoomed')
        self.root.configure(bg='#ecf0f1')

        self.current_page = None
        self.active_button = None
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.sidebar = self.create_sidebar(main_frame)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Content area
        self.content_area = tk.Frame(main_frame, bg='white')
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Initially empty content
        self.show_empty_content()

    def create_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg='#2c3e50', width=250)
        sidebar.pack_propagate(False)

        # Header
        header_frame = tk.Frame(sidebar, bg='#34495e', height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="Awan Hardware",
            font=('Arial', 16, 'bold'),
            fg='#3498db',
            bg='#34495e'
        ).pack(expand=True, pady=(15, 0))

        tk.Label(
            header_frame,
            text="POS System",
            font=('Arial', 10),
            fg='#bdc3c7',
            bg='#34495e'
        ).pack(expand=True, pady=(0, 15))

        # Menu Frame
        menu_frame = tk.Frame(sidebar, bg='#2c3e50')
        menu_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=15, pady=20)

        tk.Label(
            menu_frame,
            text="MAIN MENU",
            font=('Arial', 10, 'bold'),
            fg='#7f8c8d',
            bg='#2c3e50'
        ).pack(anchor='w', pady=(0, 10))

        # Menu buttons
        self.dashboard_btn = self.create_menu_button(menu_frame, "📊 Dashboard", self.show_dashboard)
        self.inventory_btn = self.create_menu_button(menu_frame, "📦 Inventory Management", self.show_inventory)
        self.sales_btn = self.create_menu_button(menu_frame, "💰 Point of Sale", self.show_sales)
        self.sale_mgmt_btn = self.create_menu_button(menu_frame, "📈 Sale Management", self.show_sale_management)  # Add this
        self.stock_report_btn = self.create_menu_button(menu_frame, "📊 Stock Report", self.show_stock_report)

        # Footer
        footer_frame = tk.Frame(sidebar, bg='#34495e')
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        # Account Label
        tk.Label(
            footer_frame,
            text="ACCOUNT",
            font=('Arial', 10, 'bold'),
            fg='#7f8c8d',
            bg='#34495e'
        ).pack(anchor='w', padx=15, pady=(8, 5))

        # Settings Button
        settings_btn = tk.Button(
            footer_frame,
            text="⚙️ Settings",
            font=('Arial', 11),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=self.show_settings,
            cursor='hand2',
            anchor='w'
        )
        settings_btn.pack(fill=tk.X, padx=10, pady=4, ipady=6)

        # Logout Button
        logout_btn = tk.Button(
            footer_frame,
            text="🚪 Logout",
            font=('Arial', 11, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            command=self.logout,
            cursor='hand2',
            anchor='w'
        )
        logout_btn.pack(fill=tk.X, padx=10, pady=(4, 10), ipady=6)

        return sidebar

    def create_menu_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            font=('Arial', 12),
            anchor='w',
            bg='#2c3e50',
            fg='#bdc3c7',
            relief='flat',
            command=lambda: [self.clear_content(), self.update_button_style(btn), command()],
            cursor='hand2'
        )
        btn.pack(fill=tk.X, pady=2, ipady=8, padx=5)

        def on_enter(e):
            if btn != self.active_button:
                btn.config(bg='#34495e', fg='white')

        def on_leave(e):
            if btn != self.active_button:
                btn.config(bg='#2c3e50', fg='#bdc3c7')

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def update_button_style(self, active_button):
        buttons = [self.dashboard_btn, self.inventory_btn, self.sales_btn, self.sale_mgmt_btn, self.stock_report_btn]
        for b in buttons:
            b.config(bg='#2c3e50', fg='#bdc3c7')
        if active_button:
            active_button.config(bg='#3498db', fg='white')
            self.active_button = active_button

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # Page show methods
    def show_dashboard(self): Dashboard(self.content_area)
    def show_inventory(self): InventoryManagement(self.content_area)
    def show_sales(self): SalePOS(self.content_area)
    def show_sale_management(self): SaleManagement(self.content_area)  # Add this
    def show_stock_report(self): StockReport(self.content_area)
    def show_settings(self): Settings(self.content_area)
    def show_empty_content(self):
        self.clear_content()
        empty_frame = tk.Frame(self.content_area, bg='white')
        empty_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            empty_frame,
            text="🚀 Welcome to Awan Hardware POS",
            font=('Arial', 24, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(pady=(100, 20))

        tk.Label(
            empty_frame,
            text="Select a section from the sidebar to get started",
            font=('Arial', 14),
            fg='#7f8c8d',
            bg='white'
        ).pack(pady=10)

    def logout(self):
        try:
            self.root.destroy()
            if self.login_root and self.login_root.winfo_exists():
                self.login_root.deiconify()
        except Exception as e:
            print("Logout error:", e)