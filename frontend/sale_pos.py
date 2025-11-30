import tkinter as tk
from tkinter import ttk, messagebox
from backend.sale_service import SaleService
from backend.product_service import ProductService
from PIL import Image, ImageTk
import os
from datetime import datetime

class SalePOS:
    def __init__(self, parent):
        self.parent = parent
        self.sale_service = SaleService()
        self.product_service = ProductService()
        self.cart = []
        self.current_customer = None
        self.setup_ui()
        self.load_customers()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.parent, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_frame = tk.Frame(main_frame, bg='#2c3e50')
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            title_frame,
            text="💰 POINT OF SALE",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        ).pack(pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#f8f9fa')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        left_frame = tk.Frame(content_frame, bg='#f8f9fa')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # INCREASED WIDTH for better display of all columns
        right_frame = tk.Frame(content_frame, bg='white', relief='solid', bd=1, width=600)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        right_frame.pack_propagate(False)
        
        self.setup_search_section(left_frame)
        self.setup_cart_section(right_frame)
        
    def setup_search_section(self, parent):
        search_header = tk.Frame(parent, bg='#34495e')
        search_header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            search_header,
            text="🔍 PRODUCT SEARCH",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#34495e'
        ).pack(pady=10)
        
        search_frame = tk.Frame(parent, bg='#f8f9fa')
        search_frame.pack(fill=tk.X, pady=5)
        
        search_row = tk.Frame(search_frame, bg='#f8f9fa')
        search_row.pack(fill=tk.X, pady=2)
        
        tk.Label(
            search_row,
            text="Search:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_row,
            textvariable=self.search_var,
            font=('Arial', 10),
            relief='solid',
            bd=1,
            width=30
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        self.search_entry.bind('<KeyRelease>', self.handle_search)
        
        filter_frame = tk.Frame(search_frame, bg='#f8f9fa')
        filter_frame.pack(fill=tk.X, pady=5)
        
        filters = ["Paint", "Sanitary", "Roof Sheet", "Hardware", "Limination Sheet"]
        for filter_text in filters:
            btn = tk.Button(
                filter_frame,
                text=filter_text,
                font=('Arial', 8),
                bg='#3498db',
                fg='white',
                relief='flat',
                command=lambda f=filter_text: self.quick_filter(f)
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        clear_search_btn = tk.Button(
            filter_frame,
            text="Clear",
            font=('Arial', 8),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            command=self.clear_search
        )
        clear_search_btn.pack(side=tk.RIGHT, padx=2)
        
        self.results_frame = tk.Frame(parent, bg='#f8f9fa')
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.show_empty_state()
        
        self.setup_customer_section(parent)
        
    def show_empty_state(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        empty_frame = tk.Frame(self.results_frame, bg='#f8f9fa')
        empty_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            empty_frame,
            text="🔍 Search for products",
            font=('Arial', 16),
            fg='#7f8c8d',
            bg='#f8f9fa'
        ).pack(expand=True, pady=20)
        
        tk.Label(
            empty_frame,
            text="Type in search box or use category filters",
            font=('Arial', 12),
            fg='#bdc3c7',
            bg='#f8f9fa'
        ).pack(expand=True)
        
    def setup_customer_section(self, parent):
        customer_frame = tk.Frame(parent, bg='#f8f9fa')
        customer_frame.pack(fill=tk.X, pady=5)
        
        customer_row = tk.Frame(customer_frame, bg='#f8f9fa')
        customer_row.pack(fill=tk.X)
        
        tk.Label(
            customer_row,
            text="Customer:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.customer_var = tk.StringVar(value="")
        self.customer_dropdown = ttk.Combobox(
            customer_row,
            textvariable=self.customer_var,
            state='readonly',
            font=('Arial', 10),
            width=20
        )
        self.customer_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.customer_dropdown.bind('<<ComboboxSelected>>', self.on_customer_select)
        
        add_customer_btn = tk.Button(
            customer_row,
            text="+ Add Customer",
            font=('Arial', 9),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.add_customer
        )
        add_customer_btn.pack(side=tk.RIGHT)
        
    def setup_cart_section(self, parent):
        """Setup cart section with proper layout to ensure checkout button is always visible"""
        cart_header = tk.Frame(parent, bg='#27ae60')
        cart_header.pack(fill=tk.X)
        
        tk.Label(
            cart_header,
            text="🛒 SHOPPING CART",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#27ae60'
        ).pack(pady=10)
        
        # Main container for cart content with fixed height
        cart_main_container = tk.Frame(parent, bg='white')
        cart_main_container.pack(fill=tk.BOTH, expand=True)
        
        # Cart summary frame
        self.cart_summary_frame = tk.Frame(cart_main_container, bg='#f8f9fa', relief='solid', bd=1)
        self.cart_summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        summary_frame = tk.Frame(self.cart_summary_frame, bg='#f8f9fa')
        summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.customer_name_label = tk.Label(
            summary_frame,
            text="Customer: ",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        )
        self.customer_name_label.pack(side=tk.LEFT)
        
        self.item_count_label = tk.Label(
            summary_frame,
            text="Items: 0",
            font=('Arial', 10, 'bold'),
            fg='#e67e22',
            bg='#f8f9fa'
        )
        self.item_count_label.pack(side=tk.RIGHT)
        
        # Container for treeview with fixed height (so it doesn't push button down)
        treeview_container = tk.Frame(cart_main_container, bg='white')
        treeview_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview with fixed height
        columns = ('Product', 'Details', 'Qty', 'Price', 'Total')
        self.cart_tree = ttk.Treeview(
            treeview_container, 
            columns=columns, 
            show='headings',
            height=8  # Fixed height to prevent expansion
        )
        
        # Configure columns
        self.cart_tree.heading('Product', text='PRODUCT NAME')
        self.cart_tree.heading('Details', text='DETAILS')
        self.cart_tree.heading('Qty', text='QTY')
        self.cart_tree.heading('Price', text='PRICE')
        self.cart_tree.heading('Total', text='TOTAL')
        
        self.cart_tree.column('Product', width=180, minwidth=150)
        self.cart_tree.column('Details', width=150, minwidth=120)
        self.cart_tree.column('Qty', width=80, minwidth=70)
        self.cart_tree.column('Price', width=80, minwidth=70)
        self.cart_tree.column('Total', width=90, minwidth=80)
        
        cart_scrollbar = ttk.Scrollbar(treeview_container, orient="vertical", command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=cart_scrollbar.set)
        
        self.cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cart_tree.bind('<Double-1>', self.edit_cart_item)
        
        # Cart actions frame
        cart_actions_frame = tk.Frame(cart_main_container, bg='white')
        cart_actions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        edit_btn = tk.Button(
            cart_actions_frame,
            text="✏️ Edit Item",
            font=('Arial', 9),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.edit_cart_item
        )
        edit_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        remove_btn = tk.Button(
            cart_actions_frame,
            text="🗑️ Remove",
            font=('Arial', 9),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            command=self.remove_from_cart
        )
        remove_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = tk.Button(
            cart_actions_frame,
            text="🗑️ Clear All",
            font=('Arial', 9),
            bg='#e67e22',
            fg='white',
            relief='flat',
            command=self.clear_cart
        )
        clear_btn.pack(side=tk.LEFT)
        
        # Totals frame
        totals_frame = tk.Frame(cart_main_container, bg='white')
        totals_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.subtotal_label = tk.Label(
            totals_frame,
            text="Subtotal: 0 PKR",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        self.subtotal_label.pack(anchor='e')
        
        discount_frame = tk.Frame(totals_frame, bg='white')
        discount_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(
            discount_frame,
            text="Discount:",
            font=('Arial', 10),
            fg='#2c3e50',
            bg='white'
        ).pack(side=tk.LEFT)
        
        self.discount_var = tk.StringVar(value="0")
        discount_entry = tk.Entry(
            discount_frame,
            textvariable=self.discount_var,
            font=('Arial', 10),
            width=8,
            relief='solid',
            bd=1
        )
        discount_entry.pack(side=tk.RIGHT)
        discount_entry.bind('<KeyRelease>', self.update_totals)
        
        self.total_label = tk.Label(
            totals_frame,
            text="Total: 0 PKR",
            font=('Arial', 12, 'bold'),
            fg='#27ae60',
            bg='white'
        )
        self.total_label.pack(anchor='e', pady=2)
        
        # FIXED: Checkout button container that stays at bottom
        checkout_container = tk.Frame(parent, bg='white')  # Changed to parent, not cart_main_container
        checkout_container.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)
        
        checkout_btn = tk.Button(
            checkout_container,
            text="💳 PROCESS SALE",
            font=('Arial', 14, 'bold'),  # Increased font size
            bg='#27ae60',
            fg='white',
            relief='raised',
            bd=3,
            command=self.process_sale,
            cursor='hand2',
            height=2,
            width=20
        )
        checkout_btn.pack(fill=tk.X, ipady=10)  # Increased padding
        
        # Add hover effect
        checkout_btn.bind("<Enter>", lambda e: checkout_btn.config(bg='#2ecc71', relief='solid'))
        checkout_btn.bind("<Leave>", lambda e: checkout_btn.config(bg='#27ae60', relief='raised'))
    
    def clear_search(self):
        self.search_var.set("")
        self.show_empty_state()
        
    def quick_filter(self, category):
        self.search_var.set(category)
        self.handle_search()
        
    def handle_search(self, event=None):
        search_term = self.search_var.get().strip().lower()
        
        if not search_term:
            self.show_empty_state()
            return
            
        try:
            all_products = self.product_service.get_all_products()
            filtered_products = []
            
            for product in all_products:
                try:
                    if len(product) >= 14:
                        (product_id, category_id, company, ptype, color,
                         sale_price, purchase_price, packing, volume, current_stock,
                         image_path, created_at, updated_at, category_name) = product[:14]
                        
                        search_text = f"{company} {ptype} {color} {packing} {volume} {category_name}".lower()
                        
                        if search_term in search_text:
                            filtered_products.append(product)
                except:
                    continue
                    
            self.show_search_results(filtered_products)
            
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
        
    def show_search_results(self, products):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        if not products:
            empty_frame = tk.Frame(self.results_frame, bg='#f8f9fa')
            empty_frame.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(
                empty_frame,
                text="No products found",
                font=('Arial', 16),
                fg='#7f8c8d',
                bg='#f8f9fa'
            ).pack(expand=True, pady=20)
            return
            
        canvas = tk.Canvas(self.results_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        row = 0
        col = 0
        max_cols = 4
        
        for product in products:
            product_card = self.create_product_card(scrollable_frame, product)
            if product_card:
                product_card.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
                    
        for i in range(max_cols):
            scrollable_frame.grid_columnconfigure(i, weight=1)
            
    def create_product_card(self, parent, product):
        try:
            if len(product) < 14:
                return None
                
            (product_id, category_id, company, ptype, color,
             sale_price, purchase_price, packing, volume, current_stock,
             image_path, created_at, updated_at, category_name) = product[:14]
            
            card_frame = tk.Frame(
                parent,
                bg='white',
                relief='solid',
                bd=1,
                width=160,
                height=200
            )
            card_frame.pack_propagate(False)
            
            image_frame = tk.Frame(card_frame, bg='#f8f9fa', height=70)
            image_frame.pack(fill=tk.X)
            
            try:
                if image_path and os.path.exists(image_path):
                    img = Image.open(image_path)
                    img.thumbnail((60, 60), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    img_label = tk.Label(image_frame, image=photo, bg='#f8f9fa', cursor='hand2')
                    img_label.image = photo
                    img_label.pack(expand=True, pady=3)
                    img_label.bind('<Button-1>', lambda e, pid=product_id: self.add_to_cart(pid, product))
                else:
                    category_icons = {
                        'paint': '🎨',
                        'roof sheet': '🏗️',
                        'limination sheet': '📄',
                        'sanitary': '🚿',
                        'hardware': '🔧'
                    }
                    category_lower = category_name.lower() if category_name else ''
                    icon = category_icons.get(category_lower, '📦')
                    
                    icon_label = tk.Label(
                        image_frame,
                        text=icon,
                        font=('Arial', 16),
                        bg='#f8f9fa',
                        fg='#bdc3c7',
                        cursor='hand2'
                    )
                    icon_label.pack(expand=True, pady=3)
                    icon_label.bind('<Button-1>', lambda e, pid=product_id: self.add_to_cart(pid, product))
            except:
                error_label = tk.Label(
                    image_frame,
                    text="📦",
                    font=('Arial', 16),
                    bg='#f8f9fa',
                    fg='#bdc3c7',
                    cursor='hand2'
                )
                error_label.pack(expand=True, pady=3)
                error_label.bind('<Button-1>', lambda e, pid=product_id: self.add_to_cart(pid, product))
            
            info_frame = tk.Frame(card_frame, bg='white')
            info_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
            
            company_text = company[:12] + "..." if len(company) > 12 else company
            tk.Label(
                info_frame,
                text=company_text,
                font=('Arial', 8, 'bold'),
                fg='#2c3e50',
                bg='white',
                wraplength=140
            ).pack(anchor='w')
            
            type_text = ptype[:15] + "..." if len(ptype) > 15 else ptype
            tk.Label(
                info_frame,
                text=type_text,
                font=('Arial', 7),
                fg='#7f8c8d',
                bg='white',
                wraplength=140
            ).pack(anchor='w')
            
            color_text = color[:10] + "..." if len(color) > 10 else color
            tk.Label(
                info_frame,
                text=color_text,
                font=('Arial', 7),
                fg='#34495e',
                bg='white'
            ).pack(anchor='w')
            
            tk.Label(
                info_frame,
                text=f"₨{sale_price}",
                font=('Arial', 8, 'bold'),
                fg='#27ae60',
                bg='white'
            ).pack(anchor='w')
            
            stock = current_stock
            stock_color = '#27ae60' if stock > 10 else '#e67e22' if stock > 0 else '#e74c3c'
            
            # Get measurement type WITH CATEGORY and display stock accordingly
            measurement_type = self.get_measurement_type_from_packing(packing, category_name)
            stock_text = self.format_stock_display(stock, measurement_type)
            
            tk.Label(
                info_frame,
                text=stock_text,
                font=('Arial', 7, 'bold'),
                fg=stock_color,
                bg='white'
            ).pack(anchor='w')
            
            add_btn = tk.Label(
                card_frame,
                text="➕ Add to Cart",
                font=('Arial', 8, 'bold'),
                bg='#3498db',
                fg='white',
                relief='flat',
                cursor='hand2'
            )
            add_btn.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)
            add_btn.bind('<Button-1>', lambda e, pid=product_id: self.add_to_cart(pid, product))
            
            return card_frame
            
        except Exception as e:
            print(f"Error creating product card: {e}")
            return None

    def get_measurement_type_from_packing(self, packing, category_name=None):
        """Extract measurement type from packing field - FIXED FOR GRAMS"""
        if not packing:
            return 'units'
        
        # FORCE Paint category to always be units, regardless of packing
        if category_name and category_name.lower() == 'paint':
            return 'units'
        
        packing_lower = str(packing).lower()
        
        # Check for measurement indicators in packing field
        if 'unit:' in packing_lower:
            # Extract measurement type after "Unit: "
            measurement_part = packing_lower.split('unit:')[-1].strip()
            
            # Check for exact matches first to avoid false positives
            if any(unit in measurement_part for unit in ['kilogram', 'kg']):
                return 'kg'
            elif any(unit in measurement_part for unit in ['gram', 'g ', 'gm', 'gms']):  # ADDED GRAMS
                return 'grams'
            elif any(unit in measurement_part for unit in ['pound', 'lb']):
                return 'pounds'
            elif any(unit in measurement_part for unit in ['meter', 'mtr', 'm ']):  # Added space after m to avoid matching kg
                return 'meters'
            elif any(unit in measurement_part for unit in ['feet', 'ft', 'foot']):
                return 'feet'
            elif any(unit in measurement_part for unit in ['liter', 'ltr', 'l ']):  # Added space after l to avoid matching other units
                return 'liters'
            elif any(unit in measurement_part for unit in ['dozen', 'doz']):
                return 'dozen'
            elif any(unit in measurement_part for unit in ['piece', 'pcs', 'unit']):
                return 'units'
            else:
                return 'units'  # Default to units if unknown measurement
        
        # Direct measurement checks with exact matching
        # Check for kg first to avoid false matches with meter
        if any(unit in packing_lower for unit in ['kilogram', ' kg', 'kg ']):  # Added spaces to avoid partial matches
            return 'kg'
        elif any(unit in packing_lower for unit in ['gram', ' g ', 'gm ', 'gms']):  # ADDED GRAMS with spaces
            return 'grams'
        elif any(unit in packing_lower for unit in ['pound', ' lb', 'lb ']):
            return 'pounds'
        elif any(unit in packing_lower for unit in ['meter', ' mtr', ' m ']):  # Added spaces to avoid matching kg
            return 'meters'
        elif any(unit in packing_lower for unit in ['feet', ' ft', 'foot']):
            return 'feet'
        elif any(unit in packing_lower for unit in ['liter', ' ltr', ' l ']):  # Added spaces to avoid partial matches
            return 'liters'
        elif any(unit in packing_lower for unit in ['dozen', ' doz']):
            return 'dozen'
        elif any(unit in packing_lower for unit in ['piece', ' pcs', 'unit']):
            return 'units'
        else:
            return 'units'  # Default to units

    def format_stock_display(self, stock, measurement_type):
        """Format stock display based on measurement type - UPDATED WITH GRAMS"""
        unit_display = {
            'feet': 'ft',
            'meters': 'm', 
            'kg': 'kg',
            'grams': 'g',  # ADDED GRAMS
            'pounds': 'lb',
            'liters': 'L',
            'dozen': 'doz',
            'units': 'pcs'
        }
        
        unit = unit_display.get(measurement_type, 'pcs')
        return f"Stock: {stock} {unit}"

    def format_quantity_display(self, quantity, unit_type):
        """Format quantity display based on unit type - UPDATED WITH GRAMS"""
        if unit_type == 'dozen':
            # For dozen, show both dozen and pieces for clarity
            dozens = quantity
            pieces = int(dozens * 12)
            if dozens == int(dozens):
                # Whole dozens
                return f"{int(dozens)} doz"
            else:
                # Fractional dozens - show both for clarity
                return f"{dozens:.1f} doz"
        
        unit_display = {
            'feet': 'ft',
            'meters': 'm', 
            'kg': 'kg',
            'grams': 'g',  # ADDED GRAMS
            'pounds': 'lb',
            'liters': 'L',
            'units': 'pcs'
        }
        
        unit = unit_display.get(unit_type, 'pcs')
        
        # Format numbers nicely
        if unit_type in ['units', 'grams']:
            return f"{quantity:.0f} {unit}"  # Show grams and units as whole numbers
        else:
            return f"{quantity:.2f} {unit}"

    def add_to_cart(self, product_id, product):
        try:
            if len(product) < 14:
                return
                
            (pid, category_id, company, ptype, color,
            sale_price, purchase_price, packing, volume, current_stock,
            image_path, created_at, updated_at, category_name) = product[:14]
            
            # Check if product already in cart
            for item in self.cart:
                if item['product_id'] == product_id:
                    self.edit_cart_item_by_product_id(product_id)
                    return
                    
            if current_stock <= 0:
                messagebox.showwarning("Out of Sale", "This product is out of stock!")
                return
            
            # Determine measurement type from packing field WITH CATEGORY
            measurement_type = self.get_measurement_type_from_packing(packing, category_name)
            
            if measurement_type == 'units':
                # For units-based products (default)
                self.show_quantity_popup(product_id, product, is_edit_mode=False)
            else:
                # For measurement-based products (feet, meters, kg, liters, dozen, pounds, grams, etc.)
                self.add_product_with_measurement(product_id, product, measurement_type)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add to cart: {str(e)}")

    def add_product_with_measurement(self, product_id, product, measurement_type):
        """Add product with any measurement type - INCLUDING GRAMS"""
        try:
            (pid, category_id, company, ptype, color,
            sale_price, purchase_price, packing, volume, current_stock,
            image_path, created_at, updated_at, category_name) = product[:14]
            
            # SPECIAL HANDLING FOR DOZEN - Allow piece-level input
            if measurement_type == 'dozen':
                self.add_dozen_product_with_pieces(product_id, product)
                return
            
            # Map measurement types to display names
            measurement_display = {
                'feet': 'feet',
                'meters': 'meters', 
                'kg': 'kilograms',
                'grams': 'grams',  # ADDED GRAMS
                'pounds': 'pounds',
                'liters': 'liters',
                'units': 'units'
            }
            
            unit_display = measurement_display.get(measurement_type, 'units')
            
            # Create dialog for measurement input
            dialog = tk.Toplevel(self.parent)
            dialog.title(f"Enter {unit_display.capitalize()}")
            dialog.geometry("400x250")
            dialog.configure(bg='white')
            dialog.transient(self.parent)
            dialog.grab_set()
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
            y = (dialog.winfo_screenheight() // 2) - (250 // 2)
            dialog.geometry(f"400x250+{x}+{y}")
            
            tk.Label(
                dialog,
                text=f"Enter {unit_display} for {company} - {ptype}",
                font=('Arial', 14, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(pady=15)
            
            # Available stock information
            stock_info = f"Available: {current_stock} {unit_display}"
            tk.Label(
                dialog,
                text=stock_info,
                font=('Arial', 11),
                fg='#27ae60',
                bg='white'
            ).pack(pady=5)
            
            input_frame = tk.Frame(dialog, bg='white')
            input_frame.pack(pady=15)
            
            tk.Label(
                input_frame,
                text=f"{unit_display.capitalize()}:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(side=tk.LEFT, padx=(0, 10))
            
            quantity_var = tk.StringVar(value="0")
            quantity_entry = tk.Entry(
                input_frame,
                textvariable=quantity_var,
                font=('Arial', 11),
                width=10,
                relief='solid',
                bd=1
            )
            quantity_entry.pack(side=tk.LEFT)
            quantity_entry.select_range(0, tk.END)
            quantity_entry.focus()
            
            button_frame = tk.Frame(dialog, bg='white')
            button_frame.pack(pady=15)
            
            def add_with_measurement():
                try:
                    quantity = float(quantity_var.get())
                    
                    if quantity <= 0:
                        messagebox.showerror("Error", f"{unit_display.capitalize()} must be greater than 0!")
                        return
                    
                    if quantity > current_stock:
                        messagebox.showerror("Error", f"Only {current_stock} {unit_display} available!")
                        return
                    
                    # Calculate total price
                    total_price = float(sale_price) * quantity
                    
                    cart_item = {
                        'product_id': product_id,
                        'company': company,
                        'type': ptype,
                        'color': color,
                        'unit_price': float(sale_price),
                        'purchase_price': float(purchase_price),
                        'quantity': quantity,
                        'total_price': total_price,
                        'current_stock': current_stock,
                        'category_name': category_name,
                        'packing': packing,
                        'volume': volume,
                        'unit_type': measurement_type
                    }
                    
                    self.cart.append(cart_item)
                    dialog.destroy()
                    messagebox.showinfo("Added to Cart", 
                                    f"Added {quantity} {unit_display} of {company} - {ptype} to cart!")
                    self.update_cart_display()
                    
                except ValueError:
                    messagebox.showerror("Error", f"Please enter a valid number for {unit_display}!")
            
            tk.Button(
                button_frame,
                text="Add to Cart",
                font=('Arial', 11, 'bold'),
                bg='#27ae60',
                fg='white',
                relief='flat',
                command=add_with_measurement
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Button(
                button_frame,
                text="Cancel",
                font=('Arial', 11),
                bg='#95a5a6',
                fg='white',
                relief='flat',
                command=dialog.destroy
            ).pack(side=tk.LEFT, padx=5)
            
            dialog.bind('<Return>', lambda e: add_with_measurement())
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {str(e)}")

    def add_dozen_product_with_pieces(self, product_id, product):
        """Special method for dozen products that allows piece-level input"""
        try:
            (pid, category_id, company, ptype, color,
            sale_price, purchase_price, packing, volume, current_stock,
            image_path, created_at, updated_at, category_name) = product[:14]
            
            # Calculate available pieces
            available_dozen = current_stock
            available_pieces = available_dozen * 12
            
            dialog = tk.Toplevel(self.parent)
            dialog.title("Enter Quantity (Dozen)")
            dialog.geometry("450x350")
            dialog.configure(bg='white')
            dialog.transient(self.parent)
            dialog.grab_set()
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
            y = (dialog.winfo_screenheight() // 2) - (350 // 2)
            dialog.geometry(f"450x350+{x}+{y}")
            
            tk.Label(
                dialog,
                text=f"Enter Quantity for {company} - {ptype}",
                font=('Arial', 14, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(pady=15)
            
            # Available stock information
            stock_info = f"Available: {available_dozen} dozen ({available_pieces} pieces)"
            tk.Label(
                dialog,
                text=stock_info,
                font=('Arial', 11),
                fg='#27ae60',
                bg='white'
            ).pack(pady=5)
            
            # Instruction
            tk.Label(
                dialog,
                text="💡 You can enter either dozens or pieces",
                font=('Arial', 10),
                fg='#3498db',
                bg='white'
            ).pack(pady=2)
            
            # Input frame for dozen
            dozen_frame = tk.Frame(dialog, bg='white')
            dozen_frame.pack(fill=tk.X, pady=10, padx=20)
            
            tk.Label(
                dozen_frame,
                text="Dozens:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(side=tk.LEFT)
            
            dozen_var = tk.StringVar(value="0")
            dozen_entry = tk.Entry(
                dozen_frame,
                textvariable=dozen_var,
                font=('Arial', 11),
                width=8,
                relief='solid',
                bd=1
            )
            dozen_entry.pack(side=tk.LEFT, padx=(10, 0))
            
            # Input frame for pieces
            pieces_frame = tk.Frame(dialog, bg='white')
            pieces_frame.pack(fill=tk.X, pady=10, padx=20)
            
            tk.Label(
                pieces_frame,
                text="Pieces:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(side=tk.LEFT)
            
            pieces_var = tk.StringVar(value="0")
            pieces_entry = tk.Entry(
                pieces_frame,
                textvariable=pieces_var,
                font=('Arial', 11),
                width=8,
                relief='solid',
                bd=1
            )
            pieces_entry.pack(side=tk.LEFT, padx=(10, 0))
            
            # Result display frame
            result_frame = tk.Frame(dialog, bg='#f8f9fa', relief='solid', bd=1)
            result_frame.pack(fill=tk.X, pady=10, padx=20)
            
            result_label = tk.Label(
                result_frame,
                text="Total: 0 dozen (0 pieces)",
                font=('Arial', 10, 'bold'),
                fg='#2c3e50',
                bg='#f8f9fa'
            )
            result_label.pack(pady=8)
            
            def update_result():
                """Update the result display when values change"""
                try:
                    dozens = float(dozen_var.get() or 0)
                    pieces = int(pieces_var.get() or 0)
                    
                    # Convert pieces to fractional dozens
                    pieces_fraction = pieces / 12.0
                    total_dozen = dozens + pieces_fraction
                    total_pieces = (dozens * 12) + pieces
                    
                    result_label.config(text=f"Total: {total_dozen:.2f} dozen ({total_pieces} pieces)")
                except:
                    result_label.config(text="Total: 0 dozen (0 pieces)")
            
            def add_dozen_to_cart():
                try:
                    dozens = float(dozen_var.get() or 0)
                    pieces = int(pieces_var.get() or 0)
                    
                    # Calculate total in dozen units
                    total_dozen = dozens + (pieces / 12.0)
                    total_pieces = (dozens * 12) + pieces
                    
                    if total_dozen <= 0:
                        messagebox.showerror("Error", "Quantity must be greater than 0!")
                        return
                    
                    if total_dozen > available_dozen:
                        messagebox.showerror("Error", 
                                        f"Only {available_dozen} dozen ({available_pieces} pieces) available!\n"
                                        f"You requested {total_dozen:.2f} dozen ({total_pieces} pieces)")
                        return
                    
                    # Calculate total price (price is per dozen)
                    total_price = float(sale_price) * total_dozen
                    
                    cart_item = {
                        'product_id': product_id,
                        'company': company,
                        'type': ptype,
                        'color': color,
                        'unit_price': float(sale_price),
                        'purchase_price': float(purchase_price),
                        'quantity': total_dozen,
                        'total_price': total_price,
                        'current_stock': current_stock,
                        'category_name': category_name,
                        'packing': packing,
                        'volume': volume,
                        'unit_type': 'dozen',
                        'pieces_count': total_pieces
                    }
                    
                    self.cart.append(cart_item)
                    dialog.destroy()
                    
                    messagebox.showinfo("Added to Cart", 
                                    f"Added {total_dozen:.2f} dozen ({total_pieces} pieces) of {company} - {ptype} to cart!")
                    self.update_cart_display()
                    
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numbers!")
            
            # Bind events to update result
            dozen_var.trace('w', lambda *args: update_result())
            pieces_var.trace('w', lambda *args: update_result())
            
            button_frame = tk.Frame(dialog, bg='white')
            button_frame.pack(fill=tk.X, pady=15, padx=20)
            
            tk.Button(
                button_frame,
                text="Add to Cart",
                font=('Arial', 11, 'bold'),
                bg='#27ae60',
                fg='white',
                relief='flat',
                command=add_dozen_to_cart
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Button(
                button_frame,
                text="Cancel",
                font=('Arial', 11),
                bg='#95a5a6',
                fg='white',
                relief='flat',
                command=dialog.destroy
            ).pack(side=tk.LEFT, padx=5)
            
            # Set focus and bind enter key
            dozen_entry.focus()
            dozen_entry.select_range(0, tk.END)
            dialog.bind('<Return>', lambda e: add_dozen_to_cart())
            
            # Initial update
            update_result()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add dozen product: {str(e)}")

    def show_quantity_popup(self, product_id, product, is_edit_mode=False):
        """Show quantity popup for units-based products only"""
        try:
            (pid, category_id, company, ptype, color,
            sale_price, purchase_price, packing, volume, current_stock,
            image_path, created_at, updated_at, category_name) = product[:14]
            
            # Create dialog for quantity input
            dialog = tk.Toplevel(self.parent)
            dialog.title("Enter Quantity")
            dialog.geometry("400x250")
            dialog.configure(bg='white')
            dialog.transient(self.parent)
            dialog.grab_set()
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
            y = (dialog.winfo_screenheight() // 2) - (250 // 2)
            dialog.geometry(f"400x250+{x}+{y}")
            
            tk.Label(
                dialog,
                text=f"Enter Quantity for {company} - {ptype}",
                font=('Arial', 14, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(pady=15)
            
            # Available stock information
            stock_info = f"Available: {current_stock} units"
            tk.Label(
                dialog,
                text=stock_info,
                font=('Arial', 11),
                fg='#27ae60',
                bg='white'
            ).pack(pady=5)
            
            input_frame = tk.Frame(dialog, bg='white')
            input_frame.pack(pady=15)
            
            tk.Label(
                input_frame,
                text="Quantity:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(side=tk.LEFT, padx=(0, 10))
            
            quantity_var = tk.StringVar(value="1")
            quantity_entry = tk.Entry(
                input_frame,
                textvariable=quantity_var,
                font=('Arial', 11),
                width=10,
                relief='solid',
                bd=1
            )
            quantity_entry.pack(side=tk.LEFT)
            quantity_entry.select_range(0, tk.END)
            quantity_entry.focus()
            
            button_frame = tk.Frame(dialog, bg='white')
            button_frame.pack(pady=15)
        
            def add_with_quantity():
                try:
                    quantity = int(quantity_var.get())
                    
                    if quantity <= 0:
                        messagebox.showerror("Error", "Quantity must be greater than 0!")
                        return
                    
                    if quantity > current_stock:
                        messagebox.showerror("Error", f"Only {current_stock} units available!")
                        return
                    
                    # Check if editing existing item
                    if is_edit_mode:
                        for item in self.cart:
                            if item['product_id'] == product_id:
                                item['quantity'] = quantity
                                item['total_price'] = quantity * item['unit_price']
                                break
                    else:
                        # Create new cart item
                        cart_item = {
                            'product_id': product_id,
                            'company': company,
                            'type': ptype,
                            'color': color,
                            'unit_price': float(sale_price),
                            'purchase_price': float(purchase_price),
                            'quantity': quantity,
                            'total_price': float(sale_price) * quantity,
                            'current_stock': current_stock,
                            'category_name': category_name,
                            'packing': packing,
                            'volume': volume,
                            'unit_type': 'units'  # Mark as units-based
                        }
                        
                        self.cart.append(cart_item)
                    
                    dialog.destroy()
                    self.update_cart_display()
                    
                    if is_edit_mode:
                        messagebox.showinfo("Cart Updated", f"Quantity updated to {quantity} for {company} - {ptype}!")
                    else:
                        messagebox.showinfo("Added to Cart", f"Added {quantity} units of {company} - {ptype} to cart!")
                    
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number for quantity!")
            
            # Set button text based on mode
            button_text = "Update Quantity" if is_edit_mode else "Add to Cart"
            
            tk.Button(
                button_frame,
                text=button_text,
                font=('Arial', 11, 'bold'),
                bg='#27ae60',
                fg='white',
                relief='flat',
                command=add_with_quantity
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Button(
                button_frame,
                text="Cancel",
                font=('Arial', 11),
                bg='#95a5a6',
                fg='white',
                relief='flat',
                command=dialog.destroy
            ).pack(side=tk.LEFT, padx=5)
            
            dialog.bind('<Return>', lambda e: add_with_quantity())
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {str(e)}")

    def edit_cart_item_by_product_id(self, product_id):
        """Edit cart item by product ID (used when adding existing product)"""
        for index, item in enumerate(self.cart):
            if item['product_id'] == product_id:
                self.edit_cart_item_specific(index)
                return

    def edit_cart_item_specific(self, index):
        """Edit specific cart item by index - UPDATED FOR ALL MEASUREMENT TYPES INCLUDING GRAMS"""
        try:
            item = self.cart[index]
            unit_type = item.get('unit_type', 'units')
            
            # SPECIAL HANDLING FOR DOZEN - Use piece-level editing
            if unit_type == 'dozen':
                self.edit_dozen_item_with_pieces(index)
                return
                
            # For other measurement types (grams, kg, meters, etc.)
            dialog = tk.Toplevel(self.parent)
            dialog.title("Edit Cart Item")
            dialog.geometry("400x300")
            dialog.configure(bg='white')
            dialog.transient(self.parent)
            dialog.grab_set()
            
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
            y = (dialog.winfo_screenheight() // 2) - (300 // 2)
            dialog.geometry(f"400x300+{x}+{y}")
            
            # Determine unit type and labels
            unit_type = item.get('unit_type', 'units')
            unit_display_map = {
                'feet': 'feet',
                'meters': 'meters',
                'kg': 'kilograms', 
                'grams': 'grams',  # ADDED GRAMS
                'pounds': 'pounds',
                'liters': 'liters',
                'units': 'units'
            }
            unit_label = unit_display_map.get(unit_type, 'Quantity')
            current_value = item['quantity']
            stock = item['current_stock']
            
            tk.Label(
                dialog,
                text=f"Edit: {item['company']} - {item['type']}",
                font=('Arial', 14, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(pady=10)
            
            form_frame = tk.Frame(dialog, bg='white')
            form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            qty_frame = tk.Frame(form_frame, bg='white')
            qty_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                qty_frame,
                text=f"{unit_label.capitalize()}:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(side=tk.LEFT)
            
            # Stock information
            stock_text = f"Available: {stock} {unit_label}"
            tk.Label(
                qty_frame,
                text=stock_text,
                font=('Arial', 10),
                fg='#27ae60',
                bg='white'
            ).pack(side=tk.RIGHT)
            
            qty_var = tk.StringVar(value=str(current_value))
            qty_entry = tk.Entry(
                qty_frame,
                textvariable=qty_var,
                font=('Arial', 11),
                width=10,
                relief='solid',
                bd=1
            )
            qty_entry.pack(side=tk.LEFT, padx=(10, 0))
            qty_entry.select_range(0, tk.END)
            
            price_frame = tk.Frame(form_frame, bg='white')
            price_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                price_frame,
                text="Unit Price:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(side=tk.LEFT)
            
            price_var = tk.StringVar(value=str(item['unit_price']))
            price_entry = tk.Entry(
                price_frame,
                textvariable=price_var,
                font=('Arial', 11),
                width=10,
                relief='solid',
                bd=1
            )
            price_entry.pack(side=tk.RIGHT)
            
            details_frame = tk.Frame(form_frame, bg='white')
            details_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                details_frame,
                text="Product Details:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(anchor='w')
            
            details_text = tk.Text(
                details_frame,
                height=4,
                width=40,
                font=('Arial', 10),
                relief='solid',
                bd=1
            )
            details_text.pack(fill=tk.X, pady=5)
            details_text.insert('1.0', self.get_cart_details_display(item))
            details_text.config(state='disabled')
            
            def update_item():
                try:
                    if unit_type in ['units', 'grams']:
                        new_qty = float(qty_var.get())
                    else:
                        new_qty = float(qty_var.get())
                    
                    new_price = float(price_var.get())
                    
                    if new_qty <= 0:
                        messagebox.showerror("Error", f"{unit_label.capitalize()} must be greater than 0!")
                        return
                    if new_qty > stock:
                        messagebox.showerror("Error", f"Only {stock} {unit_label} available!")
                        return
                    if new_price <= 0:
                        messagebox.showerror("Error", "Price must be greater than 0!")
                        return
                    
                    item['quantity'] = new_qty
                    item['unit_price'] = new_price
                    item['total_price'] = new_qty * new_price
                    
                    dialog.destroy()
                    self.update_cart_display()
                    messagebox.showinfo("Success", "Item updated successfully!")
                    
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numbers!")
            
            button_frame = tk.Frame(dialog, bg='white')
            button_frame.pack(fill=tk.X, padx=20, pady=15)
            
            tk.Button(
                button_frame,
                text="💾 Update Item",
                font=('Arial', 11, 'bold'),
                bg='#3498db',
                fg='white',
                relief='flat',
                command=update_item
            ).pack(side=tk.RIGHT, padx=5)
            
            tk.Button(
                button_frame,
                text="Cancel",
                font=('Arial', 11),
                bg='#95a5a6',
                fg='white',
                relief='flat',
                command=dialog.destroy
            ).pack(side=tk.RIGHT, padx=5)
            
            qty_entry.focus()
            dialog.bind('<Return>', lambda e: update_item())
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit item: {str(e)}")

    def edit_dozen_item_with_pieces(self, index):
        """Edit dozen item with piece-level input"""
        try:
            item = self.cart[index]
            current_dozen = item['quantity']
            current_pieces = int(current_dozen * 12)
            stock = item['current_stock']
            available_pieces = stock * 12
            
            dialog = tk.Toplevel(self.parent)
            dialog.title("Edit Quantity (Dozen)")
            dialog.geometry("450x400")
            dialog.configure(bg='white')
            dialog.transient(self.parent)
            dialog.grab_set()
            
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
            y = (dialog.winfo_screenheight() // 2) - (400 // 2)
            dialog.geometry(f"450x400+{x}+{y}")
            
            tk.Label(
                dialog,
                text=f"Edit: {item['company']} - {item['type']}",
                font=('Arial', 14, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(pady=10)
            
            # Available stock
            stock_info = f"Available: {stock} dozen ({available_pieces} pieces)"
            tk.Label(
                dialog,
                text=stock_info,
                font=('Arial', 11),
                fg='#27ae60',
                bg='white'
            ).pack(pady=5)
            
            # Instruction
            tk.Label(
                dialog,
                text="💡 You can enter either dozens or pieces",
                font=('Arial', 10),
                fg='#3498db',
                bg='white'
            ).pack(pady=2)
            
            # Input frame for dozen
            dozen_frame = tk.Frame(dialog, bg='white')
            dozen_frame.pack(fill=tk.X, pady=10, padx=20)
            
            tk.Label(
                dozen_frame,
                text="Dozens:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(side=tk.LEFT)
            
            dozen_var = tk.StringVar(value=str(int(current_dozen)))
            dozen_entry = tk.Entry(
                dozen_frame,
                textvariable=dozen_var,
                font=('Arial', 11),
                width=8,
                relief='solid',
                bd=1
            )
            dozen_entry.pack(side=tk.LEFT, padx=(10, 0))
            
            # Input frame for pieces
            pieces_frame = tk.Frame(dialog, bg='white')
            pieces_frame.pack(fill=tk.X, pady=10, padx=20)
            
            tk.Label(
                pieces_frame,
                text="Pieces:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(side=tk.LEFT)
            
            pieces_var = tk.StringVar(value=str(current_pieces % 12))
            pieces_entry = tk.Entry(
                pieces_frame,
                textvariable=pieces_var,
                font=('Arial', 11),
                width=8,
                relief='solid',
                bd=1
            )
            pieces_entry.pack(side=tk.LEFT, padx=(10, 0))
            
            # Result display
            result_frame = tk.Frame(dialog, bg='#f8f9fa', relief='solid', bd=1)
            result_frame.pack(fill=tk.X, pady=10, padx=20)
            
            result_label = tk.Label(
                result_frame,
                text=f"Total: {current_dozen:.2f} dozen ({current_pieces} pieces)",
                font=('Arial', 10, 'bold'),
                fg='#2c3e50',
                bg='#f8f9fa'
            )
            result_label.pack(pady=8)
            
            # Price frame
            price_frame = tk.Frame(dialog, bg='white')
            price_frame.pack(fill=tk.X, pady=10, padx=20)
            
            tk.Label(
                price_frame,
                text="Price per dozen:",
                font=('Arial', 11, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).pack(side=tk.LEFT)
            
            price_var = tk.StringVar(value=str(item['unit_price']))
            price_entry = tk.Entry(
                price_frame,
                textvariable=price_var,
                font=('Arial', 11),
                width=10,
                relief='solid',
                bd=1
            )
            price_entry.pack(side=tk.RIGHT)
            
            def update_result():
                try:
                    dozens = float(dozen_var.get() or 0)
                    pieces = int(pieces_var.get() or 0)
                    total_dozen = dozens + (pieces / 12.0)
                    total_pieces = (dozens * 12) + pieces
                    result_label.config(text=f"Total: {total_dozen:.2f} dozen ({total_pieces} pieces)")
                except:
                    pass
            
            def update_item():
                try:
                    dozens = float(dozen_var.get() or 0)
                    pieces = int(pieces_var.get() or 0)
                    new_price = float(price_var.get())
                    
                    total_dozen = dozens + (pieces / 12.0)
                    total_pieces = (dozens * 12) + pieces
                    
                    if total_dozen <= 0:
                        messagebox.showerror("Error", "Quantity must be greater than 0!")
                        return
                    
                    if total_dozen > stock:
                        messagebox.showerror("Error", 
                                           f"Only {stock} dozen ({available_pieces} pieces) available!")
                        return
                    
                    if new_price <= 0:
                        messagebox.showerror("Error", "Price must be greater than 0!")
                        return
                    
                    item['quantity'] = total_dozen
                    item['unit_price'] = new_price
                    item['total_price'] = total_dozen * new_price
                    item['pieces_count'] = total_pieces
                    
                    dialog.destroy()
                    self.update_cart_display()
                    messagebox.showinfo("Success", 
                                      f"Updated to {total_dozen:.2f} dozen ({total_pieces} pieces)!")
                    
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numbers!")
        
            # Bind events
            dozen_var.trace('w', lambda *args: update_result())
            pieces_var.trace('w', lambda *args: update_result())
            
            button_frame = tk.Frame(dialog, bg='white')
            button_frame.pack(fill=tk.X, pady=15, padx=20)
            
            tk.Button(
                button_frame,
                text="💾 Update Item",
                font=('Arial', 11, 'bold'),
                bg='#3498db',
                fg='white',
                relief='flat',
                command=update_item
            ).pack(side=tk.RIGHT, padx=5)
            
            tk.Button(
                button_frame,
                text="Cancel",
                font=('Arial', 11),
                bg='#95a5a6',
                fg='white',
                relief='flat',
                command=dialog.destroy
            ).pack(side=tk.RIGHT, padx=5)
            
            dozen_entry.focus()
            dozen_entry.select_range(0, tk.END)
            dialog.bind('<Return>', lambda e: update_item())
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit dozen item: {str(e)}")

    def edit_cart_item(self, event=None):
        """SINGLE EDIT FUNCTIONALITY - handles both button click and double-click"""
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select an item to edit!")
            return
            
        try:
            index = self.cart_tree.index(selected[0])
            self.edit_cart_item_specific(index)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit item: {str(e)}")
    def get_cart_details_display(self, item):
        """Get simplified details for cart display with proper spacing"""
        try:
            details_parts = []
            
            # Add color if available
            color = item.get('color', '')
            if color and str(color).strip() and color not in ['N/A', 'None', '']:
                color = str(color).strip()
                color = ' '.join(color.split())  # Normalize spacing
                details_parts.append(f"Color: {color}")
            
            # Add size/volume if available
            volume = item.get('volume', '')
            if volume and str(volume).strip() and volume not in ['N/A', 'None', '']:
                volume = str(volume).strip()
                volume = ' '.join(volume.split())  # Normalize spacing
                details_parts.append(f"Size: {volume}")
            else:
                # If no volume, check packing for size info
                packing = item.get('packing', '')
                if packing and str(packing).strip() and packing not in ['N/A', 'None', '']:
                    packing = str(packing).strip()
                    packing = ' '.join(packing.split())  # Normalize spacing
                    details_parts.append(f"Pack: {packing}")
            
            # Join with proper spacing
            result = ', '.join(details_parts) if details_parts else "Standard"
            
            # Ensure no extra whitespace
            result = ' '.join(result.split())
            
            return result
            
        except Exception as e:
            print(f"Error in get_cart_details_display: {e}")
            return "Product Details"

    def safe_get_product_text(self, item):
        """Safely get product text with proper spacing and formatting"""
        try:
                company = item.get('company', 'Unknown Company')
                ptype = item.get('type', 'Unknown Type')
                
                # Clean and ensure proper string conversion
                company = str(company).strip() if company else "Unknown Company"
                ptype = str(ptype).strip() if ptype else "Unknown Type"
                
                # Remove any extra whitespace and ensure single spaces
                company = ' '.join(company.split())
                ptype = ' '.join(ptype.split())
                
                # Add proper spacing and formatting
                company_display = company[:22] + "..." if len(company) > 22 else company
                type_display = ptype[:20] + "..." if len(ptype) > 20 else ptype
                
                # Return with clear line separation
                return f"{company_display}\n{type_display}"
            
        except Exception as e:
            print(f"Error in safe_get_product_text: {e}")
            return "Product Info\nDetails"

    def update_cart_display(self):
        """Update cart display with proper spacing between items"""
        try:
            # Clear existing items
            for item in self.cart_tree.get_children():
                self.cart_tree.delete(item)
                
            # Add some vertical spacing between rows
            style = ttk.Style()
            style.configure("Treeview", rowheight=35)  # Increased row height for better spacing
            
            for item in self.cart:
                try:
                    # Safe product text with proper spacing
                    product_text = self.safe_get_product_text(item)
                    
                    # Full details with proper spacing
                    details_text = self.get_cart_details_display(item)
                    
                    # Safe quantity display
                    unit_type = item.get('unit_type', 'units')
                    quantity_display = self.format_quantity_display(item['quantity'], unit_type)
                    
                    # Safe price formatting
                    try:
                        unit_price = f"₨{float(item['unit_price']):,.0f}"
                        total_price = f"₨{float(item['total_price']):,.0f}"
                    except:
                        unit_price = "₨0"
                        total_price = "₨0"
                    
                    # Insert into cart tree with proper data
                    self.cart_tree.insert('', 'end', values=(
                        product_text,              # Product name (company - type)
                        details_text,              # Full details (color, size, packing)
                        quantity_display,          # Quantity with units
                        unit_price,                # Unit price
                        total_price,               # Total price
                    ))
                    
                except Exception as e:
                    print(f"Error displaying cart item: {e}")
                    # Add a fallback item with proper spacing
                    self.cart_tree.insert('', 'end', values=(
                        "Product Info\nError",
                        "Check product data",
                        "0",
                        "₨0",
                        "₨0",
                    ))
            
            # Update item count and totals
            self.update_item_count()
            self.update_totals()
            
        except Exception as e:
            print(f"Error in update_cart_display: {e}")
            messagebox.showerror("Display Error", "Failed to update cart display")

    def update_item_count(self):
        """Update the item count display in the cart summary"""
        total_items = len(self.cart)
        self.item_count_label.config(text=f"Items: {total_items}")
    
    def update_totals(self, event=None):
        subtotal = sum(item['total_price'] for item in self.cart)
        
        try:
            discount = float(self.discount_var.get() or 0)
        except:
            discount = 0
            
        total = max(0, subtotal - discount)
        
        self.subtotal_label.config(text=f"Subtotal: ₨{subtotal:,.0f}")
        self.total_label.config(text=f"Total: ₨{total:,.0f}")
        
    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select an item to remove!")
            return
            
        try:
            index = self.cart_tree.index(selected[0])
            if index < len(self.cart):
                item = self.cart[index]
                result = messagebox.askyesno("Remove Item", f"Remove {item['company']} - {item['type']} from cart?")
                if result:
                    self.cart.pop(index)
                    self.update_cart_display()
                    messagebox.showinfo("Success", "Item removed from cart!")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove item: {str(e)}")
                
    def clear_cart(self):
        if self.cart:
            result = messagebox.askyesno("Clear Cart", "Are you sure you want to clear the entire cart?")
            if result:
                self.cart = []
                self.update_cart_display()
                messagebox.showinfo("Success", "Cart cleared!")
        
    def load_customers(self):
        try:
            customers = self.sale_service.get_all_customers()
            
            customer_names = [customer[1] for customer in customers]
            
            if "Walk-in Customer" not in customer_names:
                customer_names.insert(0, "Walk-in Customer")
                
            self.customer_dropdown['values'] = customer_names
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers: {str(e)}")
            self.customer_dropdown['values'] = ["Walk-in Customer"]
            
    def on_customer_select(self, event):
        customer_name = self.customer_var.get()
        self.customer_name_label.config(text=f"Customer: {customer_name}")
        
    def add_customer(self):
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add New Customer")
        dialog.geometry("400x400")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"400x400+{x}+{y}")
        
        tk.Label(
            dialog,
            text="Add New Customer",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(pady=15)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        name_frame = tk.Frame(form_frame, bg='white')
        name_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            name_frame,
            text="Name:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        name_entry = tk.Entry(
            name_frame,
            font=('Arial', 11),
            relief='solid',
            bd=1,
            width=30
        )
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        phone_frame = tk.Frame(form_frame, bg='white')
        phone_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            phone_frame,
            text="Phone:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        phone_entry = tk.Entry(
            phone_frame,
            font=('Arial', 11),
            relief='solid',
            bd=1,
            width=30
        )
        phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        address_frame = tk.Frame(form_frame, bg='white')
        address_frame.pack(fill=tk.BOTH, expand=True, pady=8)
        
        tk.Label(
            address_frame,
            text="Address:",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='white',
            width=12,
            anchor='w'
        ).pack(anchor='w')
        
        address_text = tk.Text(
            address_frame,
            font=('Arial', 11),
            relief='solid',
            bd=1,
            height=4
        )
        address_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        def save_customer():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            address = address_text.get('1.0', 'end-1c').strip()
            
            if not name:
                messagebox.showerror("Error", "Customer name is required!")
                return
            
            if not phone:
                messagebox.showerror("Error", "Phone number is required!")
                return
            
            try:
                existing_customers = self.sale_service.get_all_customers()
                for customer in existing_customers:
                    if customer[2] == phone:
                        messagebox.showerror("Error", f"Customer with phone number {phone} already exists!\nPlease use a different phone number.")
                        return
            except Exception as e:
                print(f"Error checking existing customers: {e}")
            
            try:
                self.sale_service.add_customer(name, phone, address)
                messagebox.showinfo("Success", "Customer added successfully!")
                self.load_customers()
                self.customer_var.set(name)
                self.customer_name_label.config(text=f"Customer: {name}")
                dialog.destroy()
                
            except Exception as e:
                if "UNIQUE constraint failed" in str(e):
                    messagebox.showerror("Error", f"Customer with phone number {phone} already exists!\nPlease use a different phone number.")
                else:
                    messagebox.showerror("Error", f"Failed to add customer: {str(e)}")
                    
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        
        save_btn = tk.Button(
            button_frame,
            text="💾 Save Customer",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=save_customer
        )
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 12),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=dialog.destroy
        )
        cancel_btn.pack(side=tk.RIGHT)
        
        name_entry.focus()
        dialog.bind('<Return>', lambda e: save_customer())
        
    def process_sale(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add products to cart before processing sale!")
            return
            
        try:
            subtotal = sum(item['total_price'] for item in self.cart)
            try:
                discount = float(self.discount_var.get() or 0)
            except:
                discount = 0
                
            total = max(0, subtotal - discount)
            
            # Validate stock - handle all measurement types including dozen and grams
            for item in self.cart:
                unit_type = item.get('unit_type', 'units')
                if item['quantity'] > item['current_stock']:
                    unit_display = self.format_quantity_display(1, unit_type).split(' ')[1]  # Get unit name
                    
                    # Special message for dozen
                    if unit_type == 'dozen':
                        available_pieces = item['current_stock'] * 12
                        messagebox.showerror(
                            "Stock Issue", 
                            f"Not enough stock for {item['company']} - {item['type']}.\n"
                            f"Available: {item['current_stock']} dozen ({available_pieces} pieces)\n"
                            f"Requested: {item['quantity']} dozen ({item['quantity'] * 12} pieces)"
                        )
                    else:
                        messagebox.showerror(
                            "Stock Issue", 
                            f"Not enough stock for {item['company']} - {item['type']}.\n"
                            f"Available: {item['current_stock']} {unit_display}\n"
                            f"Requested: {item['quantity']} {unit_display}"
                        )
                    return
                    
            # Get customer info
            customer_name = self.customer_var.get()
            customer_id = None
            
            # Find existing customer or create new one
            customers = self.sale_service.get_all_customers()
            for customer in customers:
                if customer[1] == customer_name:
                    customer_id = customer[0]
                    break

            # Handle customer creation for new customers
            if customer_id is None and customer_name != "Walk-in Customer":
                try:
                    customer_id = self.sale_service.add_customer(
                        name=customer_name,
                        phone="00000000000",
                        address="Not specified"
                    )
                except Exception as e:
                    print(f"Failed to create customer: {e}")
                    customer_id = 1

            # Use Walk-in Customer if no customer found/created
            if customer_id is None:
                customer_id = 1
                
            # Create sale
            sale_id = self.sale_service.create_sale(
                customer_id=customer_id,
                total_amount=subtotal,
                discount=discount,
                final_amount=total
            )
            
            # Add sale items and update stock
            for item in self.cart:
                # For dozen, we store the dozen quantity but need to convert to pieces for stock update
                quantity_to_deduct = item['quantity']
                
                self.sale_service.add_sale_item(
                    sale_id, 
                    item['product_id'], 
                    quantity_to_deduct,  # Store the original measurement quantity
                    item['unit_price'], 
                    item['total_price'],
                    purchase_price=item.get('purchase_price', 0)
                )
                self.sale_service.update_product_stock(item['product_id'], quantity_to_deduct)
                
            # Show success message and generate invoice
            messagebox.showinfo(
                "Sale Successful", 
                f"Sale processed successfully!\nSale ID: #{sale_id}\nTotal Amount: ₨{total:,.0f}"
            )
            self.generate_invoice(sale_id, customer_name, subtotal, discount, total)
            
            # Clear cart and reset
            self.cart = []
            self.discount_var.set("0")
            self.update_cart_display()
                
        except Exception as e:
            messagebox.showerror("Sale Failed", f"Failed to process sale: {str(e)}")
            print(f"Detailed error: {e}")

    def generate_invoice(self, sale_id, customer_name, subtotal, discount, total):
        invoice_window = tk.Toplevel(self.parent)
        invoice_window.title(f"Invoice # {sale_id}")
        invoice_window.geometry("500x700")
        invoice_window.configure(bg='white')
        
        invoice_frame = tk.Frame(invoice_window, bg='white')
        invoice_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            invoice_frame,
            text="AWAN HARDWARE",
            font=('Arial', 20, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(pady=(0, 5))
        
        tk.Label(
            invoice_frame,
            text="Hardware & Building Materials",
            font=('Arial', 12),
            fg='#7f8c8d',
            bg='white'
        ).pack(pady=(0, 10))
        
        details_frame = tk.Frame(invoice_frame, bg='#f8f9fa', relief='solid', bd=1)
        details_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            details_frame,
            text=f"Invoice #: {sale_id}",
            font=('Arial', 11, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w', padx=10, pady=5)
        
        tk.Label(
            details_frame,
            text=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            font=('Arial', 11),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w', padx=10, pady=(0, 5))
        
        tk.Label(
            details_frame,
            text=f"Customer: {customer_name}",
            font=('Arial', 11),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w', padx=10, pady=(0, 5))
        
        items_frame = tk.Frame(invoice_frame, bg='white')
        items_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ('Product', 'Details', 'Qty', 'Price', 'Total')
        invoice_tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=12)
        
        invoice_tree.heading('Product', text='Product')
        invoice_tree.heading('Details', text='Details')
        invoice_tree.heading('Qty', text='Qty')
        invoice_tree.heading('Price', text='Price')
        invoice_tree.heading('Total', text='Total')
        
        invoice_tree.column('Product', width=150)
        invoice_tree.column('Details', width=150)
        invoice_tree.column('Qty', width=60)
        invoice_tree.column('Price', width=80)
        invoice_tree.column('Total', width=80)
        
        for item in self.cart:
            product_text = f"{item['company']} - {item['type']}"
            details_text = self.get_cart_details_display(item)
            
            # Display quantity with unit in invoice
            unit_type = item.get('unit_type', 'units')
            quantity_display = self.format_quantity_display(item['quantity'], unit_type)
            
            invoice_tree.insert('', 'end', values=(
                product_text,
                details_text,
                quantity_display,
                f"₨{item['unit_price']:,.0f}",
                f"₨{item['total_price']:,.0f}"
            ))
            
        invoice_tree.pack(fill=tk.BOTH, expand=True)
        
        totals_frame = tk.Frame(invoice_frame, bg='white')
        totals_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            totals_frame,
            text=f"Subtotal: ₨{subtotal:,.0f}",
            font=('Arial', 12),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='e')
        
        tk.Label(
            totals_frame,
            text=f"Discount: -₨{discount:,.0f}",
            font=('Arial', 12),
            fg='#e74c3c',
            bg='white'
        ).pack(anchor='e')
        
        tk.Label(
            totals_frame,
            text=f"Total: ₨{total:,.0f}",
            font=('Arial', 14, 'bold'),
            fg='#27ae60',
            bg='white'
        ).pack(anchor='e', pady=5)
        
        tk.Label(
            totals_frame,
            text="Payment Method: Cash",
            font=('Arial', 11),
            fg='#7f8c8d',
            bg='white'
        ).pack(anchor='e')
        
        footer_frame = tk.Frame(invoice_frame, bg='#f8f9fa')
        footer_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            footer_frame,
            text="Thank you for your business!",
            font=('Arial', 11, 'italic'),
            fg='#7f8c8d',
            bg='#f8f9fa'
        ).pack(pady=10)
        
        print_btn = tk.Button(
            invoice_window,
            text="🖨️ Print Invoice",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat'
        )
        print_btn.pack(pady=10)