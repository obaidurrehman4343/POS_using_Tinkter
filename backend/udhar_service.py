import sqlite3
from datetime import datetime

class UdharService:
    def __init__(self, db_path='awan_hardware.db'):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise
    
    # CUSTOMER METHODS
        def add_customer(self, customer_name, phone, total_amount):
            """Add new customer with udhar - LEGACY METHOD"""
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    
                    if not customer_name or not customer_name.strip():
                        return False, "Customer name is required"
                    
                    if not total_amount or total_amount <= 0:
                        return False, "Amount must be greater than 0"
                    
                    cursor.execute('''
                        INSERT INTO customer_udhar 
                        (customer_name, phone, total_amount, paid_amount, remaining_balance, status)
                        VALUES (?, ?, ?, 0, ?, 'UNPAID')
                    ''', (
                        customer_name.strip(),
                        phone.strip() if phone else "",
                        float(total_amount),
                        float(total_amount)
                    ))
                    conn.commit()
                    return True, "Customer added successfully"
                    
            except sqlite3.Error as e:
                return False, f"Database error: {str(e)}"
            except Exception as e:
                return False, f"Error: {str(e)}"

    def get_customer_by_id(self, customer_id):
        """Get customer by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        id, customer_name, phone, address, total_amount, paid_amount, 
                        remaining_balance, created_date, status, last_payment_date
                    FROM customer_udhar 
                    WHERE id = ?
                ''', (customer_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error getting customer by ID: {e}")
            return None


    def receive_payment(self, customer_id, payment_amount, payment_date=None):
        """Receive payment from customer and update last payment date - FIXED"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Use current time if no date provided
                if payment_date is None:
                    payment_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Get current customer data - FIXED COLUMN ORDER
                cursor.execute('''
                    SELECT total_amount, paid_amount, remaining_balance, customer_name, status
                    FROM customer_udhar WHERE id = ?
                ''', (customer_id,))
                result = cursor.fetchone()
                
                if not result:
                    return False, "Customer not found"
                
                total_amount, paid_amount, remaining_balance, customer_name, current_status = result
                
                # Convert to floats to handle None values
                total_amount = float(total_amount) if total_amount else 0.0
                paid_amount = float(paid_amount) if paid_amount else 0.0
                remaining_balance = float(remaining_balance) if remaining_balance else 0.0
                
                # Validate payment amount
                if payment_amount <= 0:
                    return False, "Payment amount must be greater than 0"
                
                if payment_amount > remaining_balance:
                    return False, f"Payment amount cannot exceed remaining balance of PKR {remaining_balance:,.0f}"
                
                # Calculate new values
                new_paid = paid_amount + payment_amount
                new_balance = remaining_balance - payment_amount
                
                # Determine status
                status = 'PAID' if new_balance == 0 else 'UNPAID'
                
                # UPDATE CUSTOMER WITH CORRECT COLUMN ORDER
                cursor.execute('''
                    UPDATE customer_udhar 
                    SET paid_amount = ?, 
                        remaining_balance = ?, 
                        status = ?,
                        last_payment_date = ?
                    WHERE id = ?
                ''', (new_paid, new_balance, status, payment_date, customer_id))
                
                conn.commit()
                
                if new_balance == 0:
                    return True, f"Payment received successfully! {customer_name} is now fully paid."
                
                return True, f"Payment received successfully! Remaining balance: PKR {new_balance:,.0f}"
                
        except Exception as e:
            return False, f"Error processing payment: {str(e)}"
    
    def get_all_customers(self):
        """Get all customers - FIXED to handle correct column order"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        id, customer_name, phone, total_amount, paid_amount, 
                        remaining_balance, created_date, status, last_payment_date
                    FROM customer_udhar 
                    ORDER BY id ASC
                ''')
                result = cursor.fetchall()
                return result if result else []
        except Exception as e:
            print(f"Error getting customers: {e}")
            return []
    
    def search_customers(self, search_term):
        """Search customers by name or phone"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        id, customer_name, phone, total_amount, paid_amount, 
                        remaining_balance, created_date, status, last_payment_date
                    FROM customer_udhar 
                    WHERE customer_name LIKE ? OR phone LIKE ?
                    ORDER BY id ASC
                ''', (f'%{search_term}%', f'%{search_term}%'))
                result = cursor.fetchall()
                return result if result else []
        except Exception as e:
            print(f"Error searching customers: {e}")
            return []
    
    def get_customer_summary(self):
        """Get customer summary statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_customers,
                        COALESCE(SUM(total_amount), 0) as total_udhar,
                        COALESCE(SUM(paid_amount), 0) as total_paid,
                        COALESCE(SUM(remaining_balance), 0) as total_balance
                    FROM customer_udhar
                ''')
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(f"Error getting customer summary: {e}")
            return (0, 0, 0, 0)
    
    def force_delete_customer(self, customer_id):
        """Force delete customer (for fully paid customers)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if customer exists and is fully paid
                cursor.execute('SELECT remaining_balance FROM customer_udhar WHERE id = ?', (customer_id,))
                result = cursor.fetchone()
                
                if not result:
                    return False, "Customer not found"
                
                remaining_balance = float(result[0]) if result[0] else 0.0
                
                if remaining_balance > 0:
                    return False, "Cannot delete customer with pending balance"
                
                # Delete the customer
                cursor.execute('DELETE FROM customer_udhar WHERE id = ?', (customer_id,))
                conn.commit()
                return True, "Customer deleted successfully"
                
        except Exception as e:
            return False, f"Error deleting customer: {str(e)}"
    
    # SUPPLIER METHODS
    def add_supplier(self, supplier_name, phone, total_amount, supplier_type="Supplier"):
        """Add new supplier with udhar - LEGACY METHOD"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if not supplier_name or not supplier_name.strip():
                    return False, "Supplier name is required"
                
                if not total_amount or total_amount <= 0:
                    return False, "Amount must be greater than 0"
                
                cursor.execute('''
                    INSERT INTO supplier_udhar 
                    (supplier_name, phone, total_amount, paid_amount, remaining_balance, status, type)
                    VALUES (?, ?, ?, 0, ?, 'UNPAID', ?)
                ''', (
                    supplier_name.strip(),
                    phone.strip() if phone else "",
                    float(total_amount),
                    float(total_amount),
                    supplier_type
                ))
                conn.commit()
                return True, "Supplier added successfully"
                
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    def get_supplier_by_id(self, supplier_id):
        """Get supplier by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        id, supplier_name, phone, address, total_amount, paid_amount, 
                        remaining_balance, created_date, status, last_payment_date, type
                    FROM supplier_udhar 
                    WHERE id = ?
                ''', (supplier_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error getting supplier by ID: {e}")
            return None
    
    def make_payment(self, supplier_id, payment_amount, payment_date=None):
        """Make payment to supplier and update last payment date - FIXED"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Use current time if no date provided
                if payment_date is None:
                    payment_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Get current supplier data - FIXED COLUMN ORDER
                cursor.execute('''
                    SELECT total_amount, paid_amount, remaining_balance, supplier_name, status
                    FROM supplier_udhar WHERE id = ?
                ''', (supplier_id,))
                result = cursor.fetchone()
                
                if not result:
                    return False, "Supplier not found"
                
                total_amount, paid_amount, remaining_balance, supplier_name, current_status = result
                
                # Convert to floats to handle None values
                total_amount = float(total_amount) if total_amount else 0.0
                paid_amount = float(paid_amount) if paid_amount else 0.0
                remaining_balance = float(remaining_balance) if remaining_balance else 0.0
                
                # Validate payment amount
                if payment_amount <= 0:
                    return False, "Payment amount must be greater than 0"
                
                if payment_amount > remaining_balance:
                    return False, f"Payment amount cannot exceed remaining balance of PKR {remaining_balance:,.0f}"
                
                # Calculate new values
                new_paid = paid_amount + payment_amount
                new_balance = remaining_balance - payment_amount
                
                # Determine status
                status = 'PAID' if new_balance == 0 else 'UNPAID'
                
                # UPDATE SUPPLIER WITH CORRECT COLUMN ORDER
                cursor.execute('''
                    UPDATE supplier_udhar 
                    SET paid_amount = ?, 
                        remaining_balance = ?, 
                        status = ?,
                        last_payment_date = ?
                    WHERE id = ?
                ''', (new_paid, new_balance, status, payment_date, supplier_id))
                
                conn.commit()
                
                if new_balance == 0:
                    return True, f"Payment made successfully! {supplier_name} is now fully paid."
                
                return True, f"Payment made successfully! Remaining balance: PKR {new_balance:,.0f}"
                
        except Exception as e:
            return False, f"Error processing payment: {str(e)}"
    
    def get_all_suppliers(self):
        """Get all suppliers - FIXED to handle correct column order"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        id, supplier_name, phone, total_amount, paid_amount, 
                        remaining_balance, created_date, status, last_payment_date, type
                    FROM supplier_udhar 
                    ORDER BY id ASC
                ''')
                result = cursor.fetchall()
                return result if result else []
        except Exception as e:
            print(f"Error getting suppliers: {e}")
            return []
    
    def search_suppliers(self, search_term):
        """Search suppliers by name or phone"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        id, supplier_name, phone, total_amount, paid_amount, 
                        remaining_balance, created_date, status, last_payment_date, type
                    FROM supplier_udhar 
                    WHERE supplier_name LIKE ? OR phone LIKE ?
                    ORDER BY id ASC
                ''', (f'%{search_term}%', f'%{search_term}%'))
                result = cursor.fetchall()
                return result if result else []
        except Exception as e:
            print(f"Error searching suppliers: {e}")
            return []
    
    def get_supplier_summary(self):
        """Get supplier summary statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_suppliers,
                        COALESCE(SUM(total_amount), 0) as total_udhar,
                        COALESCE(SUM(paid_amount), 0) as total_paid,
                        COALESCE(SUM(remaining_balance), 0) as total_balance
                    FROM supplier_udhar
                ''')
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(f"Error getting supplier summary: {e}")
            return (0, 0, 0, 0)
    
    def force_delete_supplier(self, supplier_id):
        """Force delete supplier (for fully paid suppliers)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if supplier exists and is fully paid
                cursor.execute('SELECT remaining_balance FROM supplier_udhar WHERE id = ?', (supplier_id,))
                result = cursor.fetchone()
                
                if not result:
                    return False, "Supplier not found"
                
                remaining_balance = float(result[0]) if result[0] else 0.0
                
                if remaining_balance > 0:
                    return False, "Cannot delete supplier with pending balance"
                
                # Delete the supplier
                cursor.execute('DELETE FROM supplier_udhar WHERE id = ?', (supplier_id,))
                conn.commit()
                return True, "Supplier deleted successfully"
                
        except Exception as e:
            return False, f"Error deleting supplier: {str(e)}"

    # ENHANCED METHODS FOR BILL FUNCTIONALITY
    def add_customer_with_items(self, customer_name, phone, address, items):
            """Add new customer with udhar items"""
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Validate inputs
                    if not customer_name or not customer_name.strip():
                        return False, "Customer name is required"
                    
                    if not items:
                        return False, "At least one item is required"
                    
                    # Calculate total amount from items
                    total_amount = sum(item['quantity'] * item['unit_price'] for item in items)
                    
                    if total_amount <= 0:
                        return False, "Total amount must be greater than 0"
                    
                    # Insert customer
                    cursor.execute('''
                        INSERT INTO customer_udhar 
                        (customer_name, phone, address, total_amount, paid_amount, remaining_balance, status)
                        VALUES (?, ?, ?, ?, 0, ?, 'UNPAID')
                    ''', (
                        customer_name.strip(),
                        phone.strip() if phone else "",
                        address.strip() if address else "",
                        float(total_amount),
                        float(total_amount)
                    ))
                    
                    customer_id = cursor.lastrowid
                    
                    # Insert items
                    for item in items:
                        cursor.execute('''
                            INSERT INTO udhar_items 
                            (udhar_id, udhar_type, product_name, quantity, unit, unit_price, total_price)
                            VALUES (?, 'customer', ?, ?, ?, ?, ?)
                        ''', (
                            customer_id,
                            item['product_name'],
                            item['quantity'],
                            item['unit'],
                            item['unit_price'],
                            item['quantity'] * item['unit_price']
                        ))
                    
                    # Add credit transaction
                    cursor.execute('''
                        INSERT INTO udhar_transactions 
                        (udhar_id, udhar_type, transaction_type, amount, description)
                        VALUES (?, 'customer', 'credit', ?, 'Initial credit sale')
                    ''', (customer_id, total_amount))
                    
                    conn.commit()
                    return True, "Customer added successfully with items"
                    
            except sqlite3.Error as e:
                return False, f"Database error: {str(e)}"
            except Exception as e:
                return False, f"Error: {str(e)}"
    
    def get_customer_udhar_items(self, customer_id):
        """Get all items for a customer udhar"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, product_name, quantity, unit, unit_price, total_price, created_date
                    FROM udhar_items 
                    WHERE udhar_id = ? AND udhar_type = 'customer'
                    ORDER BY created_date DESC
                ''', (customer_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting customer items: {e}")
            return []
    
    def get_customer_transactions(self, customer_id):
        """Get all transactions for a customer udhar"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT transaction_type, amount, description, transaction_date
                    FROM udhar_transactions 
                    WHERE udhar_id = ? AND udhar_type = 'customer'
                    ORDER BY transaction_date DESC
                ''', (customer_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting customer transactions: {e}")
            return []
    
    def add_supplier_with_items(self, supplier_name, phone, address, items, supplier_type="Supplier"):
        """Add new supplier with udhar items"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Validate inputs
                if not supplier_name or not supplier_name.strip():
                    return False, "Supplier name is required"
                
                if not items:
                    return False, "At least one item is required"
                
                # Calculate total amount from items
                total_amount = sum(item['quantity'] * item['unit_price'] for item in items)
                
                if total_amount <= 0:
                    return False, "Total amount must be greater than 0"
                
                # Insert supplier
                cursor.execute('''
                    INSERT INTO supplier_udhar 
                    (supplier_name, phone, address, total_amount, paid_amount, remaining_balance, status, type)
                    VALUES (?, ?, ?, ?, 0, ?, 'UNPAID', ?)
                ''', (
                    supplier_name.strip(),
                    phone.strip() if phone else "",
                    address.strip() if address else "",
                    float(total_amount),
                    float(total_amount),
                    supplier_type
                ))
                
                supplier_id = cursor.lastrowid
                
                # Insert items
                for item in items:
                    cursor.execute('''
                        INSERT INTO udhar_items 
                        (udhar_id, udhar_type, product_name, quantity, unit, unit_price, total_price)
                        VALUES (?, 'supplier', ?, ?, ?, ?, ?)
                    ''', (
                        supplier_id,
                        item['product_name'],
                        item['quantity'],
                        item['unit'],
                        item['unit_price'],
                        item['quantity'] * item['unit_price']
                    ))
                
                # Add credit transaction
                cursor.execute('''
                    INSERT INTO udhar_transactions 
                    (udhar_id, udhar_type, transaction_type, amount, description)
                    VALUES (?, 'supplier', 'credit', ?, 'Initial credit purchase')
                ''', (supplier_id, total_amount))
                
                conn.commit()
                return True, "Supplier added successfully with items"
                
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_supplier_udhar_items(self, supplier_id):
        """Get all items for a supplier udhar"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, product_name, quantity, unit, unit_price, total_price, created_date
                    FROM udhar_items 
                    WHERE udhar_id = ? AND udhar_type = 'supplier'
                    ORDER BY created_date DESC
                ''', (supplier_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting supplier items: {e}")
            return []
        except Exception as e:
            print(f"Error getting supplier items: {e}")
            return []
    
    def get_supplier_transactions(self, supplier_id):
        """Get all transactions for a supplier udhar"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT transaction_type, amount, description, transaction_date
                    FROM udhar_transactions 
                    WHERE udhar_id = ? AND udhar_type = 'supplier'
                    ORDER BY transaction_date DESC
                ''', (supplier_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting supplier transactions: {e}")
            return []

    # ENHANCED SEARCH METHODS
    def search_customers_enhanced(self, search_term):
        """Search customers by name OR phone"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                search_pattern = f'%{search_term}%'
                cursor.execute('''
                    SELECT 
                        id, customer_name, phone, total_amount, paid_amount, 
                        remaining_balance, created_date, status, last_payment_date
                    FROM customer_udhar 
                    WHERE customer_name LIKE ? OR phone LIKE ?
                    ORDER BY id ASC
                ''', (search_pattern, search_pattern))
                result = cursor.fetchall()
                return result if result else []
        except Exception as e:
            print(f"Error searching customers: {e}")
            return []
    
    def search_suppliers_enhanced(self, search_term):
        """Search suppliers by name OR phone"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                search_pattern = f'%{search_term}%'
                cursor.execute('''
                    SELECT 
                        id, supplier_name, phone, total_amount, paid_amount, 
                        remaining_balance, created_date, status, last_payment_date, type
                    FROM supplier_udhar 
                    WHERE supplier_name LIKE ? OR phone LIKE ?
                    ORDER BY id ASC
                ''', (search_pattern, search_pattern))
                result = cursor.fetchall()
                return result if result else []
        except Exception as e:
            print(f"Error searching suppliers: {e}")
            return []
    def get_customer_summary_totals(self):
        """Get customer summary totals for header"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_customers,
                        COALESCE(SUM(total_amount), 0) as total_udhar,
                        COALESCE(SUM(paid_amount), 0) as total_paid,
                        COALESCE(SUM(remaining_balance), 0) as total_balance
                    FROM customer_udhar
                ''')
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(f"Error getting customer summary: {e}")
            return (0, 0, 0, 0)

    def get_supplier_summary_totals(self):
        """Get supplier summary totals for header"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_suppliers,
                        COALESCE(SUM(total_amount), 0) as total_udhar,
                        COALESCE(SUM(paid_amount), 0) as total_paid,
                        COALESCE(SUM(remaining_balance), 0) as total_balance
                    FROM supplier_udhar
                ''')
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(f"Error getting supplier summary: {e}")
            return (0, 0, 0, 0)

    def get_overall_summary(self):
        """Get overall summary for both customers and suppliers"""
        try:
            customer_summary = self.get_customer_summary_totals()
            supplier_summary = self.get_supplier_summary_totals()
            
            total_customers = customer_summary[0]
            total_customer_udhar = customer_summary[1]
            total_customer_paid = customer_summary[2]
            total_customer_balance = customer_summary[3]
            
            total_suppliers = supplier_summary[0]
            total_supplier_udhar = supplier_summary[1]
            total_supplier_paid = supplier_summary[2]
            total_supplier_balance = supplier_summary[3]
            
            # Calculate overall totals
            total_udhar = total_customer_udhar + total_supplier_udhar
            total_paid = total_customer_paid + total_supplier_paid
            total_balance = total_customer_balance + total_supplier_balance
            
            return {
                'customers': {
                    'count': total_customers,
                    'total_udhar': total_customer_udhar,
                    'total_paid': total_customer_paid,
                    'total_balance': total_customer_balance
                },
                'suppliers': {
                    'count': total_suppliers,
                    'total_udhar': total_supplier_udhar,
                    'total_paid': total_supplier_paid,
                    'total_balance': total_supplier_balance
                },
                'overall': {
                    'total_udhar': total_udhar,
                    'total_paid': total_paid,
                    'total_balance': total_balance
                }
            }
        except Exception as e:
            print(f"Error getting overall summary: {e}")
            return {
                'customers': {'count': 0, 'total_udhar': 0, 'total_paid': 0, 'total_balance': 0},
                'suppliers': {'count': 0, 'total_udhar': 0, 'total_paid': 0, 'total_balance': 0},
                'overall': {'total_udhar': 0, 'total_paid': 0, 'total_balance': 0}
            }