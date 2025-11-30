# import tkinter as tk
# from frontend.login_window import LoginWindow
# from backend.settings_service import SettingsService
# import os
# import sqlite3
# import shutil
# import glob
# from datetime import datetime

# def get_backup_locations():
#     """Get all possible backup locations"""
#     locations = []
    
#     # 1. Application directory (where exe is located)
#     current_dir = os.getcwd()  # Use current working directory
#     locations.append(current_dir)
    
#     # 2. User's Documents folder
#     documents_path = os.path.join(os.path.expanduser('~'), 'Documents', 'AwanHardwareBackups')
#     locations.append(documents_path)
    
#     # 3. User's Desktop
#     desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'AwanHardwareBackups')
#     locations.append(desktop_path)
    
#     print("🔍 Backup locations to search:")
#     for loc in locations:
#         exists = "✅" if os.path.exists(loc) else "❌"
#         print(f"   {exists} {loc}")
    
#     return locations

# def find_latest_backup():
#     """Find the latest backup file across all locations"""
#     print("🔄 Searching for backup files...")
#     backup_files = []
    
#     for location in get_backup_locations():
#         if os.path.exists(location):
#             pattern = os.path.join(location, 'awan_hardware_backup_*.db')
#             found_files = glob.glob(pattern)
#             if found_files:
#                 print(f"📍 Found {len(found_files)} backup(s) in {location}")
#                 for f in found_files[:3]:  # Show first 3 files
#                     file_time = datetime.fromtimestamp(os.path.getmtime(f))
#                     file_size = os.path.getsize(f) / (1024 * 1024)
#                     print(f"   📄 {os.path.basename(f)} - {file_time.strftime('%H:%M:%S')} - {file_size:.2f} MB")
#                 backup_files.extend(found_files)
    
#     if backup_files:
#         # Sort by modification time (newest first)
#         backup_files.sort(key=os.path.getmtime, reverse=True)
#         latest = backup_files[0]
#         latest_time = datetime.fromtimestamp(os.path.getmtime(latest))
#         print(f"✅ Latest backup: {os.path.basename(latest)} ({latest_time.strftime('%Y-%m-%d %H:%M:%S')})")
#         return latest
#     else:
#         print("❌ No backup files found in any location!")
#         return None

# def check_database_integrity():
#     """Check if main database exists and is valid"""
#     db_file = 'awan_hardware.db'
    
#     print(f"\n🔍 Checking database: {db_file}")
    
#     # Check if database exists
#     if not os.path.exists(db_file):
#         print("❌ Database file does not exist!")
#         return False
    
#     file_size = os.path.getsize(db_file) / (1024 * 1024)  # Size in MB
#     print(f"📊 Database size: {file_size:.2f} MB")
    
#     if file_size == 0:
#         print("❌ Database file is empty!")
#         return False
    
#     try:
#         # Test database connection and check essential tables
#         conn = sqlite3.connect(db_file)
#         cursor = conn.cursor()
        
#         # Check if essential tables exist
#         cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
#         all_tables = [row[0] for row in cursor.fetchall()]
#         print(f"📋 Found {len(all_tables)} tables")
        
#         required_tables = ['users', 'products', 'categories', 'sales']
#         missing_tables = [table for table in required_tables if table not in all_tables]
        
#         if missing_tables:
#             print(f"❌ Missing essential tables: {missing_tables}")
#             conn.close()
#             return False
        
#         print("✅ All essential tables found")
        
#         # Check if there's any data
#         cursor.execute("SELECT COUNT(*) FROM products")
#         product_count = cursor.fetchone()[0]
#         print(f"📦 Products in database: {product_count}")
        
#         cursor.execute("SELECT COUNT(*) FROM users")
#         user_count = cursor.fetchone()[0]
#         print(f"👥 Users in database: {user_count}")
        
#         conn.close()
        
#         if product_count == 0 and user_count == 0:
#             print("❌ Database appears to be empty (no products or users)")
#             return False
            
#         print("✅ Database integrity check passed")
#         return True
        
#     except sqlite3.Error as e:
#         print(f"❌ Database connection error: {e}")
#         return False
#     except Exception as e:
#         print(f"❌ Unexpected error during integrity check: {e}")
#         return False

# def auto_recover_database():
#     """Automatically recover from latest backup"""
#     try:
#         print("\n🔄 Starting automatic recovery process...")
        
#         # Find latest backup
#         latest_backup = find_latest_backup()
        
#         if not latest_backup:
#             print("❌ Cannot recover - no backup files found!")
#             return False
        
#         print(f"📦 Using backup: {os.path.basename(latest_backup)}")
        
#         # Create safety backup of current database (if exists)
#         current_db = 'awan_hardware.db'
#         if os.path.exists(current_db):
#             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#             safety_backup = f'corrupted_{timestamp}.db'
#             shutil.copy2(current_db, safety_backup)
#             print(f"💾 Created safety backup: {safety_backup}")
        
#         # Restore from backup
#         print("🔄 Restoring database...")
#         shutil.copy2(latest_backup, current_db)
#         print(f"✅ Successfully restored from: {os.path.basename(latest_backup)}")
        
#         # Verify restoration worked
#         print("🔍 Verifying restoration...")
#         if check_database_integrity():
#             print("🎉 Auto-recovery completed successfully!")
#             return True
#         else:
#             print("❌ Restored database failed integrity check")
#             return False
            
#     except Exception as e:
#         print(f"❌ Auto-recovery failed: {e}")
#         return False

# def initialize_application():
#     """Initialize application with smart auto-recovery"""
#     print("🚀 Starting AWAN HARDWARE POS System...")
#     print(f"📁 Working directory: {os.getcwd()}")
    
#     # Check if we need auto-recovery
#     needs_recovery = not check_database_integrity()
    
#     if needs_recovery:
#         print("\n⚠️ Database issue detected!")
#         print("🔄 Attempting automatic recovery...")
        
#         if auto_recover_database():
#             print("✅ Auto-recovery successful! Starting application...")
#         else:
#             print("❌ Auto-recovery failed!")
#             # Check if we should create fresh database
#             if not os.path.exists('awan_hardware.db'):
#                 print("🆕 Creating fresh database...")
#                 try:
#                     from backend.database import Database
#                     db = Database()
#                     print("✅ Fresh database created")
#                 except Exception as e:
#                     print(f"❌ Failed to create fresh database: {e}")
#     else:
#         print("✅ Database is healthy. Starting application...")
    
#     return True

# def main():
#     """Main application entry point"""
#     try:
#         print("=" * 60)
#         print("🛠️ AWAN HARDWARE POS - AUTO RECOVERY DEBUG MODE")
#         print("=" * 60)
        
#         # Initialize with auto-recovery
#         if not initialize_application():
#             raise Exception("Application initialization failed")
        
#         # Create and start the main application
#         root = tk.Tk()
#         root.title("AWAN HARDWARE POS System")
        
#         # Set window icon if available
#         try:
#             icon_path = 'awan_icon.ico'
#             if os.path.exists(icon_path):
#                 root.iconbitmap(icon_path)
#         except:
#             pass
        
#         # Start with login window
#         app = LoginWindow(root)
        
#         # Center the window
#         root.update_idletasks()
#         width = root.winfo_width()
#         height = root.winfo_height()
#         x = (root.winfo_screenwidth() // 2) - (width // 2)
#         y = (root.winfo_screenheight() // 2) - (height // 2)
#         root.geometry(f'+{x}+{y}')
        
#         print("✅ Application started successfully")
#         print("=" * 60)
#         root.mainloop()
        
#     except Exception as e:
#         print(f"❌ Critical error: {e}")
#         import traceback
#         traceback.print_exc()
        
#         # Simple error dialog
#         error_root = tk.Tk()
#         error_root.title("Application Error")
#         error_root.geometry("500x300")
        
#         tk.Label(error_root, text="❌ AWAN HARDWARE POS - Startup Error", 
#                 font=('Arial', 14, 'bold'), fg='red', pady=20).pack()
        
#         tk.Label(error_root, text=f"Error: {str(e)}", 
#                 font=('Arial', 9), wraplength=450, pady=10).pack()
        
#         tk.Button(error_root, text="Exit", command=error_root.destroy,
#                  bg='red', fg='white', font=('Arial', 12), pady=10, padx=20).pack(pady=20)
        
#         error_root.mainloop()

# if __name__ == '__main__':
#     main() 
import tkinter as tk
from frontend.login_window import LoginWindow
from backend.settings_service import SettingsService
import os
import sqlite3
import shutil
import glob
from datetime import datetime

def get_backup_locations():
    """Get all possible backup locations"""
    locations = []
    
    # Application directory
    current_dir = os.getcwd()
    locations.append(current_dir)
    
    # User's Documents folder
    documents_path = os.path.join(os.path.expanduser('~'), 'Documents', 'AwanHardwareBackups')
    locations.append(documents_path)
    
    # User's Desktop
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'AwanHardwareBackups')
    locations.append(desktop_path)
    
    return locations

def find_latest_backup():
    """Find the latest backup file across all locations"""
    backup_files = []
    
    for location in get_backup_locations():
        if os.path.exists(location):
            pattern = os.path.join(location, 'awan_hardware_backup_*.db')
            found_files = glob.glob(pattern)
            backup_files.extend(found_files)
    
    if backup_files:
        backup_files.sort(key=os.path.getmtime, reverse=True)
        return backup_files[0]
    return None

def check_database_integrity():
    """Check if main database exists and is valid"""
    db_file = 'awan_hardware.db'
    
    # Check if database exists
    if not os.path.exists(db_file):
        return False
    
    file_size = os.path.getsize(db_file)
    if file_size == 0:
        return False
    
    try:
        # Test database connection and check essential tables
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Check if essential tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('users', 'products', 'categories', 'sales')")
        essential_tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['users', 'products', 'categories']
        missing_tables = [table for table in required_tables if table not in essential_tables]
        
        if missing_tables:
            conn.close()
            return False
        
        # Check if there's any data
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        conn.close()
        
        if product_count == 0 and user_count == 0:
            return False
            
        return True
        
    except sqlite3.Error:
        return False
    except Exception:
        return False

def auto_recover_database():
    """Automatically recover from latest backup"""
    try:
        # Find latest backup
        latest_backup = find_latest_backup()
        
        if not latest_backup:
            return False
        
        # Create safety backup of current database (if exists)
        current_db = 'awan_hardware.db'
        if os.path.exists(current_db):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safety_backup = f'corrupted_{timestamp}.db'
            shutil.copy2(current_db, safety_backup)
        
        # Restore from backup
        shutil.copy2(latest_backup, current_db)
        
        # Verify restoration worked
        if check_database_integrity():
            return True
        else:
            return False
            
    except Exception:
        return False

def initialize_application():
    """Initialize application with smart auto-recovery"""
    
    # Check if we need auto-recovery
    needs_recovery = not check_database_integrity()
    
    if needs_recovery:
        if auto_recover_database():
            pass  # Recovery successful
        else:
            # If recovery failed and no database exists, create a fresh one
            if not os.path.exists('awan_hardware.db'):
                from backend.database import Database
                db = Database()
    
    return True

def main():
    """Main application entry point"""
    try:
        # Initialize with auto-recovery
        if not initialize_application():
            raise Exception("Application initialization failed")
        
        # Create and start the main application
        root = tk.Tk()
        root.title("AWAN HARDWARE POS System")
        
        # Set window icon if available
        try:
            icon_path = 'awan_icon.ico'
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        except:
            pass
        
        # Start with login window
        app = LoginWindow(root)
        
        # Center the window
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'+{x}+{y}')
        
        root.mainloop()
        
    except Exception as e:
        # Simple error dialog
        error_root = tk.Tk()
        error_root.title("Application Error")
        error_root.geometry("500x300")
        
        tk.Label(error_root, text="❌ AWAN HARDWARE POS - Startup Error", 
                font=('Arial', 14, 'bold'), fg='red', pady=20).pack()
        
        tk.Label(error_root, text="The application encountered an error during startup.", 
                font=('Arial', 10), pady=10).pack()
                
        tk.Label(error_root, text=f"Error: {str(e)}", 
                font=('Arial', 9), wraplength=450, pady=10).pack()
        
        tk.Label(error_root, text="Please contact support if this continues.", 
                font=('Arial', 10), pady=10).pack()
        
        tk.Button(error_root, text="Exit", command=error_root.destroy,
                 bg='red', fg='white', font=('Arial', 12), pady=10, padx=20).pack(pady=20)
        
        error_root.mainloop()

if __name__ == '__main__':
    main()
# import tkinter as tk
# from frontend.login_window import LoginWindow
# from backend.settings_service import SettingsService

# def main():
#     # Initialize settings service
#     settings_service = SettingsService()
    
#     # Initialize default settings if needed
#     settings_service.initialize_default_settings()
    
#     # Start application with single root window
#     root = tk.Tk()
#     app = LoginWindow(root)
#     root.mainloop()

# if __name__ == '__main__':
#     main()