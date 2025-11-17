import sqlite3
from datetime import datetime
import pytz 
class Database:
    def __init__(self, db_path='awan_hardware.db'):
        self.db_path = db_path
        self.init_database()
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    def get_pakistan_time(self):
        """Get current Pakistan time - FIXED: Consistent implementation"""
        try:
            pakistan_tz = pytz.timezone('Asia/Karachi')
            return datetime.now(pakistan_tz).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    def init_database(self):
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
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS customer_udhar (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_name TEXT NOT NULL,
                        phone TEXT,
                        total_amount DECIMAL(10,2) NOT NULL,
                        paid_amount DECIMAL(10,2) DEFAULT 0,
                        remaining_balance DECIMAL(10,2) NOT NULL,
                        created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        status TEXT DEFAULT 'UNPAID'
                    )
''')
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS supplier_udhar (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            supplier_name TEXT NOT NULL,
                            phone TEXT,
                            total_amount DECIMAL(10,2) NOT NULL,
                            paid_amount DECIMAL(10,2) DEFAULT 0,
                            remaining_balance DECIMAL(10,2) NOT NULL,
                            created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                            status TEXT DEFAULT 'UNPAID',
                            type TEXT DEFAULT 'Supplier'
                        )
''')
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        role TEXT NOT NULL DEFAULT 'cashier',
                        full_name TEXT NOT NULL,
                        phone TEXT,
                        is_active INTEGER DEFAULT 1,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        last_login DATETIME
            )
        ''')
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
            # Insert default categories
            categories = [
                ('Paint', 'All types of paints and colors'),
                ('Sanitary', 'Sanitary ware and bathroom fittings'),
                ('Hardware', 'Hardware tools and equipment'),
                ('Roof Sheet', 'Roofing sheets and materials'),
                ('Limination Sheet', 'Lamination sheets and materials')
            ]
            
            cursor.executemany('''
                INSERT OR IGNORE INTO categories (name, description) 
                VALUES (?, ?)
            ''', categories)
            
            # Insert sample customers
            # sample_customers = [
            #     ('Ali Ahmed', '03001234567', 'ali@email.com', 'Main Market, Lahore'),
            #     ('Fatima Khan', '03119876543', 'fatima@email.com', 'Gulberg, Lahore'),
            #     ('Usman Malik', '03211234567', 'usman@email.com', 'Model Town, Lahore'),
            #     ('Walk-in Customer', '00000000000', '', 'No Address')
            # ]
            
            # cursor.executemany('''
            #     INSERT OR IGNORE INTO customers (name, phone, email, address) 
            #     VALUES (?, ?, ?, ?)
            # ''', sample_customers)
            
    def get_all_categories(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM categories ORDER BY name')
            return cursor.fetchall()
        
    def add_category(self, name, description=""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO categories (name, description) 
                VALUES (?, ?)
            ''', (name, description))
            return cursor.lastrowid
        
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
            return cursor.lastrowid
        
    def get_products_by_category(self, category_id):
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
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, c.name as category_name 
                FROM products p 
                JOIN categories c ON p.category_id = c.id 
                ORDER BY c.name, p.company, p.type
            ''')
            return cursor.fetchall()
            
    def delete_product(self, product_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
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
            return cursor.rowcount

    # NEW METHODS FOR POS SYSTEM
    
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
            return cursor.lastrowid
    
    def create_sale(self, customer_id, total_amount, discount, final_amount, payment_method='cash'):
        """Create a new sale record"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sales (customer_id, total_amount, discount, final_amount, payment_method)
                VALUES (?, ?, ?, ?, ?)
            ''', (customer_id, total_amount, discount, final_amount, payment_method))
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
            return cursor.lastrowid
    
    def update_product_stock(self, product_id, quantity_sold):
        """Update product stock after sale"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products 
                SET current_stock = current_stock - ? 
                WHERE id = ?
            ''', (quantity_sold, product_id))
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
    
    def get_sale_items(self, sale_id):
        """Get all items for a specific sale"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT si.*, p.company, p.type, p.color, p.packing, p.volume
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