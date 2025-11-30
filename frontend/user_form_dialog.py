# frontend/user_form_dialog.py

import tkinter as tk
from tkinter import ttk, messagebox
from backend.user_service import UserService

class UserFormDialog:
    def __init__(self, parent, user_service, refresh_callback, user_id=None):
        self.parent = parent
        self.user_service = user_service
        self.refresh_callback = refresh_callback
        self.user_id = user_id
        self.is_edit_mode = user_id is not None
        
        self.setup_dialog()
        self.create_form()
        
        if self.is_edit_mode:
            self.load_user_data()
    
    def setup_dialog(self):
        """Setup dialog window"""
        title = "Edit User" if self.is_edit_mode else "Add New User"
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(title)
        self.dialog.geometry("500x600")
        self.dialog.configure(bg='white')
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"500x600+{x}+{y}")
    
    def create_form(self):
        """Create user form"""
        main_frame = tk.Frame(self.dialog, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title_text = "✏️ Edit User" if self.is_edit_mode else "👤 Add New User"
        tk.Label(
            main_frame,
            text=title_text,
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 20))
        
        # Form fields
        self.create_form_fields(main_frame)
        
        # Buttons
        self.create_buttons(main_frame)
    
    def create_form_fields(self, parent):
        """Create form input fields"""
        # Username
        username_frame = tk.Frame(parent, bg='white')
        username_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            username_frame,
            text="Username:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(
            username_frame,
            textvariable=self.username_var,
            font=('Arial', 11),
            relief='solid',
            bd=1
        )
        self.username_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(10, 0))
        
        # Full Name
        fullname_frame = tk.Frame(parent, bg='white')
        fullname_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            fullname_frame,
            text="Full Name:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.fullname_var = tk.StringVar()
        self.fullname_entry = tk.Entry(
            fullname_frame,
            textvariable=self.fullname_var,
            font=('Arial', 11),
            relief='solid',
            bd=1
        )
        self.fullname_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(10, 0))
        
        # Role
        role_frame = tk.Frame(parent, bg='white')
        role_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            role_frame,
            text="Role:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.role_var = tk.StringVar(value='cashier')
        role_combo = ttk.Combobox(
            role_frame,
            textvariable=self.role_var,
            values=['owner', 'manager', 'cashier'],
            state="readonly",
            font=('Arial', 11)
        )
        role_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(10, 0))
        
        # Phone
        phone_frame = tk.Frame(parent, bg='white')
        phone_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            phone_frame,
            text="Phone:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.phone_var = tk.StringVar()
        self.phone_entry = tk.Entry(
            phone_frame,
            textvariable=self.phone_var,
            font=('Arial', 11),
            relief='solid',
            bd=1
        )
        self.phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(10, 0))
        
        # Password (only for new users or when changing)
        if not self.is_edit_mode:
            password_frame = tk.Frame(parent, bg='white')
            password_frame.pack(fill=tk.X, pady=10)
            
            tk.Label(
                password_frame,
                text="Password:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white',
                width=12,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            self.password_var = tk.StringVar()
            self.password_entry = tk.Entry(
                password_frame,
                textvariable=self.password_var,
                font=('Arial', 11),
                relief='solid',
                bd=1,
                show='•'
            )
            self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(10, 0))
            
            # Confirm Password
            confirm_frame = tk.Frame(parent, bg='white')
            confirm_frame.pack(fill=tk.X, pady=10)
            
            tk.Label(
                confirm_frame,
                text="Confirm Password:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white',
                width=12,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            self.confirm_password_var = tk.StringVar()
            self.confirm_password_entry = tk.Entry(
                confirm_frame,
                textvariable=self.confirm_password_var,
                font=('Arial', 11),
                relief='solid',
                bd=1,
                show='•'
            )
            self.confirm_password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(10, 0))
        
        # Status (only for edit mode)
        if self.is_edit_mode:
            status_frame = tk.Frame(parent, bg='white')
            status_frame.pack(fill=tk.X, pady=10)
            
            tk.Label(
                status_frame,
                text="Status:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white',
                width=12,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            self.status_var = tk.BooleanVar(value=True)
            status_check = tk.Checkbutton(
                status_frame,
                text="Active User",
                variable=self.status_var,
                bg='white',
                fg='#2c3e50',
                font=('Arial', 11)
            )
            status_check.pack(side=tk.LEFT, padx=(10, 0))
    
    def create_buttons(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg='white')
        button_frame.pack(fill=tk.X, pady=20)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 11, 'bold'),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.dialog.destroy,
            padx=20,
            pady=10
        )
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save button
        save_text = "Update User" if self.is_edit_mode else "Create User"
        save_btn = tk.Button(
            button_frame,
            text=save_text,
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.save_user,
            padx=20,
            pady=10
        )
        save_btn.pack(side=tk.LEFT)
        
        # Change password button (only for edit mode)
        if self.is_edit_mode:
            change_pwd_btn = tk.Button(
                button_frame,
                text="Change Password",
                font=('Arial', 11),
                bg='#3498db',
                fg='white',
                relief='flat',
                cursor='hand2',
                command=self.change_password,
                padx=20,
                pady=10
            )
            change_pwd_btn.pack(side=tk.RIGHT)
    
    def load_user_data(self):
        """Load user data for editing"""
        try:
            user = self.user_service.get_user_by_id(self.user_id)
            if user:
                user_id, username, role, full_name, phone, is_active, created_at, last_login = user
                
                self.username_var.set(username)
                self.fullname_var.set(full_name)
                self.role_var.set(role)
                self.phone_var.set(phone or "")
                self.status_var.set(bool(is_active))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load user data: {str(e)}")
    
    def validate_form(self):
        """Validate form data"""
        if not self.username_var.get().strip():
            messagebox.showerror("Error", "Please enter username!")
            self.username_entry.focus()
            return False
        
        if not self.fullname_var.get().strip():
            messagebox.showerror("Error", "Please enter full name!")
            self.fullname_entry.focus()
            return False
        
        if not self.is_edit_mode:
            if not self.password_var.get():
                messagebox.showerror("Error", "Please enter password!")
                self.password_entry.focus()
                return False
            
            if self.password_var.get() != self.confirm_password_var.get():
                messagebox.showerror("Error", "Passwords do not match!")
                self.confirm_password_entry.focus()
                return False
            
            if len(self.password_var.get()) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters!")
                self.password_entry.focus()
                return False
        
        return True
    
    def save_user(self):
        """Save user data"""
        try:
            if not self.validate_form():
                return
            
            username = self.username_var.get().strip()
            full_name = self.fullname_var.get().strip()
            role = self.role_var.get()
            phone = self.phone_var.get().strip()
            
            if self.is_edit_mode:
                is_active = 1 if self.status_var.get() else 0
                self.user_service.update_user(self.user_id, username, role, full_name, phone, is_active)
                messagebox.showinfo("Success", "User updated successfully!")
            else:
                password = self.password_var.get()
                self.user_service.add_user(username, password, role, full_name, phone)
                messagebox.showinfo("Success", "User created successfully!")
            
            self.dialog.destroy()
            if self.refresh_callback:
                self.refresh_callback()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save user: {str(e)}")
    
    def change_password(self):
        """Open change password dialog"""
        from frontend.change_password_dialog import ChangePasswordDialog
        ChangePasswordDialog(self.dialog, self.user_service, self.user_id)