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
        self.current_filter = None  # No filter initially
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title and Controls
        title_frame = tk.Frame(main_frame, bg='white')
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            title_frame,
            text="📊 STOCK REPORT",
            font=('Arial', 20, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(side=tk.LEFT)
        
        # Control buttons
        control_frame = tk.Frame(title_frame, bg='white')
        control_frame.pack(side=tk.RIGHT)
        
        # Refresh button
        refresh_btn = tk.Button(
            control_frame,
            text="🔄 Refresh",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.refresh_data
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Export PDF button
        export_btn = tk.Button(
            control_frame,
            text="📤 Export PDF",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.export_pdf_report
        )
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # 🔍 QUICK FILTERS FRAME
        quick_filters_frame = tk.Frame(main_frame, bg='#f8f9fa', relief='solid', bd=1)
        quick_filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            quick_filters_frame,
            text="Select Category:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(side=tk.LEFT, padx=10, pady=8)
        
        # Category filters - DIRECT CATEGORY BUTTONS
        categories = ["All", "Paint", "Sanitary", "Roof Sheet", "Hardware", "Limination Sheet"]
        self.category_buttons = {}
        
        for category in categories:
            btn = tk.Button(
                quick_filters_frame,
                text=category,
                font=('Arial', 10, 'bold'),
                bg='#3498db',
                fg='white',
                relief='flat',
                command=lambda c=category: self.filter_by_category(c)
            )
            btn.pack(side=tk.LEFT, padx=3, pady=3)
            self.category_buttons[category] = btn
        
        # Current filter display
        self.filter_label = tk.Label(
            quick_filters_frame,
            text="Please select a category",
            font=('Arial', 10, 'bold'),
            fg='#e67e22',
            bg='#f8f9fa'
        )
        self.filter_label.pack(side=tk.RIGHT, padx=10)
        
        # Summary Cards Frame
        self.summary_frame = tk.Frame(main_frame, bg='#f8f9fa')
        self.summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.setup_summary_cards()
        
        # Products Display Frame
        self.products_display_frame = tk.Frame(main_frame, bg='white')
        self.products_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initial message - NO PRODUCTS SHOWN INITIALLY
        self.initial_message_label = tk.Label(
            self.products_display_frame,
            text="👆 Please select a category to view stock report",
            font=('Arial', 16, 'bold'),
            fg='#7f8c8d',
            bg='white'
        )
        self.initial_message_label.pack(expand=True, pady=50)
        
        # Products count label (hidden initially)
        self.products_count_label = tk.Label(
            self.products_display_frame,
            text="",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        
        # Treeview for products (hidden initially)
        self.tree_frame = tk.Frame(self.products_display_frame, bg='white')
        
        # Create treeview with simple columns
        columns = ('Product', 'Category', 'Stock', 'Price', 'Value', 'Status')
        self.products_tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings', height=20)
        
        # Define headings
        self.products_tree.heading('Product', text='Product Name')
        self.products_tree.heading('Category', text='Category') 
        self.products_tree.heading('Stock', text='Stock Qty')
        self.products_tree.heading('Price', text='Unit Price')
        self.products_tree.heading('Value', text='Stock Value')
        self.products_tree.heading('Status', text='Stock Status')
        
        # Define columns with reasonable widths
        self.products_tree.column('Product', width=250, anchor='w')
        self.products_tree.column('Category', width=120, anchor='center')
        self.products_tree.column('Stock', width=80, anchor='center')
        self.products_tree.column('Price', width=100, anchor='e')
        self.products_tree.column('Value', width=120, anchor='e')
        self.products_tree.column('Status', width=100, anchor='center')
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Load initial summary data only (no products)
        self.parent.after(100, self.load_initial_summary)
    
    def setup_summary_cards(self):
        """Setup summary cards with overall statistics"""
        # Clear existing cards
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        
        self.summary_cards = {}
        summary_items = [
            ("Total Products", "0", "#3498db"),
            ("Total Categories", "0", "#e67e22"),
            ("Inventory Value", "₨0", "#27ae60"),
            ("Low Stock Items", "0", "#e74c3c"),
            ("Out of Stock", "0", "#95a5a6")
        ]
        
        for i, (title, value, color) in enumerate(summary_items):
            card = tk.Frame(self.summary_frame, bg='white', relief='solid', bd=1, width=180, height=100)
            card.pack(side=tk.LEFT, padx=5, pady=5)
            card.pack_propagate(False)
            
            # Title
            tk.Label(
                card,
                text=title,
                font=('Arial', 10, 'bold'),
                fg=color,
                bg='white'
            ).pack(pady=(15, 5))
            
            # Value
            value_label = tk.Label(
                card,
                text=value,
                font=('Arial', 16, 'bold'),
                fg=color,
                bg='white'
            )
            value_label.pack(pady=5)
            
            self.summary_cards[title] = value_label
        
        # Low stock warning
        warning_frame = tk.Frame(self.summary_frame, bg='#fff3cd', relief='solid', bd=1, width=200, height=100)
        warning_frame.pack(side=tk.LEFT, padx=5, pady=5)
        warning_frame.pack_propagate(False)
        
        tk.Label(
            warning_frame,
            text="⚠️ Low Stock Alert",
            font=('Arial', 10, 'bold'),
            fg='#856404',
            bg='#fff3cd'
        ).pack(pady=10)
        
        tk.Label(
            warning_frame,
            text="Stock < 5 items",
            font=('Arial', 9),
            fg='#856404',
            bg='#fff3cd'
        ).pack()
    
    def show_products_display(self):
        """Show the products table and hide the initial message"""
        self.initial_message_label.pack_forget()
        self.products_count_label.pack(anchor='w', pady=(0, 10))
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def show_initial_message(self):
        """Show the initial message and hide products table"""
        # Clear tree
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Hide products display
        self.products_count_label.pack_forget()
        self.tree_frame.pack_forget()
        
        # Show initial message
        self.initial_message_label.pack(expand=True, pady=50)
    
    def filter_by_category(self, category):
        """Filter products by category - DIRECT CATEGORY FILTERING"""
        self.current_filter = category
        self.filter_label.config(text=f"Showing: {category} Products")
        self.update_button_colors()
        self.load_stock_data()
    
    def update_button_colors(self):
        """Update button colors to show active filter"""
        for category, btn in self.category_buttons.items():
            if category == self.current_filter:
                btn.config(bg='#e67e22')  # Orange for active
            else:
                btn.config(bg='#3498db')  # Blue for inactive
    
    def load_initial_summary(self):
        """Load only summary data initially"""
        try:
            summary = self.stock_service.get_stock_summary()
            self.update_summary_cards(summary)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load summary data: {str(e)}")
    
    def refresh_data(self):
        """Refresh data based on current filter"""
        if self.current_filter:
            self.load_stock_data()
        else:
            self.load_initial_summary()
            messagebox.showinfo("Info", "Please select a category to refresh data")
    
    def load_stock_data(self):
        """Load stock data based on current filter"""
        try:
            # Show products display
            self.show_products_display()
            
            # Load products based on filter
            if self.current_filter == "All":
                products_data = self.stock_service.get_all_products()
            else:
                products_data = self.stock_service.get_products_by_category(self.current_filter)
            
            self.update_products_tree(products_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load stock data: {str(e)}")
    
    def update_summary_cards(self, summary):
        """Update summary cards with data"""
        self.summary_cards["Total Products"].config(text=str(summary['total_products']))
        self.summary_cards["Total Categories"].config(text=str(summary['total_categories']))
        self.summary_cards["Inventory Value"].config(text=f"₨{summary['total_value']:,.0f}")
        self.summary_cards["Low Stock Items"].config(text=str(summary['low_stock_count']))
        self.summary_cards["Out of Stock"].config(text=str(summary['out_of_stock_count']))
    
    def update_products_tree(self, products_data):
        """Update products treeview with individual products"""
        # Clear existing data
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Update products count label
        self.products_count_label.config(text=f"Products: {len(products_data)}")
        
        # Add product data
        for product in products_data:
            try:
                if len(product) >= 14:
                    (product_id, category_id, company, ptype, color,
                     sale_price, purchase_price, packing, volume, current_stock,
                     image_path, created_at, updated_at, category_name) = product[:14]
                    
                    # Create product display text
                    product_text = f"{company} - {ptype}"
                    if color and color.strip() and color != 'N/A':
                        product_text += f" ({color})"
                    if packing and packing.strip():
                        product_text += f" - {packing}"
                    
                    # Calculate stock value
                    stock_value = current_stock * purchase_price
                    
                    # Determine status with emojis
                    if current_stock == 0:
                        status = "❌ Out of Stock"
                    elif current_stock <= 2:
                        status = "🔴 Critical"
                    elif current_stock < 5:
                        status = "🟡 Low Stock"
                    else:
                        status = "✅ In Stock"
                    
                    # Insert into treeview
                    self.products_tree.insert('', 'end', values=(
                        product_text,
                        category_name,
                        current_stock,
                        f"₨{purchase_price:,.0f}",
                        f"₨{stock_value:,.0f}",
                        status
                    ))
                    
            except Exception:
                continue
    
    def export_pdf_report(self):
        """Export complete stock report to PDF"""
        try:
            filename = filedialog.asksaveasfilename(
                title="Export Stock Report as PDF",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            
            if filename:
                # Create PDF document
                doc = SimpleDocTemplate(filename, pagesize=A4)
                elements = []
                
                # Get styles
                styles = getSampleStyleSheet()
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=16,
                    spaceAfter=30,
                    alignment=1,
                    textColor=colors.HexColor('#2c3e50')
                )
                
                heading_style = ParagraphStyle(
                    'CustomHeading',
                    parent=styles['Heading2'],
                    fontSize=12,
                    spaceAfter=12,
                    textColor=colors.HexColor('#34495e')
                )
                
                # Title
                elements.append(Paragraph("AWAN HARDWARE - STOCK REPORT", title_style))
                elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}", styles['Normal']))
                elements.append(Spacer(1, 20))
                
                # Summary Section
                elements.append(Paragraph("SUMMARY", heading_style))
                summary = self.stock_service.get_stock_summary()
                summary_data = [
                    ['Total Products', str(summary['total_products'])],
                    ['Total Categories', str(summary['total_categories'])],
                    ['Total Inventory Value', f"₨{summary['total_value']:,.0f}"],
                    ['Low Stock Items (<5)', str(summary['low_stock_count'])],
                    ['Out of Stock Items', str(summary['out_of_stock_count'])]
                ]
                
                summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
                summary_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(summary_table)
                elements.append(Spacer(1, 20))
                
                # Category Overview Section
                elements.append(Paragraph("CATEGORY OVERVIEW", heading_style))
                category_data = self.stock_service.get_category_stock_overview()
                cat_table_data = [['Category', 'Products', 'Total Stock', 'Stock Value']]
                
                for category in category_data:
                    category_name, product_count, total_stock, total_value = category
                    cat_table_data.append([
                        category_name,
                        str(product_count),
                        str(total_stock or 0),
                        f"₨{total_value or 0:,.0f}"
                    ])
                
                cat_table = Table(cat_table_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1.2*inch])
                cat_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8)
                ]))
                elements.append(cat_table)
                elements.append(Spacer(1, 20))
                
                # Current Category Products Section (if a category is selected)
                if self.current_filter and self.current_filter != "All":
                    elements.append(Paragraph(f"{self.current_filter.upper()} PRODUCTS", heading_style))
                    
                    # Get products for current category
                    if self.current_filter == "All":
                        products_data = self.stock_service.get_all_products()
                    else:
                        products_data = self.stock_service.get_products_by_category(self.current_filter)
                    
                    if products_data:
                        products_table_data = [['Product', 'Stock', 'Price', 'Value', 'Status']]
                        
                        for product in products_data:
                            if len(product) >= 14:
                                (product_id, category_id, company, ptype, color,
                                 sale_price, purchase_price, packing, volume, current_stock,
                                 image_path, created_at, updated_at, category_name) = product[:14]
                                
                                product_text = f"{company} - {ptype}"
                                if color and color != 'N/A':
                                    product_text += f" ({color})"
                                
                                # Determine status
                                if current_stock == 0:
                                    status = "Out of Stock"
                                elif current_stock <= 2:
                                    status = "Critical"
                                elif current_stock < 5:
                                    status = "Low Stock"
                                else:
                                    status = "In Stock"
                                
                                stock_value = current_stock * purchase_price
                                
                                products_table_data.append([
                                    product_text,
                                    str(current_stock),
                                    f"₨{purchase_price:,.0f}",
                                    f"₨{stock_value:,.0f}",
                                    status
                                ])
                        
                        products_table = Table(products_table_data, colWidths=[2.5*inch, 0.6*inch, 0.8*inch, 1*inch, 0.8*inch])
                        products_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 9),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('FONTSIZE', (0, 1), (-1, -1), 7)
                        ]))
                        elements.append(products_table)
                
                # Low Stock Products Section
                elements.append(Paragraph("LOW STOCK PRODUCTS (Less than 5 items)", heading_style))
                low_stock_data = self.stock_service.get_low_stock_products()
                
                if low_stock_data:
                    low_stock_table_data = [['Product', 'Category', 'Stock', 'Status', 'Price']]
                    
                    for product in low_stock_data:
                        if len(product) >= 14:
                            (product_id, category_id, company, ptype, color,
                             sale_price, purchase_price, packing, volume, current_stock,
                             image_path, created_at, updated_at, category_name) = product[:14]
                            
                            product_text = f"{company} - {ptype}"
                            if color and color != 'N/A':
                                product_text += f" ({color})"
                            
                            status = "Out of Stock" if current_stock == 0 else "Critical" if current_stock <= 2 else "Low"
                            
                            low_stock_table_data.append([
                                product_text,
                                category_name,
                                str(current_stock),
                                status,
                                f"₨{purchase_price:,.0f}"
                            ])
                    
                    low_stock_table = Table(low_stock_table_data, colWidths=[2*inch, 1*inch, 0.6*inch, 0.8*inch, 0.8*inch])
                    low_stock_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 9),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 1), (-1, -1), 7)
                    ]))
                    elements.append(low_stock_table)
                else:
                    elements.append(Paragraph("No low stock products found.", styles['Normal']))
                
                # Build PDF
                doc.build(elements)
                messagebox.showinfo("Success", f"Stock report exported successfully!\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")