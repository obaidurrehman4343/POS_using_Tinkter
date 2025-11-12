import tkinter as tk
from tkinter import ttk

class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Welcome Section - SIMPLE VERSION
        welcome_frame = tk.Frame(main_frame, bg='#3498db', relief='raised', bd=1)
        welcome_frame.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(
            welcome_frame,
            text="Welcome to Awan Hardware POS",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#3498db'
        ).pack(pady=30)
        
        tk.Label(
            welcome_frame,
            text="Your complete hardware store management solution",
            font=('Arial', 14),
            fg='#ecf0f1',
            bg='#3498db'
        ).pack(pady=(0, 30))
        
        # Empty Content Area - NO STATS, JUST WELCOME MESSAGE
        content_frame = tk.Frame(main_frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        tk.Label(
            content_frame,
            text="👆 Use the sidebar to navigate through different section",
            font=('Arial', 16),
            fg='#7f8c8d',
            bg='white'
        ).pack(expand=True)