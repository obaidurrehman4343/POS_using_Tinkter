import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.user_service import UserService
from backend.backup_service import BackupService
import os
from datetime import datetime

class SettingsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.user_service = UserService()
        self.backup_service = BackupService()
        self.current_user = None  # Will be set from main window
        
        self.setup_ui()
        self.load_users()
        self.load_backup_history()
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="⚙️ Settings & Administration",
            font=('Arial', 20, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(side=tk.LEFT)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Users tab
        users_tab = tk.Frame(notebook, bg='white')
        notebook.add(users_tab, text="👥 User Management")
        
        # Backup tab
        backup_tab = tk.Frame(notebook, bg='white')
        notebook.add(backup_tab, text="💾 Backup & Recovery")
        
        self.setup_users_tab(users_tab)
        self.setup_backup_tab(backup_tab)
    
    def setup_users_tab(self, parent):
        # Header
        header_frame = tk.Frame(parent, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="User Management",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(side=tk.LEFT)
        
        # Add user button
        add_user_btn = tk.Button(
            header_frame,
            text="+ Add New User",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.add_new_user
        )
        add_user_btn.pack(side=tk.RIGHT)
        
        # Users table
        table_frame = tk.Frame(parent, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Username', 'Full Name', 'Role', 'Phone', 'Status', 'Last Login', 'Actions')
        self.users_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        # Define headings
        for col in columns:
            self.users_tree.heading(col, text=col)
        
        # Define columns
        self.users_tree.column('ID', width=40)
        self.users_tree.column('Username', width=100)
        self.users_tree.column('Full Name', width=150)
        self.users_tree.column('Role', width=80)
        self.users_tree.column('Phone', width=100)
        self.users_tree.column('Status', width=80)
        self.users_tree.column('Last Login', width=120)
        self.users_tree.column('Actions', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click for editing
        self.users_tree.bind('<Double-1>', self.edit_user)
    
    def setup_backup_tab(self, parent):
        # Header with buttons
        header_frame = tk.Frame(parent, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="Database Backup & Recovery",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = tk.Frame(header_frame, bg='white')
        button_frame.pack(side=tk.RIGHT)
        
        backup_btn = tk.Button(
            button_frame,
            text="🔄 Create Backup",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.create_backup
        )
        backup_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        restore_btn = tk.Button(
            button_frame,
            text="📥 Restore Backup",
            font=('Arial', 11),
            bg='#e67e22',
            fg='white',
            relief='flat',
            command=self.restore_backup
        )
        restore_btn.pack(side=tk.LEFT)
        
        # Backup history table
        table_frame = tk.Frame(parent, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Filename', 'Date', 'Size', 'Created By', 'Actions')
        self.backup_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        # Define headings
        for col in columns:
            self.backup_tree.heading(col, text=col)
        
        # Define columns
        self.backup_tree.column('ID', width=40)
        self.backup_tree.column('Filename', width=200)
        self.backup_tree.column('Date', width=150)
        self.backup_tree.column('Size', width=80)
        self.backup_tree.column('Created By', width=120)
        self.backup_tree.column('Actions', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.backup_tree.yview)
        self.backup_tree.configure(yscrollcommand=scrollbar.set)
        
        self.backup_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_users(self):
        """Load users into the table"""
        # Clear existing data
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        users = self.user_service.get_all_users()
        
        for user in users:
            user_id, username, role, full_name, phone, is_active, created_at, last_login = user
            
            status = "Active" if is_active else "Inactive"
            
            # Format last login
            last_login_str = "Never"
            if last_login:
                try:
                    last_login_str = last_login[:16]  # Show only date and time
                except:
                    last_login_str = "Unknown"
            
            self.users_tree.insert('', 'end', values=(
                user_id,
                username,
                full_name,
                role.capitalize(),
                phone or "N/A",
                status,
                last_login_str,
                "Edit | Delete"
            ))
    
    def load_backup_history(self):
        """Load backup history into the table"""
        # Clear existing data
        for item in self.backup_tree.get_children():
            self.backup_tree.delete(item)
        
        backups = self.backup_service.get_backup_history()
        
        for backup in backups:
            backup_id, filename, backup_path, file_size, created_at, created_by_username, created_by_name = backup
            
            # Format file size
            size_str = self.backup_service.get_backup_file_size(backup_path) if os.path.exists(backup_path) else "Missing"
            
            # Format date
            created_date = created_at[:16] if created_at else "Unknown"
            
            created_by = created_by_name or created_by_username or "System"
            
            self.backup_tree.insert('', 'end', values=(
                backup_id,
                filename,
                created_date,
                size_str,
                created_by,
                "Restore | Delete"
            ))
    
    def add_new_user(self):
        """Open add new user dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add New User")
        dialog.geometry("400x400")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"400x400+{x}+{y}")
        
        tk.Label(
            dialog,
            text="Add New User",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(pady=15)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Username
        tk.Label(form_frame, text="Username:", font=('Arial', 11, 'bold'), 
                fg='#2c3e50', bg='white').pack(anchor='w', pady=(0, 5))
        username_var = tk.StringVar()
        username_entry = tk.Entry(form_frame, textvariable=username_var, 
                                 font=('Arial', 11), width=30)
        username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Password
        tk.Label(form_frame, text="Password:", font=('Arial', 11, 'bold'), 
                fg='#2c3e50', bg='white').pack(anchor='w', pady=(0, 5))
        password_var = tk.StringVar()
        password_entry = tk.Entry(form_frame, textvariable=password_var, 
                                 font=('Arial', 11), width=30, show='*')
        password_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Full Name
        tk.Label(form_frame, text="Full Name:", font=('Arial', 11, 'bold'), 
                fg='#2c3e50', bg='white').pack(anchor='w', pady=(0, 5))
        fullname_var = tk.StringVar()
        fullname_entry = tk.Entry(form_frame, textvariable=fullname_var, 
                                 font=('Arial', 11), width=30)
        fullname_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Role
        tk.Label(form_frame, text="Role:", font=('Arial', 11, 'bold'), 
                fg='#2c3e50', bg='white').pack(anchor='w', pady=(0, 5))
        role_var = tk.StringVar(value='cashier')
        role_frame = tk.Frame(form_frame, bg='white')
        role_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Radiobutton(role_frame, text="Admin", variable=role_var, value='admin',
                      font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=(0, 20))
        tk.Radiobutton(role_frame, text="Cashier", variable=role_var, value='cashier',
                      font=('Arial', 10), bg='white').pack(side=tk.LEFT)
        
        # Phone
        tk.Label(form_frame, text="Phone (Optional):", font=('Arial', 11, 'bold'), 
                fg='#2c3e50', bg='white').pack(anchor='w', pady=(0, 5))
        phone_var = tk.StringVar()
        phone_entry = tk.Entry(form_frame, textvariable=phone_var, 
                              font=('Arial', 11), width=30)
        phone_entry.pack(fill=tk.X, pady=(0, 20))
        
        def save_user():
            username = username_var.get().strip()
            password = password_var.get().strip()
            full_name = fullname_var.get().strip()
            role = role_var.get()
            phone = phone_var.get().strip()
            
            if not username or not password or not full_name:
                messagebox.showerror("Error", "Please fill all required fields!")
                return
            
            if len(password) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters!")
                return
            
            success, message = self.user_service.add_user(username, password, role, full_name, phone)
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.load_users()
            else:
                messagebox.showerror("Error", message)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Button(
            button_frame,
            text="Save User",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=save_user
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 11),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=dialog.destroy
        ).pack(side=tk.RIGHT)
        
        username_entry.focus()
    
    def edit_user(self, event):
        """Edit user on double click"""
        selected = self.users_tree.selection()
        if not selected:
            return
        
        item = self.users_tree.item(selected[0])
        values = item['values']
        
        if not values:
            return
        
        user_id = values[0]
        
        # For now, just show a simple edit dialog for password change
        self.change_password_dialog(user_id)
    
    def change_password_dialog(self, user_id):
        """Dialog to change user password"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Change Password")
        dialog.geometry("350x200")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"350x200+{x}+{y}")
        
        tk.Label(
            dialog,
            text="Change Password",
            font=('Arial', 14, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(pady=15)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(form_frame, text="New Password:", font=('Arial', 11, 'bold'), 
                fg='#2c3e50', bg='white').pack(anchor='w', pady=(0, 5))
        password_var = tk.StringVar()
        password_entry = tk.Entry(form_frame, textvariable=password_var, 
                                 font=('Arial', 11), width=25, show='*')
        password_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(form_frame, text="Confirm Password:", font=('Arial', 11, 'bold'), 
                fg='#2c3e50', bg='white').pack(anchor='w', pady=(0, 5))
        confirm_var = tk.StringVar()
        confirm_entry = tk.Entry(form_frame, textvariable=confirm_var, 
                                font=('Arial', 11), width=25, show='*')
        confirm_entry.pack(fill=tk.X, pady=(0, 20))
        
        def save_password():
            new_password = password_var.get().strip()
            confirm_password = confirm_var.get().strip()
            
            if not new_password:
                messagebox.showerror("Error", "Please enter new password!")
                return
            
            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match!")
                return
            
            if len(new_password) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters!")
                return
            
            success, message = self.user_service.change_password(user_id, new_password)
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
            else:
                messagebox.showerror("Error", message)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            button_frame,
            text="Change Password",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=save_password
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 11),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=dialog.destroy
        ).pack(side=tk.RIGHT)
        
        password_entry.focus()
    
    def create_backup(self):
        """Create database backup"""
        result = messagebox.askyesno("Create Backup", "Create a backup of the database now?")
        if result:
            success, message, backup_path = self.backup_service.create_backup(
                getattr(self.current_user, 'id', None) if self.current_user else None
            )
            
            if success:
                messagebox.showinfo("Success", message)
                self.load_backup_history()
            else:
                messagebox.showerror("Error", message)
    
    def restore_backup(self):
        """Restore database from backup"""
        # Option 1: Select from existing backups
        selected = self.backup_tree.selection()
        if selected:
            item = self.backup_tree.item(selected[0])
            values = item['values']
            backup_id = values[0]
            filename = values[1]
            
            result = messagebox.askyesno(
                "Restore Backup", 
                f"WARNING: This will replace current database with backup:\n{filename}\n\nThis action cannot be undone!\n\nContinue?"
            )
            
            if result:
                # Find backup path from history
                backups = self.backup_service.get_backup_history()
                backup_path = None
                for backup in backups:
                    if backup[0] == backup_id:
                        backup_path = backup[2]
                        break
                
                if backup_path and os.path.exists(backup_path):
                    success, message = self.backup_service.restore_backup(backup_path)
                    if success:
                        messagebox.showinfo("Success", f"{message}\n\nApplication will restart.")
                        # Restart application
                        self.parent.destroy()
                        import main
                        main.main()
                    else:
                        messagebox.showerror("Error", message)
                else:
                    messagebox.showerror("Error", "Backup file not found")
        
        else:
            # Option 2: Select backup file manually
            file_path = filedialog.askopenfilename(
                title="Select Backup File",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )
            
            if file_path:
                result = messagebox.askyesno(
                    "Restore Backup", 
                    f"WARNING: This will replace current database with:\n{file_path}\n\nThis action cannot be undone!\n\nContinue?"
                )
                
                if result:
                    success, message = self.backup_service.restore_backup(file_path)
                    if success:
                        messagebox.showinfo("Success", f"{message}\n\nApplication will restart.")
                        # Restart application
                        self.parent.destroy()
                        import main
                        main.main()
                    else:
                        messagebox.showerror("Error", message)