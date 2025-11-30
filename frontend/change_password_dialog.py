# frontend/change_password_dialog.py

import tkinter as tk
from tkinter import messagebox
from backend.user_service import UserService

class ChangePasswordDialog:
    def __init__(self, parent, user_service, user_id):
        self.parent = parent
        self.user_service = user_service
        self.user_id = user_id
        
        self.setup_dialog()
        self.create_form()
    
    def setup_dialog(self):
        """Setup dialog window"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Change Password")
        self.dialog.geometry("400x300")
        self.dialog.configure(bg='white')
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
    
    def create_form(self):
        """Create password change form"""
        main_frame = tk.Frame(self.dialog, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        tk.Label(
            main_frame,
            text="🔑 Change Password",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w', pady=(0, 20))
        
        # New Password
        new_frame = tk.Frame(main_frame, bg='white')
        new_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            new_frame,
            text="New Password:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.new_password_var = tk.StringVar()
        self.new_password_entry = tk.Entry(
            new_frame,
            textvariable=self.new_password_var,
            font=('Arial', 11),
            relief='solid',
            bd=1,
            show='•'
        )
        self.new_password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(10, 0))
        
        # Confirm Password
        confirm_frame = tk.Frame(main_frame, bg='white')
        confirm_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            confirm_frame,
            text="Confirm Password:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=15,
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
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='white')
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
            pady=8
        )
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Change button
        change_btn = tk.Button(
            button_frame,
            text="Change Password",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.change_password,
            padx=20,
            pady=8
        )
        change_btn.pack(side=tk.LEFT)
    
    def change_password(self):
        """Change user password"""
        try:
            new_password = self.new_password_var.get()
            confirm_password = self.confirm_password_var.get()
            
            if not new_password:
                messagebox.showerror("Error", "Please enter new password!")
                self.new_password_entry.focus()
                return
            
            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match!")
                self.confirm_password_entry.focus()
                return
            
            if len(new_password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters!")
                self.new_password_entry.focus()
                return
            
            self.user_service.change_user_password(self.user_id, new_password)
            messagebox.showinfo("Success", "Password changed successfully!")
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change password: {str(e)}")