import tkinter as tk

class StockReport:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            main_frame,
            text="📈 Stock Report - Coming Soon",
            font=('Arial', 24, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(expand=True)