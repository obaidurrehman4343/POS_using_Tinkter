import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
from datetime import datetime

class DataRecoveryWindow:
    def __init__(self, parent, db_path):
        self.parent = parent
        self.db_path = db_path
        self.backup_path = self.get_backup_path()
        
        self.setup_ui()
        self.load_backup_info()
    
    def get_backup_path(self):
        base_path = os.path.dirname(self.db_path)
        return os.path.join(base_path, 'awan_hardware_backup.db')
    
    def setup_ui(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Data Recovery - Awan Hardware POS")
        self.window.geometry("600x500")
        self.window.configure(bg='white')
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"600x500+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(self.window, bg='#e74c3c', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🛡️ DATA RECOVERY CENTER",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#e74c3c'
        ).pack(expand=True)
        
        # Main content
        content_frame = tk.Frame(self.window, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Current Database Info
        current_frame = tk.LabelFrame(content_frame, text="Current Database Status", 
                                    font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50')
        current_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.current_info = tk.Text(current_frame, height=4, width=60, font=('Arial', 10))
        self.current_info.pack(fill=tk.X, padx=10, pady=10)
        self.current_info.config(state='disabled')
        
        # Backup Database Info
        backup_frame = tk.LabelFrame(content_frame, text="Backup Database", 
                                   font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50')
        backup_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.backup_info = tk.Text(backup_frame, height=4, width=60, font=('Arial', 10))
        self.backup_info.pack(fill=tk.X, padx=10, pady=10)
        self.backup_info.config(state='disabled')
        
        # Recovery Actions
        actions_frame = tk.LabelFrame(content_frame, text="Recovery Actions", 
                                    font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50')
        actions_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Buttons
        btn_frame = tk.Frame(actions_frame, bg='white')
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create Backup Button
        backup_btn = tk.Button(
            btn_frame,
            text="💾 Create Backup Now",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            command=self.create_backup,
            padx=20,
            pady=10
        )
        backup_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Restore Backup Button
        restore_btn = tk.Button(
            btn_frame,
            text="🔄 Restore from Backup",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.restore_backup,
            padx=20,
            pady=10
        )
        restore_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Import Backup Button
        import_btn = tk.Button(
            btn_frame,
            text="📁 Import Backup File",
            font=('Arial', 11, 'bold'),
            bg='#e67e22',
            fg='white',
            command=self.import_backup,
            padx=20,
            pady=10
        )
        import_btn.pack(side=tk.LEFT)
    
    def load_backup_info(self):
        """Load information about current and backup databases"""
        # Current DB info
        current_text = ""
        if os.path.exists(self.db_path):
            stats = os.stat(self.db_path)
            current_text = f"✅ Database: {os.path.basename(self.db_path)}\n"
            current_text += f"📁 Size: {stats.st_size:,} bytes\n"
            current_text += f"📅 Modified: {datetime.fromtimestamp(stats.st_mtime)}\n"
            current_text += f"📍 Path: {self.db_path}"
        else:
            current_text = "❌ Database file not found!\nPlease restore from backup."
        
        self.current_info.config(state='normal')
        self.current_info.delete(1.0, tk.END)
        self.current_info.insert(1.0, current_text)
        self.current_info.config(state='disabled')
        
        # Backup DB info
        backup_text = ""
        if os.path.exists(self.backup_path):
            stats = os.stat(self.backup_path)
            backup_text = f"✅ Backup: {os.path.basename(self.backup_path)}\n"
            backup_text += f"📁 Size: {stats.st_size:,} bytes\n"
            backup_text += f"📅 Modified: {datetime.fromtimestamp(stats.st_mtime)}\n"
            backup_text += f"📍 Path: {self.backup_path}"
        else:
            backup_text = "❌ No backup file found!\nPlease create a backup or import one."
        
        self.backup_info.config(state='normal')
        self.backup_info.delete(1.0, tk.END)
        self.backup_info.insert(1.0, backup_text)
        self.backup_info.config(state='disabled')
    
    def create_backup(self):
        """Create a manual backup"""
        try:
            shutil.copy2(self.db_path, self.backup_path)
            messagebox.showinfo("Success", "Backup created successfully!")
            self.load_backup_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup:\n{str(e)}")
    
    def restore_backup(self):
        """Restore from backup"""
        if not os.path.exists(self.backup_path):
            messagebox.showerror("Error", "No backup file found to restore!")
            return
        
        result = messagebox.askyesno(
            "Confirm Restore",
            "WARNING: This will replace your current database with the backup.\n\n"
            "Current data will be lost. Continue?"
        )
        
        if result:
            try:
                # Backup current DB first
                if os.path.exists(self.db_path):
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    backup_current = f"{self.db_path}.before_restore_{timestamp}"
                    shutil.copy2(self.db_path, backup_current)
                
                # Restore from backup
                shutil.copy2(self.backup_path, self.db_path)
                messagebox.showinfo("Success", "Database restored successfully from backup!")
                self.load_backup_info()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to restore backup:\n{str(e)}")
    
    def import_backup(self):
        """Import a backup file"""
        file_path = filedialog.askopenfilename(
            title="Select Backup Database File",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                shutil.copy2(file_path, self.backup_path)
                messagebox.showinfo("Success", "Backup file imported successfully!")
                self.load_backup_info()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import backup:\n{str(e)}")