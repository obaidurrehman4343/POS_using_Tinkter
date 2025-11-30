import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.settings_service import SettingsService
import os
from datetime import datetime
import shutil
import glob

class SettingsWindow:
    def __init__(self, parent, user_session=None, dashboard_callback=None):
        self.parent = parent
        self.user_session = user_session
        self.dashboard_callback = dashboard_callback
        self.settings_service = SettingsService()
        
        # Initialize variables
        self.content_frame = None
        self.backups_list_backup_files = []
        self.recovery_status = None
        self.backups_listbox = None
        
        # Initialize tkinter variables
        self.backup_interval_var = tk.StringVar()
        self.backup_path_var = tk.StringVar()
        
        # Modern color palette
        self.colors = {
            'primary': '#3b82f6',
            'primary_dark': '#1e40af',
            'success': '#10b981',
            'danger': '#ef4444',
            'warning': '#f59e0b',
            'info': '#06b6d4',
            'dark': '#1f2937',
            'light': '#f8fafc',
            'background': '#f9fafb',
            'white': '#ffffff',
            'gray': '#6b7280',
            'light_gray': '#e5e7eb',
            'border': '#d1d5db'
        }
        
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup beautiful full-page settings window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Settings - AWAN HARDWARE")
        self.window.geometry("900x700")
        self.window.configure(bg=self.colors['background'])
        self.window.resizable(True, True)
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Make it full-page
        self.window.state('zoomed')
        
        # Main container with modern layout
        self.main_frame = tk.Frame(self.window, bg=self.colors['background'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Create modern header
        self.create_modern_header()
        
        # Create content area with sidebar navigation
        self.create_content_area()
        
        # Center window
        self.center_window()
    
    def create_modern_header(self):
        """Create modern header with back button and title"""
        header_frame = tk.Frame(self.main_frame, bg=self.colors['white'], height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=self.colors['white'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        
        # Back button with modern style
        back_btn = tk.Button(
            header_content,
            text="← Back to Dashboard",
            font=('Arial', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.go_to_dashboard,
            padx=20,
            pady=10,
            bd=0
        )
        back_btn.pack(side=tk.LEFT)
        
        # Title
        tk.Label(
            header_content,
            text="SYSTEM SETTINGS & SECURITY",
            font=('Arial', 20, 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['white']
        ).pack(side=tk.RIGHT)
    
    def create_content_area(self):
        """Create content area with sidebar navigation"""
        content_container = tk.Frame(self.main_frame, bg=self.colors['background'])
        content_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Sidebar navigation
        self.create_sidebar(content_container)
        
        # Main content area
        self.content_frame = tk.Frame(content_container, bg=self.colors['white'], relief='solid', bd=1)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Show default tab
        self.show_backup_tab()
    
    def create_sidebar(self, parent):
        """Create modern sidebar navigation"""
        sidebar_frame = tk.Frame(parent, bg=self.colors['white'], width=250, relief='solid', bd=1)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        sidebar_frame.pack_propagate(False)
        
        # Sidebar content
        sidebar_content = tk.Frame(sidebar_frame, bg=self.colors['white'])
        sidebar_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=30)
        
        # Navigation title
        tk.Label(
            sidebar_content,
            text="Settings Menu",
            font=('Arial', 16, 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['white']
        ).pack(anchor='w', pady=(0, 30))
        
        # Navigation items
        nav_items = [
            ("💾 Backup & Restore", self.show_backup_tab),
            ("🔄 Data Recovery", self.show_recovery_tab),
            ("👥 User Management", self.show_user_management_tab)
        ]
        
        self.nav_buttons = {}
        for text, command in nav_items:
            btn = tk.Button(
                sidebar_content,
                text=text,
                font=('Arial', 12),
                bg=self.colors['white'],
                fg=self.colors['dark'],
                relief='flat',
                anchor='w',
                cursor='hand2',
                command=command,
                padx=15,
                pady=12,
                width=20
            )
            btn.pack(fill=tk.X, pady=5)
            self.nav_buttons[text] = btn
    
    def show_backup_tab(self):
        """Show backup and restore tab"""
        self.clear_content()
        self.update_nav_buttons("💾 Backup & Restore")
        
        content = tk.Frame(self.content_frame, bg=self.colors['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        tk.Label(
            content,
            text="💾 Backup & Restore",
            font=('Arial', 18, 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['white']
        ).pack(anchor='w', pady=(0, 30))
        
        # Backup settings card
        backup_card = self.create_setting_card(content, "Auto Backup Configuration")
        
        # Backup interval
        interval_frame = tk.Frame(backup_card, bg=self.colors['white'])
        interval_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            interval_frame,
            text="Auto-backup Frequency:",
            font=('Arial', 11, 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['white'],
            width=20,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        interval_combo = ttk.Combobox(
            interval_frame,
            textvariable=self.backup_interval_var,
            values=["Disabled", "Daily", "Weekly", "Monthly"],
            state="readonly",
            font=('Arial', 11),
            width=15
        )
        interval_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Backup path
        path_frame = tk.Frame(backup_card, bg=self.colors['white'])
        path_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            path_frame,
            text="Backup Location:",
            font=('Arial', 11, 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['white'],
            width=20,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        path_entry = tk.Entry(
            path_frame,
            textvariable=self.backup_path_var,
            font=('Arial', 11),
            width=40
        )
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10), ipady=4)
        
        browse_btn = tk.Button(
            path_frame,
            text="Browse",
            font=('Arial', 10),
            bg=self.colors['info'],
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.browse_backup_path
        )
        browse_btn.pack(side=tk.LEFT)
        
        # Auto-save settings when changed
        interval_combo.bind('<<ComboboxSelected>>', self.auto_save_backup_settings)
        self.backup_path_var.trace('w', self.auto_save_backup_settings)
        
        # Manual backup section
        manual_card = self.create_setting_card(content, "Manual Backup")
        
        # Backup button
        backup_btn = tk.Button(
            manual_card,
            text="💾 Create Backup Now",
            font=('Arial', 12, 'bold'),
            bg=self.colors['success'],
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.manual_backup,
            padx=30,
            pady=15
        )
        backup_btn.pack(anchor='w', pady=10)
        
        # Status label
        self.backup_status_label = tk.Label(
            manual_card,
            text="Ready to create backup",
            font=('Arial', 10),
            fg=self.colors['gray'],
            bg=self.colors['white']
        )
        self.backup_status_label.pack(anchor='w')

    def show_recovery_tab(self):
        """Show data recovery tab"""
        self.clear_content()
        self.update_nav_buttons("🔄 Data Recovery")
        
        content = tk.Frame(self.content_frame, bg=self.colors['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        tk.Label(
            content,
            text="🔄 Data Recovery",
            font=('Arial', 18, 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['white']
        ).pack(anchor='w', pady=(0, 20))
        
        # Recovery card
        recovery_card = self.create_setting_card(content, "Database Recovery Center")
        
        # Description
        tk.Label(
            recovery_card,
            text="Restore your data from backup files in case of system crash or data loss.",
            font=('Arial', 11),
            fg=self.colors['gray'],
            bg=self.colors['white']
        ).pack(anchor='w', pady=(0, 20))
        
        # Available backups section
        backups_frame = tk.Frame(recovery_card, bg=self.colors['white'])
        backups_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            backups_frame,
            text="Available Backups:",
            font=('Arial', 12, 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['white']
        ).pack(anchor='w', pady=(0, 10))
        
        # Listbox for backups with scrollbar
        list_frame = tk.Frame(backups_frame, bg=self.colors['white'])
        list_frame.pack(fill=tk.X, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.backups_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=('Arial', 10),
            height=8,
            selectmode=tk.SINGLE
        )
        self.backups_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.backups_listbox.yview)
        
        # Recovery buttons frame
        buttons_frame = tk.Frame(recovery_card, bg=self.colors['white'])
        buttons_frame.pack(fill=tk.X, pady=20)
        
        # Restore button
        restore_btn = tk.Button(
            buttons_frame,
            text="🔄 Restore Selected Backup",
            font=('Arial', 12, 'bold'),
            bg=self.colors['success'],
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.restore_selected_backup,
            padx=20,
            pady=10
        )
        restore_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Refresh button
        refresh_btn = tk.Button(
            buttons_frame,
            text="🔄 Refresh List",
            font=('Arial', 10),
            bg=self.colors['info'],
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.load_available_backups,
            padx=15,
            pady=8
        )
        refresh_btn.pack(side=tk.LEFT)
        
        # Status label
        self.recovery_status = tk.Label(
            recovery_card,
            text="Select a backup and click 'Restore' to recover your data",
            font=('Arial', 10),
            fg=self.colors['gray'],
            bg=self.colors['white'],
            wraplength=600
        )
        self.recovery_status.pack(anchor='w', pady=10)
        
        # Warning label
        warning_label = tk.Label(
            recovery_card,
            text="⚠️ Warning: This will replace your current database. Make sure to backup current data first!",
            font=('Arial', 10, 'bold'),
            fg=self.colors['danger'],
            bg=self.colors['white'],
            wraplength=600
        )
        warning_label.pack(anchor='w', pady=10)
        
        # Load available backups
        self.load_available_backups()

    def show_user_management_tab(self):
        """Show user management tab"""
        self.clear_content()
        self.update_nav_buttons("👥 User Management")
        
        content = tk.Frame(self.content_frame, bg=self.colors['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        tk.Label(
            content,
            text="👥 User Management",
            font=('Arial', 18, 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['white']
        ).pack(anchor='w', pady=(0, 20))
        
        # Description
        tk.Label(
            content,
            text="Manage system users, roles, and permissions",
            font=('Arial', 12),
            fg=self.colors['gray'],
            bg=self.colors['white']
        ).pack(anchor='w', pady=(0, 30))
        
        # User management card
        user_card = self.create_setting_card(content, "User Accounts Management")
        
        # Description
        tk.Label(
            user_card,
            text="Add, edit, or remove user accounts. Manage roles and permissions.",
            font=('Arial', 11),
            fg=self.colors['gray'],
            bg=self.colors['white']
        ).pack(anchor='w', pady=(0, 20))
        
        # Open user management button
        manage_btn = tk.Button(
            user_card,
            text="👥 Open User Management",
            font=('Arial', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.open_user_management,
            padx=30,
            pady=15
        )
        manage_btn.pack(anchor='w')

    def load_available_backups(self):
        """Load all available backup files"""
        try:
            # Clear current list
            if self.backups_listbox:
                self.backups_listbox.delete(0, tk.END)
            
            self.backups_list_backup_files.clear()
            
            # Look for backup files
            backup_locations = [
                '.',
                'backup',
                'backups',
                self.settings_service.get_backup_directory()
            ]
            
            backup_files = []
            
            for location in backup_locations:
                if os.path.exists(location):
                    for file in os.listdir(location):
                        if file.startswith('awan_hardware_backup_') and file.endswith('.db'):
                            full_path = os.path.join(location, file)
                            backup_files.append(full_path)
            
            # Sort by modification time (newest first)
            backup_files.sort(key=os.path.getmtime, reverse=True)
            
            if not backup_files:
                if self.backups_listbox:
                    self.backups_listbox.insert(tk.END, "No backup files found!")
                if self.recovery_status:
                    self.recovery_status.config(text="No backup files found in the application directory.")
                return
            
            # Add backups to listbox
            for backup_file in backup_files:
                file_name = os.path.basename(backup_file)
                file_time = datetime.fromtimestamp(os.path.getmtime(backup_file))
                file_size = os.path.getsize(backup_file) / (1024 * 1024)
                
                display_text = f"{file_name} ({file_time.strftime('%Y-%m-%d %H:%M')}) - {file_size:.2f} MB"
                if self.backups_listbox:
                    self.backups_listbox.insert(tk.END, display_text)
                self.backups_list_backup_files.append(backup_file)
            
            if self.recovery_status:
                self.recovery_status.config(text=f"Found {len(backup_files)} backup file(s). Select one to restore.")
            
        except Exception as e:
            if self.recovery_status:
                self.recovery_status.config(text=f"Error loading backups: {str(e)}")

    def restore_selected_backup(self):
        """Restore the selected backup file"""
        try:
            if not self.backups_listbox:
                messagebox.showerror("Error", "Backup list not initialized")
                return
                
            selection = self.backups_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a backup file to restore.")
                return
            
            # Confirm restoration
            confirm = messagebox.askyesno(
                "Confirm Restoration",
                "⚠️ This will replace your current database with the selected backup.\n\n"
                "All current data will be lost and replaced with the backup data.\n\n"
                "Are you sure you want to continue?",
                icon='warning'
            )
            
            if not confirm:
                return
            
            selected_index = selection[0]
            if selected_index >= len(self.backups_list_backup_files):
                messagebox.showerror("Error", "Invalid backup selection")
                return
                
            backup_file_path = self.backups_list_backup_files[selected_index]
            
            if self.recovery_status:
                self.recovery_status.config(text="Restoring backup... Please wait.")
            self.window.update()
            
            # Create backup of current database first
            current_db = 'awan_hardware.db'
            if os.path.exists(current_db):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                safety_backup = f'pre_restore_backup_{timestamp}.db'
                shutil.copy2(current_db, safety_backup)
            
            # Perform the restoration
            shutil.copy2(backup_file_path, current_db)
            
            if self.recovery_status:
                self.recovery_status.config(text="✅ Recovery successful! Please restart the application.")
            
            messagebox.showinfo(
                "Recovery Complete",
                "✅ Database restored successfully!\n\n"
                "Please restart the application to use the recovered data."
            )
            
        except Exception as e:
            if self.recovery_status:
                self.recovery_status.config(text=f"❌ Recovery failed: {str(e)}")
            messagebox.showerror("Recovery Error", f"Failed to restore backup:\n{str(e)}")

    def open_user_management(self):
        """Open user management dialog"""
        try:
            from frontend.user_management_dialog import UserManagementDialog
            UserManagementDialog(self.window, self.user_session)
        except ImportError as e:
            messagebox.showerror("Error", f"User management module not available: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open user management: {str(e)}")

    def create_setting_card(self, parent, title):
        """Create a modern setting card"""
        card = tk.Frame(parent, bg=self.colors['light_gray'], relief='flat', bd=0)
        card.pack(fill=tk.X, pady=(0, 20))
        
        content = tk.Frame(card, bg=self.colors['white'], relief='solid', bd=1)
        content.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        inner_content = tk.Frame(content, bg=self.colors['white'])
        inner_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Card title
        tk.Label(
            inner_content,
            text=title,
            font=('Arial', 14, 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['white']
        ).pack(anchor='w', pady=(0, 15))
        
        return inner_content

    def update_nav_buttons(self, active_tab):
        """Update navigation buttons state"""
        for text, btn in self.nav_buttons.items():
            if text == active_tab:
                btn.config(bg=self.colors['primary'], fg='white')
            else:
                btn.config(bg=self.colors['white'], fg=self.colors['dark'])

    def clear_content(self):
        """Clear main content area"""
        if self.content_frame:
            for widget in self.content_frame.winfo_children():
                widget.destroy()
        
        # Reset UI elements when content is cleared
        self.recovery_status = None
        self.backups_listbox = None

    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def go_to_dashboard(self):
        """Return to dashboard"""
        if self.dashboard_callback:
            self.window.destroy()
            self.dashboard_callback()
        else:
            self.window.destroy()

    def load_settings(self):
        """Load settings from database"""
        try:
            # Load backup settings
            backup_interval = self.settings_service.get_setting('backup_interval', 'Disabled')
            backup_path = self.settings_service.get_setting('backup_path', os.path.expanduser('~/awan_hardware/backups'))
            
            self.backup_interval_var.set(backup_interval)
            self.backup_path_var.set(backup_path)
            
        except Exception as e:
            pass

    def auto_save_backup_settings(self, *args):
        """Automatically save backup settings when changed"""
        try:
            self.settings_service.set_setting('backup_interval', self.backup_interval_var.get())
            self.settings_service.set_setting('backup_path', self.backup_path_var.get())
        except Exception as e:
            pass

    def browse_backup_path(self):
        """Browse for backup directory"""
        path = filedialog.askdirectory(
            title="Select Backup Directory",
            initialdir=self.backup_path_var.get()
        )
        if path:
            self.backup_path_var.set(path)

    def manual_backup(self):
        """Perform manual database backup to fixed location"""
        try:
            self.backup_status_label.config(text="Creating backup in Documents folder...")
            self.window.update()
            
            backup_path = self.settings_service.backup_database(
                user_id=self.user_session['user_id'] if self.user_session else None
            )
            
            if backup_path:
                backup_dir = os.path.dirname(backup_path)
                self.backup_status_label.config(text=f"Backup created in: {backup_dir}")
                messagebox.showinfo("Backup Complete", 
                    f"✅ Database backup created successfully!\n\n"
                    f"📍 Location: {backup_dir}\n\n"
                    f"This backup will be used for automatic recovery if needed.")
            else:
                self.backup_status_label.config(text="Backup failed")
                messagebox.showerror("Error", "Failed to create backup")
                
        except Exception as e:
            self.backup_status_label.config(text="Backup failed")
            messagebox.showerror("Error", f"Failed to create backup: {str(e)}")




# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# from backend.settings_service import SettingsService
# import os
# from datetime import datetime
# import shutil
# import glob

# class SettingsWindow:
#     def __init__(self, parent, user_session=None, dashboard_callback=None):
#         self.parent = parent
#         self.user_session = user_session
#         self.dashboard_callback = dashboard_callback
#         self.settings_service = SettingsService()
        
#         # Initialize variables
#         self.content_frame = None
#         self.backups_list_backup_files = []  # Store backup file paths
#         self.recovery_status = None  # Initialize as None
#         self.backups_listbox = None  # Initialize as None
        
#         # Initialize tkinter variables
#         self.backup_interval_var = tk.StringVar()
#         self.backup_path_var = tk.StringVar()
        
#         # Modern color palette
#         self.colors = {
#             'primary': '#3b82f6',
#             'primary_dark': '#1e40af',
#             'success': '#10b981',
#             'danger': '#ef4444',
#             'warning': '#f59e0b',
#             'info': '#06b6d4',
#             'dark': '#1f2937',
#             'light': '#f8fafc',
#             'background': '#f9fafb',
#             'white': '#ffffff',
#             'gray': '#6b7280',
#             'light_gray': '#e5e7eb',
#             'border': '#d1d5db'
#         }
        
#         self.setup_ui()
#         self.load_settings()
    
#     def setup_ui(self):
#         """Setup beautiful full-page settings window"""
#         self.window = tk.Toplevel(self.parent)
#         self.window.title("Settings - AWAN HARDWARE")
#         self.window.geometry("900x700")
#         self.window.configure(bg=self.colors['background'])
#         self.window.resizable(True, True)
#         self.window.transient(self.parent)
#         self.window.grab_set()
        
#         # Make it full-page
#         self.window.state('zoomed')
        
#         # Main container with modern layout
#         self.main_frame = tk.Frame(self.window, bg=self.colors['background'])
#         self.main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
#         # Create modern header
#         self.create_modern_header()
        
#         # Create content area with sidebar navigation
#         self.create_content_area()
        
#         # Center window
#         self.center_window()
    
#     def create_modern_header(self):
#         """Create modern header with back button and title"""
#         header_frame = tk.Frame(self.main_frame, bg=self.colors['white'], height=80)
#         header_frame.pack(fill=tk.X, padx=0, pady=0)
#         header_frame.pack_propagate(False)
        
#         header_content = tk.Frame(header_frame, bg=self.colors['white'])
#         header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        
#         # Back button with modern style
#         back_btn = tk.Button(
#             header_content,
#             text="← Back to Dashboard",
#             font=('Arial', 12, 'bold'),
#             bg=self.colors['primary'],
#             fg='white',
#             relief='flat',
#             cursor='hand2',
#             command=self.go_to_dashboard,
#             padx=20,
#             pady=10,
#             bd=0
#         )
#         back_btn.pack(side=tk.LEFT)
        
#         # Title
#         tk.Label(
#             header_content,
#             text="SYSTEM SETTINGS & SECURITY",
#             font=('Arial', 20, 'bold'),
#             fg=self.colors['dark'],
#             bg=self.colors['white']
#         ).pack(side=tk.RIGHT)
    
#     def create_content_area(self):
#         """Create content area with sidebar navigation"""
#         content_container = tk.Frame(self.main_frame, bg=self.colors['background'])
#         content_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
#         # Sidebar navigation (NOW WITH 3 TABS - ADDED DATA RECOVERY)
#         self.create_sidebar(content_container)
        
#         # Main content area
#         self.content_frame = tk.Frame(content_container, bg=self.colors['white'], relief='solid', bd=1)
#         self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
#         # Show default tab
#         self.show_backup_tab()
    
#     def create_sidebar(self, parent):
#         """Create modern sidebar navigation with 3 tabs (added data recovery)"""
#         sidebar_frame = tk.Frame(parent, bg=self.colors['white'], width=250, relief='solid', bd=1)
#         sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
#         sidebar_frame.pack_propagate(False)
        
#         # Sidebar content
#         sidebar_content = tk.Frame(sidebar_frame, bg=self.colors['white'])
#         sidebar_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=30)
        
#         # Navigation title
#         tk.Label(
#             sidebar_content,
#             text="Settings Menu",
#             font=('Arial', 16, 'bold'),
#             fg=self.colors['dark'],
#             bg=self.colors['white']
#         ).pack(anchor='w', pady=(0, 30))
        
#         # 3 Navigation items (ADDED DATA RECOVERY)
#         nav_items = [
#             ("💾 Backup & Restore", self.show_backup_tab),
#             ("🔄 Data Recovery", self.show_recovery_tab),  # NEW TAB
#             ("👥 User Management", self.show_user_management_tab)
#         ]
        
#         self.nav_buttons = {}
#         for text, command in nav_items:
#             btn = tk.Button(
#                 sidebar_content,
#                 text=text,
#                 font=('Arial', 12),
#                 bg=self.colors['white'],
#                 fg=self.colors['dark'],
#                 relief='flat',
#                 anchor='w',
#                 cursor='hand2',
#                 command=command,
#                 padx=15,
#                 pady=12,
#                 width=20
#             )
#             btn.pack(fill=tk.X, pady=5)
#             self.nav_buttons[text] = btn
    
#     def show_backup_tab(self):
#         """Show backup and restore tab"""
#         self.clear_content()
#         self.update_nav_buttons("💾 Backup & Restore")
        
#         content = tk.Frame(self.content_frame, bg=self.colors['white'])
#         content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
#         # Title
#         tk.Label(
#             content,
#             text="💾 Backup & Restore",
#             font=('Arial', 18, 'bold'),
#             fg=self.colors['dark'],
#             bg=self.colors['white']
#         ).pack(anchor='w', pady=(0, 30))
        
#         # Backup settings card
#         backup_card = self.create_setting_card(content, "Auto Backup Configuration")
        
#         # Backup interval
#         interval_frame = tk.Frame(backup_card, bg=self.colors['white'])
#         interval_frame.pack(fill=tk.X, pady=10)
        
#         tk.Label(
#             interval_frame,
#             text="Auto-backup Frequency:",
#             font=('Arial', 11, 'bold'),
#             fg=self.colors['dark'],
#             bg=self.colors['white'],
#             width=20,
#             anchor='w'
#         ).pack(side=tk.LEFT)
        
#         interval_combo = ttk.Combobox(
#             interval_frame,
#             textvariable=self.backup_interval_var,
#             values=["Disabled", "Daily", "Weekly", "Monthly"],
#             state="readonly",
#             font=('Arial', 11),
#             width=15
#         )
#         interval_combo.pack(side=tk.LEFT, padx=(10, 0))
        
#         # Backup path
#         path_frame = tk.Frame(backup_card, bg=self.colors['white'])
#         path_frame.pack(fill=tk.X, pady=10)
        
#         tk.Label(
#             path_frame,
#             text="Backup Location:",
#             font=('Arial', 11, 'bold'),
#             fg=self.colors['dark'],
#             bg=self.colors['white'],
#             width=20,
#             anchor='w'
#         ).pack(side=tk.LEFT)
        
#         path_entry = tk.Entry(
#             path_frame,
#             textvariable=self.backup_path_var,
#             font=('Arial', 11),
#             width=40
#         )
#         path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10), ipady=4)
        
#         browse_btn = tk.Button(
#             path_frame,
#             text="Browse",
#             font=('Arial', 10),
#             bg=self.colors['info'],
#             fg='white',
#             relief='flat',
#             cursor='hand2',
#             command=self.browse_backup_path
#         )
#         browse_btn.pack(side=tk.LEFT)
        
#         # Auto-save settings when changed
#         interval_combo.bind('<<ComboboxSelected>>', self.auto_save_backup_settings)
#         self.backup_path_var.trace('w', self.auto_save_backup_settings)
        
#         # Manual backup section
#         manual_card = self.create_setting_card(content, "Manual Backup")
        
#         # Backup button
#         backup_btn = tk.Button(
#             manual_card,
#             text="💾 Create Backup Now",
#             font=('Arial', 12, 'bold'),
#             bg=self.colors['success'],
#             fg='white',
#             relief='flat',
#             cursor='hand2',
#             command=self.manual_backup,
#             padx=30,
#             pady=15
#         )
#         backup_btn.pack(anchor='w', pady=10)
        
#         # Status label
#         self.backup_status_label = tk.Label(
#             manual_card,
#             text="Ready to create backup",
#             font=('Arial', 10),
#             fg=self.colors['gray'],
#             bg=self.colors['white']
#         )
#         self.backup_status_label.pack(anchor='w')

#     def show_recovery_tab(self):
#         """Show data recovery tab - FIXED VERSION"""
#         self.clear_content()
#         self.update_nav_buttons("🔄 Data Recovery")
        
#         content = tk.Frame(self.content_frame, bg=self.colors['white'])
#         content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
#         # Title
#         tk.Label(
#             content,
#             text="🔄 Data Recovery",
#             font=('Arial', 18, 'bold'),
#             fg=self.colors['dark'],
#             bg=self.colors['white']
#         ).pack(anchor='w', pady=(0, 20))
        
#         # Recovery card
#         recovery_card = self.create_setting_card(content, "Database Recovery Center")
        
#         # Description
#         tk.Label(
#             recovery_card,
#             text="Restore your data from backup files in case of system crash or data loss.",
#             font=('Arial', 11),
#             fg=self.colors['gray'],
#             bg=self.colors['white']
#         ).pack(anchor='w', pady=(0, 20))
        
#         # Available backups section
#         backups_frame = tk.Frame(recovery_card, bg=self.colors['white'])
#         backups_frame.pack(fill=tk.X, pady=10)
        
#         tk.Label(
#             backups_frame,
#             text="Available Backups:",
#             font=('Arial', 12, 'bold'),
#             fg=self.colors['dark'],
#             bg=self.colors['white']
#         ).pack(anchor='w', pady=(0, 10))
        
#         # Listbox for backups with scrollbar
#         list_frame = tk.Frame(backups_frame, bg=self.colors['white'])
#         list_frame.pack(fill=tk.X, pady=5)
        
#         scrollbar = ttk.Scrollbar(list_frame)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
#         self.backups_listbox = tk.Listbox(
#             list_frame,
#             yscrollcommand=scrollbar.set,
#             font=('Arial', 10),
#             height=8,
#             selectmode=tk.SINGLE
#         )
#         self.backups_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         scrollbar.config(command=self.backups_listbox.yview)
        
#         # Recovery buttons frame
#         buttons_frame = tk.Frame(recovery_card, bg=self.colors['white'])
#         buttons_frame.pack(fill=tk.X, pady=20)
        
#         # Restore button
#         restore_btn = tk.Button(
#             buttons_frame,
#             text="🔄 Restore Selected Backup",
#             font=('Arial', 12, 'bold'),
#             bg=self.colors['success'],
#             fg='white',
#             relief='flat',
#             cursor='hand2',
#             command=self.restore_selected_backup,
#             padx=20,
#             pady=10
#         )
#         restore_btn.pack(side=tk.LEFT, padx=(0, 10))
        
#         # Refresh button
#         refresh_btn = tk.Button(
#             buttons_frame,
#             text="🔄 Refresh List",
#             font=('Arial', 10),
#             bg=self.colors['info'],
#             fg='white',
#             relief='flat',
#             cursor='hand2',
#             command=self.load_available_backups,
#             padx=15,
#             pady=8
#         )
#         refresh_btn.pack(side=tk.LEFT)
        
#         # Status label - THIS IS THE KEY FIX: Create and assign to self.recovery_status
#         self.recovery_status = tk.Label(
#             recovery_card,
#             text="Select a backup and click 'Restore' to recover your data",
#             font=('Arial', 10),
#             fg=self.colors['gray'],
#             bg=self.colors['white'],
#             wraplength=600
#         )
#         self.recovery_status.pack(anchor='w', pady=10)
        
#         # Warning label
#         warning_label = tk.Label(
#             recovery_card,
#             text="⚠️ Warning: This will replace your current database. Make sure to backup current data first!",
#             font=('Arial', 10, 'bold'),
#             fg=self.colors['danger'],
#             bg=self.colors['white'],
#             wraplength=600
#         )
#         warning_label.pack(anchor='w', pady=10)
        
#         # Load available backups AFTER creating the status label
#         self.load_available_backups()

#     def show_user_management_tab(self):
#         """Show user management tab"""
#         self.clear_content()
#         self.update_nav_buttons("👥 User Management")
        
#         content = tk.Frame(self.content_frame, bg=self.colors['white'])
#         content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
#         # Title
#         tk.Label(
#             content,
#             text="👥 User Management",
#             font=('Arial', 18, 'bold'),
#             fg=self.colors['dark'],
#             bg=self.colors['white']
#         ).pack(anchor='w', pady=(0, 20))
        
#         # Description
#         tk.Label(
#             content,
#             text="Manage system users, roles, and permissions",
#             font=('Arial', 12),
#             fg=self.colors['gray'],
#             bg=self.colors['white']
#         ).pack(anchor='w', pady=(0, 30))
        
#         # User management card
#         user_card = self.create_setting_card(content, "User Accounts Management")
        
#         # Description
#         tk.Label(
#             user_card,
#             text="Add, edit, or remove user accounts. Manage roles and permissions.",
#             font=('Arial', 11),
#             fg=self.colors['gray'],
#             bg=self.colors['white']
#         ).pack(anchor='w', pady=(0, 20))
        
#         # Open user management button
#         manage_btn = tk.Button(
#             user_card,
#             text="👥 Open User Management",
#             font=('Arial', 12, 'bold'),
#             bg=self.colors['primary'],
#             fg='white',
#             relief='flat',
#             cursor='hand2',
#             command=self.open_user_management,
#             padx=30,
#             pady=15
#         )
#         manage_btn.pack(anchor='w')

#     def load_available_backups(self):
#         """Load all available backup files - FIXED VERSION"""
#         try:
#             # Clear current list
#             if self.backups_listbox:
#                 self.backups_listbox.delete(0, tk.END)
            
#             self.backups_list_backup_files.clear()
            
#             # Look for backup files in current directory and backup folder
#             backup_locations = [
#                 '.',  # Current directory
#                 'backup',
#                 'backups',
#                 self.settings_service.get_backup_directory()  # Use the fixed backup directory
#             ]
            
#             backup_files = []
            
#             for location in backup_locations:
#                 if os.path.exists(location):
#                     for file in os.listdir(location):
#                         if file.startswith('awan_hardware_backup_') and file.endswith('.db'):
#                             full_path = os.path.join(location, file)
#                             backup_files.append(full_path)
            
#             # Sort by modification time (newest first)
#             backup_files.sort(key=os.path.getmtime, reverse=True)
            
#             if not backup_files:
#                 if self.backups_listbox:
#                     self.backups_listbox.insert(tk.END, "No backup files found!")
#                 if self.recovery_status:
#                     self.recovery_status.config(text="No backup files found in the application directory.")
#                 return
            
#             # Add backups to listbox
#             for backup_file in backup_files:
#                 file_name = os.path.basename(backup_file)
#                 file_time = datetime.fromtimestamp(os.path.getmtime(backup_file))
#                 file_size = os.path.getsize(backup_file) / (1024 * 1024)  # Size in MB
                
#                 display_text = f"{file_name} ({file_time.strftime('%Y-%m-%d %H:%M')}) - {file_size:.2f} MB"
#                 if self.backups_listbox:
#                     self.backups_listbox.insert(tk.END, display_text)
#                 self.backups_list_backup_files.append(backup_file)  # Store actual path
            
#             if self.recovery_status:
#                 self.recovery_status.config(text=f"Found {len(backup_files)} backup file(s). Select one to restore.")
            
#         except Exception as e:
#             error_msg = f"Error loading backups: {str(e)}"
#             print(error_msg)
#             if self.recovery_status:
#                 self.recovery_status.config(text=error_msg)

#     def restore_selected_backup(self):
#         """Restore the selected backup file - FIXED VERSION"""
#         try:
#             if not self.backups_listbox:
#                 messagebox.showerror("Error", "Backup list not initialized")
#                 return
                
#             selection = self.backups_listbox.curselection()
#             if not selection:
#                 messagebox.showwarning("No Selection", "Please select a backup file to restore.")
#                 return
            
#             # Confirm restoration
#             confirm = messagebox.askyesno(
#                 "Confirm Restoration",
#                 "⚠️ This will replace your current database with the selected backup.\n\n"
#                 "All current data will be lost and replaced with the backup data.\n\n"
#                 "Are you sure you want to continue?",
#                 icon='warning'
#             )
            
#             if not confirm:
#                 return
            
#             selected_index = selection[0]
#             if selected_index >= len(self.backups_list_backup_files):
#                 messagebox.showerror("Error", "Invalid backup selection")
#                 return
                
#             backup_file_path = self.backups_list_backup_files[selected_index]
            
#             if self.recovery_status:
#                 self.recovery_status.config(text="Restoring backup... Please wait.")
#             self.window.update()
            
#             # Create backup of current database first
#             current_db = 'awan_hardware.db'
#             if os.path.exists(current_db):
#                 timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#                 safety_backup = f'pre_restore_backup_{timestamp}.db'
#                 shutil.copy2(current_db, safety_backup)
            
#             # Perform the restoration
#             shutil.copy2(backup_file_path, current_db)
            
#             if self.recovery_status:
#                 self.recovery_status.config(text="✅ Recovery successful! Please restart the application.")
            
#             messagebox.showinfo(
#                 "Recovery Complete",
#                 "✅ Database restored successfully!\n\n"
#                 "Please restart the application to use the recovered data."
#             )
            
#         except Exception as e:
#             error_msg = f"❌ Recovery failed: {str(e)}"
#             print(error_msg)
#             if self.recovery_status:
#                 self.recovery_status.config(text=error_msg)
#             messagebox.showerror("Recovery Error", f"Failed to restore backup:\n{str(e)}")

#     def open_user_management(self):
#         """Open user management dialog"""
#         try:
#             from frontend.user_management_dialog import UserManagementDialog
#             UserManagementDialog(self.window, self.user_session)
#         except ImportError as e:
#             messagebox.showerror("Error", f"User management module not available: {str(e)}")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to open user management: {str(e)}")

#     def create_setting_card(self, parent, title):
#         """Create a modern setting card"""
#         card = tk.Frame(parent, bg=self.colors['light_gray'], relief='flat', bd=0)
#         card.pack(fill=tk.X, pady=(0, 20))
        
#         content = tk.Frame(card, bg=self.colors['white'], relief='solid', bd=1)
#         content.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
#         inner_content = tk.Frame(content, bg=self.colors['white'])
#         inner_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
#         # Card title
#         tk.Label(
#             inner_content,
#             text=title,
#             font=('Arial', 14, 'bold'),
#             fg=self.colors['dark'],
#             bg=self.colors['white']
#         ).pack(anchor='w', pady=(0, 15))
        
#         return inner_content

#     def update_nav_buttons(self, active_tab):
#         """Update navigation buttons state"""
#         for text, btn in self.nav_buttons.items():
#             if text == active_tab:
#                 btn.config(bg=self.colors['primary'], fg='white')
#             else:
#                 btn.config(bg=self.colors['white'], fg=self.colors['dark'])

#     def clear_content(self):
#         """Clear main content area"""
#         if self.content_frame:
#             for widget in self.content_frame.winfo_children():
#                 widget.destroy()
        
#         # Reset UI elements when content is cleared
#         self.recovery_status = None
#         self.backups_listbox = None

#     def center_window(self):
#         """Center window on screen"""
#         self.window.update_idletasks()
#         width = self.window.winfo_width()
#         height = self.window.winfo_height()
#         x = (self.window.winfo_screenwidth() // 2) - (width // 2)
#         y = (self.window.winfo_screenheight() // 2) - (height // 2)
#         self.window.geometry(f'{width}x{height}+{x}+{y}')

#     def go_to_dashboard(self):
#         """Return to dashboard"""
#         if self.dashboard_callback:
#             self.window.destroy()
#             self.dashboard_callback()
#         else:
#             self.window.destroy()

#     def load_settings(self):
#         """Load settings from database"""
#         try:
#             # Load backup settings
#             backup_interval = self.settings_service.get_setting('backup_interval', 'Disabled')
#             backup_path = self.settings_service.get_setting('backup_path', os.path.expanduser('~/awan_hardware/backups'))
            
#             self.backup_interval_var.set(backup_interval)
#             self.backup_path_var.set(backup_path)
            
#         except Exception as e:
#             print(f"Error loading settings: {e}")

#     def auto_save_backup_settings(self, *args):
#         """Automatically save backup settings when changed"""
#         try:
#             self.settings_service.set_setting('backup_interval', self.backup_interval_var.get())
#             self.settings_service.set_setting('backup_path', self.backup_path_var.get())
#         except Exception as e:
#             print(f"Error auto-saving settings: {e}")

#     def browse_backup_path(self):
#         """Browse for backup directory"""
#         path = filedialog.askdirectory(
#             title="Select Backup Directory",
#             initialdir=self.backup_path_var.get()
#         )
#         if path:
#             self.backup_path_var.set(path)

#     def manual_backup(self):
#         """Perform manual database backup to fixed location"""
#         try:
#             self.backup_status_label.config(text="Creating backup in Documents folder...")
#             self.window.update()
            
#             backup_path = self.settings_service.backup_database(
#                 user_id=self.user_session['user_id'] if self.user_session else None
#             )
            
#             if backup_path:
#                 backup_dir = os.path.dirname(backup_path)
#                 self.backup_status_label.config(text=f"Backup created in: {backup_dir}")
#                 messagebox.showinfo("Backup Complete", 
#                     f"✅ Database backup created successfully!\n\n"
#                     f"📍 Location: {backup_dir}\n\n"
#                     f"This backup will be used for automatic recovery if needed.")
#             else:
#                 self.backup_status_label.config(text="Backup failed")
#                 messagebox.showerror("Error", "Failed to create backup")
                
#         except Exception as e:
#             self.backup_status_label.config(text="Backup failed")
#             messagebox.showerror("Error", f"Failed to create backup: {str(e)}")