from backend.database import Database
from datetime import datetime

class SaleService:
    def __init__(self):
        self.db = Database()
    
    def get_connection(self):
        """Get database connection"""
        return self.db.get_connection()
    
    def get_all_customers(self):
        """Get all customers"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM customers ORDER BY name')
            return cursor.fetchall()
    
    def add_customer(self, name, phone, address):
        """Add new customer without email"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO customers (name, phone, address)
                VALUES (?, ?, ?)
            ''', (name, phone, address))
            return cursor.lastrowid
    
    def get_all_products(self):
        """Get all products for POS"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, c.name as category_name 
                FROM products p 
                JOIN categories c ON p.category_id = c.id 
                ORDER BY c.name, p.company, p.type
            ''')
            return cursor.fetchall()
    
    def create_sale(self, customer_id, total_amount, discount, final_amount, payment_method='cash'):
        """Create a new sale"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sales (customer_id, total_amount, discount, final_amount, payment_method)
                VALUES (?, ?, ?, ?, ?)
            ''', (customer_id, total_amount, discount, final_amount, payment_method))
            return cursor.lastrowid
    
    def add_sale_item(self, sale_id, product_id, quantity, unit_price, total_price):
        """Add item to sale"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, total_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (sale_id, product_id, quantity, unit_price, total_price))
            return cursor.lastrowid
    
    def update_product_stock(self, product_id, quantity):
        """Update product stock after sale"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products 
                SET current_stock = current_stock - ? 
                WHERE id = ?
            ''', (quantity, product_id))
            return cursor.rowcount
    
    def get_sales_report(self, start_date=None, end_date=None):
        """Get sales report with customer information - FIXED VERSION"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Use JOIN to get customer names
            cursor.execute('''
                SELECT 
                    s.id,
                    s.customer_id,
                    s.total_amount,
                    s.discount, 
                    s.final_amount,
                    s.payment_method,
                    s.sale_date,
                    c.name as customer_name,
                    c.phone as customer_phone
                FROM sales s 
                LEFT JOIN customers c ON s.customer_id = c.id 
                ORDER BY s.sale_date ASC 
            ''')
            
            sales = cursor.fetchall()
            return sales
    
    def get_sale_details(self, sale_id):
        """Get sale details with customer information"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    s.*, 
                    c.name as customer_name, 
                    c.phone, 
                    c.address
                FROM sales s 
                LEFT JOIN customers c ON s.customer_id = c.id 
                WHERE s.id = ?
            ''', (sale_id,))
            result = cursor.fetchone()
            return result
    
    def get_sale_items(self, sale_id):
        """Get sale items with product and category information"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    si.*, 
                    p.company, 
                    p.type, 
                    p.color,
                    c.name as category_name
                FROM sale_items si
                JOIN products p ON si.product_id = p.id
                JOIN categories c ON p.category_id = c.id
                WHERE si.sale_id = ?
            ''', (sale_id,))
            return cursor.fetchall()
    
    def get_sales_summary(self):
        """Get sales summary for dashboard"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total sales count
            cursor.execute('SELECT COUNT(*) FROM sales')
            total_sales = cursor.fetchone()[0]
            
            # Total revenue
            cursor.execute('SELECT COALESCE(SUM(final_amount), 0) FROM sales')
            total_revenue = cursor.fetchone()[0]
            
            # Today's sales
            cursor.execute('''
                SELECT COALESCE(SUM(final_amount), 0) 
                FROM sales 
                WHERE DATE(sale_date) = DATE('now')
            ''')
            today_revenue = cursor.fetchone()[0]
            
            return {
                'total_sales': total_sales,
                'total_revenue': total_revenue,
                'today_revenue': today_revenue
            }