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
        """Add new customer with udhar"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Validate inputs
                if not customer_name or not customer_name.strip():
                    return False, "Customer name is required"
                
                if not total_amount or total_amount <= 0:
                    return False, "Amount must be greater than 0"
                
                # Insert customer
                cursor.execute('''
                    INSERT INTO customer_udhar 
                    (customer_name, phone, total_amount, remaining_balance, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    customer_name.strip(),
                    phone.strip() if phone else "",
                    float(total_amount),
                    float(total_amount),
                    'UNPAID'
                ))
                conn.commit()
                return True, "Customer added successfully"
                
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def receive_payment(self, customer_id, payment_amount):
        """Receive payment from customer"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get current customer data
                cursor.execute('''
                    SELECT total_amount, paid_amount, remaining_balance 
                    FROM customer_udhar WHERE id = ?
                ''', (customer_id,))
                result = cursor.fetchone()
                
                if not result:
                    return False, "Customer not found"
                
                total_amount, paid_amount, remaining_balance = result
                
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
                
                # Update customer
                cursor.execute('''
                    UPDATE customer_udhar 
                    SET paid_amount = ?, remaining_balance = ?, status = ?
                    WHERE id = ?
                ''', (new_paid, new_balance, status, customer_id))
                conn.commit()
                
                # If fully paid, delete the customer
                if new_balance == 0:
                    cursor.execute('DELETE FROM customer_udhar WHERE id = ?', (customer_id,))
                    conn.commit()
                    return True, "Payment received successfully and customer removed (fully paid)"
                
                return True, "Payment received successfully"
                
        except Exception as e:
            return False, f"Error processing payment: {str(e)}"
    
    def get_all_customers(self):
        """Get all customers - OLDEST FIRST (natural order)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM customer_udhar 
                    ORDER BY id ASC
                ''')
                result = cursor.fetchall()
                return result if result else []  # Always return a list
        except Exception as e:
            print(f"Error getting customers: {e}")
            return []  # FIXED: Return empty list instead of None
    
    def search_customers(self, search_term):
        """Search customers by name or phone - OLDEST FIRST"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM customer_udhar 
                    WHERE customer_name LIKE ? OR phone LIKE ?
                    ORDER BY id ASC
                ''', (f'%{search_term}%', f'%{search_term}%'))
                result = cursor.fetchall()
                return result if result else []  # Always return a list
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
        """Add new supplier with udhar"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Validate inputs
                if not supplier_name or not supplier_name.strip():
                    return False, "Supplier name is required"
                
                if not total_amount or total_amount <= 0:
                    return False, "Amount must be greater than 0"
                
                # Insert supplier
                cursor.execute('''
                    INSERT INTO supplier_udhar 
                    (supplier_name, phone, total_amount, remaining_balance, status, type)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    supplier_name.strip(),
                    phone.strip() if phone else "",
                    float(total_amount),
                    float(total_amount),
                    'UNPAID',
                    supplier_type
                ))
                conn.commit()
                return True, "Supplier added successfully"
                
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def make_payment(self, supplier_id, payment_amount):
        """Make payment to supplier"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get current supplier data
                cursor.execute('''
                    SELECT total_amount, paid_amount, remaining_balance 
                    FROM supplier_udhar WHERE id = ?
                ''', (supplier_id,))
                result = cursor.fetchone()
                
                if not result:
                    return False, "Supplier not found"
                
                total_amount, paid_amount, remaining_balance = result
                
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
                
                # Update supplier
                cursor.execute('''
                    UPDATE supplier_udhar 
                    SET paid_amount = ?, remaining_balance = ?, status = ?
                    WHERE id = ?
                ''', (new_paid, new_balance, status, supplier_id))
                conn.commit()
                
                # If fully paid, delete the supplier
                if new_balance == 0:
                    cursor.execute('DELETE FROM supplier_udhar WHERE id = ?', (supplier_id,))
                    conn.commit()
                    return True, "Payment made successfully and supplier removed (fully paid)"
                
                return True, "Payment made successfully"
                
        except Exception as e:
            return False, f"Error processing payment: {str(e)}"
    
    def get_all_suppliers(self):
        """Get all suppliers - OLDEST FIRST (natural order)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM supplier_udhar 
                    ORDER BY id ASC
                ''')
                result = cursor.fetchall()
                return result if result else []  # Always return a list
        except Exception as e:
            print(f"Error getting suppliers: {e}")
            return []
    
    def search_suppliers(self, search_term):
        """Search suppliers by name or phone - OLDEST FIRST"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM supplier_udhar 
                    WHERE supplier_name LIKE ? OR phone LIKE ?
                    ORDER BY id ASC
                ''', (f'%{search_term}%', f'%{search_term}%'))
                result = cursor.fetchall()
                return result if result else []  # Always return a list
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