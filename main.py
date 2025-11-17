import tkinter as tk
from frontend.login_window import LoginWindow





def main():
    # Start notification service in background thread
   
    
    # Start application
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()