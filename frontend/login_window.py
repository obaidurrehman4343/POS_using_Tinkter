# import tkinter as tk
# from tkinter import messagebox
# from PIL import Image, ImageTk
# import sys
# import os
# from backend.database import Database
# from frontend.main_window import MainWindow

# class LoginWindow:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Awan Hardware POS")
        
#         # Set close protocol to handle proper termination
#         self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
#         # Start fullscreen/maximized
#         try:
#             self.root.state('zoomed')
#         except:
#             self.root.attributes('-zoomed', True)

#         self.root.configure(bg='#3498db')
#         self.is_running = True
        
#         self.setup_ui()

#     def setup_ui(self):
#         # Main container with background image
#         main_container = tk.Frame(self.root, bg='#3498db')
#         main_container.pack(fill=tk.BOTH, expand=True)
        
#         # Add background image
#         self.add_background_image(main_container)
        
#         # Center the login container
#         self.login_container = tk.Frame(main_container, bg='#2c3e50', relief='solid', bd=2)
#         self.login_container.place(relx=0.5, rely=0.5, anchor='center', width=900, height=650)
        
#         # Create left and right sections
#         self.create_left_section()
#         self.create_right_section()

#     def add_background_image(self, parent):
#         """Add background image to the login window"""
#         try:
#             # Try to load from template folder first
#             image_path = "template/background1.jpg"
#             if not os.path.exists(image_path):
#                 # If not found, create a simple gradient background
#                 self.create_gradient_background(parent)
#                 return
            
#             # Load and resize background image
#             image = Image.open(image_path)
#             # Get screen dimensions
#             screen_width = parent.winfo_screenwidth()
#             screen_height = parent.winfo_screenheight()
#             image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            
#             bg_photo = ImageTk.PhotoImage(image)
            
#             # Create background label
#             bg_label = tk.Label(parent, image=bg_photo)
#             bg_label.image = bg_photo  # Keep a reference
#             bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
#         except Exception as e:
#             # If image loading fails, create gradient background
#             print(f"Could not load background image: {e}")
#             self.create_gradient_background(parent)

#     def create_gradient_background(self, parent):
#         """Create a gradient background as fallback"""
#         canvas = tk.Canvas(parent, bg='#3498db', highlightthickness=0)
#         canvas.pack(fill=tk.BOTH, expand=True)
        
#         # Create gradient effect
#         width = 1400
#         height = 800
#         for i in range(height):
#             color_value = int(52 + (155 * i / height))  # Gradient from #3498db to lighter blue
#             color = f'#{color_value:02x}{152 + (50 * i / height):02x}{219 + (36 * i / height):02x}'
#             canvas.create_line(0, i, width, i, fill=color)

#     def create_left_section(self):
#         """Create the left brand section"""
#         left_frame = tk.Frame(self.login_container, bg='#34495e', width=450)
#         left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         left_frame.pack_propagate(False)
        
#         # Brand content
#         brand_container = tk.Frame(left_frame, bg='#34495e')
#         brand_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=60)
        
#         # Logo
#         logo_frame = tk.Frame(brand_container, bg='#3498db', width=80, height=80)
#         logo_frame.pack(pady=(0, 30))
#         logo_frame.pack_propagate(False)
        
#         logo_label = tk.Label(
#             logo_frame, text="AH",
#             font=('Arial', 32, 'bold'),
#             fg='white', bg='#3498db'
#         )
#         logo_label.pack(expand=True)
        
#         # Company name
#         tk.Label(
#             brand_container, text="AWAN HARDWARE",
#             font=('Arial', 28, 'bold'),
#             fg='white', bg='#34495e'
#         ).pack(pady=(0, 10))
        
#         # Subtitle
#         tk.Label(
#             brand_container, text="PAINT AND SANITARY STORE ARJA",
#             font=('Arial', 16),
#             fg='#3498db', bg='#34495e'
#         ).pack(pady=(0, 20))
        
#         # Decorative line
#         line_frame = tk.Frame(brand_container, bg='#3498db', height=3)
#         line_frame.pack(fill=tk.X, pady=(0, 20))
        
#         # Tagline
#         tk.Label(
#             brand_container,
#             text="Your Trusted Partner in\nHardware & Paint Solutions",
#             font=('Arial', 14),
#             fg='#ecf0f1', bg='#34495e',
#             justify='center'
#         ).pack(pady=(20, 0))

#     def create_right_section(self):
#         """Create the right login section"""
#         right_frame = tk.Frame(self.login_container, bg='#2c3e50', width=450)
#         right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
#         right_frame.pack_propagate(False)
        
#         # Login content
#         login_container = tk.Frame(right_frame, bg='#2c3e50')
#         login_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=40)
        
#         # Login icon
#         tk.Label(
#             login_container, text="🔐",
#             font=('Arial', 40),
#             fg='white', bg='#2c3e50'
#         ).pack(pady=(20, 10))
        
#         # Login title
#         tk.Label(
#             login_container, text="USER LOGIN",
#             font=('Arial', 22, 'bold'),
#             fg='white', bg='#2c3e50'
#         ).pack(pady=(0, 30))
        
#         # Username field
#         self.create_input_field(login_container, "Username", "👤", 0)
        
#         # Password field
#         self.create_input_field(login_container, "Password", "🔒", 1)
        
#         # Show password checkbox
#         self.show_password_var = tk.BooleanVar()
#         checkbox_frame = tk.Frame(login_container, bg='#2c3e50')
#         checkbox_frame.pack(fill=tk.X, pady=(15, 25))
        
#         tk.Checkbutton(
#             checkbox_frame, text="Show password",
#             variable=self.show_password_var,
#             command=self.toggle_password,
#             bg='#2c3e50', fg='#ecf0f1',
#             selectcolor='#2c3e50',
#             activebackground='#2c3e50',
#             activeforeground='white',
#             font=('Arial', 10), cursor='hand2'
#         ).pack(anchor='w')
        
#         # LOGIN BUTTON - Made smaller and more prominent
#         button_frame = tk.Frame(login_container, bg='#2c3e50')
#         button_frame.pack(fill=tk.X, pady=(10, 20))
        
#         self.login_btn = tk.Button(
#             button_frame, text="LOGIN",
#             font=('Arial', 14, 'bold'),  # Reduced font size
#             fg='white', bg='#27ae60',
#             relief='raised', bd=3,
#             cursor='hand2',
#             command=self.handle_login,
#             width=12, height=2,  # Made width much smaller
#             activebackground='#2ecc71',
#             activeforeground='white'
#         )
#         self.login_btn.pack()  # Center the button
        
#         # Add hover effect
#         self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg='#2ecc71', relief='solid', bd=4))
#         self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg='#27ae60', relief='raised', bd=3))
        
#         # Footer
#         footer_frame = tk.Frame(login_container, bg='#2c3e50')
#         footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        
#         tk.Label(
#             footer_frame,
#             text="Default: owner/owner123 or cashier/cashier123",
#             font=('Arial', 9),
#             fg='#95a5a6', bg='#2c3e50'
#         ).pack()
        
#         # Bind enter key
#         self.username_input.bind('<Return>', lambda e: self.handle_login())
#         self.password_input.bind('<Return>', lambda e: self.handle_login())

#     def create_input_field(self, parent, label_text, icon, index):
#         """Create an input field with modern styling"""
#         field_frame = tk.Frame(parent, bg='#2c3e50')
#         field_frame.pack(fill=tk.X, pady=(0, 15))
        
#         # Label with icon
#         label = tk.Label(
#             field_frame, text=f"{icon} {label_text}",
#             font=('Arial', 11, 'bold'),
#             fg='#ecf0f1', bg='#2c3e50'
#         )
#         label.pack(anchor='w')
        
#         # Input field container
#         input_container = tk.Frame(field_frame, bg='#34495e', relief='solid', bd=1)
#         input_container.pack(fill=tk.X, pady=(5, 0))
        
#         if index == 0:  # Username
#             self.username_input = tk.Entry(
#                 input_container, font=('Arial', 12),
#                 bg='#34495e', fg='white',
#                 relief='flat', bd=0, insertbackground='#3498db',
#                 width=25
#             )
#             self.username_input.pack(fill=tk.X, ipady=8, padx=5)
#         else:  # Password
#             self.password_input = tk.Entry(
#                 input_container, font=('Arial', 12),
#                 bg='#34495e', fg='white',
#                 show='•', relief='flat', bd=0,
#                 insertbackground='#3498db',
#                 width=25
#             )
#             self.password_input.pack(fill=tk.X, ipady=8, padx=5)

#     def toggle_password(self):
#         self.password_input.config(show='' if self.show_password_var.get() else '•')

#     def handle_login(self, event=None):
#         username = self.username_input.get().strip()
#         password = self.password_input.get()

#         if not username or not password:
#             messagebox.showerror("Login Failed", "Please enter both username and password!")
#             return

#         # Loading state
#         self.login_btn.config(text="⏳", state='disabled', bg='#95a5a6')  # Just show loading icon
#         self.root.update()

#         try:
#             db = Database()
#             user_data = db.authenticate_user(username, password)

#             if user_data:
#                 permissions = self.get_user_permissions(user_data[2])

#                 user_session = {
#                     'user_id': user_data[0],
#                     'username': user_data[1],
#                     'role': user_data[2],
#                     'full_name': user_data[3],
#                     'permissions': permissions
#                 }

#                 self.root.withdraw()
#                 self.open_main_window(user_session)
#             else:
#                 messagebox.showerror("Login Failed", "Invalid username or password!")
#                 self.password_input.delete(0, tk.END)
#                 self.password_input.focus()
#                 self.login_btn.config(text="LOGIN", state='normal', bg='#27ae60')

#         except Exception as e:
#             messagebox.showerror("Database Error", f"Error connecting to database: {str(e)}")
#             self.login_btn.config(text="LOGIN", state='normal', bg='#27ae60')

#     def get_user_permissions(self, role):
#         permissions = {
#             'owner': ['dashboard', 'inventory_management', 'point_of_sale', 'sale_report', 'stock_report', 'udhar_management'],
#             'manager': ['dashboard', 'inventory_management', 'point_of_sale', 'sale_report', 'stock_report'],
#             'cashier': ['point_of_sale', 'stock_report', 'inventory_management']
#         }
#         return permissions.get(role, [])

#     def open_main_window(self, user_session):
#         self.main_root = tk.Toplevel(self.root)
#         self.main_root.title(f"Awan Hardware POS - {user_session['full_name']} ({user_session['role'].title()})")
#         self.main_root.state('zoomed')
#         self.main_root.configure(bg='#ecf0f1')
        
#         # Set protocol for main window close
#         self.main_root.protocol("WM_DELETE_WINDOW", self.on_main_window_close)
        
#         self.main_app = MainWindow(self.main_root, user_session)
#         self.main_app.login_root = self.root

#     def on_main_window_close(self):
#         """When the main window is closed, terminate the entire application"""
#         self.terminate_application()

#     def on_close(self):
#         """Handle application close from login window"""
#         self.terminate_application()

#     def terminate_application(self):
#         """Completely terminate the application"""
#         try:
#             self.is_running = False
            
#             # Destroy all windows
#             if hasattr(self, 'main_root') and self.main_root:
#                 self.main_root.destroy()
            
#             if self.root:
#                 self.root.destroy()
            
#             # Force quit the application
#             self.root.quit()
            
#         except Exception as e:
#             print(f"Error during termination: {e}")
#         finally:
#             # Ensure complete exit
#             os._exit(0)
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import os
from backend.database import Database
from frontend.main_window import MainWindow

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Awan Hardware POS")
        
        # Set close protocol to handle proper termination
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Start fullscreen/maximized
        try:
            self.root.state('zoomed')
        except:
            self.root.attributes('-zoomed', True)

        self.root.configure(bg='#3498db')
        self.is_running = True
        self.main_app = None
        self.is_login_screen = True  # Track current screen state
        
        self.setup_ui()

    def setup_ui(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Reset state
        self.is_login_screen = True
        
        # Main container with background image
        main_container = tk.Frame(self.root, bg='#3498db')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Add background image
        self.add_background_image(main_container)
        
        # Center the login container
        self.login_container = tk.Frame(main_container, bg='#2c3e50', relief='solid', bd=2)
        self.login_container.place(relx=0.5, rely=0.5, anchor='center', width=900, height=650)
        
        # Create left and right sections
        self.create_left_section()
        self.create_right_section()
        
        # Bind Enter key to root window for immediate login after logout
        self.root.bind('<Return>', self.handle_login_enter)

    def add_background_image(self, parent):
        """Add background image to the login window"""
        try:
            # Try to load from template folder first
            if getattr(sys, 'frozen', False):
                # Running as executable
                base_path = os.path.dirname(sys.executable)
            else:
                # Running as script
                base_path = os.path.dirname(os.path.dirname(__file__))
            
            image_path = os.path.join(base_path, "template", "background1.jpg")
            
            if not os.path.exists(image_path):
                # If not found, create a simple gradient background
                self.create_gradient_background(parent)
                return
            
            # Load and resize background image
            image = Image.open(image_path)
            # Get screen dimensions
            screen_width = parent.winfo_screenwidth()
            screen_height = parent.winfo_screenheight()
            image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            
            bg_photo = ImageTk.PhotoImage(image)
            
            # Create background label
            bg_label = tk.Label(parent, image=bg_photo)
            bg_label.image = bg_photo  # Keep a reference
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
        except Exception as e:
            # If image loading fails, create gradient background
            self.create_gradient_background(parent)

    def create_gradient_background(self, parent):
        """Create a gradient background as fallback"""
        canvas = tk.Canvas(parent, bg='#3498db', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create gradient effect
        width = 1400
        height = 800
        for i in range(height):
            # Convert to integers before formatting as hex
            red = int(52 + (155 * i / height))
            green = int(152 + (50 * i / height))
            blue = int(219 + (36 * i / height))
            
            # Format as hex with 2 digits
            color = f'#{red:02x}{green:02x}{blue:02x}'
            canvas.create_line(0, i, width, i, fill=color)

    def create_left_section(self):
        """Create the left brand section"""
        left_frame = tk.Frame(self.login_container, bg='#34495e', width=450)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_frame.pack_propagate(False)
        
        # Brand content
        brand_container = tk.Frame(left_frame, bg='#34495e')
        brand_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=60)
        
        # Logo
        logo_frame = tk.Frame(brand_container, bg='#3498db', width=80, height=80)
        logo_frame.pack(pady=(0, 30))
        logo_frame.pack_propagate(False)
        
        logo_label = tk.Label(
            logo_frame, text="AH",
            font=('Arial', 32, 'bold'),
            fg='white', bg='#3498db'
        )
        logo_label.pack(expand=True)
        
        # Company name
        tk.Label(
            brand_container, text="AWAN HARDWARE",
            font=('Arial', 28, 'bold'),
            fg='white', bg='#34495e'
        ).pack(pady=(0, 10))
        
        # Subtitle
        tk.Label(
            brand_container, text="PAINT AND SANITARY STORE ARJA",
            font=('Arial', 16),
            fg='#3498db', bg='#34495e'
        ).pack(pady=(0, 20))
        
        # Decorative line
        line_frame = tk.Frame(brand_container, bg='#3498db', height=3)
        line_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Tagline
        tk.Label(
            brand_container,
            text="Your Trusted Partner in\nHardware & Paint Solutions",
            font=('Arial', 14),
            fg='#ecf0f1', bg='#34495e',
            justify='center'
        ).pack(pady=(20, 0))

    def create_right_section(self):
        """Create the right login section"""
        right_frame = tk.Frame(self.login_container, bg='#2c3e50', width=450)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)
        
        # Login content
        login_container = tk.Frame(right_frame, bg='#2c3e50')
        login_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=40)
        
        # Login icon
        tk.Label(
            login_container, text="🔐",
            font=('Arial', 40),
            fg='white', bg='#2c3e50'
        ).pack(pady=(20, 10))
        
        # Login title
        tk.Label(
            login_container, text="USER LOGIN",
            font=('Arial', 22, 'bold'),
            fg='white', bg='#2c3e50'
        ).pack(pady=(0, 30))
        
        # Username field
        self.create_input_field(login_container, "Username", "👤", 0)
        
        # Password field
        self.create_input_field(login_container, "Password", "🔒", 1)
        
        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        checkbox_frame = tk.Frame(login_container, bg='#2c3e50')
        checkbox_frame.pack(fill=tk.X, pady=(15, 25))
        
        tk.Checkbutton(
            checkbox_frame, text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password,
            bg='#2c3e50', fg='#ecf0f1',
            selectcolor='#2c3e50',
            activebackground='#2c3e50',
            activeforeground='white',
            font=('Arial', 10), cursor='hand2'
        ).pack(anchor='w')
        
        # LOGIN BUTTON
        button_frame = tk.Frame(login_container, bg='#2c3e50')
        button_frame.pack(fill=tk.X, pady=(10, 20))
        
        self.login_btn = tk.Button(
            button_frame, text="LOGIN",
            font=('Arial', 14, 'bold'),
            fg='white', bg='#27ae60',
            relief='raised', bd=3,
            cursor='hand2',
            command=self.handle_login,
            width=12, height=2,
            activebackground='#2ecc71',
            activeforeground='white'
        )
        self.login_btn.pack()
        
        # Add hover effect
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg='#2ecc71', relief='solid', bd=4))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg='#27ae60', relief='raised', bd=3))
        
        # Footer
        footer_frame = tk.Frame(login_container, bg='#2c3e50')
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        
        tk.Label(
            footer_frame,
            text="Default: owner/owner123 or cashier/cashier123",
            font=('Arial', 9),
            fg='#95a5a6', bg='#2c3e50'
        ).pack()
        
        # Bind enter key to both fields
        self.username_input.bind('<Return>', self.handle_login_enter)
        self.password_input.bind('<Return>', self.handle_login_enter)

    def create_input_field(self, parent, label_text, icon, index):
        """Create an input field with modern styling"""
        field_frame = tk.Frame(parent, bg='#2c3e50')
        field_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Label with icon
        label = tk.Label(
            field_frame, text=f"{icon} {label_text}",
            font=('Arial', 11, 'bold'),
            fg='#ecf0f1', bg='#2c3e50'
        )
        label.pack(anchor='w')
        
        # Input field container
        input_container = tk.Frame(field_frame, bg='#34495e', relief='solid', bd=1)
        input_container.pack(fill=tk.X, pady=(5, 0))
        
        if index == 0:  # Username
            self.username_input = tk.Entry(
                input_container, font=('Arial', 12),
                bg='#34495e', fg='white',
                relief='flat', bd=0, insertbackground='#3498db',
                width=25
            )
            self.username_input.pack(fill=tk.X, ipady=8, padx=5)
        else:  # Password
            self.password_input = tk.Entry(
                input_container, font=('Arial', 12),
                bg='#34495e', fg='white',
                show='•', relief='flat', bd=0,
                insertbackground='#3498db',
                width=25
            )
            self.password_input.pack(fill=tk.X, ipady=8, padx=5)

    def toggle_password(self):
        if hasattr(self, 'password_input') and self.password_input.winfo_exists():
            self.password_input.config(show='' if self.show_password_var.get() else '•')

    def handle_login_enter(self, event=None):
        """Handle login when Enter key is pressed - with safety check"""
        if self.is_login_screen:
            self.handle_login(event)

    def handle_login(self, event=None):
        """Handle login with safety checks for UI elements"""
        # Check if we're on login screen and UI elements exist
        if not self.is_login_screen:
            return
            
        try:
            username = self.username_input.get().strip()
            password = self.password_input.get()
        except (AttributeError, tk.TclError):
            # UI elements don't exist or were destroyed
            return

        if not username or not password:
            messagebox.showerror("Login Failed", "Please enter both username and password!")
            return

        # Loading state
        self.login_btn.config(text="⏳", state='disabled', bg='#95a5a6')
        self.root.update()

        try:
            db = Database()
            user_data = db.authenticate_user(username, password)

            if user_data:
                permissions = self.get_user_permissions(user_data[2])

                user_session = {
                    'user_id': user_data[0],
                    'username': user_data[1],
                    'role': user_data[2],
                    'full_name': user_data[3],
                    'permissions': permissions
                }

                self.open_main_window(user_session)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password!")
                if hasattr(self, 'password_input') and self.password_input.winfo_exists():
                    self.password_input.delete(0, tk.END)
                    self.password_input.focus()
                if hasattr(self, 'login_btn') and self.login_btn.winfo_exists():
                    self.login_btn.config(text="LOGIN", state='normal', bg='#27ae60')

        except Exception as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {str(e)}")
            if hasattr(self, 'login_btn') and self.login_btn.winfo_exists():
                self.login_btn.config(text="LOGIN", state='normal', bg='#27ae60')

    def get_user_permissions(self, role):
        permissions = {
            'owner': ['dashboard', 'inventory_management', 'point_of_sale', 'sale_report', 'stock_report', 'udhar_management'],
            'manager': ['dashboard', 'inventory_management', 'point_of_sale', 'sale_report', 'stock_report'],
            'cashier': ['point_of_sale', 'stock_report', 'inventory_management']
        }
        return permissions.get(role, [])

    def open_main_window(self, user_session):
        """Switch to main application window - REUSE THE SAME ROOT WINDOW"""
        # Update state
        self.is_login_screen = False
        
        # Clear login UI
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Unbind Enter key to prevent conflicts
        self.root.unbind('<Return>')
        
        # Reconfigure root window for main application
        self.root.title(f"Awan Hardware POS - {user_session['full_name']} ({user_session['role'].title()})")
        self.root.configure(bg='#ecf0f1')
        
        # Create main application in the same root window
        self.main_app = MainWindow(self.root, user_session)
        self.main_app.login_root = self

    def show_login_screen(self):
        """Reset and show the login screen"""
        # Update state
        self.is_login_screen = True
        
        # Clear main application
        if self.main_app:
            self.main_app = None
        
        # Clear all widgets from root window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Setup login UI
        self.setup_ui()
        
        # Ensure window is properly shown
        self.root.deiconify()
        try:
            self.root.state('zoomed')
        except:
            self.root.attributes('-zoomed', True)

    def on_close(self):
        """Handle application close from login window"""
        self.terminate_application()

    def terminate_application(self):
        """Completely terminate the application"""
        try:
            self.is_running = False
            self.root.quit()
            self.root.destroy()
        except Exception:
            pass
        finally:
            os._exit(0)