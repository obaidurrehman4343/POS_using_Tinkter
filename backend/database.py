# # database.py

# import sqlite3
# from datetime import datetime
# import pytz 
# import os

# class Database:
#     def __init__(self, db_path='awan_hardware.db'):
#         self.db_path = db_path
#         self.init_database()
        
#     def get_connection(self):
#         return sqlite3.connect(self.db_path)

#     def get_pakistan_time(self):
#         """Get current Pakistan time - FIXED: Consistent implementation"""
#         try:
#             pakistan_tz = pytz.timezone('Asia/Karachi')
#             return datetime.now(pakistan_tz).strftime('%Y-%m-%d %H:%M:%S')
#         except:
#             return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
#     def init_database(self):
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
            
#             # Create categories table
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS categories (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     name TEXT NOT NULL UNIQUE,
#                     description TEXT,
#                     created_at DATETIME DEFAULT CURRENT_TIMESTAMP
#                 )
#             ''')
            
#             # Create products table
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS products (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     category_id INTEGER NOT NULL,
#                     company TEXT NOT NULL,
#                     type TEXT NOT NULL,
#                     color TEXT NOT NULL,
#                     sale_price DECIMAL(10,2) NOT NULL,
#                     purchase_price DECIMAL(10,2) NOT NULL,
#                     packing TEXT,
#                     volume TEXT,
#                     current_stock INTEGER DEFAULT 0,
#                     image_path TEXT,
#                     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#                     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#                     FOREIGN KEY (category_id) REFERENCES categories (id)
#                 )
#             ''')
            
#             # Create customers table for POS
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS customers (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     name TEXT NOT NULL,
#                     phone TEXT UNIQUE,
#                     email TEXT,
#                     address TEXT,
#                     created_at DATETIME DEFAULT CURRENT_TIMESTAMP
#                 )
#             ''')
            
#             # Create sales table for POS
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS sales (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     customer_id INTEGER,
#                     total_amount DECIMAL(10,2) NOT NULL,
#                     discount DECIMAL(10,2) DEFAULT 0,
#                     final_amount DECIMAL(10,2) NOT NULL,
#                     payment_method TEXT DEFAULT 'cash',
#                     sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
#                     FOREIGN KEY (customer_id) REFERENCES customers (id)
#                 )
#             ''')
            
#             # Create sale_items table for POS
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS sale_items (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     sale_id INTEGER NOT NULL,
#                     product_id INTEGER NOT NULL,
#                     quantity INTEGER NOT NULL,
#                     unit_price DECIMAL(10,2) NOT NULL,
#                     total_price DECIMAL(10,2) NOT NULL,
#                     purchase_price DECIMAL(10,2) NOT NULL DEFAULT 0,
#                     FOREIGN KEY (sale_id) REFERENCES sales (id),
#                     FOREIGN KEY (product_id) REFERENCES products (id)
#                 )
#             ''')
            
#             cursor.execute('''
#                     CREATE TABLE IF NOT EXISTS customer_udhar (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         customer_name TEXT NOT NULL,
#                         phone TEXT,
#                         total_amount DECIMAL(10,2) NOT NULL,
#                         paid_amount DECIMAL(10,2) DEFAULT 0,
#                         remaining_balance DECIMAL(10,2) NOT NULL,
#                         created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
#                          last_payment_date DATETIME,
#                         status TEXT DEFAULT 'UNPAID'
#                     )
#             ''')
#             cursor.execute('''
#                         CREATE TABLE IF NOT EXISTS supplier_udhar (
#                             id INTEGER PRIMARY KEY AUTOINCREMENT,
#                             supplier_name TEXT NOT NULL,
#                             phone TEXT,
#                             total_amount DECIMAL(10,2) NOT NULL,
#                             paid_amount DECIMAL(10,2) DEFAULT 0,
#                             remaining_balance DECIMAL(10,2) NOT NULL,
#                             created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
#                              last_payment_date DATETIME,
#                             status TEXT DEFAULT 'UNPAID',
#                             type TEXT DEFAULT 'Supplier'
#                         )
#             ''')
            
#             # --- CONSOLIDATED USERS TABLE ---
#             # This is the corrected table definition
#             cursor.execute('''
#                     CREATE TABLE IF NOT EXISTS users (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         username TEXT UNIQUE NOT NULL,
#                         password TEXT NOT NULL,
#                         role TEXT NOT NULL DEFAULT 'cashier',
#                         full_name TEXT NOT NULL,
#                         phone TEXT,
#                         is_active INTEGER DEFAULT 1,
#                         created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#                         last_login DATETIME
#             )
#             ''')

#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS backup_history (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     filename TEXT NOT NULL,
#                     backup_path TEXT NOT NULL,
#                     file_size INTEGER,
#                     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#                     created_by INTEGER,
#                     FOREIGN KEY (created_by) REFERENCES users (id)
#             )
#             ''')
#             cursor.execute('''
#                     CREATE TABLE IF NOT EXISTS measurements (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         name TEXT NOT NULL,
#                         code TEXT NOT NULL,
#                         type TEXT NOT NULL,
#                         base_unit TEXT NOT NULL,
#                         conversion_factor REAL NOT NULL,
#                         description TEXT
#     )
# ''')
#             cursor.execute('''
#                     CREATE TABLE IF NOT EXISTS app_settings (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         setting_key TEXT UNIQUE NOT NULL,
#                         setting_value TEXT NOT NULL,
#                         setting_type TEXT NOT NULL,
#                         category TEXT NOT NULL,
#                         description TEXT,
#                         updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
#                     )
# ''')
#             cursor.execute('''
#                     CREATE TABLE IF NOT EXISTS security_settings (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         setting_name TEXT UNIQUE NOT NULL,
#                         setting_value TEXT NOT NULL,
#                         description TEXT,
#                         updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
#                     )
# ''')        

#             # Insert default categories
#             categories = [
#                 ('Paint', 'All types of paints and colors'),
#                 ('Sanitary', 'Sanitary ware and bathroom fittings'),
#                 ('Hardware', 'Hardware tools and equipment'),
#                 ('Roof Sheet', 'Roofing sheets and materials'),
#                 ('Limination Sheet', 'Lamination sheets and materials')
#             ]
            
#             cursor.executemany('''
#                 INSERT OR IGNORE INTO categories (name, description) 
#                 VALUES (?, ?)
#             ''', categories)
#             # Insert default measurement units
#             default_measurements = [
#                 ('Meter', 'm', 'Length', 'meter', 1.0, 'Base unit for length'),
#                 ('Centimeter', 'cm', 'Length', 'meter', 0.01, '100 cm = 1 meter'),
#                 ('Feet', 'ft', 'Length', 'meter', 0.3048, '1 ft = 0.3048 meters'),
#                 ('Kilogram', 'kg', 'Weight', 'gram', 1000.0, '1 kg = 1000 grams'),
#                 ('Gram', 'g', 'Weight', 'gram', 1.0, 'Base unit for weight'),
#                 ('Liter', 'L', 'Volume', 'liter', 1.0, 'Base unit for volume'),
#                 ('Milliliter', 'ml', 'Volume', 'liter', 0.001, '1000 ml = 1 liter'),
#                 ('Piece', 'pcs', 'Count', 'piece', 1.0, 'Base unit for counting items'),
#                 ('Pounds', 'lb', 'Weight', 'gram', 453.592, '1 pound = 453.592 grams'),
#                 ('Dozen', 'doz', 'Count', 'piece', 12.0, '1 dozen = 12 pieces') # NEW
# ]            
#             cursor.executemany('''
#                 INSERT OR IGNORE INTO measurements (name, code, type, base_unit, conversion_factor, description)
#                 VALUES (?, ?, ?, ?, ?, ?)
#             ''', default_measurements)
#             # --- CONSOLIDATED USER INSERTION ---
#             # Insert default users if they don't exist
#             default_security_settings = [
#                 ('login_required', 'True', 'Require login to access system'),
#                 ('auto_lock_timer', '15', 'Auto lock timer in minutes'),
#                 ('max_login_attempts', '3', 'Maximum allowed login attempts'),
#                 ('session_timeout', '30', 'Session timeout in minutes'),
#                 ('password_policy', 'medium', 'Password strength requirement')
#             ]

#             cursor.executemany('''
#                 INSERT OR IGNORE INTO security_settings (setting_name, setting_value, description)
#                 VALUES (?, ?, ?)
#             ''', default_security_settings)
            
#             default_app_settings = [
#                     ('backup_interval', 'daily', 'text', 'system', 'Auto-backup frequency'),
#                     ('backup_path', os.path.expanduser('~/awan_hardware/backups'), 'text', 'system', 'Default backup location'),
                    
#                 ]
#             cursor.executemany('''
#                 INSERT OR IGNORE INTO app_settings (setting_key, setting_value, setting_type, category, description)
#                 VALUES (?, ?, ?, ?, ?)
#             ''', default_app_settings)

#             default_users = [
#                 ('owner', 'owner123', 'owner', 'Store Owner'),
#                 ('cashier', 'cashier123', 'cashier', 'Store Cashier')
#             ]
            
#             for username, password, role, full_name in default_users:
#                 cursor.execute('''
#                     INSERT OR IGNORE INTO users (username, password, role, full_name) 
#                     VALUES (?, ?, ?, ?)
#                 ''', (username, password, role, full_name))
            
#             conn.commit()
    
#     # --- CONSOLIDATED USER METHODS ---

#     def authenticate_user(self, username, password):
#         """Authenticate user and return user data"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT id, username, role, full_name 
#                 FROM users 
#                 WHERE username = ? AND password = ? AND is_active = 1
#             ''', (username, password))
#             return cursor.fetchone()
    
#     def get_user_permissions(self, role):
#         """Get module permissions based on role"""
#         permissions = {
#             'owner': ['dashboard', 'inventory_management', 'point_of_sale', 'sale_report', 'stock_report', 'udhar_management'],
#             'manager': ['dashboard', 'inventory_management', 'point_of_sale', 'sale_report', 'stock_report'],
#             'cashier': ['point_of_sale', 'stock_report', 'inventory_management']
#         }
#         return permissions.get(role, [])
    
#     def authenticate_user(self, username, password):
#         """Authenticate user and return user data"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT id, username, role, full_name 
#                 FROM users 
#                 WHERE username = ? AND password = ? AND is_active = 1
#             ''', (username, password))
#             return cursor.fetchone()
    
#     def add_user(self, username, password, role, full_name, phone=""):
#         """Add new user"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 INSERT INTO users (username, password, role, full_name, phone)
#                 VALUES (?, ?, ?, ?, ?)
#             ''', (username, password, role, full_name, phone))
#             conn.commit()
#             return cursor.lastrowid

#     # --- USER MANAGEMENT METHODS ---
    
#     def get_all_users(self):
#         """Get all users from database"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT id, username, role, full_name, phone, is_active, created_at, last_login
#                 FROM users 
#                 ORDER BY created_at ASC
#             ''')
#             return cursor.fetchall()

#     def update_user(self, user_id, username, role, full_name, phone, is_active):
#         """Update existing user"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 UPDATE users 
#                 SET username = ?, role = ?, full_name = ?, phone = ?, is_active = ?
#                 WHERE id = ?
#             ''', (username, role, full_name, phone, is_active, user_id))
#             conn.commit()
#             return cursor.rowcount

#     def delete_user(self, user_id):
#         """Delete user (soft delete by setting is_active=0)"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('UPDATE users SET is_active = 0 WHERE id = ?', (user_id,))
#             conn.commit()
#             return cursor.rowcount

#     def change_user_password(self, user_id, new_password):
#         """Change user password"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('UPDATE users SET password = ? WHERE id = ?', (new_password, user_id))
#             conn.commit()
#             return cursor.rowcount

#     def check_username_exists(self, username, exclude_user_id=None):
#         """Check if username already exists"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             if exclude_user_id:
#                 cursor.execute('SELECT COUNT(*) FROM users WHERE username = ? AND id != ?', 
#                              (username, exclude_user_id))
#             else:
#                 cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
#             return cursor.fetchone()[0] > 0

#     def get_user_by_id(self, user_id):
#         """Get user by ID"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT id, username, role, full_name, phone, is_active, created_at, last_login
#                 FROM users WHERE id = ?
#             ''', (user_id,))
#             return cursor.fetchone()
#     def reset_auto_increment(self, table_name):
#         """Reset auto-increment counter for a table"""
#         try:
#             with self.get_connection() as conn:
#                 cursor = conn.cursor()
#                 cursor.execute("DELETE FROM sqlite_sequence WHERE name=?", (table_name,))
#                 conn.commit()
#                 return True
#         except Exception as e:
#             print(f"Error resetting auto-increment for {table_name}: {e}")
#             return False

#     # --- REST OF YOUR DATABASE METHODS (unchanged) ---

#     def get_all_categories(self):
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('SELECT * FROM categories ORDER BY name')
#             return cursor.fetchall()
        
#     def add_category(self, name, description=""):
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 INSERT INTO categories (name, description) 
#                 VALUES (?, ?)
#             ''', (name, description))
#             return cursor.lastrowid
        
#     def add_product(self, product_data):
#         """Add product with Pakistan time"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
            
#             pakistan_time = self.get_pakistan_time()
            
#             cursor.execute('''
#                 INSERT INTO products 
#                 (category_id, company, type, color, sale_price, purchase_price, 
#                  packing, volume, current_stock, image_path, created_at, updated_at)
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             ''', (
#                 product_data['category_id'],
#                 product_data['company'],
#                 product_data['type'],
#                 product_data['color'],
#                 product_data['sale_price'],
#                 product_data['purchase_price'],
#                 product_data.get('packing', ''),
#                 product_data.get('volume', ''),
#                 product_data.get('current_stock', 0),
#                 product_data.get('image_path', ''),
#                 pakistan_time,
#                 pakistan_time
#             ))
#             return cursor.lastrowid
        
#     def get_products_by_category(self, category_id):
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT p.*, c.name as category_name 
#                 FROM products p 
#                 JOIN categories c ON p.category_id = c.id 
#                 WHERE p.category_id = ?
#                 ORDER BY p.company, p.type
#             ''', (category_id,))
#             return cursor.fetchall()
        
#     def get_all_products(self):
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT p.*, c.name as category_name 
#                 FROM products p 
#                 JOIN categories c ON p.category_id = c.id 
#                 ORDER BY c.name, p.company, p.type
#             ''')
#             return cursor.fetchall()
            
#     def delete_product(self, product_id):
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
#             return cursor.rowcount
            
#     def update_product(self, product_id, product_data):
#         """Update existing product"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 UPDATE products 
#                 SET category_id=?, company=?, type=?, color=?, sale_price=?, purchase_price=?, 
#                     packing=?, volume=?, current_stock=?, image_path=?, updated_at=CURRENT_TIMESTAMP
#                 WHERE id=?
#             ''', (
#                 product_data['category_id'],
#                 product_data['company'],
#                 product_data['type'],
#                 product_data['color'],
#                 product_data['sale_price'],
#                 product_data['purchase_price'],
#                 product_data.get('packing', ''),
#                 product_data.get('volume', ''),
#                 product_data.get('current_stock', 0),
#                 product_data.get('image_path', ''),
#                 product_id
#             ))
#             return cursor.rowcount

#     # NEW METHODS FOR POS SYSTEM
    
#     def get_all_customers(self):  # FIXED: Corrected method name
#         """Get all customers for dropdown"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('SELECT * FROM customers ORDER BY name')
#             return cursor.fetchall()
    
#     def add_customer(self, name, phone, email="", address=""):
#         """Add new customer with Pakistan time"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
            
#             pakistan_time = self.get_pakistan_time()
            
#             cursor.execute('''
#                 INSERT INTO customers (name, phone, email, address, created_at)
#                 VALUES (?, ?, ?, ?, ?)
#             ''', (name, phone, email, address, pakistan_time))
#             return cursor.lastrowid
    
#     def create_sale(self, customer_id, total_amount, discount, final_amount, payment_method='cash'):
#         """Create a new sale record"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 INSERT INTO sales (customer_id, total_amount, discount, final_amount, payment_method)
#                 VALUES (?, ?, ?, ?, ?)
#             ''', (customer_id, total_amount, discount, final_amount, payment_method))
#             return cursor.lastrowid
    
#     def add_sale_item(self, sale_id, product_id, quantity, unit_price, total_price, purchase_price=0):
#         """Add item to a sale with purchase price for profit calculation"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
            
#             # If purchase_price not provided, get it from products table
#             if purchase_price == 0:
#                 cursor.execute('SELECT purchase_price FROM products WHERE id = ?', (product_id,))
#                 result = cursor.fetchone()
#                 purchase_price = result[0] if result else 0
            
#             cursor.execute('''
#                 INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, total_price, purchase_price)
#                 VALUES (?, ?, ?, ?, ?, ?)
#             ''', (sale_id, product_id, quantity, unit_price, total_price, purchase_price))
#             return cursor.lastrowid
    
#     def update_product_stock(self, product_id, quantity_sold):
#         """Update product stock after sale"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 UPDATE products 
#                 SET current_stock = current_stock - ? 
#                 WHERE id = ?
#             ''', (quantity_sold, product_id))
#             return cursor.rowcount
    
#     def get_sale_items(self, sale_id):
#         """Get all items for a specific sale with profit information"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT 
#                     si.*, 
#                     p.company, 
#                     p.type, 
#                     p.color, 
#                     p.packing, 
#                     p.volume,
#                     (si.unit_price - si.purchase_price) * si.quantity as item_profit
#                 FROM sale_items si
#                 JOIN products p ON si.product_id = p.id
#                 WHERE si.sale_id = ?
#             ''', (sale_id,))
#             return cursor.fetchall()
    
#     def get_customer_by_name(self, customer_name):
#         """Get customer by name"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('SELECT * FROM customers WHERE name = ?', (customer_name,))
#             return cursor.fetchone()
    
#     def get_low_stock_products(self, threshold=10):
#         """Get products with low stock"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT p.*, c.name as category_name 
#                 FROM products p 
#                 JOIN categories c ON p.category_id = c.id 
#                 WHERE p.current_stock <= ?
#                 ORDER BY p.current_stock ASC
#             ''', (threshold,))
#             return cursor.fetchall()

   # database.py
# database.py

import sqlite3
from datetime import datetime
import pytz 
import os

class Database:
    def __init__(self, db_path='awan_hardware.db'):
        self.db_path = db_path
        self.init_database()
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_pakistan_time(self):
        """Get current Pakistan time"""
        try:
            pakistan_tz = pytz.timezone('Asia/Karachi')
            return datetime.now(pakistan_tz).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    def init_database(self):
        """Initialize all database tables with proper structure"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create categories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create products table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    company TEXT NOT NULL,
                    type TEXT NOT NULL,
                    color TEXT NOT NULL,
                    sale_price DECIMAL(10,2) NOT NULL,
                    purchase_price DECIMAL(10,2) NOT NULL,
                    packing TEXT,
                    volume TEXT,
                    current_stock INTEGER DEFAULT 0,
                    image_path TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            ''')
            
            # Create customers table for POS
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT UNIQUE,
                    email TEXT,
                    address TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create sales table for POS
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    total_amount DECIMAL(10,2) NOT NULL,
                    discount DECIMAL(10,2) DEFAULT 0,
                    final_amount DECIMAL(10,2) NOT NULL,
                    payment_method TEXT DEFAULT 'cash',
                    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                )
            ''')
            
            # Create sale_items table for POS
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sale_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sale_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price DECIMAL(10,2) NOT NULL,
                    total_price DECIMAL(10,2) NOT NULL,
                    purchase_price DECIMAL(10,2) NOT NULL DEFAULT 0,
                    FOREIGN KEY (sale_id) REFERENCES sales (id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')
            
            # Customer Udhar table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customer_udhar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT NOT NULL,
                    phone TEXT,
                    total_amount DECIMAL(10,2) NOT NULL,
                    paid_amount DECIMAL(10,2) DEFAULT 0,
                    remaining_balance DECIMAL(10,2) NOT NULL,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_payment_date DATETIME,
                    status TEXT DEFAULT 'UNPAID'
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS udhar_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    udhar_id INTEGER NOT NULL,
                    udhar_type TEXT NOT NULL, -- 'customer' or 'supplier'
                    product_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price DECIMAL(10,2) NOT NULL,
                    total_price DECIMAL(10,2) NOT NULL,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (udhar_id) REFERENCES customer_udhar(id) ON DELETE CASCADE
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS udhar_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    udhar_id INTEGER NOT NULL,
                    udhar_type TEXT NOT NULL,
                    transaction_type TEXT NOT NULL, -- 'credit' or 'payment'
                    amount DECIMAL(10,2) NOT NULL,
                    description TEXT,
                    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    created_by INTEGER,
                    FOREIGN KEY (udhar_id) REFERENCES customer_udhar(id) ON DELETE CASCADE
                )
            ''')
            
            # Supplier Udhar table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS supplier_udhar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    supplier_name TEXT NOT NULL,
                    phone TEXT,
                    total_amount DECIMAL(10,2) NOT NULL,
                    paid_amount DECIMAL(10,2) DEFAULT 0,
                    remaining_balance DECIMAL(10,2) NOT NULL,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_payment_date DATETIME,
                    status TEXT DEFAULT 'UNPAID',
                    type TEXT DEFAULT 'Supplier'
                )
            ''')
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'cashier',
                    full_name TEXT NOT NULL,
                    phone TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_login DATETIME
                )
            ''')

            # Backup history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS backup_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    backup_path TEXT NOT NULL,
                    file_size INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    created_by INTEGER,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # Measurements table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS measurements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    code TEXT NOT NULL,
                    type TEXT NOT NULL,
                    base_unit TEXT NOT NULL,
                    conversion_factor REAL NOT NULL,
                    description TEXT
                )
            ''')
            
            # App settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS app_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setting_key TEXT UNIQUE NOT NULL,
                    setting_value TEXT NOT NULL,
                    setting_type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Security settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS security_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setting_name TEXT UNIQUE NOT NULL,
                    setting_value TEXT NOT NULL,
                    description TEXT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # AUDIT LOGS TABLE - CRITICAL FOR SETTINGS SERVICE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT,
                    action TEXT NOT NULL,
                    ip_address TEXT,
                    details TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            # Insert default categories
            default_categories = [
                ('Paint', 'All types of paints and colors'),
                ('Sanitary', 'Sanitary ware and bathroom fittings'),
                ('Hardware', 'Hardware tools and equipment'),
                ('Roof Sheet', 'Roofing sheets and materials'),
                ('Limination Sheet', 'Lamination sheets and materials')
            ]
            
            cursor.executemany('''
                INSERT OR IGNORE INTO categories (name, description) 
                VALUES (?, ?)
            ''', default_categories)
            
            # Insert default measurement units
            default_measurements = [
                ('Meter', 'm', 'Length', 'meter', 1.0, 'Base unit for length'),
                ('Centimeter', 'cm', 'Length', 'meter', 0.01, '100 cm = 1 meter'),
                ('Feet', 'ft', 'Length', 'meter', 0.3048, '1 ft = 0.3048 meters'),
                ('Kilogram', 'kg', 'Weight', 'gram', 1000.0, '1 kg = 1000 grams'),
                ('Gram', 'g', 'Weight', 'gram', 1.0, 'Base unit for weight'),
                ('Liter', 'L', 'Volume', 'liter', 1.0, 'Base unit for volume'),
                ('Milliliter', 'ml', 'Volume', 'liter', 0.001, '1000 ml = 1 liter'),
                ('Piece', 'pcs', 'Count', 'piece', 1.0, 'Base unit for counting items'),
                ('Pounds', 'lb', 'Weight', 'gram', 453.592, '1 pound = 453.592 grams'),
                ('Dozen', 'doz', 'Count', 'piece', 12.0, '1 dozen = 12 pieces')
            ]            
            
            cursor.executemany('''
                INSERT OR IGNORE INTO measurements (name, code, type, base_unit, conversion_factor, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', default_measurements)
            
            # Insert default security settings
            default_security_settings = [
                ('login_required', 'True', 'Require login to access system'),
                ('auto_lock_timer', '15', 'Auto lock timer in minutes'),
                ('max_login_attempts', '3', 'Maximum allowed login attempts'),
                ('session_timeout', '30', 'Session timeout in minutes'),
                ('password_policy', 'medium', 'Password strength requirement')
            ]

            cursor.executemany('''
                INSERT OR IGNORE INTO security_settings (setting_name, setting_value, description)
                VALUES (?, ?, ?)
            ''', default_security_settings)
            
            # Insert default app settings
            default_app_settings = [
                ('backup_interval', 'daily', 'text', 'system', 'Auto-backup frequency'),
                ('backup_path', os.path.join(os.path.expanduser('~'), 'Documents', 'AwanHardwareBackups'), 'text', 'system', 'Default backup location'),
                ('dashboard_refresh', '30', 'number', 'system', 'Dashboard refresh interval in seconds'),
                ('theme', 'light', 'text', 'system', 'UI theme selection')
            ]
            
            cursor.executemany('''
                INSERT OR IGNORE INTO app_settings (setting_key, setting_value, setting_type, category, description)
                VALUES (?, ?, ?, ?, ?)
            ''', default_app_settings)

            # Insert default users
            default_users = [
                ('owner', 'owner123', 'owner', 'Store Owner'),
                ('cashier', 'cashier123', 'cashier', 'Store Cashier'),
                ('manager', 'manager123', 'manager', 'Store Manager')
            ]
            
            for username, password, role, full_name in default_users:
                cursor.execute('''
                    INSERT OR IGNORE INTO users (username, password, role, full_name) 
                    VALUES (?, ?, ?, ?)
                ''', (username, password, role, full_name))
            
            conn.commit()

    # ==================== USER MANAGEMENT METHODS ====================

    def authenticate_user(self, username, password):
        """Authenticate user and return user data"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, username, role, full_name 
                FROM users 
                WHERE username = ? AND password = ? AND is_active = 1
            ''', (username, password))
            result = cursor.fetchone()
            return result

    def get_user_permissions(self, role):
        """Get module permissions based on role"""
        permissions = {
            'owner': ['dashboard', 'inventory_management', 'point_of_sale', 'sale_report', 'stock_report', 'udhar_management', 'user_management', 'settings'],
            'manager': ['dashboard', 'inventory_management', 'point_of_sale', 'sale_report', 'stock_report', 'settings'],
            'cashier': ['point_of_sale', 'stock_report', 'inventory_management']
        }
        return permissions.get(role, [])

    def add_user(self, username, password, role, full_name, phone=""):
        """Add new user"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password, role, full_name, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, password, role, full_name, phone))
            conn.commit()
            return cursor.lastrowid

    def get_all_users(self):
        """Get all users from database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, username, role, full_name, phone, is_active, created_at, last_login
                FROM users 
                ORDER BY created_at ASC
            ''')
            return cursor.fetchall()

    def update_user(self, user_id, username, role, full_name, phone, is_active):
        """Update existing user"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET username = ?, role = ?, full_name = ?, phone = ?, is_active = ?
                WHERE id = ?
            ''', (username, role, full_name, phone, is_active, user_id))
            conn.commit()
            return cursor.rowcount

    def delete_user(self, user_id):
        """Delete user (soft delete by setting is_active=0)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET is_active = 0 WHERE id = ?', (user_id,))
            conn.commit()
            return cursor.rowcount

    def change_user_password(self, user_id, new_password):
        """Change user password"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = ? WHERE id = ?', (new_password, user_id))
            conn.commit()
            return cursor.rowcount

    def check_username_exists(self, username, exclude_user_id=None):
        """Check if username already exists"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if exclude_user_id:
                cursor.execute('SELECT COUNT(*) FROM users WHERE username = ? AND id != ?', 
                             (username, exclude_user_id))
            else:
                cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
            return cursor.fetchone()[0] > 0

    def get_user_by_id(self, user_id):
        """Get user by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, username, role, full_name, phone, is_active, created_at, last_login
                FROM users WHERE id = ?
            ''', (user_id,))
            return cursor.fetchone()

    def update_user_last_login(self, user_id):
        """Update user's last login time"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET last_login = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (user_id,))
            conn.commit()
            return cursor.rowcount

    # ==================== CATEGORY METHODS ====================

    def get_all_categories(self):
        """Get all categories"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM categories ORDER BY name')
            return cursor.fetchall()
        
    def add_category(self, name, description=""):
        """Add new category"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO categories (name, description) 
                VALUES (?, ?)
            ''', (name, description))
            conn.commit()
            return cursor.lastrowid

    def update_category(self, category_id, name, description):
        """Update existing category"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE categories 
                SET name = ?, description = ? 
                WHERE id = ?
            ''', (name, description, category_id))
            conn.commit()
            return cursor.rowcount

    def delete_category(self, category_id):
        """Delete category"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
            conn.commit()
            return cursor.rowcount

    # ==================== PRODUCT METHODS ====================
        
    def add_product(self, product_data):
        """Add product with Pakistan time"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            pakistan_time = self.get_pakistan_time()
            
            cursor.execute('''
                INSERT INTO products 
                (category_id, company, type, color, sale_price, purchase_price, 
                 packing, volume, current_stock, image_path, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product_data['category_id'],
                product_data['company'],
                product_data['type'],
                product_data['color'],
                product_data['sale_price'],
                product_data['purchase_price'],
                product_data.get('packing', ''),
                product_data.get('volume', ''),
                product_data.get('current_stock', 0),
                product_data.get('image_path', ''),
                pakistan_time,
                pakistan_time
            ))
            conn.commit()
            return cursor.lastrowid
        
    def get_products_by_category(self, category_id):
        """Get products by category ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, c.name as category_name 
                FROM products p 
                JOIN categories c ON p.category_id = c.id 
                WHERE p.category_id = ?
                ORDER BY p.company, p.type
            ''', (category_id,))
            return cursor.fetchall()
        
    def get_all_products(self):
        """Get all products with category names"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, c.name as category_name 
                FROM products p 
                JOIN categories c ON p.category_id = c.id 
                ORDER BY c.name, p.company, p.type
            ''')
            return cursor.fetchall()

    def get_product_by_id(self, product_id):
        """Get product by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, c.name as category_name 
                FROM products p 
                JOIN categories c ON p.category_id = c.id 
                WHERE p.id = ?
            ''', (product_id,))
            return cursor.fetchone()
            
    def delete_product(self, product_id):
        """Delete product"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            conn.commit()
            return cursor.rowcount
            
    def update_product(self, product_id, product_data):
        """Update existing product"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products 
                SET category_id=?, company=?, type=?, color=?, sale_price=?, purchase_price=?, 
                    packing=?, volume=?, current_stock=?, image_path=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            ''', (
                product_data['category_id'],
                product_data['company'],
                product_data['type'],
                product_data['color'],
                product_data['sale_price'],
                product_data['purchase_price'],
                product_data.get('packing', ''),
                product_data.get('volume', ''),
                product_data.get('current_stock', 0),
                product_data.get('image_path', ''),
                product_id
            ))
            conn.commit()
            return cursor.rowcount

    def update_product_stock(self, product_id, new_stock):
        """Update product stock quantity"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products 
                SET current_stock = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (new_stock, product_id))
            conn.commit()
            return cursor.rowcount

    def search_products(self, search_term):
        """Search products by company, type, or color"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            search_pattern = f'%{search_term}%'
            cursor.execute('''
                SELECT p.*, c.name as category_name 
                FROM products p 
                JOIN categories c ON p.category_id = c.id 
                WHERE p.company LIKE ? OR p.type LIKE ? OR p.color LIKE ?
                ORDER BY p.company, p.type
            ''', (search_pattern, search_pattern, search_pattern))
            return cursor.fetchall()

    # ==================== POS SYSTEM METHODS ====================
    
    def get_all_customers(self):
        """Get all customers for dropdown"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM customers ORDER BY name')
            return cursor.fetchall()
    
    def add_customer(self, name, phone, email="", address=""):
        """Add new customer with Pakistan time"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            pakistan_time = self.get_pakistan_time()
            
            cursor.execute('''
                INSERT INTO customers (name, phone, email, address, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, phone, email, address, pakistan_time))
            conn.commit()
            return cursor.lastrowid
    
    def create_sale(self, customer_id, total_amount, discount, final_amount, payment_method='cash'):
        """Create a new sale record"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sales (customer_id, total_amount, discount, final_amount, payment_method)
                VALUES (?, ?, ?, ?, ?)
            ''', (customer_id, total_amount, discount, final_amount, payment_method))
            conn.commit()
            return cursor.lastrowid
    
    def add_sale_item(self, sale_id, product_id, quantity, unit_price, total_price, purchase_price=0):
        """Add item to a sale with purchase price for profit calculation"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # If purchase_price not provided, get it from products table
            if purchase_price == 0:
                cursor.execute('SELECT purchase_price FROM products WHERE id = ?', (product_id,))
                result = cursor.fetchone()
                purchase_price = result[0] if result else 0
            
            cursor.execute('''
                INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, total_price, purchase_price)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (sale_id, product_id, quantity, unit_price, total_price, purchase_price))
            conn.commit()
            return cursor.lastrowid
    
    def update_product_stock_after_sale(self, product_id, quantity_sold):
        """Update product stock after sale"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products 
                SET current_stock = current_stock - ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (quantity_sold, product_id))
            conn.commit()
            return cursor.rowcount
    
    def get_sale_items(self, sale_id):
        """Get all items for a specific sale with profit information"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    si.*, 
                    p.company, 
                    p.type, 
                    p.color, 
                    p.packing, 
                    p.volume,
                    (si.unit_price - si.purchase_price) * si.quantity as item_profit
                FROM sale_items si
                JOIN products p ON si.product_id = p.id
                WHERE si.sale_id = ?
            ''', (sale_id,))
            return cursor.fetchall()
    
    def get_customer_by_name(self, customer_name):
        """Get customer by name"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM customers WHERE name = ?', (customer_name,))
            return cursor.fetchone()

    def get_customer_by_id(self, customer_id):
        """Get customer by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
            return cursor.fetchone()

    def get_all_sales(self, limit=100):
        """Get all sales with customer information"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.*, c.name as customer_name 
                FROM sales s 
                LEFT JOIN customers c ON s.customer_id = c.id 
                ORDER BY s.sale_date DESC 
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()

    # ==================== STOCK MANAGEMENT METHODS ====================
    
    def get_low_stock_products(self, threshold=10):
        """Get products with low stock"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, c.name as category_name 
                FROM products p 
                JOIN categories c ON p.category_id = c.id 
                WHERE p.current_stock <= ?
                ORDER BY p.current_stock ASC
            ''', (threshold,))
            return cursor.fetchall()

    def get_out_of_stock_products(self):
        """Get products that are out of stock"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, c.name as category_name 
                FROM products p 
                JOIN categories c ON p.category_id = c.id 
                WHERE p.current_stock <= 0
                ORDER BY p.company, p.type
            ''')
            return cursor.fetchall()

    # ==================== UDHAR MANAGEMENT METHODS ====================
    
    def add_customer_udhar(self, customer_name, phone, total_amount, paid_amount=0):
        """Add customer udhar record"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            remaining_balance = total_amount - paid_amount
            status = 'PAID' if remaining_balance == 0 else 'UNPAID'
            
            cursor.execute('''
                INSERT INTO customer_udhar (customer_name, phone, total_amount, paid_amount, remaining_balance, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (customer_name, phone, total_amount, paid_amount, remaining_balance, status))
            conn.commit()
            return cursor.lastrowid

    def add_supplier_udhar(self, supplier_name, phone, total_amount, paid_amount=0, udhar_type='Supplier'):
        """Add supplier udhar record"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            remaining_balance = total_amount - paid_amount
            status = 'PAID' if remaining_balance == 0 else 'UNPAID'
            
            cursor.execute('''
                INSERT INTO supplier_udhar (supplier_name, phone, total_amount, paid_amount, remaining_balance, status, type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (supplier_name, phone, total_amount, paid_amount, remaining_balance, status, udhar_type))
            conn.commit()
            return cursor.lastrowid

    def get_all_customer_udhar(self):
        """Get all customer udhar records"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM customer_udhar ORDER BY created_date DESC')
            return cursor.fetchall()

    def get_all_supplier_udhar(self):
        """Get all supplier udhar records"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM supplier_udhar ORDER BY created_date DESC')
            return cursor.fetchall()

    def update_customer_udhar_payment(self, udhar_id, paid_amount):
        """Update customer udhar payment"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE customer_udhar 
                SET paid_amount = paid_amount + ?, 
                    remaining_balance = total_amount - (paid_amount + ?),
                    last_payment_date = CURRENT_TIMESTAMP,
                    status = CASE WHEN (total_amount - (paid_amount + ?)) = 0 THEN 'PAID' ELSE 'UNPAID' END
                WHERE id = ?
            ''', (paid_amount, paid_amount, paid_amount, udhar_id))
            conn.commit()
            return cursor.rowcount

    # ==================== SETTINGS AND AUDIT METHODS ====================
    
    def get_app_settings(self):
        """Get all app settings"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM app_settings')
            return cursor.fetchall()
    
    def update_app_setting(self, setting_key, setting_value):
        """Update app setting"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE app_settings 
                SET setting_value = ?, updated_at = CURRENT_TIMESTAMP
                WHERE setting_key = ?
            ''', (setting_value, setting_key))
            conn.commit()
            return cursor.rowcount

    def get_security_settings(self):
        """Get all security settings"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM security_settings')
            return cursor.fetchall()

    def log_audit_event(self, user_id=None, username=None, action=None, ip_address=None, details=None):
        """Log audit event - CRITICAL FOR SETTINGS SERVICE"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO audit_logs (user_id, username, action, ip_address, details)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, username, action, ip_address, details))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error logging audit event: {e}")
            return False

    def get_audit_logs(self, limit=50):
        """Get audit logs"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT username, action, timestamp, ip_address, details
                    FROM audit_logs 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting audit logs: {e}")
            return []

    # ==================== MEASUREMENT METHODS ====================
    
    def get_all_measurements(self):
        """Get all measurement units"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM measurements ORDER BY type, name')
            return cursor.fetchall()
    
    def add_measurement(self, name, code, type, base_unit, conversion_factor, description=""):
        """Add new measurement unit"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO measurements (name, code, type, base_unit, conversion_factor, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, code, type, base_unit, conversion_factor, description))
            conn.commit()
            return cursor.lastrowid

    def update_measurement(self, measurement_id, name, code, type, base_unit, conversion_factor, description):
        """Update measurement unit"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE measurements 
                SET name=?, code=?, type=?, base_unit=?, conversion_factor=?, description=?
                WHERE id=?
            ''', (name, code, type, base_unit, conversion_factor, description, measurement_id))
            conn.commit()
            return cursor.rowcount

    def delete_measurement(self, measurement_id):
        """Delete measurement unit"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM measurements WHERE id = ?', (measurement_id,))
            conn.commit()
            return cursor.rowcount

    # ==================== BACKUP AND SYSTEM METHODS ====================

    def reset_auto_increment(self, table_name):
        """Reset auto-increment counter for a table"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM sqlite_sequence WHERE name=?", (table_name,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error resetting auto-increment for {table_name}: {e}")
            return False

    def get_database_stats(self):
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Count products
            cursor.execute('SELECT COUNT(*) FROM products')
            stats['total_products'] = cursor.fetchone()[0]
            
            # Count categories
            cursor.execute('SELECT COUNT(*) FROM categories')
            stats['total_categories'] = cursor.fetchone()[0]
            
            # Count customers
            cursor.execute('SELECT COUNT(*) FROM customers')
            stats['total_customers'] = cursor.fetchone()[0]
            
            # Count sales
            cursor.execute('SELECT COUNT(*) FROM sales')
            stats['total_sales'] = cursor.fetchone()[0]
            
            # Count users
            cursor.execute('SELECT COUNT(*) FROM users')
            stats['total_users'] = cursor.fetchone()[0]
            
            return stats

    def check_database_integrity(self):
        """Check database integrity"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA integrity_check")
                result = cursor.fetchone()
                return result[0] == 'ok'
        except Exception as e:
            print(f"Error checking database integrity: {e}")
            return False

    def backup_database(self, backup_path):
        """Create a backup of the database"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception as e:
            print(f"Error creating database backup: {e}")
            return False

# # Test the database initialization
# if __name__ == "__main__":
#     db = Database()
#     print("✅ Database initialization completed successfully!")
    
#     # Print some statistics
#     stats = db.get_database_stats()
#     print(f"📊 Database Statistics:")
#     print(f"   Products: {stats['total_products']}")
#     print(f"   Categories: {stats['total_categories']}")
#     print(f"   Customers: {stats['total_customers']}")
#     print(f"   Sales: {stats['total_sales']}")
#     print(f"   Users: {stats['total_users']}")
    
#     # Check integrity
#     if db.check_database_integrity():
#         print("✅ Database integrity check passed")
#     else:
#         print("❌ Database integrity check failed")