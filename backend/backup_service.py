import sqlite3
import shutil
import os
from datetime import datetime
import tkinter.messagebox as messagebox

class BackupService:
    def __init__(self, db_path='awan_hardware.db'):
        self.db_path = db_path
        self.backup_dir = 'backups'
        
        # Create backup directory if it doesn't exist
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def create_backup(self, user_id=None):
        """Create database backup"""
        try:
            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"awan_hardware_backup_{timestamp}.db"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # Create backup
            shutil.copy2(self.db_path, backup_path)
            
            # Get file size
            file_size = os.path.getsize(backup_path)
            
            # Save backup record to database
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO backup_history (filename, backup_path, file_size, created_by)
                    VALUES (?, ?, ?, ?)
                ''', (backup_filename, backup_path, file_size, user_id))
                conn.commit()
            
            return True, f"Backup created successfully: {backup_filename}", backup_path
            
        except Exception as e:
            return False, f"Backup failed: {str(e)}", None
    
    def restore_backup(self, backup_path):
        """Restore database from backup"""
        try:
            # Check if backup file exists
            if not os.path.exists(backup_path):
                return False, "Backup file not found"
            
            # Close any existing connections
            import gc
            gc.collect()
            
            # Create temporary backup of current database
            temp_backup = f"{self.db_path}.temp_backup"
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, temp_backup)
            
            try:
                # Replace current database with backup
                shutil.copy2(backup_path, self.db_path)
                
                # Verify the restored database
                try:
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = cursor.fetchall()
                    conn.close()
                    
                    if not tables:
                        # Restore from temp backup if verification fails
                        if os.path.exists(temp_backup):
                            shutil.copy2(temp_backup, self.db_path)
                        return False, "Backup file is corrupted"
                    
                except sqlite3.Error:
                    # Restore from temp backup if verification fails
                    if os.path.exists(temp_backup):
                        shutil.copy2(temp_backup, self.db_path)
                    return False, "Backup file is corrupted"
                
                # Clean up temp backup
                if os.path.exists(temp_backup):
                    os.remove(temp_backup)
                
                return True, "Database restored successfully"
                
            except Exception as restore_error:
                # Restore from temp backup if restore fails
                if os.path.exists(temp_backup):
                    shutil.copy2(temp_backup, self.db_path)
                    if os.path.exists(temp_backup):
                        os.remove(temp_backup)
                return False, f"Restore failed: {str(restore_error)}"
            
        except Exception as e:
            return False, f"Restore error: {str(e)}"
    
    def get_backup_history(self):
        """Get backup history"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT bh.id, bh.filename, bh.backup_path, bh.file_size, 
                           bh.created_at, u.username, u.full_name
                    FROM backup_history bh
                    LEFT JOIN users u ON bh.created_by = u.id
                    ORDER BY bh.created_at DESC
                    LIMIT 20
                ''')
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting backup history: {e}")
            return []
    
    def get_backup_file_size(self, file_path):
        """Get human readable file size"""
        try:
            size = os.path.getsize(file_path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return "Unknown"
    
    def delete_backup(self, backup_id, backup_path):
        """Delete backup file and record"""
        try:
            # Delete file
            if os.path.exists(backup_path):
                os.remove(backup_path)
            
            # Delete record
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM backup_history WHERE id = ?', (backup_id,))
                conn.commit()
            
            return True, "Backup deleted successfully"
            
        except Exception as e:
            return False, f"Error deleting backup: {str(e)}"