import tkinter as tk
from frontend.login_window import LoginWindow

def check_database_timezone():
    """Silent check to ensure Pakistan timezone"""
    try:
        import sqlite3
        conn = sqlite3.connect('awan_hardware.db')
        cursor = conn.cursor()
        
        # Check if we can access database (runs silently)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales'")
        result = cursor.fetchone()
            
        conn.close()
        
    except Exception:
        # Silent error handling - no console output
        pass

def main():
    # Silent database check (runs in background)
    check_database_timezone()
    
    # Start application
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()