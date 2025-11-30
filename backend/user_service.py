# backend/user_service.py

from backend.database import Database

class UserService:
    def __init__(self):
        self.db = Database()
    
    def get_all_users(self):
        """Get all users"""
        return self.db.get_all_users()
    
    def get_next_user_id(self):
        """Get what the next user ID will be"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='users'")
                result = cursor.fetchone()
                return (result[0] + 1) if result else 1
        except:
            return 1
    
    def fix_user_sequence(self):
        """Fix user ID sequence to continue from current max ID"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get current maximum user ID
                cursor.execute("SELECT MAX(id) FROM users")
                max_id = cursor.fetchone()[0] or 0
                
                # Update sqlite_sequence to continue from max_id
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")
                cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('users', ?)", (max_id,))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error fixing user sequence: {e}")
            return False
    
    def add_user(self, username, password, role, full_name, phone=""):
        """Add new user with validation and sequence fix"""
        # Fix sequence before adding new user to ensure proper ID assignment
        self.fix_user_sequence()
        
        # Validation
        if not username or not username.strip():
            raise ValueError("Username is required")
        
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        if not full_name or not full_name.strip():
            raise ValueError("Full name is required")
        
        if role not in ['owner', 'cashier', 'manager']:
            raise ValueError("Invalid role")
        
        # Check if username exists
        if self.db.check_username_exists(username):
            raise ValueError(f"Username '{username}' already exists")
        
        # Add user to database
        return self.db.add_user(username, password, role, full_name, phone)
    
    def update_user(self, user_id, username, role, full_name, phone, is_active):
        """Update user with validation"""
        # Validation
        if not username or not username.strip():
            raise ValueError("Username is required")
        
        if not full_name or not full_name.strip():
            raise ValueError("Full name is required")
        
        if role not in ['owner', 'cashier', 'manager']:
            raise ValueError("Invalid role")
        
        # Check if username exists (excluding current user)
        if self.db.check_username_exists(username, user_id):
            raise ValueError(f"Username '{username}' already exists")
        
        # Update user
        return self.db.update_user(user_id, username, role, full_name, phone, is_active)
    
    def delete_user(self, user_id):
        """Delete user (soft delete)"""
        return self.db.delete_user(user_id)
    
    def change_user_password(self, user_id, new_password):
        """Change user password"""
        if not new_password or len(new_password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        return self.db.change_user_password(user_id, new_password)
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return self.db.get_user_by_id(user_id)
    
    def get_available_roles(self):
        """Get available user roles"""
        return [
            ('owner', 'Owner - Full system access'),
            ('manager', 'Manager - Inventory and sales management'),
            ('cashier', 'Cashier - POS and basic operations')
        ]
    
    def reset_user_sequence_manual(self):
        """Manual method to reset user sequence (for admin use)"""
        return self.fix_user_sequence()