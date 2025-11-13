import sqlite3
from datetime import datetime, timedelta

class StockService:
    def __init__(self, db_path='awan_hardware.db'):
        self.db_path = db_path
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_category_stock_overview(self):
        """Get stock overview by category"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    c.name as category_name,
                    COUNT(p.id) as product_count,
                    SUM(p.current_stock) as total_stock,
                    SUM(p.current_stock * p.purchase_price) as total_value
                FROM categories c
                LEFT JOIN products p ON c.id = p.category_id
                GROUP BY c.id, c.name
                ORDER BY total_value DESC
            ''')
            return cursor.fetchall()
    
    def get_low_stock_products(self):
        """Get products with low stock (less than 5)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    p.*,
                    c.name as category_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.current_stock < 5
                ORDER BY p.current_stock ASC, c.name
            ''')
            return cursor.fetchall()
    
    def get_products_by_category(self, category_name):
        """Get all products for a specific category"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    p.*,
                    c.name as category_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE c.name = ?
                ORDER BY p.company, p.type
            ''', (category_name,))
            return cursor.fetchall()
    
    def get_low_stock_by_category(self, category_name):
        """Get low stock products for a specific category"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    p.*,
                    c.name as category_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE c.name = ? AND p.current_stock < 5
                ORDER BY p.current_stock ASC
            ''', (category_name,))
            return cursor.fetchall()
    
    def get_all_products(self):
        """Get all products from database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    p.*,
                    c.name as category_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                ORDER BY c.name, p.company, p.type
            ''')
            return cursor.fetchall()
    
    def get_total_inventory_value(self):
        """Get total inventory value"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT SUM(current_stock * purchase_price) 
                FROM products
            ''')
            result = cursor.fetchone()
            return result[0] if result[0] else 0
    
    def get_reorder_list(self):
        """Generate reorder list for products below 5"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    p.company,
                    p.type,
                    p.color,
                    c.name as category_name,
                    p.current_stock,
                    p.packing,
                    p.volume,
                    p.purchase_price
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.current_stock < 5
                ORDER BY c.name, p.current_stock ASC
            ''')
            return cursor.fetchall()
    
    def get_stock_summary(self):
        """Get overall stock summary"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total products
            cursor.execute('SELECT COUNT(*) FROM products')
            total_products = cursor.fetchone()[0]
            
            # Total categories
            cursor.execute('SELECT COUNT(*) FROM categories')
            total_categories = cursor.fetchone()[0]
            
            # Total stock value
            total_value = self.get_total_inventory_value()
            
            # Low stock count (less than 5)
            cursor.execute('SELECT COUNT(*) FROM products WHERE current_stock < 5')
            low_stock_count = cursor.fetchone()[0]
            
            # Out of stock count
            cursor.execute('SELECT COUNT(*) FROM products WHERE current_stock = 0')
            out_of_stock_count = cursor.fetchone()[0]
            
            return {
                'total_products': total_products,
                'total_categories': total_categories,
                'total_value': total_value,
                'low_stock_count': low_stock_count,
                'out_of_stock_count': out_of_stock_count
            }