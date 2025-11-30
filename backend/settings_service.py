# import sqlite3
# import os
# from datetime import datetime
# import hashlib
# import shutil

# class SettingsService:
#     def __init__(self, db_path='awan_hardware.db'):
#         self.db_path = db_path
    
#     def get_connection(self):
#         """Get database connection"""
#         try:
#             return sqlite3.connect(self.db_path)
#         except sqlite3.Error as e:
#             print(f"Database connection error: {e}")
#             raise
    
#     def get_backup_directory(self):
#         """Get the fixed backup directory that survives app reinstallation"""
#         backup_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'AwanHardwareBackups')
#         os.makedirs(backup_dir, exist_ok=True)
#         return backup_dir
    
#     def backup_database(self, user_id=None):
#         """Create database backup in fixed location - SINGLE METHOD"""
#         try:
#             backup_dir = self.get_backup_directory()
            
#             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#             filename = f"awan_hardware_backup_{timestamp}.db"
#             full_path = os.path.join(backup_dir, filename)
            
#             print(f"📦 Creating backup: {filename}")
#             print(f"📍 Backup location: {backup_dir}")
            
#             # Copy database file
#             shutil.copy2(self.db_path, full_path)
            
#             # Verify backup was created
#             if os.path.exists(full_path):
#                 file_size = os.path.getsize(full_path) / (1024 * 1024)  # Size in MB
#                 print(f"✅ Backup created successfully: {file_size:.2f} MB")
                
#                 # Log backup action
#                 try:
#                     self.log_audit_event(
#                         user_id=user_id,
#                         username='System',
#                         action='BACKUP_CREATED',
#                         details=f'Backup created: {filename}'
#                     )
#                 except:
#                     print("⚠️ Could not log audit event (table might not exist)")
                
#                 return full_path
#             else:
#                 print("❌ Backup file was not created")
#                 return None
                
#         except Exception as e:
#             print(f"❌ Error creating backup: {e}")
#             return None
    
#     def initialize_default_settings(self):
#         """Initialize default settings"""
#         try:
#             with self.get_connection() as conn:
#                 cursor = conn.cursor()
                
#                 # Default app settings
#                 default_app_settings = [
#                     ('backup_interval', 'daily', 'text', 'system', 'Auto-backup frequency'),
#                     ('backup_path', self.get_backup_directory(), 'text', 'system', 'Default backup location'),
#                     ('dashboard_refresh', '30', 'number', 'system', 'Dashboard refresh interval in seconds'),
#                     ('theme', 'light', 'text', 'system', 'UI theme selection')
#                 ]
                
#                 for key, value, setting_type, category, description in default_app_settings:
#                     cursor.execute('SELECT COUNT(*) FROM app_settings WHERE setting_key = ?', (key,))
#                     exists = cursor.fetchone()[0] > 0
                    
#                     if not exists:
#                         cursor.execute('''
#                             INSERT INTO app_settings 
#                             (setting_key, setting_value, setting_type, category, description)
#                             VALUES (?, ?, ?, ?, ?)
#                         ''', (key, value, setting_type, category, description))
                
#                 conn.commit()
#                 return True
                
#         except Exception as e:
#             print(f"Error initializing settings: {e}")
#             return False
    
#     def get_setting(self, key, default=None):
#         """Get setting value from app_settings table"""
#         try:
#             with self.get_connection() as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('SELECT setting_value FROM app_settings WHERE setting_key = ?', (key,))
#                 result = cursor.fetchone()
#                 return result[0] if result and result[0] else default
#         except Exception as e:
#             return default
    
#     def set_setting(self, key, value):
#         """Update or create a setting in app_settings table"""
#         try:
#             with self.get_connection() as conn:
#                 cursor = conn.cursor()
                
#                 # Check if setting exists
#                 cursor.execute('SELECT COUNT(*) FROM app_settings WHERE setting_key = ?', (key,))
#                 exists = cursor.fetchone()[0] > 0
                
#                 if exists:
#                     # Update existing setting
#                     cursor.execute('''
#                         UPDATE app_settings 
#                         SET setting_value = ?, updated_at = CURRENT_TIMESTAMP
#                         WHERE setting_key = ?
#                     ''', (value, key))
#                 else:
#                     # Insert new setting with default type and category
#                     cursor.execute('''
#                         INSERT INTO app_settings 
#                         (setting_key, setting_value, setting_type, category, description)
#                         VALUES (?, ?, 'text', 'system', 'User defined setting')
#                     ''', (key, value))
                
#                 conn.commit()
#                 return True
                
#         except Exception as e:
#             print(f"Error setting setting {key}: {e}")
#             return False
    
#     def get_security_setting(self, setting_name, default=None):
#         """Get security setting value"""
#         try:
#             with self.get_connection() as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('SELECT setting_value FROM security_settings WHERE setting_name = ?', (setting_name,))
#                 result = cursor.fetchone()
#                 return result[0] if result and result[0] else default
#         except Exception as e:
#             return default
    
#     def set_security_setting(self, setting_name, value):
#         """Update security setting"""
#         try:
#             with self.get_connection() as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''
#                     UPDATE security_settings 
#                     SET setting_value = ?, updated_at = CURRENT_TIMESTAMP
#                     WHERE setting_name = ?
#                 ''', (value, setting_name))
#                 conn.commit()
#             return True
#         except Exception as e:
#             print(f"Error setting security setting {setting_name}: {e}")
#             return False
    
#     def log_audit_event(self, user_id=None, username=None, action=None, ip_address=None, details=None):
#         """Log audit event"""
#         try:
#             with self.get_connection() as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''
#                     INSERT INTO audit_logs 
#                     (user_id, username, action, ip_address, details)
#                     VALUES (?, ?, ?, ?, ?)
#                 ''', (user_id, username, action, ip_address, details))
#                 conn.commit()
#             return True
#         except Exception as e:
#             print(f"Error logging audit event: {e}")
#             return False
    
#     def get_audit_logs(self, limit=50):
#         """Get audit logs"""
#         try:
#             with self.get_connection() as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''
#                     SELECT username, action, timestamp, ip_address, details
#                     FROM audit_logs 
#                     ORDER BY timestamp DESC 
#                     LIMIT ?
#                 ''', (limit,))
#                 return cursor.fetchall()
#         except Exception as e:
#             print(f"Error getting audit logs: {e}")
#             return []
    
#     # USER MANAGEMENT METHODS
#     def get_all_users(self):
#         """Get all users through user service"""
#         try:
#             from backend.user_service import UserService
#             user_service = UserService()
#             return user_service.get_all_users()
#         except Exception as e:
#             print(f"Error getting users: {e}")
#             return []

#     def add_user(self, username, password, role, full_name, phone=""):
#         """Add new user through user service"""
#         try:
#             from backend.user_service import UserService
#             user_service = UserService()
#             return user_service.add_user(username, password, role, full_name, phone)
#         except Exception as e:
#             print(f"Error adding user: {e}")
#             raise e

#     def update_user(self, user_id, username, role, full_name, phone, is_active):
#         """Update user through user service"""
#         try:
#             from backend.user_service import UserService
#             user_service = UserService()
#             return user_service.update_user(user_id, username, role, full_name, phone, is_active)
#         except Exception as e:
#             print(f"Error updating user: {e}")
#             raise e

#     def delete_user(self, user_id):
#         """Delete user through user service"""
#         try:
#             from backend.user_service import UserService
#             user_service = UserService()
#             return user_service.delete_user(user_id)
#         except Exception as e:
#             print(f"Error deleting user: {e}")
#             raise e

#     def change_user_password_service(self, user_id, new_password):
#         """Change user password through user service"""
#         try:
#             from backend.user_service import UserService
#             user_service = UserService()
#             return user_service.change_user_password(user_id, new_password)
#         except Exception as e:
#             print(f"Error changing user password: {e}")
#             raise e
import sqlite3
import os
from datetime import datetime
import shutil

class SettingsService:
    def __init__(self, db_path='awan_hardware.db'):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error:
            raise
    
    def get_backup_directory(self):
        """Get the fixed backup directory that survives app reinstallation"""
        backup_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'AwanHardwareBackups')
        os.makedirs(backup_dir, exist_ok=True)
        return backup_dir
    
    def backup_database(self, user_id=None):
        """Create database backup in fixed location"""
        try:
            backup_dir = self.get_backup_directory()
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"awan_hardware_backup_{timestamp}.db"
            full_path = os.path.join(backup_dir, filename)
            
            # Copy database file
            shutil.copy2(self.db_path, full_path)
            
            # Verify backup was created
            if os.path.exists(full_path):
                # Log backup action
                try:
                    self.log_audit_event(
                        user_id=user_id,
                        username='System',
                        action='BACKUP_CREATED',
                        details=f'Backup created: {filename}'
                    )
                except:
                    pass  # Skip if logging fails
                
                return full_path
            else:
                return None
                
        except Exception:
            return None
    
    def initialize_default_settings(self):
        """Initialize default settings"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Default app settings
                default_app_settings = [
                    ('backup_interval', 'daily', 'text', 'system', 'Auto-backup frequency'),
                    ('backup_path', self.get_backup_directory(), 'text', 'system', 'Default backup location'),
                    ('dashboard_refresh', '30', 'number', 'system', 'Dashboard refresh interval in seconds'),
                    ('theme', 'light', 'text', 'system', 'UI theme selection')
                ]
                
                for key, value, setting_type, category, description in default_app_settings:
                    cursor.execute('SELECT COUNT(*) FROM app_settings WHERE setting_key = ?', (key,))
                    exists = cursor.fetchone()[0] > 0
                    
                    if not exists:
                        cursor.execute('''
                            INSERT INTO app_settings 
                            (setting_key, setting_value, setting_type, category, description)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (key, value, setting_type, category, description))
                
                conn.commit()
                return True
                
        except Exception:
            return False
    
    def get_setting(self, key, default=None):
        """Get setting value from app_settings table"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT setting_value FROM app_settings WHERE setting_key = ?', (key,))
                result = cursor.fetchone()
                return result[0] if result and result[0] else default
        except Exception:
            return default
    
    def set_setting(self, key, value):
        """Update or create a setting in app_settings table"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if setting exists
                cursor.execute('SELECT COUNT(*) FROM app_settings WHERE setting_key = ?', (key,))
                exists = cursor.fetchone()[0] > 0
                
                if exists:
                    # Update existing setting
                    cursor.execute('''
                        UPDATE app_settings 
                        SET setting_value = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE setting_key = ?
                    ''', (value, key))
                else:
                    # Insert new setting with default type and category
                    cursor.execute('''
                        INSERT INTO app_settings 
                        (setting_key, setting_value, setting_type, category, description)
                        VALUES (?, ?, 'text', 'system', 'User defined setting')
                    ''', (key, value))
                
                conn.commit()
                return True
                
        except Exception:
            return False
    
    def get_security_setting(self, setting_name, default=None):
        """Get security setting value"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT setting_value FROM security_settings WHERE setting_name = ?', (setting_name,))
                result = cursor.fetchone()
                return result[0] if result and result[0] else default
        except Exception:
            return default
    
    def set_security_setting(self, setting_name, value):
        """Update security setting"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE security_settings 
                    SET setting_value = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE setting_name = ?
                ''', (value, setting_name))
                conn.commit()
            return True
        except Exception:
            return False
    
    def log_audit_event(self, user_id=None, username=None, action=None, ip_address=None, details=None):
        """Log audit event"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO audit_logs 
                    (user_id, username, action, ip_address, details)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, username, action, ip_address, details))
                conn.commit()
            return True
        except Exception:
            return False
    
    def get_audit_logs(self, limit=50):
        """Get audit logs"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT username, action, timestamp, ip_address, details
                    FROM audit_logs 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
                return cursor.fetchall()
        except Exception:
            return []
    
    # USER MANAGEMENT METHODS
    def get_all_users(self):
        """Get all users through user service"""
        try:
            from backend.user_service import UserService
            user_service = UserService()
            return user_service.get_all_users()
        except Exception:
            return []

    def add_user(self, username, password, role, full_name, phone=""):
        """Add new user through user service"""
        try:
            from backend.user_service import UserService
            user_service = UserService()
            return user_service.add_user(username, password, role, full_name, phone)
        except Exception as e:
            raise e

    def update_user(self, user_id, username, role, full_name, phone, is_active):
        """Update user through user service"""
        try:
            from backend.user_service import UserService
            user_service = UserService()
            return user_service.update_user(user_id, username, role, full_name, phone, is_active)
        except Exception as e:
            raise e

    def delete_user(self, user_id):
        """Delete user through user service"""
        try:
            from backend.user_service import UserService
            user_service = UserService()
            return user_service.delete_user(user_id)
        except Exception as e:
            raise e

    def change_user_password_service(self, user_id, new_password):
        """Change user password through user service"""
        try:
            from backend.user_service import UserService
            user_service = UserService()
            return user_service.change_user_password(user_id, new_password)
        except Exception as e:
            raise e