import tkinter as tk
from tkinter import messagebox
import sys
import os
# At the top of login_window.py
from frontend.main_window import MainWindow

# Add the parent directory to path to import main_window
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Awan Hardware POS - Login")
        self.root.geometry("400x450")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(True, True)
        
        # Handle window close (X button)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Center the window
        self.center_window()
        
        self.setup_ui()
        self.auto_fill_credentials()
        
    def center_window(self):
        self.root.update_idletasks()
        width = 400
        height = 450
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Header
        header_label = tk.Label(
            main_frame, 
            text="Awan Hardware POS", 
            font=('Arial', 20, 'bold'),
            fg='#3498db',
            bg='#2c3e50'
        )
        header_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Login to Continue",
            font=('Arial', 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Login Frame
        login_frame = tk.Frame(main_frame, bg='#34495e', relief='flat')
        login_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Username
        tk.Label(
            login_frame,
            text="Username:",
            font=('Arial', 11, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        ).pack(anchor='w', pady=(20, 5), padx=20)
        
        self.username_input = tk.Entry(
            login_frame,
            font=('Arial', 12),
            bg='#2c3e50',
            fg='white',
            insertbackground='white',
            relief='solid',
            bd=1
        )
        self.username_input.pack(fill=tk.X, padx=20, pady=(0, 15), ipady=8)
        
        # Password
        tk.Label(
            login_frame,
            text="Password:",
            font=('Arial', 11, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        ).pack(anchor='w', pady=(0, 5), padx=20)
        
        self.password_input = tk.Entry(
            login_frame,
            font=('Arial', 12),
            bg='#2c3e50',
            fg='white',
            show='*',
            insertbackground='white',
            relief='solid',
            bd=1
        )
        self.password_input.pack(fill=tk.X, padx=20, pady=(0, 20), ipady=8)
        
        # Login Button
        login_btn = tk.Button(
            login_frame,
            text="LOGIN",
            font=('Arial', 14, 'bold'),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            activeforeground='white',
            relief='flat',
            command=self.handle_login,
            cursor='hand2'
        )
        login_btn.pack(fill=tk.X, padx=20, pady=10, ipady=10)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.handle_login())
        
    def auto_fill_credentials(self):
        self.username_input.delete(0, tk.END)
        self.password_input.delete(0, tk.END)
        self.username_input.insert(0, 'admin')
        self.password_input.insert(0, 'password1234')
        
    def handle_login(self):
        username = self.username_input.get()
        password = self.password_input.get()
        
        if username == 'admin' and password == 'password1234':
            # Hide login and show main window
            self.root.withdraw()
            self.open_main_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")
            
    def open_main_window(self):
        # Hide login
        self.root.withdraw()

        # Create main window
        self.main_root = tk.Toplevel(self.root)
        self.main_root.title("Awan Hardware POS")
        self.main_root.state('zoomed')
        self.main_root.configure(bg='#ecf0f1')

        # Pass login root to main window for logout
        self.main_app = MainWindow(self.main_root)
        self.main_app.login_root = self.root

        # Handle closing main window
        self.main_root.protocol("WM_DELETE_WINDOW", self.on_main_window_close)

        
    def on_main_window_close(self):
        # When main window is closed, show login again
        self.main_root.destroy()
        self.root.deiconify()
        
    def on_close(self):
        self.root.quit()
        self.root.destroy()
        sys.exit(0)
