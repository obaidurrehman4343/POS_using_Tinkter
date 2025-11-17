import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.stock_service import StockService
import csv
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class StockReport:
    def __init__(self, parent):
        self.parent = parent
        self.stock_service = StockService()
        self.current_filter = "All"
        
        # Modern professional color palette
        self.colors = {
            'primary': '#3b82f6',      # Modern blue
            'secondary': '#6366f1',    # Indigo
            'success': '#10b981',      # Emerald
            'warning': '#f59e0b',      # Amber
            'danger': '#ef4444',       # Red
            'info': '#06b6d4',         # Cyan
            'dark': '#1f2937',         # Gray-800
            'light': '#f8fafc',       # Gray-50
            'white': '#ffffff',        # White
            'gray': '#6b7280',         # Gray-500
            'light_gray': '#e5e7eb',   # Gray-200
            'background': '#f9fafb',   # Gray-50
            'card_bg': '#ffffff'       # White
        }
        
        self.setup_ui()
        self.load_initial_data()
        
    def setup_ui(self):
        # Main container with clean background
        self.main_container = tk.Frame(self.parent, bg=self.colors['background'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create modern header
        self.create_header()
        
        # Create stats cards row
        self.create_stats_cards()
        
        # Create filter bar
        self.create_filter_bar()
        
        # Create data display area
        self.create_data_display()
    
    def create_header(self):
        """Create beautiful header section"""
        header_frame = tk.Frame(self.main_container, bg='white', relief='flat', bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_content = tk.Frame(header_frame, bg='white')
        header_content.pack(fill=tk.X, padx=25, pady=20)
        
        # Left side - Title and description
        title_frame = tk.Frame(header_content, bg='white')
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            title_frame,
            text="📦 AWAN HARDWARE STOCK DASHBOARD",
            font=('Arial', 22, 'bold'),
            fg=self.colors['dark'],
            bg='white'
        ).pack(anchor='w')
        
        tk.Label(
            title_frame,
            text="Real-time inventory analytics and stock monitoring",
            font=('Arial', 12),
            fg=self.colors['gray'],
            bg='white'
        ).pack(anchor='w', pady=(5, 0))
        
        # Right side - Action buttons
        action_frame = tk.Frame(header_content, bg='white')
        action_frame.pack(side=tk.RIGHT)
        
        # Export PDF button
        export_btn = tk.Button(
            action_frame,
            text="📄 Export Low Stock Report",
            font=('Arial', 11, 'bold'),
            bg=self.colors['success'],
            fg='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            padx=20,
            pady=10,
            command=self.export_low_stock_pdf
        )
        export_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Refresh button
        refresh_btn = tk.Button(
            action_frame,
            text="🔄 Refresh Data",
            font=('Arial', 11),
            bg=self.colors['primary'],
            fg='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            padx=20,
            pady=10,
            command=self.refresh_data
        )
        refresh_btn.pack(side=tk.LEFT)
    
    def create_stats_cards(self):
        """Create beautiful stats cards row - WITHOUT INVENTORY VALUE"""
        stats_container = tk.Frame(self.main_container, bg=self.colors['background'])
        stats_container.pack(fill=tk.X, pady=(0, 20))
        
        # Configure grid for 3 columns
        for i in range(3):
            stats_container.grid_columnconfigure(i, weight=1)
        
        # Stats data - Focused on stock-specific metrics (no inventory value)
        self.stats_labels = {}
        stats_data = [
            ("Total Products", "0", self.colors['primary'], "📊", "All products in inventory"),
            ("Active Categories", "0", self.colors['info'], "🏷️", "Product categories"), 
            ("Low Stock Items", "0", self.colors['warning'], "⚠️", "Items below threshold")
        ]
        
        for i, (title, value, color, icon, description) in enumerate(stats_data):
            card = self.create_beautiful_stat_card(stats_container, title, value, color, icon, description)
            card.grid(row=0, column=i, padx=(0 if i == 0 else 10, 0), sticky='ew')
            self.stats_labels[title] = card
    
    def create_beautiful_stat_card(self, parent, title, value, color, icon, description):
        """Create beautiful stat card with modern design"""
        # Main card with shadow effect
        card = tk.Frame(parent, bg=self.colors['light_gray'], relief='flat', bd=0)
        
        # Card content
        content = tk.Frame(card, bg='white', relief='solid', bd=1)
        content.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        inner_content = tk.Frame(content, bg='white')
        inner_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Icon and title row
        header_frame = tk.Frame(inner_content, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Icon with colored background
        icon_frame = tk.Frame(header_frame, bg=color, width=44, height=44)
        icon_frame.pack(side=tk.LEFT, padx=(0, 12))
        icon_frame.pack_propagate(False)
        
        tk.Label(
            icon_frame,
            text=icon,
            font=('Arial', 18),
            bg=color,
            fg='white'
        ).pack(expand=True)
        
        # Title and description
        text_frame = tk.Frame(header_frame, bg='white')
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            text_frame,
            text=title,
            font=('Arial', 12, 'bold'),
            fg=self.colors['dark'],
            bg='white'
        ).pack(anchor='w')
        
        tk.Label(
            text_frame,
            text=description,
            font=('Arial', 9),
            fg=self.colors['gray'],
            bg='white'
        ).pack(anchor='w', pady=(2, 0))
        
        # Value
        value_label = tk.Label(
            inner_content,
            text=value,
            font=('Arial', 22, 'bold'),
            fg=color,
            bg='white'
        )
        value_label.pack(anchor='w')
        
        # Store reference
        card.value_label = value_label
        
        return card
    
    def create_filter_bar(self):
        """Create beautiful filter bar with category buttons"""
        filter_container = tk.Frame(self.main_container, bg='white', relief='solid', bd=1)
        filter_container.pack(fill=tk.X, pady=(0, 20))
        
        filter_content = tk.Frame(filter_container, bg='white')
        filter_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Filter label
        tk.Label(
            filter_content,
            text="Filter by Category:",
            font=('Arial', 11, 'bold'),
            fg=self.colors['dark'],
            bg='white'
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        # Category filter buttons
        self.filter_buttons = {}
        categories = [
            ("All", "📦"),
            ("Paint", "🎨"),
            ("Sanitary", "🚿"),
            ("Hardware", "🔧"),
            ("Roof Sheet", "🏗️"),
            ("Limination Sheet", "📄")
        ]
        
        for display_name, icon in categories:
            btn = tk.Button(
                filter_content,
                text=f" {icon} {display_name} ",
                font=('Arial', 10),
                bg=self.colors['light_gray'],
                fg=self.colors['dark'],
                relief='flat',
                bd=0,
                cursor='hand2',
                padx=12,
                pady=6,
                command=lambda cat=display_name: self.filter_by_category(cat)
            )
            btn.pack(side=tk.LEFT, padx=(0, 8))
            self.filter_buttons[display_name] = btn
        
        # Set initial active filter
        self.update_filter_buttons("All")
    
    def create_data_display(self):
        """Create beautiful data display area"""
        # Main display container
        display_container = tk.Frame(self.main_container, bg='white', relief='solid', bd=1)
        display_container.pack(fill=tk.BOTH, expand=True)
        
        # Display header
        display_header = tk.Frame(display_container, bg=self.colors['light_gray'])
        display_header.pack(fill=tk.X, padx=0, pady=0)
        
        self.data_title = tk.Label(
            display_header,
            text="📦 All Products Inventory",
            font=('Arial', 14, 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['light_gray'],
            padx=20,
            pady=15
        )
        self.data_title.pack(side=tk.LEFT)
        
        self.product_count_label = tk.Label(
            display_header,
            text="",
            font=('Arial', 11),
            fg=self.colors['gray'],
            bg=self.colors['light_gray'],
            padx=20,
            pady=15
        )
        self.product_count_label.pack(side=tk.RIGHT)
        
        # Table container
        table_container = tk.Frame(display_container, bg='white')
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create modern treeview
        columns = ('Product', 'Category', 'Stock', 'Unit Price', 'Stock Value', 'Status')
        self.products_tree = ttk.Treeview(table_container, columns=columns, show='headings', height=18)
        
        # Configure columns
        self.products_tree.heading('Product', text='PRODUCT NAME')
        self.products_tree.heading('Category', text='CATEGORY')
        self.products_tree.heading('Stock', text='STOCK')
        self.products_tree.heading('Unit Price', text='UNIT PRICE')
        self.products_tree.heading('Stock Value', text='STOCK VALUE')
        self.products_tree.heading('Status', text='STATUS')
        
        self.products_tree.column('Product', width=300, anchor='w')
        self.products_tree.column('Category', width=120, anchor='center')
        self.products_tree.column('Stock', width=80, anchor='center')
        self.products_tree.column('Unit Price', width=120, anchor='e')
        self.products_tree.column('Stock Value', width=140, anchor='e')
        self.products_tree.column('Status', width=100, anchor='center')
        
        # Style treeview for modern look
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Treeview",
            background='white',
            foreground=self.colors['dark'],
            fieldbackground='white',
            borderwidth=0,
            font=('Arial', 10),
            rowheight=28
        )
        
        style.configure(
            "Treeview.Heading",
            background=self.colors['primary'],
            foreground='white',
            relief='flat',
            font=('Arial', 10, 'bold'),
            padding=(10, 8)
        )
        
        style.map(
            "Treeview",
            background=[('selected', self.colors['info'])],
            foreground=[('selected', 'white')]
        )
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load initial data
        self.load_products_data()
    
    def filter_by_category(self, category):
        """Filter products by category"""
        self.current_filter = category
        self.update_filter_buttons(category)
        
        # Update title
        if category == "All":
            self.data_title.config(text="📦 All Products Inventory")
        else:
            self.data_title.config(text=f"📦 {category} Inventory")
        
        # Load data
        self.load_products_data()
    
    def update_filter_buttons(self, active_category):
        """Update filter button states"""
        for category_name, btn in self.filter_buttons.items():
            if category_name == active_category:
                btn.config(bg=self.colors['primary'], fg='white')
            else:
                btn.config(bg=self.colors['light_gray'], fg=self.colors['dark'])
    
    def load_initial_data(self):
        """Load initial statistics"""
        try:
            summary = self.stock_service.get_stock_summary()
            self.update_stats(summary)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def refresh_data(self):
        """Refresh all data"""
        try:
            summary = self.stock_service.get_stock_summary()
            self.update_stats(summary)
            self.load_products_data()
            messagebox.showinfo("Success", "Data refreshed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh data: {str(e)}")
    
    def load_products_data(self):
        """Load products data based on current filter"""
        try:
            # Get products
            if self.current_filter == "All":
                products = self.stock_service.get_all_products()
            else:
                products = self.stock_service.get_products_by_category(self.current_filter)
            
            # Update count
            self.product_count_label.config(text=f"{len(products)} products")
            
            # Clear existing data
            for item in self.products_tree.get_children():
                self.products_tree.delete(item)
            
            # Add products
            for product in products:
                try:
                    if len(product) >= 14:
                        (product_id, category_id, company, ptype, color,
                         sale_price, purchase_price, packing, volume, current_stock,
                         image_path, created_at, updated_at, category_name) = product[:14]
                        
                        # Product name
                        product_name = f"{company} - {ptype}"
                        if color and color.strip() and color != 'N/A':
                            product_name += f" ({color})"
                        
                        # Stock value
                        stock_value = current_stock * purchase_price
                        
                        # Status with better formatting
                        if current_stock == 0:
                            status = "❌ Out of Stock"
                        elif current_stock <= 2:
                            status = "🔴 Critical"
                        elif current_stock < 5:
                            status = "🟡 Low Stock"
                        else:
                            status = "✅ In Stock"
                        
                        # Insert into tree
                        self.products_tree.insert('', 'end', values=(
                            product_name,
                            category_name,
                            current_stock,
                            f"₨{purchase_price:,.0f}",
                            f"₨{stock_value:,.0f}",
                            status
                        ))
                        
                except Exception:
                    continue
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {str(e)}")
    
    def update_stats(self, summary):
        """Update statistics cards - WITHOUT INVENTORY VALUE"""
        self.stats_labels["Total Products"].value_label.config(text=str(summary['total_products']))
        self.stats_labels["Active Categories"].value_label.config(text=str(summary['total_categories']))
        self.stats_labels["Low Stock Items"].value_label.config(text=str(summary['low_stock_count']))
    
    def export_low_stock_pdf(self):
        """Export PDF with only categories that have low stock"""
        try:
            # Get all low stock products
            low_stock_products = self.stock_service.get_low_stock_products()
            
            if not low_stock_products:
                messagebox.showinfo("Info", "No low stock products found to export!")
                return
            
            # Group low stock products by category
            categories_with_low_stock = {}
            for product in low_stock_products:
                if len(product) >= 14:
                    category_name = product[13]
                    if category_name not in categories_with_low_stock:
                        categories_with_low_stock[category_name] = []
                    categories_with_low_stock[category_name].append(product)
            
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                title="Export Low Stock Report",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            
            if filename:
                # Create PDF
                doc = SimpleDocTemplate(filename, pagesize=A4)
                elements = []
                
                # Get styles
                styles = getSampleStyleSheet()
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=18,
                    spaceAfter=30,
                    alignment=1,
                    textColor=colors.HexColor('#1e40af')
                )
                
                heading_style = ParagraphStyle(
                    'CustomHeading',
                    parent=styles['Heading2'],
                    fontSize=14,
                    spaceAfter=16,
                    textColor=colors.HexColor('#111827')
                )
                
                # Title
                elements.append(Paragraph("LOW STOCK INVENTORY REPORT", title_style))
                elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}", styles['Normal']))
                elements.append(Paragraph(f"Categories with Low Stock: {len(categories_with_low_stock)}", styles['Normal']))
                elements.append(Spacer(1, 20))
                
                # Summary table
                elements.append(Paragraph("SUMMARY BY CATEGORY", heading_style))
                summary_data = [['Category', 'Low Stock Items', 'Total Value']]
                total_low_stock_items = 0
                total_low_stock_value = 0
                
                for category_name, products in categories_with_low_stock.items():
                    item_count = len(products)
                    total_value = sum(p[9] * p[5] for p in products if len(p) > 9)  # stock * purchase_price
                    
                    summary_data.append([
                        category_name,
                        str(item_count),
                        f"₨{total_value:,.0f}"
                    ])
                    
                    total_low_stock_items += item_count
                    total_low_stock_value += total_value
                
                # Add total row
                summary_data.append([
                    'TOTAL',
                    str(total_low_stock_items),
                    f"₨{total_low_stock_value:,.0f}"
                ])
                
                summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
                summary_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-2, -1), colors.HexColor('#fef2f2')),
                    ('BACKGROUND', (-1, 0), (-1, -1), colors.HexColor('#fee2e2')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fecaca')),
                    ('FONTSIZE', (0, 1), (-1, -1), 10)
                ]))
                elements.append(summary_table)
                elements.append(Spacer(1, 20))
                
                # Detailed breakdown for each category
                for category_name, products in categories_with_low_stock.items():
                    elements.append(Paragraph(f"{category_name.upper()} - DETAILED BREAKDOWN", heading_style))
                    
                    category_data = [['Product', 'Current Stock', 'Unit Price', 'Stock Value', 'Status']]
                    
                    for product in products:
                        if len(product) >= 14:
                            (product_id, category_id, company, ptype, color,
                             sale_price, purchase_price, packing, volume, current_stock,
                             image_path, created_at, updated_at, cat_name) = product[:14]
                            
                            product_name = f"{company} - {ptype}"
                            if color and color != 'N/A':
                                product_name += f" ({color})"
                            
                            stock_value = current_stock * purchase_price
                            
                            if current_stock == 0:
                                status = "Out of Stock"
                            elif current_stock <= 2:
                                status = "Critical"
                            else:
                                status = "Low Stock"
                            
                            category_data.append([
                                product_name,
                                str(current_stock),
                                f"₨{purchase_price:,.0f}",
                                f"₨{stock_value:,.0f}",
                                status
                            ])
                    
                    category_table = Table(category_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1.2*inch, 1*inch])
                    category_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0ea5e9')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
                        ('FONTSIZE', (0, 1), (-1, -1), 9)
                    ]))
                    elements.append(category_table)
                    elements.append(Spacer(1, 15))
                
                # Build PDF
                doc.build(elements)
                messagebox.showinfo("Success", f"Low stock report exported successfully!\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")