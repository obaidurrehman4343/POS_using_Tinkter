# frontend/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from frontend.dashboard import Dashboard
from frontend.inventory_management import InventoryManagement
from frontend.sale_pos import SalePOS
from frontend.sale_management import SaleManagement
from frontend.stock_report import StockReport
from frontend.udhar_management import UdharManagement

class MainWindow:
    def __init__(self, parent, user_session):
        self.parent = parent
        self.user_session = user_session
        self.current_content = None
        self.login_root = None  # This should reference LoginWindow instance
        
        # Track all module instances
        self.module_instances = {}
        
        self.setup_ui()
        self.refresh_sidebar()
        self.show_default_view()
    
    def setup_ui(self):
        # Set window properties
        self.parent.title("AWAN HARDWARE - POS SYSTEM")
        self.parent.geometry("1400x800")
        self.parent.configure(bg='#ecf0f1')
        
        # Main container for sidebar and content
        main_container = tk.Frame(self.parent, bg='#ecf0f1')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.sidebar = tk.Frame(main_container, bg='#34495e', width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Content area
        self.content_area = tk.Frame(main_container, bg='#ecf0f1')
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def refresh_sidebar(self):
        """Refresh sidebar content"""
        self.create_sidebar_content()
    
    def create_sidebar_content(self):
        """Create sidebar content"""
        # Clear any existing content in the sidebar first
        for widget in self.sidebar.winfo_children():
            widget.destroy()
            
        # --- TOP: User Info ---
        user_frame = tk.Frame(self.sidebar, bg='#2c3e50', pady=15)
        user_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        tk.Label(
            user_frame,
            text=f"👤 {self.user_session['full_name']}",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#2c3e50'
        ).pack(anchor='w')
        
        tk.Label(
            user_frame,
            text=f"Role: {self.user_session['role'].title()}",
            font=('Arial', 10),
            fg='#bdc3c7',
            bg='#2c3e50'
        ).pack(anchor='w', pady=(5, 0))

        # --- MIDDLE: Navigation Buttons ---
        nav_container = tk.Frame(self.sidebar, bg='#34495e')
        nav_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Separator(nav_container, orient='horizontal').pack(fill=tk.X, pady=(0, 10))
        
        self.create_navigation_buttons(nav_container)

        # --- BOTTOM: Sidebar Footer with Settings and Logout Button ---
        sidebar_footer = tk.Frame(self.sidebar, bg='#2c3e50', height=80)
        sidebar_footer.pack(side=tk.BOTTOM, fill=tk.X)
        sidebar_footer.pack_propagate(False)
        
        ttk.Separator(self.sidebar, orient='horizontal').pack(fill=tk.X, side=tk.BOTTOM, before=sidebar_footer)
        
        # Settings Button
        settings_btn = tk.Button(
            sidebar_footer,
            text="⚙️ Settings",
            font=('Arial', 11, 'bold'),
            bg='#34495e',
            fg='white',
            activebackground='#2c3e50',
            activeforeground='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.show_settings
        )
        settings_btn.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Logout Button - FIXED: Now goes back to login screen
        logout_btn = tk.Button(
            sidebar_footer,
            text="🚪 Logout",
            font=('Arial', 11, 'bold'),
            bg='#c0392b',
            fg='white',
            activebackground='#a93226',
            activeforeground='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.logout  # This should go back to login, not terminate
        )
        logout_btn.pack(fill=tk.X, padx=10, pady=(0, 10))
    
    def show_default_view(self):
        """Show appropriate default view based on user permissions"""
        permissions = self.user_session['permissions']
        
        if 'dashboard' in permissions:
            self.show_dashboard()
        elif 'point_of_sale' in permissions:
            self.show_pos()
        elif 'inventory_management' in permissions:
            self.show_inventory()
        else:
            if permissions:
                first_module = permissions[0]
                if first_module == 'dashboard':
                    self.show_dashboard()
                elif first_module == 'point_of_sale':
                    self.show_pos()
                elif first_module == 'inventory_management':
                    self.show_inventory()
                elif first_module == 'sale_report':
                    self.show_sales_report()
                elif first_module == 'stock_report':
                    self.show_stock_report()
                elif first_module == 'udhar_management':
                    self.show_udhar()
            else:
                self.clear_content()
                message_label = tk.Label(
                    self.content_area,
                    text="No modules available for your role. Please contact administrator.",
                    font=('Arial', 14),
                    fg='#7f8c8d',
                    bg='#ecf0f1'
                )
                message_label.pack(expand=True)
    
    def create_navigation_buttons(self, parent_frame):
        """Create navigation buttons based on user permissions"""
        all_modules = {
            'dashboard': ('📊 Dashboard', self.show_dashboard),
            'inventory_management': ('📦 Inventory Management', self.show_inventory),
            'point_of_sale': ('💰 Point Of Sale', self.show_pos),
            'sale_report': ('📈 Sales Report', self.show_sales_report),
            'stock_report': ('📋 Stock Report', self.show_stock_report),
            'udhar_management': ('💳 Udhar Management', self.show_udhar)
        }
        
        user_permissions = self.user_session['permissions']
        
        buttons_created = 0
        for module_key in user_permissions:
            if module_key in all_modules:
                display_name, command = all_modules[module_key]
                
                btn = tk.Button(
                    parent_frame,
                    text=display_name,
                    font=('Arial', 11),
                    bg='#34495e',
                    fg='white',
                    relief='flat',
                    anchor='w',
                    command=lambda cmd=command: [self.clear_content(), cmd()],
                    cursor='hand2',
                    padx=10,
                    pady=8
                )
                btn.pack(fill=tk.X, pady=5)
                buttons_created += 1
        
        if buttons_created == 0:
            no_access_label = tk.Label(
                parent_frame,
                text="No modules available",
                font=('Arial', 10),
                fg='#bdc3c7',
                bg='#34495e'
            )
            no_access_label.pack(pady=20)
            
            contact_label = tk.Label(
                parent_frame,
                text="Contact administrator",
                font=('Arial', 9),
                fg='#95a5a6',
                bg='#34495e'
            )
            contact_label.pack()
    
    def clear_content(self):
        """Clear the content area completely"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        self.current_content = None
    
    def show_dashboard(self):
        if 'dashboard' in self.user_session['permissions']:
            self.clear_content()
            self.current_content = Dashboard(self.content_area)
    
    def show_inventory(self):
        if 'inventory_management' in self.user_session['permissions']:
            self.clear_content()
            self.current_content = InventoryManagement(self.content_area, self.user_session)
    
    def show_pos(self):
        if 'point_of_sale' in self.user_session['permissions']:
            self.clear_content()
            self.current_content = SalePOS(self.content_area)
    
    def show_sales_report(self):
        if 'sale_report' in self.user_session['permissions']:
            self.clear_content()
            self.current_content = SaleManagement(self.content_area)
    
    def show_stock_report(self):
        if 'stock_report' in self.user_session['permissions']:
            self.clear_content()
            self.current_content = StockReport(self.content_area)
    
    def show_udhar(self):
        if 'udhar_management' in self.user_session['permissions']:
            self.clear_content()
            self.current_content = UdharManagement(self.content_area)
    
    def show_settings(self):
        try:
            from frontend.settings_window import SettingsWindow
            SettingsWindow(self.parent, self.user_session, self.refresh_user_session)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open settings: {str(e)}")
    
    def refresh_user_session(self):
        try:
            from backend.database import Database
            db = Database()
            
            user_data = db.get_user_by_id(self.user_session['user_id'])
            if user_data:
                user_id, username, role, full_name, phone, is_active, created_at, last_login = user_data
                
                self.user_session['username'] = username
                self.user_session['role'] = role
                self.user_session['full_name'] = full_name
                self.user_session['phone'] = phone
                self.user_session['permissions'] = db.get_user_permissions(role)
                
                self.parent.title(f"AWAN HARDWARE - POS SYSTEM - {full_name} ({role.title()})")
                self.refresh_sidebar()
                self.show_default_view()
                
        except Exception as e:
            print(f"Error refreshing user session: {e}")

    def logout(self):
        """Handle the logout process - GO BACK TO LOGIN SCREEN"""
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            # Clear all content
            self.clear_content()
            self.module_instances.clear()
            
            # IMPORTANT: Call show_login_screen on the login_root (LoginWindow instance)
            if hasattr(self, 'login_root') and self.login_root:
                try:
                    # This should call the show_login_screen method of LoginWindow
                    self.login_root.show_login_screen()
                except Exception as e:
                    print(f"Error during logout: {e}")
# import tkinter as tk
# from tkinter import ttk, messagebox
# from frontend.dashboard import Dashboard
# from frontend.inventory_management import InventoryManagement
# from frontend.sale_pos import SalePOS
# from frontend.sale_management import SaleManagement
# from frontend.stock_report import StockReport
# from frontend.udhar_management import UdharManagement

# class MainWindow:
#     def __init__(self, parent, user_session):
#         self.parent = parent
#         self.user_session = user_session
#         self.current_content = None
#         self.login_root = None
#         self.sale_pos_instance = None  # Track SalePOS instance
        
#         self.setup_ui()
#         # Force refresh sidebar immediately after login
#         self.refresh_sidebar()
#         # Show appropriate default view based on user role
#         self.show_default_view()
    
#     def setup_ui(self):
#         self.parent.title("AWAN HARDWARE - POS SYSTEM")
#         self.parent.geometry("1400x800")
#         self.parent.configure(bg='#ecf0f1')
        
#         # Main container for sidebar and content
#         main_container = tk.Frame(self.parent, bg='#ecf0f1')
#         main_container.pack(fill=tk.BOTH, expand=True)
        
#         # Sidebar
#         self.sidebar = tk.Frame(main_container, bg='#34495e', width=250)
#         self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
#         self.sidebar.pack_propagate(False)
        
#         # Content area
#         self.content_area = tk.Frame(main_container, bg='#ecf0f1')
#         self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
#     def refresh_sidebar(self):
#         """Refresh sidebar content"""
#         self.create_sidebar_content()
    
#     def create_sidebar_content(self):
#         """Create sidebar content"""
#         # Clear any existing content in the sidebar first
#         for widget in self.sidebar.winfo_children():
#             widget.destroy()
            
#         # --- TOP: User Info ---
#         user_frame = tk.Frame(self.sidebar, bg='#2c3e50', pady=15)
#         user_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        
#         tk.Label(
#             user_frame,
#             text=f"👤 {self.user_session['full_name']}",
#             font=('Arial', 12, 'bold'),
#             fg='white',
#             bg='#2c3e50'
#         ).pack(anchor='w')
        
#         tk.Label(
#             user_frame,
#             text=f"Role: {self.user_session['role'].title()}",
#             font=('Arial', 10),
#             fg='#bdc3c7',
#             bg='#2c3e50'
#         ).pack(anchor='w', pady=(5, 0))

#         # --- MIDDLE: Navigation Buttons ---
#         nav_container = tk.Frame(self.sidebar, bg='#34495e')
#         nav_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
#         ttk.Separator(nav_container, orient='horizontal').pack(fill=tk.X, pady=(0, 10))
        
#         self.create_navigation_buttons(nav_container)

#         # --- BOTTOM: Sidebar Footer with Settings and Logout Button ---
#         sidebar_footer = tk.Frame(self.sidebar, bg='#2c3e50', height=80)
#         sidebar_footer.pack(side=tk.BOTTOM, fill=tk.X)
#         sidebar_footer.pack_propagate(False)
        
#         ttk.Separator(self.sidebar, orient='horizontal').pack(fill=tk.X, side=tk.BOTTOM, before=sidebar_footer)
        
#         # Settings Button
#         settings_btn = tk.Button(
#             sidebar_footer,
#             text="⚙️ Settings",
#             font=('Arial', 11, 'bold'),
#             bg='#34495e',
#             fg='white',
#             activebackground='#2c3e50',
#             activeforeground='white',
#             relief='flat',
#             bd=0,
#             cursor='hand2',
#             command=self.show_settings
#         )
#         settings_btn.pack(fill=tk.X, padx=10, pady=(10, 5))
        
#         # Logout Button
#         logout_btn = tk.Button(
#             sidebar_footer,
#             text="🚪 Logout",
#             font=('Arial', 11, 'bold'),
#             bg='#c0392b',
#             fg='white',
#             activebackground='#a93226',
#             activeforeground='white',
#             relief='flat',
#             bd=0,
#             cursor='hand2',
#             command=self.logout
#         )
#         logout_btn.pack(fill=tk.X, padx=10, pady=(0, 10))
    
#     def show_default_view(self):
#         """Show appropriate default view based on user permissions"""
#         permissions = self.user_session['permissions']
        
#         if 'dashboard' in permissions:
#             self.show_dashboard()
#         elif 'point_of_sale' in permissions:
#             self.show_pos()
#         elif 'inventory_management' in permissions:
#             self.show_inventory()
#         else:
#             # If no specific permissions, show the first available module
#             if permissions:
#                 first_module = permissions[0]
#                 if first_module == 'dashboard':
#                     self.show_dashboard()
#                 elif first_module == 'point_of_sale':
#                     self.show_pos()
#                 elif first_module == 'inventory_management':
#                     self.show_inventory()
#                 elif first_module == 'sale_report':
#                     self.show_sales_report()
#                 elif first_module == 'stock_report':
#                     self.show_stock_report()
#                 elif first_module == 'udhar_management':
#                     self.show_udhar()
#             else:
#                 # Fallback: show empty content with message
#                 self.clear_content()
#                 message_label = tk.Label(
#                     self.content_area,
#                     text="No modules available for your role. Please contact administrator.",
#                     font=('Arial', 14),
#                     fg='#7f8c8d',
#                     bg='#ecf0f1'
#                 )
#                 message_label.pack(expand=True)
    
#     def create_navigation_buttons(self, parent_frame):
#         """Create navigation buttons based on user permissions"""
#         # Define all modules with their display names and icons
#         all_modules = {
#             'dashboard': ('📊 Dashboard', self.show_dashboard),
#             'inventory_management': ('📦 Inventory Management', self.show_inventory),
#             'point_of_sale': ('💰 Point Of Sale', self.show_pos),
#             'sale_report': ('📈 Sales Report', self.show_sales_report),
#             'stock_report': ('📋 Stock Report', self.show_stock_report),
#             'udhar_management': ('💳 Udhar Management', self.show_udhar)
#         }
        
#         # Get user's permitted modules
#         user_permissions = self.user_session['permissions']
        
#         # Create buttons only for permitted modules
#         buttons_created = 0
#         for module_key in user_permissions:
#             if module_key in all_modules:
#                 display_name, command = all_modules[module_key]
                
#                 btn = tk.Button(
#                     parent_frame,
#                     text=display_name,
#                     font=('Arial', 11),
#                     bg='#34495e',
#                     fg='white',
#                     relief='flat',
#                     anchor='w',
#                     command=lambda cmd=command: [self.clear_content(), cmd()],
#                     cursor='hand2',
#                     padx=10,
#                     pady=8
#                 )
#                 btn.pack(fill=tk.X, pady=5)
#                 buttons_created += 1
        
#         # If no buttons were created, show a message
#         if buttons_created == 0:
#             no_access_label = tk.Label(
#                 parent_frame,
#                 text="No modules available",
#                 font=('Arial', 10),
#                 fg='#bdc3c7',
#                 bg='#34495e'
#             )
#             no_access_label.pack(pady=20)
            
#             contact_label = tk.Label(
#                 parent_frame,
#                 text="Contact administrator",
#                 font=('Arial', 9),
#                 fg='#95a5a6',
#                 bg='#34495e'
#             )
#             contact_label.pack()
    
#     def clear_content(self):
#         """Clear the content area completely and destroy any SalePOS instances"""
#         # Destroy all existing widgets in the content area
#         for widget in self.content_area.winfo_children():
#             widget.destroy()
        
#         # Clear any SalePOS instance reference
#         self.sale_pos_instance = None
#         self.current_content = None
    
#     def show_dashboard(self):
#         if 'dashboard' in self.user_session['permissions']:
#             self.clear_content()
#             self.current_content = Dashboard(self.content_area)
    
#     def show_inventory(self):
#         if 'inventory_management' in self.user_session['permissions']:
#             self.clear_content()
#             self.current_content = InventoryManagement(self.content_area, self.user_session)
    
#     def show_pos(self):
#         if 'point_of_sale' in self.user_session['permissions']:
#             self.clear_content()
            
#             # Create only one instance of SalePOS and reuse it
#             if self.sale_pos_instance is None:
#                 self.sale_pos_instance = SalePOS(self.content_area)
#                 self.current_content = self.sale_pos_instance
#             else:
#                 # If instance exists, just repack it
#                 self.current_content = self.sale_pos_instance
#                 if hasattr(self.current_content, 'main_frame'):
#                     self.current_content.main_frame.pack(fill=tk.BOTH, expand=True)
    
#     def show_sales_report(self):
#         if 'sale_report' in self.user_session['permissions']:
#             self.clear_content()
#             self.current_content = SaleManagement(self.content_area)
    
#     def show_stock_report(self):
#         if 'stock_report' in self.user_session['permissions']:
#             self.clear_content()
#             self.current_content = StockReport(self.content_area)
    
#     def show_udhar(self):
#         if 'udhar_management' in self.user_session['permissions']:
#             self.clear_content()
#             self.current_content = UdharManagement(self.content_area)
    
#     def show_settings(self):
#         """Show settings window"""
#         try:
#             from frontend.settings_window import SettingsWindow
#             SettingsWindow(self.parent, self.user_session, self.refresh_user_session)
#         except ImportError as e:
#             messagebox.showerror("Error", f"Settings module not available: {str(e)}")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to open settings: {str(e)}")
    
#     def refresh_user_session(self):
#         """Refresh user session data after changes (like role/permission updates)"""
#         try:
#             from backend.database import Database
#             db = Database()
            
#             # Get updated user data
#             user_data = db.get_user_by_id(self.user_session['user_id'])
#             if user_data:
#                 user_id, username, role, full_name, phone, is_active, created_at, last_login = user_data
                
#                 # Update user session with new data
#                 self.user_session['username'] = username
#                 self.user_session['role'] = role
#                 self.user_session['full_name'] = full_name
#                 self.user_session['phone'] = phone
#                 self.user_session['permissions'] = db.get_user_permissions(role)
                
#                 # Update window title
#                 self.parent.title(f"AWAN HARDWARE - POS SYSTEM - {full_name} ({role.title()})")
                
#                 # Refresh sidebar to show/hide modules based on new permissions
#                 self.refresh_sidebar()
                
#                 # Show appropriate default view based on new permissions
#                 self.show_default_view()
                
#         except Exception as e:
#             print(f"Error refreshing user session: {e}")
    
#     def logout(self):
#         """Handle the logout process - FIXED to properly clean up"""
#         result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
#         if result:
#             # Clear all content and instances first
#             self.clear_content()
            
#             # Destroy the main window
#             self.parent.destroy()
            
#             # Show the login window using the login_root reference
#             if hasattr(self, 'login_root') and self.login_root:
#                 try:
#                     # Clear any existing main window references
#                     if hasattr(self.login_root, 'main_root'):
#                         self.login_root.main_root = None
                    
#                     # Call the show_login_screen method if it exists
#                     if hasattr(self.login_root, 'show_login_screen'):
#                         self.login_root.show_login_screen()
#                     else:
#                         # Fallback: manually show and reset the login window
#                         self.login_root.deiconify()
#                         try:
#                             self.login_root.state('zoomed')
#                         except:
#                             self.login_root.attributes('-zoomed', True)
                        
#                         # Clear login fields
#                         if hasattr(self.login_root, 'username_input'):
#                             self.login_root.username_input.delete(0, tk.END)
#                         if hasattr(self.login_root, 'password_input'):
#                             self.login_root.password_input.delete(0, tk.END)
                        
#                         # Reset login button
#                         if hasattr(self.login_root, 'login_btn'):
#                             self.login_root.login_btn.config(text="LOGIN", state='normal', bg='#27ae60')
                        
#                         # Focus username field
#                         if hasattr(self.login_root, 'username_input'):
#                             self.login_root.username_input.focus()
                            
#                 except Exception as e:
#                     print(f"Error showing login screen: {e}")