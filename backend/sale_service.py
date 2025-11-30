from backend.database import Database
from datetime import datetime
import calendar

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
        """Create a new sale record with Pakistan time - FIXED: removed duplicate code"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # ✅ Pakistan time manually set karien
            pakistan_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute('''
                INSERT INTO sales (customer_id, total_amount, discount, final_amount, payment_method, sale_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (customer_id, total_amount, discount, final_amount, payment_method, pakistan_time))
            
            sale_id = cursor.lastrowid
            
            return sale_id
    
    def add_sale_item(self, sale_id, product_id, quantity, unit_price, total_price, purchase_price=0):
        """Add item to sale with purchase price"""
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
        """Get sales report for a date range - FIXED for correct schema"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if start_date and end_date:
                    start_with_time = f"{start_date} 00:00:00"
                    end_with_time = f"{end_date} 23:59:59"
                    
                    cursor.execute('''
                        SELECT 
                            s.id,
                            s.customer_id,
                            s.total_amount,
                            s.discount,
                            s.final_amount,
                            s.payment_method,
                            s.sale_date,
                            c.name as customer_name
                        FROM sales s 
                        LEFT JOIN customers c ON s.customer_id = c.id 
                        WHERE s.sale_date BETWEEN ? AND ?
                        ORDER BY s.sale_date ASC  -- ✅ CHANGED FROM DESC TO ASC
                    ''', (start_with_time, end_with_time))
                else:
                    cursor.execute('''
                        SELECT 
                            s.id,
                            s.customer_id,
                            s.total_amount,
                            s.discount,
                            s.final_amount,
                            s.payment_method,
                            s.sale_date,
                            c.name as customer_name
                        FROM sales s 
                        LEFT JOIN customers c ON s.customer_id = c.id 
                        ORDER BY s.sale_date ASC  -- ✅ CHANGED FROM DESC TO ASC
                    ''')
                
                sales = cursor.fetchall()
                return sales
                
        except Exception as e:
            return []
            
    
    def get_sale_details(self, sale_id):
        """Get sale details with stored customer_name"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT *
                FROM sales
                WHERE id = ?
            ''', (sale_id,))
            return cursor.fetchone()

    
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
        """Get sales summary for dashboard - FIXED"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Total sales count
                cursor.execute('SELECT COUNT(*) FROM sales')
                total_sales = cursor.fetchone()[0]
                
                # Total revenue
                cursor.execute('SELECT COALESCE(SUM(final_amount), 0) FROM sales')
                total_revenue = cursor.fetchone()[0]
                
                # Today's sales - FIXED to use Pakistan time
                today = datetime.now().strftime('%Y-%m-%d')
                cursor.execute('''
                    SELECT COALESCE(SUM(final_amount), 0) 
                    FROM sales 
                    WHERE DATE(sale_date) = DATE(?)
                ''', (today,))
                today_revenue = cursor.fetchone()[0]
                
                return {
                    'total_sales': total_sales,
                    'total_revenue': total_revenue,
                    'today_revenue': today_revenue
                }
        except Exception as e:
            return {
                'total_sales': 0,
                'total_revenue': 0,
                'today_revenue': 0
            }