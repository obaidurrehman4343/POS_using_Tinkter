import sqlite3
from datetime import datetime, timedelta

class StockService:
    def __init__(self, db_path='awan_hardware.db'):
        self.db_path = db_path
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_measurement_type_from_packing(self, packing, category_name=None):
        """Extract measurement type from packing field - UPDATED FOR DOZEN AND POUNDS"""
        if not packing:
            return 'units'
        
        # FORCE Paint category to always be units, regardless of packing
        if category_name and category_name.lower() == 'paint':
            return 'units'
        
        packing_lower = str(packing).lower()
        
        # Check for measurement indicators in packing field
        if 'unit:' in packing_lower:
            # Extract measurement type after "Unit: "
            measurement_part = packing_lower.split('unit:')[-1].strip()
            
            # UPDATED: Added dozen and pounds recognition
            if any(unit in measurement_part for unit in ['feet', 'ft', 'foot']):
                return 'feet'
            elif any(unit in measurement_part for unit in ['meter', 'mtr', 'm']):
                return 'meters'
            elif any(unit in measurement_part for unit in ['kg', 'kilogram']):
                return 'kg'
            elif any(unit in measurement_part for unit in ['pound', 'pounds', 'lb']):  # NEW: Pounds
                return 'pounds'
            elif any(unit in measurement_part for unit in ['liter', 'ltr', 'l']):
                return 'liters'
            elif any(unit in measurement_part for unit in ['dozen', 'doz']):  # NEW: Dozen
                return 'dozen'
            elif any(unit in measurement_part for unit in ['piece', 'pcs', 'unit']):
                return 'units'
            else:
                return 'units'  # Default to units if unknown measurement
        
        # Direct measurement checks - UPDATED
        if any(unit in packing_lower for unit in ['feet', 'ft', 'foot']):
            return 'feet'
        elif any(unit in packing_lower for unit in ['meter', 'mtr', 'm']):
            return 'meters'
        elif any(unit in packing_lower for unit in ['kg', 'kilogram']):
            return 'kg'
        elif any(unit in packing_lower for unit in ['pound', 'pounds', 'lb']):  # NEW: Pounds
            return 'pounds'
        elif any(unit in packing_lower for unit in ['liter', 'ltr', 'l']):
            return 'liters'
        elif any(unit in packing_lower for unit in ['dozen', 'doz']):  # NEW: Dozen
            return 'dozen'
        elif any(unit in packing_lower for unit in ['piece', 'pcs', 'unit']):
            return 'units'
        else:
            return 'units'  # Default to units

    def format_stock_display(self, stock, measurement_type):
        """Format stock display based on measurement type - UPDATED FOR DOZEN AND POUNDS"""
        # UPDATED: Added dozen and pounds
        unit_display = {
            'feet': 'ft',
            'meters': 'm', 
            'kg': 'kg',
            'pounds': 'lb',  # NEW
            'liters': 'L',
            'units': 'pcs',
            'dozen': 'doz'   # NEW
        }
        
        unit = unit_display.get(measurement_type, 'pcs')
        return f"{stock} {unit}"

    def get_stock_status(self, current_stock, measurement_type):
        """Determine stock status with appropriate thresholds for each measurement type - UPDATED"""
        if current_stock == 0:
            return "❌ Out of Stock"
        
        # Define thresholds for different measurement types - UPDATED
        thresholds = {
            'feet': {'critical': 10, 'low': 25},
            'meters': {'critical': 5, 'low': 15},
            'kg': {'critical': 2, 'low': 5},
            'pounds': {'critical': 2, 'low': 5},  # NEW: Same as kg
            'liters': {'critical': 2, 'low': 5},
            'units': {'critical': 2, 'low': 5},
            'dozen': {'critical': 1, 'low': 2}    # NEW: Different thresholds for dozen
        }
        
        threshold = thresholds.get(measurement_type, thresholds['units'])
        
        if current_stock <= threshold['critical']:
            return "🔴 Critical"
        elif current_stock < threshold['low']:
            return "🟡 Low Stock"
        else:
            return "✅ In Stock"

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
        """Get products with low stock - with measurement-aware thresholds"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    p.*,
                    c.name as category_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                ORDER BY p.current_stock ASC, c.name
            ''')
            all_products = cursor.fetchall()
            
            # Filter products based on measurement-aware thresholds
            low_stock_products = []
            for product in all_products:
                if len(product) >= 14:
                    packing = product[7]  # packing field at index 7
                    current_stock = product[9]  # current_stock at index 9
                    category_name = product[13]  # category_name at index 13
                    
                    measurement_type = self.get_measurement_type_from_packing(packing, category_name)
                    status = self.get_stock_status(current_stock, measurement_type)
                    
                    # Include if status indicates low stock or critical
                    if "Critical" in status or "Low Stock" in status:
                        low_stock_products.append(product)
            
            return low_stock_products
    
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
        """Get low stock products for a specific category with measurement-aware thresholds"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    p.*,
                    c.name as category_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE c.name = ?
                ORDER BY p.current_stock ASC
            ''', (category_name,))
            category_products = cursor.fetchall()
            
            # Filter based on measurement-aware thresholds
            low_stock_products = []
            for product in category_products:
                if len(product) >= 14:
                    packing = product[7]
                    current_stock = product[9]
                    cat_name = product[13]
                    
                    measurement_type = self.get_measurement_type_from_packing(packing, cat_name)
                    status = self.get_stock_status(current_stock, measurement_type)
                    
                    if "Critical" in status or "Low Stock" in status:
                        low_stock_products.append(product)
            
            return low_stock_products
    
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
        """Generate reorder list for products below threshold with measurement awareness"""
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
                ORDER BY c.name, p.current_stock ASC
            ''')
            all_products = cursor.fetchall()
            
            # Filter products that need reordering based on measurement type
            reorder_products = []
            for product in all_products:
                if len(product) >= 8:
                    packing = product[5]  # packing field
                    current_stock = product[4]  # current_stock
                    category_name = product[3]  # category_name
                    
                    measurement_type = self.get_measurement_type_from_packing(packing, category_name)
                    status = self.get_stock_status(current_stock, measurement_type)
                    
                    if "Critical" in status or "Low Stock" in status:
                        reorder_products.append(product)
            
            return reorder_products
    
    def get_stock_summary(self):
        """Get overall stock summary with measurement-aware low stock counting"""
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
            
            # Get all products to count low stock with measurement awareness
            cursor.execute('SELECT p.*, c.name as category_name FROM products p JOIN categories c ON p.category_id = c.id')
            all_products = cursor.fetchall()
            
            low_stock_count = 0
            out_of_stock_count = 0
            
            for product in all_products:
                if len(product) >= 14:
                    current_stock = product[9]
                    packing = product[7]
                    category_name = product[13]
                    
                    if current_stock == 0:
                        out_of_stock_count += 1
                    else:
                        measurement_type = self.get_measurement_type_from_packing(packing, category_name)
                        status = self.get_stock_status(current_stock, measurement_type)
                        if "Critical" in status or "Low Stock" in status:
                            low_stock_count += 1
            
            return {
                'total_products': total_products,
                'total_categories': total_categories,
                'total_value': total_value,
                'low_stock_count': low_stock_count,
                'out_of_stock_count': out_of_stock_count
            }
# import sqlite3
# from datetime import datetime, timedelta

# class StockService:
#     def __init__(self, db_path='awan_hardware.db'):
#         self.db_path = db_path
    
#     def get_connection(self):
#         return sqlite3.connect(self.db_path)
    
#     def get_category_stock_overview(self):
#         """Get stock overview by category"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT 
#                     c.name as category_name,
#                     COUNT(p.id) as product_count,
#                     SUM(p.current_stock) as total_stock,
#                     SUM(p.current_stock * p.purchase_price) as total_value
#                 FROM categories c
#                 LEFT JOIN products p ON c.id = p.category_id
#                 GROUP BY c.id, c.name
#                 ORDER BY total_value DESC
#             ''')
#             return cursor.fetchall()
    
#     def get_low_stock_products(self):
#         """Get products with low stock (less than 5)"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT 
#                     p.*,
#                     c.name as category_name
#                 FROM products p
#                 JOIN categories c ON p.category_id = c.id
#                 WHERE p.current_stock < 5
#                 ORDER BY p.current_stock ASC, c.name
#             ''')
#             return cursor.fetchall()
    
#     def get_products_by_category(self, category_name):
#         """Get all products for a specific category"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT 
#                     p.*,
#                     c.name as category_name
#                 FROM products p
#                 JOIN categories c ON p.category_id = c.id
#                 WHERE c.name = ?
#                 ORDER BY p.company, p.type
#             ''', (category_name,))
#             return cursor.fetchall()
    
#     def get_low_stock_by_category(self, category_name):
#         """Get low stock products for a specific category"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT 
#                     p.*,
#                     c.name as category_name
#                 FROM products p
#                 JOIN categories c ON p.category_id = c.id
#                 WHERE c.name = ? AND p.current_stock < 5
#                 ORDER BY p.current_stock ASC
#             ''', (category_name,))
#             return cursor.fetchall()
    
#     def get_all_products(self):
#         """Get all products from database"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT 
#                     p.*,
#                     c.name as category_name
#                 FROM products p
#                 JOIN categories c ON p.category_id = c.id
#                 ORDER BY c.name, p.company, p.type
#             ''')
#             return cursor.fetchall()
    
#     def get_total_inventory_value(self):
#         """Get total inventory value"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT SUM(current_stock * purchase_price) 
#                 FROM products
#             ''')
#             result = cursor.fetchone()
#             return result[0] if result[0] else 0
    
#     def get_reorder_list(self):
#         """Generate reorder list for products below 5"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT 
#                     p.company,
#                     p.type,
#                     p.color,
#                     c.name as category_name,
#                     p.current_stock,
#                     p.packing,
#                     p.volume,
#                     p.purchase_price
#                 FROM products p
#                 JOIN categories c ON p.category_id = c.id
#                 WHERE p.current_stock < 5
#                 ORDER BY c.name, p.current_stock ASC
#             ''')
#             return cursor.fetchall()
    
#     def get_stock_summary(self):
#         """Get overall stock summary"""
#         with self.get_connection() as conn:
#             cursor = conn.cursor()
            
#             # Total products
#             cursor.execute('SELECT COUNT(*) FROM products')
#             total_products = cursor.fetchone()[0]
            
#             # Total categories
#             cursor.execute('SELECT COUNT(*) FROM categories')
#             total_categories = cursor.fetchone()[0]
            
#             # Total stock value
#             total_value = self.get_total_inventory_value()
            
#             # Low stock count (less than 5)
#             cursor.execute('SELECT COUNT(*) FROM products WHERE current_stock < 5')
#             low_stock_count = cursor.fetchone()[0]
            
#             # Out of stock count
#             cursor.execute('SELECT COUNT(*) FROM products WHERE current_stock = 0')
#             out_of_stock_count = cursor.fetchone()[0]
            
#             return {
#                 'total_products': total_products,
#                 'total_categories': total_categories,
#                 'total_value': total_value,
#                 'low_stock_count': low_stock_count,
#                 'out_of_stock_count': out_of_stock_count
#             }  