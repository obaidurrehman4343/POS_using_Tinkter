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
        
        right_frame = tk.Frame(content_frame, bg='white', relief='solid', bd=1, width=400)
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
        
        self.customer_var = tk.StringVar(value="Walk-in Customer")
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
        cart_header = tk.Frame(parent, bg='#27ae60')
        cart_header.pack(fill=tk.X)
        
        tk.Label(
            cart_header,
            text="🛒 SHOPPING CART",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#27ae60'
        ).pack(pady=10)
        
        self.customer_info_frame = tk.Frame(parent, bg='#f8f9fa', relief='solid', bd=1)
        self.customer_info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.customer_name_label = tk.Label(
            self.customer_info_frame,
            text="Customer: Walk-in Customer",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        )
        self.customer_name_label.pack(anchor='w', pady=5)
        
        cart_items_frame = tk.Frame(parent, bg='white')
        cart_items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ('Product', 'Details', 'Qty', 'Price', 'Total', 'Actions')
        self.cart_tree = ttk.Treeview(
            cart_items_frame, 
            columns=columns, 
            show='headings',
            height=12
        )
        
        self.cart_tree.heading('Product', text='Product')
        self.cart_tree.heading('Details', text='Details')
        self.cart_tree.heading('Qty', text='Qty')
        self.cart_tree.heading('Price', text='Price')
        self.cart_tree.heading('Total', text='Total')
        self.cart_tree.heading('Actions', text='Actions')
        
        self.cart_tree.column('Product', width=120)
        self.cart_tree.column('Details', width=150)
        self.cart_tree.column('Qty', width=50)
        self.cart_tree.column('Price', width=80)
        self.cart_tree.column('Total', width=80)
        self.cart_tree.column('Actions', width=80)
        
        cart_scrollbar = ttk.Scrollbar(cart_items_frame, orient="vertical", command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=cart_scrollbar.set)
        
        self.cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cart_tree.bind('<Double-1>', self.edit_cart_item)
        
        cart_actions_frame = tk.Frame(parent, bg='white')
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
        
        totals_frame = tk.Frame(parent, bg='white')
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
        
        checkout_btn = tk.Button(
            parent,
            text="💳 PROCESS SALE",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.process_sale,
            cursor='hand2'
        )
        checkout_btn.pack(fill=tk.X, padx=10, pady=10, ipady=10)
    
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
            stock_text = f"Stock: {stock}"
            
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

    def add_to_cart(self, product_id, product):
        try:
            if len(product) < 14:
                return
                
            (pid, category_id, company, ptype, color,
             sale_price, purchase_price, packing, volume, current_stock,
             image_path, created_at, updated_at, category_name) = product[:14]
            
            for item in self.cart:
                if item['product_id'] == product_id:
                    if item['quantity'] < item['current_stock']:
                        item['quantity'] += 1
                        item['total_price'] = item['quantity'] * item['unit_price']
                        messagebox.showinfo("Cart Updated", f"Quantity increased for {item['company']} - {item['type']}")
                    else:
                        messagebox.showwarning("Stock Limit", f"Only {item['current_stock']} items available!")
                    self.update_cart_display()
                    return
                    
            if current_stock <= 0:
                messagebox.showwarning("Out of Stock", "This product is out of stock!")
                return
            
            cart_item = {
                'product_id': product_id,
                'company': company,
                'type': ptype,
                'color': color,
                'unit_price': float(sale_price),
                'quantity': 1,
                'total_price': float(sale_price),
                'current_stock': current_stock,
                'category_name': category_name,
                'packing': packing,
                'volume': volume
            }
            
            self.cart.append(cart_item)
            messagebox.showinfo("Added to Cart", f"Added {company} - {ptype} to cart!")
            self.update_cart_display()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add to cart: {str(e)}")

    def get_product_details_display(self, item):
        category = item['category_name'].lower() if item['category_name'] else ''
        
        if 'paint' in category:
            return f"Color: {item['color']}\nPacking: {item['packing']}"
        elif 'roof sheet' in category:
            return f"Color: {item['color']}\nSize: {item['volume']}"
        elif 'limination sheet' in category:
            return f"Color: {item['color']}\nSize: {item['volume']}"
        elif 'sanitary' in category:
            return f"Color: {item['color']}\nSize: {item['volume']}"
        else:
            return f"Color: {item['color']}\nPacking: {item['packing']}"

    def edit_cart_item(self, event=None):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select an item to edit!")
            return
            
        try:
            index = self.cart_tree.index(selected[0])
            if index < len(self.cart):
                item = self.cart[index]
                
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
                    text="Quantity:",
                    font=('Arial', 11, 'bold'),
                    fg='#2c3e50',
                    bg='white'
                ).pack(side=tk.LEFT)
                
                qty_var = tk.StringVar(value=str(item['quantity']))
                qty_entry = tk.Entry(
                    qty_frame,
                    textvariable=qty_var,
                    font=('Arial', 11),
                    width=10,
                    relief='solid',
                    bd=1
                )
                qty_entry.pack(side=tk.RIGHT)
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
                details_text.insert('1.0', self.get_product_details_display(item))
                
                def update_item():
                    try:
                        new_qty = int(qty_var.get())
                        new_price = float(price_var.get())
                        
                        if new_qty <= 0:
                            messagebox.showerror("Error", "Quantity must be greater than 0!")
                            return
                        if new_qty > item['current_stock']:
                            messagebox.showerror("Error", f"Only {item['current_stock']} items available!")
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
                
    def update_cart_display(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
            
        for item in self.cart:
            product_text = f"{item['company']} - {item['type']}"
            details_text = self.get_product_details_display(item)
            
            self.cart_tree.insert('', 'end', values=(
                product_text,
                details_text,
                item['quantity'],
                f"₨{item['unit_price']:,.0f}",
                f"₨{item['total_price']:,.0f}",
                "✏️ Edit"
            ))
            
        self.update_totals()
        
    def update_totals(self, event=None):
        subtotal = sum(item['total_price'] for item in self.cart)
        
        try:
            discount = float(self.discount_var.get() or 0)
        except:
            discount = 0
            
        total = max(0, subtotal - discount)
        
        self.subtotal_label.config(text=f"Subtotal: ₨{subtotal:,.0f}")
        self.total_label.config(text=f"Total: ₨{total:,.0f}")
        
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
            
            for item in self.cart:
                if item['quantity'] > item['current_stock']:
                    messagebox.showerror(
                        "Stock Issue", 
                        f"Not enough stock for {item['company']} - {item['type']}. Available: {item['current_stock']}"
                    )
                    return
                    
            customer_name = self.customer_var.get()
            customer_id = None
            
            customers = self.sale_service.get_all_customers()
            for customer in customers:
                if customer[1] == customer_name:
                    customer_id = customer[0]
                    break

            if customer_id is None and customer_name != "Walk-in Customer":
                try:
                    customer_id = self.sale_service.add_customer(
                        name=customer_name,
                        phone="00000000000",
                        address="Not specified"
                    )
                except Exception as e:
                    customer_id = 1

            if customer_id is None:
                customer_id = 1
                    
            sale_id = self.sale_service.create_sale(customer_id, subtotal, discount, total, 'cash')
            
            for item in self.cart:
                self.sale_service.add_sale_item(sale_id, item['product_id'], item['quantity'], item['unit_price'], item['total_price'])
                self.sale_service.update_product_stock(item['product_id'], item['quantity'])
                
            messagebox.showinfo("Sale Successful", f"Sale processed successfully!\nSale ID: #{sale_id}\nTotal Amount: ₨{total:,.0f}")
            self.generate_invoice(sale_id, customer_name, subtotal, discount, total)
            
            self.cart = []
            self.discount_var.set("0")
            self.update_cart_display()
                
        except Exception as e:
            messagebox.showerror("Sale Failed", f"Failed to process sale: {str(e)}")
            
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
            details_text = self.get_product_details_display(item)
            
            invoice_tree.insert('', 'end', values=(
                product_text,
                details_text,
                item['quantity'],
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