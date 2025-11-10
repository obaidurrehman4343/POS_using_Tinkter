import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path='awan_hardware.db'):
        self.db_path = db_path
        self.init_database()
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)
        
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
            
            # Create products table WITH color column
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    company TEXT NOT NULL,
                    type TEXT NOT NULL,
                    color TEXT NOT NULL,  -- ADD COLOR COLUMN
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
        """Add product with color"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO products 
                (category_id, company, type, color, sale_price, purchase_price, 
                 packing, volume, current_stock, image_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product_data['category_id'],
                product_data['company'],
                product_data['type'],
                product_data['color'],  # ADD COLOR
                product_data['sale_price'],
                product_data['purchase_price'],
                product_data['packing'],
                product_data['volume'],
                product_data['current_stock'],
                product_data.get('image_path', '')
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
                product_data['packing'],
                product_data['volume'],
                product_data['current_stock'],
                product_data.get('image_path', ''),
                product_id
            ))
            return cursor.rowcount