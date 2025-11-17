import sqlite3
import hashlib
from datetime import datetime

class UserService:
    def __init__(self, db_path='awan_hardware.db'):
        self.db_path = db_path
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def hash_password(self, password):
        """Simple password hashing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, username, role, full_name, password_hash 
                    FROM users 
                    WHERE username = ? AND is_active = 1
                ''', (username,))
                user = cursor.fetchone()
                
                if user and user[4] == self.hash_password(password):
                    # Update last login
                    cursor.execute('''
                        UPDATE users SET last_login = ? WHERE id = ?
                    ''', (datetime.now(), user[0]))
                    conn.commit()
                    
                    return {
                        'id': user[0],
                        'username': user[1],
                        'role': user[2],
                        'full_name': user[3]
                    }
                return None
        except Exception as e:
            print(f"Error verifying user: {e}")
            return None
    
    def get_all_users(self):
        """Get all users"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, username, role, full_name, phone, is_active, created_at, last_login
                    FROM users 
                    ORDER BY created_at DESC
                ''')
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
    
    def add_user(self, username, password, role, full_name, phone=""):
        """Add new user"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if username exists
                cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
                if cursor.fetchone():
                    return False, "Username already exists"
                
                password_hash = self.hash_password(password)
                
                cursor.execute('''
                    INSERT INTO users (username, password_hash, role, full_name, phone)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, password_hash, role, full_name, phone))
                
                conn.commit()
                return True, "User added successfully"
                
        except Exception as e:
            return False, f"Error adding user: {str(e)}"
    
    def update_user(self, user_id, role=None, full_name=None, phone=None, is_active=None):
        """Update user information"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                updates = []
                params = []
                
                if role is not None:
                    updates.append("role = ?")
                    params.append(role)
                
                if full_name is not None:
                    updates.append("full_name = ?")
                    params.append(full_name)
                
                if phone is not None:
                    updates.append("phone = ?")
                    params.append(phone)
                
                if is_active is not None:
                    updates.append("is_active = ?")
                    params.append(is_active)
                
                if updates:
                    params.append(user_id)
                    query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
                    cursor.execute(query, params)
                    conn.commit()
                
                return True, "User updated successfully"
                
        except Exception as e:
            return False, f"Error updating user: {str(e)}"
    
    def change_password(self, user_id, new_password):
        """Change user password"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                password_hash = self.hash_password(new_password)
                
                cursor.execute('''
                    UPDATE users SET password_hash = ? WHERE id = ?
                ''', (password_hash, user_id))
                
                conn.commit()
                return True, "Password changed successfully"
                
        except Exception as e:
            return False, f"Error changing password: {str(e)}"
    
    def delete_user(self, user_id):
        """Delete user (soft delete)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Prevent deleting the last admin
                cursor.execute('SELECT COUNT(*) FROM users WHERE role = "admin" AND is_active = 1')
                admin_count = cursor.fetchone()[0]
                
                cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
                user_role = cursor.fetchone()[0]
                
                if user_role == 'admin' and admin_count <= 1:
                    return False, "Cannot delete the last admin user"
                
                cursor.execute('UPDATE users SET is_active = 0 WHERE id = ?', (user_id,))
                conn.commit()
                
                return True, "User deleted successfully"
                
        except Exception as e:
            return False, f"Error deleting user: {str(e)}"