# frontend/user_management_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox
from backend.user_service import UserService
from frontend.user_form_dialog import UserFormDialog

class UserManagementDialog:
    def __init__(self, parent, user_session, refresh_callback=None):
        self.parent = parent
        self.user_session = user_session
        self.refresh_callback = refresh_callback
        self.user_service = UserService()
        
        # Check if current user has permission to manage users
        if user_session['role'] != 'owner':
            messagebox.showerror("Permission Denied", "Only owners can manage users!")
            return
        
        self.setup_dialog()
        self.create_ui()
        self.load_users()
    
    def setup_dialog(self):
        """Setup dialog window"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("User Management - AWAN HARDWARE")
        self.dialog.geometry("800x600")
        self.dialog.configure(bg='#f8f9fa')
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"800x600+{x}+{y}")
    
    def create_ui(self):
        """Create user interface"""
        # Main container
        main_frame = tk.Frame(self.dialog, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="👥 USER MANAGEMENT",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#2c3e50',
            pady=15
        ).pack()
        
        # Controls frame
        controls_frame = tk.Frame(main_frame, bg='#f8f9fa')
        controls_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Add user button
        add_btn = tk.Button(
            controls_frame,
            text="+ Add New User",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.add_new_user,
            padx=20,
            pady=10
        )
        add_btn.pack(side=tk.LEFT)
        
        # Refresh button
        refresh_btn = tk.Button(
            controls_frame,
            text="🔄 Refresh",
            font=('Arial', 11),
            bg='#3498db',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.load_users,
            padx=20,
            pady=10
        )
        refresh_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Users table frame
        table_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview
        columns = ('ID', 'Username', 'Full Name', 'Role', 'Phone', 'Status', 'Created')
        self.users_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.users_tree.heading('ID', text='ID')
        self.users_tree.heading('Username', text='USERNAME')
        self.users_tree.heading('Full Name', text='FULL NAME')
        self.users_tree.heading('Role', text='ROLE')
        self.users_tree.heading('Phone', text='PHONE')
        self.users_tree.heading('Status', text='STATUS')
        self.users_tree.heading('Created', text='CREATED DATE')
        
        self.users_tree.column('ID', width=50)
        self.users_tree.column('Username', width=100)
        self.users_tree.column('Full Name', width=150)
        self.users_tree.column('Role', width=80)
        self.users_tree.column('Phone', width=100)
        self.users_tree.column('Status', width=80)
        self.users_tree.column('Created', width=120)
        
        # Style treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background='white', fieldbackground='white', rowheight=25)
        style.configure("Treeview.Heading", background='#34495e', foreground='white', font=('Arial', 10, 'bold'))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click for editing
        self.users_tree.bind('<Double-1>', self.edit_user)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="",
            font=('Arial', 10),
            fg='#7f8c8d',
            bg='#f8f9fa'
        )
        self.status_label.pack(fill=tk.X, pady=(10, 0))
    
    def load_users(self):
        """Load all users into the table"""
        try:
            # Clear existing data
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            users = self.user_service.get_all_users()
            
            if not users:
                self.users_tree.insert('', 'end', values=("No", "users", "found", "", "", "", ""))
                return
            
            for user in users:
                user_id, username, role, full_name, phone, is_active, created_at, last_login = user
                
                # Format status
                status = "Active" if is_active else "Inactive"
                status_icon = "✅" if is_active else "❌"
                
                # Format date
                created_date = created_at.split(' ')[0] if created_at else "N/A"
                
                self.users_tree.insert('', 'end', values=(
                    user_id,
                    username,
                    full_name,
                    role.title(),
                    phone or "N/A",
                    f"{status_icon} {status}",
                    created_date
                ))
            
            self.status_label.config(text=f"Loaded {len(users)} users")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {str(e)}")
    
    def add_new_user(self):
        """Open add new user dialog"""
        UserFormDialog(self.dialog, self.user_service, self.load_users)
    
    def edit_user(self, event):
        """Edit selected user"""
        selected = self.users_tree.selection()
        if not selected:
            return
        
        selected_item = self.users_tree.item(selected[0])
        values = selected_item['values']
        
        if not values or values[0] == "No":
            return
        
        user_id = values[0]
        UserFormDialog(self.dialog, self.user_service, self.load_users, user_id)