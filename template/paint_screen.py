# import tkinter as tk
# from tkinter import ttk, messagebox, simpledialog, filedialog
# from PIL import Image, ImageTk
# import os
# import shutil
# from pathlib import Path
# from datetime import datetime
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors
# import webbrowser
# from reportlab.pdfgen import canvas
# from reportlab.platypus import Table, TableStyle
# from reportlab.lib.units import inch
# import threading
# import time
# from controllers.paint_module import (
#     get_companies,
#     add_paint,
#     search_paints,
#     delete_paint,
#     get_paint_by_id,
#     update_paint,
# )
# from controllers.database import get_conn
# from controllers.config import BASE_DIR
# from controllers.sales import create_sale

# class CartItem:
#     def __init__(self, paint_data, quantity=1):
#         self.paint_data = paint_data
#         self.quantity = int(quantity)
#         self.unit_price = float(paint_data.get("sale_price", 0.0))
#         self.total_price = self.quantity * self.unit_price

# class BlinkingCardManager:
#     """Manage blinking cards for low stock items"""
#     def __init__(self):
#         self.blinking_cards = []
#         self.blink_thread = None
#         self.stop_blinking = False
       
#     def start_blinking(self):
#         if self.blink_thread is None:
#             self.stop_blinking = False
#             self.blink_thread = threading.Thread(target=self._blink_worker, daemon=True)
#             self.blink_thread.start()
   
#     def stop_all_blinking(self):
#         self.stop_blinking = True
#         for card_info in list(self.blinking_cards):
#             card, original_bg, _ = card_info
#             try:
#                 card.config(bg=original_bg)
#             except:
#                 pass
#         self.blinking_cards.clear()
   
#     def add_blinking_card(self, card, original_bg):
#         # avoid duplicates
#         if any(c[0] == card for c in self.blinking_cards):
#             return
#         self.blinking_cards.append([card, original_bg, False])
#         self.start_blinking()
   
#     def remove_blinking_card(self, card):
#         self.blinking_cards = [c for c in self.blinking_cards if c[0] != card]
   
#     def _blink_worker(self):
#         blink_colors = ["#fee2e2", "#fef2f2"]
       
#         while not self.stop_blinking and self.blinking_cards:
#             for card_info in list(self.blinking_cards):
#                 card, original_bg, blink_state = card_info
               
#                 try:
#                     if card.winfo_exists():
#                         new_color = blink_colors[1] if blink_state else blink_colors[0]
#                         # schedule on main thread
#                         try:
#                             card.after(0, lambda c=card, nc=new_color: c.config(bg=nc))
#                         except:
#                             try:
#                                 card.config(bg=new_color)
#                             except:
#                                 pass
#                         card_info[2] = not blink_state
#                     else:
#                         try:
#                             self.blinking_cards.remove(card_info)
#                         except:
#                             pass
#                 except:
#                     try:
#                         self.blinking_cards.remove(card_info)
#                     except:
#                         pass
#             time.sleep(0.8)
       
#         self.blink_thread = None

# class PaintModule(ttk.Frame):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.master = parent
#         self.configure(style="Main.TFrame")
#         self.colors = {
#             "primary": "#2563eb",
#             "secondary": "#64748b",
#             "success": "#10b981",
#             "warning": "#f59e0b",
#             "danger": "#ef4444",
#             "light": "#f8fafc",
#             "dark": "#1e293b",
#         }
#         self.cart = []  # list[CartItem]
#         self.blink_manager = BlinkingCardManager()
#         self.paint_images_dir = BASE_DIR / "assets" / "paint_images"
#         self.paint_images_dir.mkdir(exist_ok=True, parents=True)
#         self.selected_image_path = None
#         self.setup_styles()
#         self.build_modern_ui()
#         self.load_companies()

#     def __del__(self):
#         try:
#             self.blink_manager.stop_all_blinking()
#         except:
#             pass

#     def setup_styles(self):
#         style = ttk.Style()
#         try:
#             style.theme_use("clam")
#         except Exception:
#             pass
#         style.configure("Main.TFrame", background=self.colors["light"])
#         style.configure("Card.TFrame", background="white", relief="raised", borderwidth=1)
#         style.configure("Card.TLabel", background="white", font=("Segoe UI", 9))
#         style.configure("Header.TLabel", background=self.colors["primary"], foreground="white", font=("Segoe UI", 14, "bold"))

#     def build_modern_ui(self):
#         header = tk.Frame(self, bg=self.colors["primary"], height=80)
#         header.pack(fill="x", padx=10, pady=(10, 5))
#         header.pack_propagate(False)
        
#         back_btn = tk.Button(
#             header,
#             text="← Back to Dashboard",
#             bg=self.colors["secondary"],
#             fg="white",
#             font=("Segoe UI", 10),
#             relief="flat",
#             padx=15,
#             pady=8,
#             command=self.go_back,
#         )
#         back_btn.pack(side="left", padx=25, pady=20)
        
#         tk.Label(
#             header,
#             text="🎨 Paint Inventory Management",
#             bg=self.colors["primary"],
#             fg="white",
#             font=("Segoe UI", 18, "bold"),
#         ).pack(side="left", padx=25, pady=20)
        
#         btn_frame = tk.Frame(header, bg=self.colors["primary"])
#         btn_frame.pack(side="right", padx=20, pady=20)
        
#         self.cart_btn = tk.Button(
#             btn_frame,
#             text="🛒 Cart (0)",
#             bg=self.colors["warning"],
#             fg="white",
#             font=("Segoe UI", 10, "bold"),
#             relief="flat",
#             padx=15,
#             pady=8,
#             command=self.show_cart_summary,
#         )
#         self.cart_btn.pack(side="left", padx=5)
        
#         tk.Button(
#             btn_frame,
#             text="➕ Add New Paint",
#             bg=self.colors["success"],
#             fg="white",
#             font=("Segoe UI", 10, "bold"),
#             relief="flat",
#             padx=15,
#             pady=8,
#             command=self.add_paint_dialog,
#         ).pack(side="left", padx=5)
        
#         # ✅ REMOVED: Stock Report button from paint module
        
#         content = ttk.Frame(self, style="Main.TFrame")
#         content.pack(fill="both", expand=True, padx=10, pady=5)
#         self.build_modern_sidebar(content)
#         self.build_modern_gallery(content)

#     def build_modern_sidebar(self, parent):
#         sidebar = tk.Frame(parent, bg="white", width=280, relief="raised", borderwidth=1)
#         sidebar.pack(side="left", fill="y", padx=(0, 10))
#         sidebar.pack_propagate(False)
        
#         tk.Label(
#             sidebar,
#             text="🔍 Filters & Actions",
#             bg=self.colors["primary"],
#             fg="white",
#             font=("Segoe UI", 12, "bold"),
#             pady=10,
#         ).pack(fill="x")
        
#         filter_content = tk.Frame(sidebar, bg="white", padx=15, pady=15)
#         filter_content.pack(fill="both", expand=True)
        
#         tk.Label(filter_content, text="Company:", bg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
#         self.company_var = tk.StringVar()
#         self.company_combo = ttk.Combobox(filter_content, textvariable=self.company_var, width=20, font=("Segoe UI", 9), state="readonly")
#         self.company_combo.pack(fill="x", pady=(0, 15))
#         self.company_combo.bind("<<ComboboxSelected>>", lambda e: self.on_company_selected())
        
#         tk.Label(filter_content, text="Search (type/volume/color):", bg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
#         self.search_var = tk.StringVar()
#         search_entry = ttk.Entry(filter_content, textvariable=self.search_var, font=("Segoe UI", 9))
#         search_entry.pack(fill="x", pady=(0, 10))
#         search_entry.bind("<Return>", lambda e: self.on_search())
        
#         ttk.Button(filter_content, text="🔍 Search", command=self.on_search).pack(fill="x", pady=5)
#         ttk.Button(filter_content, text="🔄 Refresh", command=self.load_paints).pack(fill="x", pady=5)
#         ttk.Button(filter_content, text="➕ Add Company", command=self.add_company).pack(fill="x", pady=5)
        
#         cart_frame = tk.Frame(filter_content, bg="white", pady=10)
#         cart_frame.pack(fill="x", pady=(20, 0))
       
#         tk.Label(cart_frame, text="🛒 Cart Actions", bg="white", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
       
#         ttk.Button(cart_frame, text="🧹 Clear Cart", command=self.clear_cart).pack(fill="x", pady=3)

#     def build_modern_gallery(self, parent):
#         main_area = tk.Frame(parent, bg=self.colors["light"])
#         main_area.pack(side="left", fill="both", expand=True)
        
#         gallery_header = tk.Frame(main_area, bg="white", height=50)
#         gallery_header.pack(fill="x", pady=(0, 10))
#         gallery_header.pack_propagate(False)
        
#         tk.Label(
#             gallery_header,
#             text="Available Paints",
#             bg="white",
#             font=("Segoe UI", 12, "bold"),
#             fg=self.colors["dark"],
#         ).pack(side="left", padx=20, pady=15)
        
#         self.canvas = tk.Canvas(main_area, bg=self.colors["light"], highlightthickness=0)
#         self.scrollbar = ttk.Scrollbar(main_area, orient="vertical", command=self.canvas.yview)
#         self.canvas.configure(yscrollcommand=self.scrollbar.set)
#         self.scrollbar.pack(side="right", fill="y")
#         self.canvas.pack(side="left", fill="both", expand=True)
        
#         self.card_frame = tk.Frame(self.canvas, bg=self.colors["light"])
#         self.canvas_window = self.canvas.create_window((0, 0), window=self.card_frame, anchor="nw")
#         self.card_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

#     # ---------------- Cart System Methods ----------------
#     def add_to_cart(self, paint_id):
#         """
#         Add paint to cart. No popup here — simply increment by 1 if exists, else add quantity=1.
#         """
#         try:
#             paint = get_paint_by_id(paint_id)
#             if not paint:
#                 messagebox.showerror("Error", "Paint not found!")
#                 return
#             if not isinstance(paint, dict):
#                 paint = dict(paint)
#             current_stock = int(paint.get("stock", 0))
#             if current_stock <= 0:
#                 messagebox.showerror("Error", "This paint is out of stock!")
#                 return

#             # find existing cart item
#             for item in self.cart:
#                 if item.paint_data.get("id") == paint.get("id"):
#                     if item.quantity + 1 > current_stock:
#                         messagebox.showerror("Error", f"Cannot add more than available stock ({current_stock})")
#                         return
#                     item.quantity += 1
#                     item.total_price = item.quantity * item.unit_price
#                     break
#             else:
#                 self.cart.append(CartItem(paint, 1))

#             self.update_cart_display()
#             # Show success message
#             messagebox.showinfo("Success", "Item added to cart!")
            
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to add to cart: {e}")

#     def remove_from_cart(self, index):
#         if 0 <= index < len(self.cart):
#             self.cart.pop(index)
#             self.update_cart_display()

#     def update_cart_quantity(self, index, new_quantity):
#         if 0 <= index < len(self.cart):
#             item = self.cart[index]
#             max_stock = int(item.paint_data.get("stock", 0))
#             if new_quantity <= max_stock:
#                 item.quantity = new_quantity
#                 item.total_price = new_quantity * item.unit_price
#                 self.update_cart_display()
#             else:
#                 messagebox.showerror("Error", f"Cannot exceed available stock of {max_stock}")

#     def clear_cart(self):
#         if self.cart:
#             result = messagebox.askyesno("Clear Cart", "Are you sure you want to clear the cart?")
#             if result:
#                 self.cart.clear()
#                 self.update_cart_display()
#                 messagebox.showinfo("Success", "Cart cleared!")

#     def update_cart_display(self):
#         total_items = sum(int(item.quantity) for item in self.cart)
#         self.cart_btn.config(text=f"🛒 Cart ({total_items})")

#     # ---------------- Checkout / Cart Summary ----------------
#     def show_cart_summary(self):
#         """Open a professional checkout window where user can edit qty/price and create invoice."""
#         if not self.cart:
#             messagebox.showinfo("Cart", "Your cart is empty!")
#             return

#         checkout = tk.Toplevel(self)
#         checkout.title("🧾 Checkout — Sale Details")
#         checkout.geometry("900x640")
#         checkout.configure(bg="#f9fafb")
#         checkout.transient(self)
#         checkout.grab_set()

#         # header
#         header = tk.Frame(checkout, bg=self.colors["primary"], height=60)
#         header.pack(fill="x")
#         header.pack_propagate(False)
#         tk.Label(header, text="🧾 Checkout — Sale Details", bg=self.colors["primary"], fg="white",
#                  font=("Segoe UI", 16, "bold")).pack(padx=16, pady=10)

#         body = tk.Frame(checkout, bg="white", padx=16, pady=12, relief="flat")
#         body.pack(fill="both", expand=True, padx=12, pady=12)

#         # Customer details area
#         cust_frame = tk.LabelFrame(body, text="Customer Details", bg="white", font=("Segoe UI", 11, "bold"))
#         cust_frame.pack(fill="x", pady=(0, 8))

#         tk.Label(cust_frame, text="Name:", bg="white", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="e", padx=8, pady=8)
#         customer_name_var = tk.StringVar()
#         customer_name_entry = ttk.Entry(cust_frame, textvariable=customer_name_var, width=30)
#         customer_name_entry.grid(row=0, column=1, sticky="w", padx=8, pady=8)

#         tk.Label(cust_frame, text="Phone:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=2, sticky="e", padx=8)
#         phone_var = tk.StringVar()
#         ttk.Entry(cust_frame, textvariable=phone_var, width=20).grid(row=0, column=3, sticky="w", padx=8)

#         tk.Label(cust_frame, text="Address:", bg="white", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="ne", padx=8, pady=6)
#         address_var = tk.StringVar()
#         ttk.Entry(cust_frame, textvariable=address_var, width=70).grid(row=1, column=1, columnspan=3, sticky="w", padx=8, pady=6)

#         # Cart table area (scrollable)
#         table_outer = tk.Frame(body, bg="white")
#         table_outer.pack(fill="both", expand=True, pady=(6, 10))

#         canvas = tk.Canvas(table_outer, bg="white", highlightthickness=0)
#         vsb = ttk.Scrollbar(table_outer, orient="vertical", command=canvas.yview)
#         scroll_frame = tk.Frame(canvas, bg="white")
#         scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
#         canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
#         canvas.configure(yscrollcommand=vsb.set)
#         canvas.pack(side="left", fill="both", expand=True)
#         vsb.pack(side="right", fill="y")

#         # table header
#         header_row = tk.Frame(scroll_frame, bg=self.colors["primary"], pady=8)
#         header_row.pack(fill="x", padx=6, pady=(0, 6))
#         headers = [("Product", 40), ("Unit Price", 12), ("Quantity", 12), ("Line Total", 16), ("Action", 10)]
#         for i, (h, w) in enumerate(headers):
#             tk.Label(header_row, text=h, bg=self.colors["primary"], fg="white", font=("Segoe UI", 10, "bold"),
#                      width=w, anchor="w").grid(row=0, column=i, padx=4)

#         # keep references for controls so we can read on Confirm
#         controls = []  # list of (CartItem, unit_var, qty_var, line_var, max_stock, line_label_widget)

#         for idx, cart_item in enumerate(self.cart):
#             row_bg = "#f8fafc" if idx % 2 == 0 else "white"
#             row_frame = tk.Frame(scroll_frame, bg=row_bg, pady=8, padx=6, relief="flat")
#             row_frame.pack(fill="x", padx=2, pady=2)

#             paint = cart_item.paint_data
#             product_text = f"{paint.get('company','')} - {paint.get('color','')}\n{paint.get('type','')} ({paint.get('volume','')})"
#             tk.Label(row_frame, text=product_text, bg=row_bg, font=("Segoe UI", 9), justify="left", anchor="w", width=40).grid(row=0, column=0, sticky="w")

#             unit_var = tk.StringVar(value=f"{cart_item.unit_price:.2f}")
#             unit_entry = ttk.Entry(row_frame, textvariable=unit_var, width=12, justify="right")
#             unit_entry.grid(row=0, column=1, padx=6)

#             max_stock = int(paint.get("stock", 0)) if paint.get("stock", None) is not None else 999999
#             qty_var = tk.StringVar(value=str(cart_item.quantity))
#             qty_spin = tk.Spinbox(row_frame, from_=1, to=max_stock if max_stock>0 else 999999, textvariable=qty_var, width=8)
#             qty_spin.grid(row=0, column=2, padx=6)

#             # line total label
#             initial_line = (float(unit_var.get()) if unit_var.get() else 0.0) * (int(qty_var.get()) if qty_var.get() else 0)
#             line_var = tk.StringVar(value=f"{initial_line:.2f} PKR")
#             line_lbl = tk.Label(row_frame, textvariable=line_var, bg=row_bg, font=("Segoe UI", 10, "bold"), fg=self.colors["primary"], width=16)
#             line_lbl.grid(row=0, column=3, padx=6)

#             def make_recalc(uvar, qvar, lvar):
#                 def recalc(*_):
#                     try:
#                         up = float(uvar.get())
#                     except:
#                         up = 0.0
#                     try:
#                         q = int(qvar.get())
#                     except:
#                         q = 0
#                     lvar.set(f"{(up * q):.2f} PKR")
#                 return recalc

#             recalc = make_recalc(unit_var, qty_var, line_var)
#             # traces / bindings
#             try:
#                 unit_var.trace_add("write", lambda *a, r=recalc: r())
#             except:
#                 unit_var.trace("w", lambda *a, r=recalc: r())
#             try:
#                 qty_var.trace_add("write", lambda *a, r=recalc: r())
#             except:
#                 qty_var.trace("w", lambda *a, r=recalc: r())

#             # Remove button
#             rm_btn = tk.Button(row_frame, text="🗑️ Remove", bg=self.colors["danger"], fg="white", relief="flat",
#                                command=lambda i=idx: (self.cart.pop(i), self.update_cart_display(), checkout.destroy(), self.show_cart_summary()))
#             rm_btn.grid(row=0, column=4, padx=6)

#             controls.append((cart_item, unit_var, qty_var, line_var, max_stock, line_lbl))

#             # column weights
#             for c in range(5):
#                 row_frame.columnconfigure(c, weight=1)

#         # Grand total area
#         footer = tk.Frame(checkout, bg="#f9fafb")
#         footer.pack(fill="x", padx=12, pady=(0,12), side="bottom")

#         grand_label = tk.Label(footer, text="Grand Total:", bg="#f9fafb", font=("Segoe UI", 14, "bold"), fg=self.colors["dark"])
#         grand_label.pack(side="left", padx=(6,12))
#         grand_var = tk.StringVar(value="0.00 PKR")
#         grand_amt_label = tk.Label(footer, textvariable=grand_var, bg="#f9fafb", font=("Segoe UI", 14, "bold"), fg=self.colors["success"])
#         grand_amt_label.pack(side="left")

#         # live grand total computation
#         def compute_grand():
#             total = 0.0
#             for _, uvar, qvar, _, _, _ in controls:
#                 try:
#                     up = float(uvar.get())
#                 except:
#                     up = 0.0
#                 try:
#                     q = int(qvar.get())
#                 except:
#                     q = 0
#                 total += up * q
#             return total

#         def refresh_grand():
#             grand_var.set(f"{compute_grand():.2f} PKR")
#             checkout.after(200, refresh_grand)

#         refresh_grand()

#         # bottom action buttons
#         actions = tk.Frame(footer, bg="#f9fafb")
#         actions.pack(side="right")

#         def on_confirm_generate():
#             name = customer_name_var.get().strip()
#             if not name:
#                 messagebox.showerror("Validation", "Please enter customer name.")
#                 return

#             # validate and apply updates back to cart items
#             for (cart_item, uvar, qvar, lvar, max_stock, _) in controls:
#                 try:
#                     new_unit = float(uvar.get())
#                 except:
#                     messagebox.showerror("Validation", "Invalid unit price entered.")
#                     return
#                 try:
#                     new_qty = int(qvar.get())
#                 except:
#                     messagebox.showerror("Validation", "Invalid quantity entered.")
#                     return
#                 if new_qty < 1:
#                     messagebox.showerror("Validation", "Quantity must be at least 1.")
#                     return
#                 if max_stock > 0 and new_qty > max_stock:
#                     messagebox.showerror("Stock Error", f"Requested quantity ({new_qty}) exceeds available stock ({max_stock}).")
#                     return
#                 cart_item.unit_price = new_unit
#                 cart_item.quantity = new_qty
#                 cart_item.total_price = new_unit * new_qty

#             # call your existing process_sale_and_generate_invoice with customer and cart
#             try:
#                 checkout.grab_release()
#                 checkout.destroy()
#                 self.process_sale_and_generate_invoice(name, phone_var.get(), address_var.get())
#             except Exception as e:
#                 messagebox.showerror("Error", f"Failed to process sale: {e}")

#         tk.Button(actions, text="🧾 Confirm & Generate Invoice", bg=self.colors["success"], fg="white",
#                   font=("Segoe UI", 11, "bold"), relief="flat", padx=12, pady=8, command=on_confirm_generate).pack(side="right", padx=8)

#         tk.Button(actions, text="🛒 Continue Shopping", bg=self.colors["secondary"], fg="white",
#                   font=("Segoe UI", 10), relief="flat", padx=12, pady=8, command=lambda: (checkout.destroy())).pack(side="right", padx=8)

#         # autofocus name
#         customer_name_entry.focus_set()

#     # ---------------- Sales Processing ----------------
#     def process_sale_and_generate_invoice(self, customer_name, phone, address):
#         try:
#             sale_records = []
           
#             for item in self.cart:
#                 paint = item.paint_data
#                 current_stock = self.get_current_stock(paint["id"])
               
#                 if item.quantity > current_stock:
#                     messagebox.showerror(
#                         "Stock Error",
#                         f"Insufficient stock for {paint['company']} {paint['color']}!\nAvailable: {current_stock}, Requested: {item.quantity}"
#                     )
#                     return
                   
#                 sale_id = create_sale(
#                     paint["id"],
#                     item.quantity,
#                     item.unit_price,
#                     item.total_price,
#                     "Cash",
#                     customer_name,
#                 )
               
#                 if sale_id:
#                     sale_records.append({
#                         "sale_id": sale_id,
#                         "paint_data": paint,
#                         "quantity": item.quantity,
#                         "unit_price": item.unit_price,
#                         "total_price": item.total_price
#                     })
#                 else:
#                     messagebox.showerror("Error", f"Failed to process sale for {paint['company']}!")
#                     return
                   
#             invoice_path = self.generate_professional_invoice(sale_records, customer_name, phone, address)
#             self.cart.clear()
#             self.update_cart_display()
#             self.load_paints()
           
#             messagebox.showinfo(
#                 "Success!",
#                 f"Invoice generated successfully!\n\nTotal Sales: {len(sale_records)} items\nTotal Amount: {sum(item['total_price'] for item in sale_records):.0f} PKR\n\nInvoice saved at: {invoice_path}"
#             )
           
#             try:
#                 os.startfile(invoice_path)
#             except:
#                 webbrowser.open(invoice_path)
               
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to process sale: {str(e)}")

#     def generate_professional_invoice(self, sale_records, customer_name, phone, address):
#         invoice_id = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
#         pdf_dir = Path("invoices")
#         pdf_dir.mkdir(exist_ok=True)
#         pdf_path = pdf_dir / f"invoice_{invoice_id}.pdf"

#         c = canvas.Canvas(str(pdf_path), pagesize=A4)
#         width, height = A4
#         y = height - 50

#         # -------------------------
#         # HEADER — COMPANY INFO
#         # -------------------------
#         c.setFont("Helvetica-Bold", 18)
#         c.setFillColor(colors.HexColor("#222222"))
#         c.drawCentredString(width / 2, y, "AWAN HARDWARE & SANITARY STORE")
#         y -= 20

#         c.setFont("Helvetica", 11)
#         c.setFillColor(colors.HexColor("#333333"))
#         c.drawCentredString(width / 2, y, "ARJA, KASHMIR")
#         y -= 25

#         c.setStrokeColor(colors.lightgrey)
#         c.line(50, y, width - 50, y)
#         y -= 30

#         # -------------------------
#         # INVOICE INFO LINE
#         # -------------------------
#         c.setFont("Helvetica-Bold", 11)
#         c.setFillColor(colors.black)
#         c.drawString(50, y, "Invoice No:")
#         c.setFont("Helvetica", 10)
#         c.drawString(125, y, invoice_id)

#         c.setFont("Helvetica-Bold", 11)
#         c.drawRightString(width - 150, y, "Date:")
#         c.setFont("Helvetica", 10)
#         c.drawRightString(width - 80, y, datetime.now().strftime("%d/%m/%Y"))

#         y -= 30

#         # -------------------------
#         # CUSTOMER INFO BLOCK
#         # -------------------------
#         c.setFont("Helvetica-Bold", 11)
#         c.drawString(50, y, "Name:")
#         c.setFont("Helvetica", 10)
#         c.drawString(95, y, customer_name or "N/A")

#         c.setFont("Helvetica-Bold", 11)
#         c.drawRightString(width - 150, y, "Phone:")
#         c.setFont("Helvetica", 10)
#         c.drawRightString(width - 80, y, phone or "N/A")

#         y -= 20
#         c.setFont("Helvetica-Bold", 11)
#         c.drawString(50, y, "Address:")
#         c.setFont("Helvetica", 10)
#         c.drawString(115, y, address or "N/A")

#         y -= 40

#         # -------------------------
#         # CENTERED TITLE — INVOICE
#         # -------------------------
#         c.setFont("Helvetica-Bold", 22)
#         c.setFillColor(colors.HexColor("#2563eb"))
#         c.drawCentredString(width / 2, y, "INVOICE")
#         y -= 40

#         # -------------------------
#         # TABLE HEADER — COMPANY | TYPE | UNIT PRICE | QTY | TOTAL
#         # -------------------------
#         header_height = 22
#         c.setFillColor(colors.HexColor("#2563eb"))
#         c.rect(50, y - header_height + 6, width - 100, header_height, fill=True, stroke=False)
#         c.setFillColor(colors.white)
#         c.setFont("Helvetica-Bold", 10)

#         c.drawString(60, y - 8, "COMPANY")
#         c.drawString(width - 370, y - 8, "TYPE")
#         c.drawString(width - 270, y - 8, "UNIT PRICE")
#         c.drawString(width - 170, y - 8, "QTY")
#         c.drawRightString(width - 60, y - 8, "TOTAL")

#         y -= 30
#         c.setFillColor(colors.black)
#         c.setFont("Helvetica", 10)

#         # -------------------------
#         # TABLE BODY
#         # -------------------------
#         total_amount = 0
#         for i, sale in enumerate(sale_records):
#             paint = sale["paint_data"]
#             company = paint.get("company", "N/A")
#             paint_type = paint.get("type", "N/A")
#             unit_price = sale.get("unit_price", 0)
#             qty = int(sale.get("quantity", 1))
#             total_price = sale.get("total_price", unit_price * qty)

#             # Alternate row color
#             if i % 2 == 1:
#                 c.setFillColor(colors.HexColor("#f9f9f9"))
#                 c.rect(50, y - 2, width - 100, 18, fill=True, stroke=False)
#                 c.setFillColor(colors.black)

#             if y < 110:
#                 c.showPage()
#                 width, height = A4
#                 y = height - 80
#                 c.setFont("Helvetica", 10)

#             c.drawString(60, y, company)
#             c.drawString(width - 370, y, paint_type)
#             c.drawString(width - 270, y, f"{unit_price:.0f} PKR")
#             c.drawString(width - 170, y, str(qty))
#             c.drawRightString(width - 60, y, f"{total_price:.0f} PKR")

#             total_amount += total_price
#             y -= 20

#         # -------------------------
#         # SUMMARY
#         # -------------------------
#         y -= 10
#         c.setStrokeColor(colors.lightgrey)
#         c.line(50, y, width - 50, y)
#         y -= 20

#         c.setFont("Helvetica-Bold", 10)
#         c.drawString(60, y, "SUBTOTAL")
#         c.drawRightString(width - 60, y, f"{total_amount:.0f} PKR")
#         y -= 25

#         beige_height = 28
#         c.setFillColor(colors.HexColor("#f5f2ea"))
#         c.rect(50, y - beige_height + 8, width - 100, beige_height, fill=True, stroke=False)
#         c.setFillColor(colors.black)
#         c.setFont("Helvetica-Bold", 12)
#         c.drawString(60, y - 4, "TOTAL")
#         c.drawRightString(width - 60, y - 4, f"{total_amount:.0f} PKR")
#         y -= (beige_height + 20)

#         # -------------------------
#         # FOOTER
#         # -------------------------
#         footer_y = 60
#         c.setFont("Helvetica", 10)
#         c.setFillColor(colors.HexColor("#333333"))
#         c.drawCentredString(width / 2, footer_y + 20,
#                             "Shahid Shabir: 03465932701 | Abid Shabbir: 03475632606")

#         c.setFont("Helvetica-Oblique", 10)
#         c.setFillColor(colors.grey)
#         c.drawCentredString(width / 2, footer_y, "Thank you for your business!")

#         c.showPage()
#         c.save()
#         return pdf_path

#     def get_current_stock(self, paint_id):
#         conn = get_conn()
#         cur = conn.cursor()
#         cur.execute("SELECT stock FROM paints WHERE id = ?", (paint_id,))
#         result = cur.fetchone()
#         conn.close()
#         return result["stock"] if result else 0

#     def setup_card_blinking(self, card, stock_float, original_bg):
#         if stock_float < 5 and stock_float > 0:
#             self.blink_manager.add_blinking_card(card, original_bg)
#         else:
#             self.blink_manager.remove_blinking_card(card)

#     def _get_columns_str(self):
#         try:
#             conn = get_conn()
#             cur = conn.cursor()
#             cur.execute("PRAGMA table_info(paints)")
#             cols = cur.fetchall()
#             conn.close()
#             if not cols:
#                 return ""
#             names = [c[1] for c in cols]
#             wanted = []
#             for n in ("id", "company", "color", "type", "volume", "purchase_price", "sale_price", "stock", "image_path"):
#                 if n in names:
#                     wanted.append(n)
#             return ", ".join(wanted)
#         except Exception as e:
#             print("Error getting columns:", e)
#             return ""

#     def load_companies(self):
#         companies = get_companies()
#         if not companies:
#             companies = ["Newlac", "Berger", "Brighto"]
#         self.company_combo["values"] = companies
#         self.company_var.set("")

#     def add_company(self):
#         new_company = simpledialog.askstring("Add Company", "Enter new company name:", parent=self)
#         if not new_company:
#             return
#         new_company = new_company.strip().title()
#         current = list(self.company_combo["values"])
#         if new_company not in current:
#             current.append(new_company)
#             current.sort()
#             self.company_combo["values"] = current
#             self.company_var.set(new_company)
#             messagebox.showinfo("Success", f"{new_company} added successfully!", parent=self)
#             self.on_company_selected()
#         else:
#             messagebox.showinfo("Info", f"{new_company} already exists.", parent=self)

#     def on_company_selected(self):
#         self.load_paints()

#     def load_paints(self):
#         self.blink_manager.stop_all_blinking()
#         for w in self.card_frame.winfo_children():
#             w.destroy()
            
#         company = (self.company_var.get() or "").strip()
#         if not company:
#             no_select_frame = tk.Frame(self.card_frame, bg=self.colors["light"], pady=50)
#             no_select_frame.pack(expand=True, fill="both")
#             tk.Label(
#                 no_select_frame,
#                 text="🏢 Please select a company to view paints",
#                 bg=self.colors["light"],
#                 fg=self.colors["secondary"],
#                 font=("Segoe UI", 13, "bold"),
#             ).pack(pady=(0, 8))
#             tk.Label(
#                 no_select_frame,
#                 text="Choose a company from the dropdown on the left.",
#                 bg=self.colors["light"],
#                 fg=self.colors["secondary"],
#                 font=("Segoe UI", 11),
#             ).pack()
#             return
            
#         columns_str = self._get_columns_str()
#         if not columns_str:
#             tk.Label(self.card_frame, text="Database not ready or no columns.", bg=self.colors["light"]).pack()
#             return
            
#         conn = get_conn()
#         cur = conn.cursor()
#         try:
#             query = f"SELECT {columns_str} FROM paints WHERE company=? ORDER BY type, color"
#             cur.execute(query, (company,))
#             rows = cur.fetchall()
#         except Exception as e:
#             print("DB error:", e)
#             rows = []
#         finally:
#             conn.close()
            
#         if not rows:
#             no_data_frame = tk.Frame(self.card_frame, bg=self.colors["light"], pady=50)
#             no_data_frame.pack(expand=True, fill="both")
#             tk.Label(no_data_frame, text=f"🎨 No paints found for {company}", bg=self.colors["light"], fg=self.colors["secondary"], font=("Segoe UI", 14, "bold")).pack(pady=(0, 10))
#             tk.Label(no_data_frame, text="Add new paints to get started", bg=self.colors["light"], fg=self.colors["secondary"], font=("Segoe UI", 11)).pack()
#             return
            
#         per_row = 5
#         row, col = 0, 0
#         for paint in rows:
#             card = self.create_modern_card(self.card_frame, paint)
#             card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
#             col += 1
#             if col >= per_row:
#                 col = 0
#                 row += 1
                
#         for i in range(per_row):
#             self.card_frame.columnconfigure(i, weight=1)

#     def on_search(self):
#         company = (self.company_var.get() or "").strip()
#         query = (self.search_var.get() or "").strip()
#         if not query:
#             self.load_paints()
#             return
            
#         rows = search_paints(company, query)
#         for w in self.card_frame.winfo_children():
#             w.destroy()
            
#         if not rows:
#             no_data_frame = tk.Frame(self.card_frame, bg=self.colors["light"], pady=50)
#             no_data_frame.pack(expand=True, fill="both")
#             tk.Label(no_data_frame, text="No paints found matching your search.", bg=self.colors["light"], fg=self.colors["secondary"], font=("Segoe UI", 13)).pack(pady=(0, 10))
#             return
            
#         per_row = 5
#         row, col = 0, 0
#         for paint in rows:
#             card = self.create_modern_card(self.card_frame, paint)
#             card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
#             col += 1
#             if col >= per_row:
#                 col = 0
#                 row += 1
                
#         for i in range(per_row):
#             self.card_frame.columnconfigure(i, weight=1)

#     def format_number(self, value):
#         try:
#             num = float(value)
#             return int(num) if num.is_integer() else num
#         except (ValueError, TypeError):
#             return value

#     def create_modern_card(self, parent, paint):
#         if isinstance(paint, dict) or hasattr(paint, "keys"):
#             def g(k, fallback=""):
#                 return paint[k] if k in paint.keys() else fallback
#             pid = g("id", "")
#             company = g("company", "")
#             color = g("color", "")
#             ptype = g("type", "")
#             volume = g("volume", "")
#             purchase = g("purchase_price", 0)
#             sale = g("sale_price", 0)
#             stock = g("stock", 0)
#             image_path = g("image_path", None)
#         else:
#             tup = list(paint)
#             while len(tup) < 8:
#                 tup.append(None)
#             pid = tup[0]
#             company = tup[1]
#             color = tup[2]
#             ptype = tup[3]
#             volume = tup[4]
#             purchase = tup[5]
#             sale = tup[6]
#             stock = tup[7]
#             image_path = tup[8] if len(tup) > 8 else None
            
#         try:
#             stock_float = float(stock) if stock is not None else 0.0
#         except Exception:
#             stock_float = 0.0
            
#         card_bg = "white"
#         if stock_float < 5:
#             card_bg = "#fef2f2"
            
#         card = tk.Frame(parent, bg=card_bg, relief="raised", borderwidth=1, padx=12, pady=10)
#         original_bg = card_bg
        
#         preview_frame = tk.Frame(card, bg=card_bg)
#         preview_frame.pack(pady=(0, 8))
        
#         if image_path and os.path.exists(image_path):
#             try:
#                 img = Image.open(image_path)
#                 img = img.resize((80, 80), Image.Resampling.LANCZOS)
#                 photo = ImageTk.PhotoImage(img)
#                 img_label = tk.Label(preview_frame, image=photo, bg=card_bg)
#                 img_label.image = photo
#                 img_label.pack()
#             except Exception:
#                 self.create_color_box(preview_frame, color, card_bg)
#         else:
#             self.create_color_box(preview_frame, color, card_bg)
            
#         details_frame = tk.Frame(card, bg=card_bg)
#         details_frame.pack(fill="x")
        
#         tk.Label(details_frame, text=f"Company: {company}", bg=card_bg, font=("Segoe UI", 10, "bold"), fg=self.colors["dark"]).pack(anchor="w")
#         tk.Label(details_frame, text=f"Color: {color}", bg=card_bg, font=("Segoe UI", 10), fg=self.colors["secondary"]).pack(anchor="w", pady=(3, 0))
#         tk.Label(details_frame, text=f"Type: {ptype}", bg=card_bg, font=("Segoe UI", 10), fg=self.colors["secondary"]).pack(anchor="w", pady=(3, 0))
#         tk.Label(details_frame, text=f"Volume: {volume}", bg=card_bg, font=("Segoe UI", 10), fg=self.colors["secondary"]).pack(anchor="w", pady=(3, 0))
        
#         price_frame = tk.Frame(details_frame, bg=card_bg)
#         price_frame.pack(fill="x", pady=(8, 0))
#         tk.Label(price_frame, text=f"Purchase: {self.format_number(purchase)} PKR", bg=card_bg, font=("Segoe UI", 9), fg=self.colors["secondary"]).pack(anchor="w")
#         tk.Label(price_frame, text=f"Sale: {self.format_number(sale)} PKR", bg=card_bg, font=("Segoe UI", 10, "bold"), fg=self.colors["primary"]).pack(anchor="w")
        
#         stock_frame = tk.Frame(details_frame, bg=card_bg)
#         stock_frame.pack(fill="x", pady=(8, 0))
#         stock_color = self.colors["success"] if stock_float > 10 else self.colors["warning"] if stock_float > 5 else self.colors["danger"]
#         tk.Label(stock_frame, text=f"Stock: {self.format_number(stock)}", bg=card_bg, font=("Segoe UI", 10, "bold"), fg=stock_color).pack(side="left")
        
#         action_frame = tk.Frame(details_frame, bg=card_bg)
#         action_frame.pack(fill="x", pady=(10, 0))
        
#         add_to_cart_btn = tk.Button(
#             action_frame,
#             text="🛒 Add to Cart",
#             bg=self.colors["success"],
#             fg="white",
#             relief="flat",
#             padx=8,
#             pady=3,
#             command=lambda pid=pid: self.add_to_cart(pid)
#         )
#         add_to_cart_btn.pack(side="left", padx=(0, 6))
       
#         if stock_float <= 0:
#             add_to_cart_btn.config(state="disabled", bg=self.colors["secondary"])
            
#         tk.Button(action_frame, text="Edit", bg=self.colors["primary"], fg="white", relief="flat", padx=10, pady=3, command=lambda pid=pid: self.edit_paint(pid)).pack(side="left", padx=(0, 6))
#         tk.Button(action_frame, text="Delete", bg=self.colors["danger"], fg="white", relief="flat", padx=10, pady=3, command=lambda pid=pid: self.delete_single_paint(pid)).pack(side="left")
        
#         self.setup_card_blinking(card, stock_float, original_bg)
#         return card

#     def create_color_box(self, parent, color, bg_color):
#         if color and isinstance(color, str) and color.startswith("#") and len(color) == 7:
#             c = color
#         else:
#             c = "#CCCCCC"
#         color_frame = tk.Frame(parent, bg=c, width=60, height=60, relief="solid", borderwidth=2)
#         color_frame.pack()
#         color_frame.pack_propagate(False)

#     def delete_single_paint(self, paint_id):
#         result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this paint?\nThis action cannot be undone.", icon="warning")
#         if result:
#             success = delete_paint(paint_id)
#             if success:
#                 messagebox.showinfo("Success", "Paint deleted successfully!")
#                 self.load_paints()
#             else:
#                 messagebox.showerror("Error", "Failed to delete paint!")

#     def edit_paint(self, paint_id):
#         paint = get_paint_by_id(paint_id)
#         if not paint:
#             messagebox.showerror("Error", "Paint not found!")
#             return
            
#         form = tk.Toplevel(self)
#         form.title("Edit Paint")
#         form.geometry("450x580")
#         form.configure(bg="white")
#         form.transient(self)
#         form.grab_set()
        
#         ttk.Label(form, text="✏️ Edit Paint Details", font=("Segoe UI", 13, "bold")).pack(pady=(15, 10))
#         container = ttk.Frame(form)
#         container.pack(padx=20, pady=5, fill="x")
        
#         # Define categories for dropdown
#         categories = ["paint", "sanitary", "hardware", "chadran", "limination"]
        
#         fields = ["Company", "Color", "Type", "Volume", "Purchase Price", "Sale Price", "Stock", "Category"]
#         entries = {}
#         for idx, name in enumerate(fields):
#             ttk.Label(container, text=f"{name}:", font=("Segoe UI", 10)).grid(row=idx, column=0, sticky="e", pady=6, padx=5)
            
#             if name == "Category":
#                 # Create dropdown for category
#                 category_var = tk.StringVar(value=paint.get("category", "paint"))
#                 category_combo = ttk.Combobox(container, textvariable=category_var, values=categories, state="readonly", width=22)
#                 category_combo.grid(row=idx, column=1, sticky="w", pady=6)
#                 entries[name] = category_combo
#             else:
#                 ent = ttk.Entry(container, width=25)
#                 ent.grid(row=idx, column=1, sticky="w", pady=6)
                
#                 if name == "Company":
#                     ent.insert(0, paint["company"])
#                 elif name == "Color":
#                     ent.insert(0, paint["color"])
#                 elif name == "Type":
#                     ent.insert(0, paint["type"])
#                 elif name == "Volume":
#                     ent.insert(0, paint["volume"])
#                 elif name == "Purchase Price":
#                     purchase_value = paint["purchase_price"]
#                     ent.insert(0, str(int(purchase_value)) if purchase_value and float(purchase_value).is_integer() else str(purchase_value))
#                 elif name == "Sale Price":
#                     sale_value = paint["sale_price"]
#                     ent.insert(0, str(int(sale_value)) if sale_value and float(sale_value).is_integer() else str(sale_value))
#                 elif name == "Stock":
#                     stock_value = paint["stock"]
#                     ent.insert(0, str(int(stock_value)) if stock_value and float(stock_value).is_integer() else str(stock_value))
#                 entries[name] = ent
                
#         # ... rest of the image handling code remains the same ...
        
#         def save():
#             company = entries["Company"].get().strip()
#             color = entries["Color"].get().strip()
#             ptype = entries["Type"].get().strip()
#             volume = entries["Volume"].get().strip()
#             purchase = self.safe_float(entries["Purchase Price"].get())
#             sale = self.safe_float(entries["Sale Price"].get())
#             stock = self.safe_float(entries["Stock"].get())
#             category = entries["Category"].get().strip()
            
#             if not company or not color or not ptype or not volume:
#                 messagebox.showerror("Validation", "All fields are required.", parent=form)
#                 return
                
#             image_path = self.selected_image_path if isinstance(self.selected_image_path, (str, os.PathLike)) else None
#             update_paint(paint_id, company, color, ptype, volume, purchase, sale, stock, category, image_path)
#             self.load_paints()
#             messagebox.showinfo("Success", "Paint updated successfully!", parent=form)
#             form.destroy()
            
#         ttk.Button(form, text="💾 Update", command=save).pack(pady=(10, 4))
#         ttk.Button(form, text="❌ Cancel", command=form.destroy).pack()
#         entries["Company"].focus_set()

#     def choose_image(self, parent):
#         file_path = filedialog.askopenfilename(parent=parent, title="Select Product Image", filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")])
#         if file_path:
#             filename = Path(file_path).name
#             destination = self.paint_images_dir / filename
#             try:
#                 shutil.copy2(file_path, destination)
#                 self.selected_image_path = str(destination)
#                 try:
#                     self.image_label.config(text=f"📁 {filename}")
#                 except Exception:
#                     pass
#             except Exception as e:
#                 messagebox.showerror("Error", f"Failed to copy image: {e}")

#     def safe_float(self, value):
#         try:
#             return float(value) if value else 0.0
#         except (ValueError, TypeError):
#             return 0.0

#     def add_paint_dialog(self):
#         form = tk.Toplevel(self)
#         form.title("Add New Paint")
#         form.geometry("450x580")  # Increased height for category
#         form.configure(bg="white")
#         form.transient(self)
#         form.grab_set()
        
#         ttk.Label(form, text="🖌️ Add Paint Details", font=("Segoe UI", 13, "bold")).pack(pady=(15, 10))
#         container = ttk.Frame(form)
#         container.pack(padx=20, pady=5, fill="x")
        
#         # Define categories for dropdown
#         categories = ["paint", "sanitary", "hardware", "chadran", "limination"]
        
#         fields = ["Company", "Color", "Type", "Volume", "Purchase Price", "Sale Price", "Stock", "Category"]
#         entries = {}
#         for idx, name in enumerate(fields):
#             ttk.Label(container, text=f"{name}:", font=("Segoe UI", 10)).grid(row=idx, column=0, sticky="e", pady=6, padx=5)
            
#             if name == "Category":
#                 # Create dropdown for category
#                 category_var = tk.StringVar(value="paint")
#                 category_combo = ttk.Combobox(container, textvariable=category_var, values=categories, state="readonly", width=22)
#                 category_combo.grid(row=idx, column=1, sticky="w", pady=6)
#                 entries[name] = category_combo
#             else:
#                 ent = ttk.Entry(container, width=25)
#                 ent.grid(row=idx, column=1, sticky="w", pady=6)
                
#                 if name == "Company":
#                     company_value = self.company_var.get()
#                     ent.insert(0, company_value)
#                 entries[name] = ent
                
#         self.selected_image_path = None
#         ttk.Label(container, text="Product Image:", font=("Segoe UI", 10)).grid(row=8, column=0, sticky="e", pady=6, padx=5)
#         image_frame = ttk.Frame(container)
#         image_frame.grid(row=8, column=1, columnspan=2, sticky="w", pady=6)
#         ttk.Button(image_frame, text="📷 Choose Image", command=lambda: self.choose_image(form)).pack(side="left", padx=(0, 10))
#         self.image_label = ttk.Label(image_frame, text="No image selected", foreground="gray")
#         self.image_label.pack(side="left")
        
#         def save():
#             company = entries["Company"].get().strip()
#             color = entries["Color"].get().strip()
#             ptype = entries["Type"].get().strip()
#             volume = entries["Volume"].get().strip()
#             purchase = self.safe_float(entries["Purchase Price"].get())
#             sale = self.safe_float(entries["Sale Price"].get())
#             stock = self.safe_float(entries["Stock"].get())
#             category = entries["Category"].get().strip()
            
#             if not company or not color or not ptype or not volume:
#                 messagebox.showerror("Validation", "Company, Color, Type and Volume are required.", parent=form)
#                 return
            
#             # Use the updated add_paint function with category
#             add_paint(company, color, ptype, volume, purchase, sale, stock, category, self.selected_image_path)
#             self.load_paints()
#             messagebox.showinfo("Success", "Paint added successfully!", parent=form)
#             form.destroy()
            
#         ttk.Button(form, text="💾 Save", command=save).pack(pady=(10, 4))
#         ttk.Button(form, text="❌ Cancel", command=form.destroy).pack()
#         entries["Company"].focus_set()

#     def go_back(self):
#         try:
#             from template.dashboard import Dashboard
#         except Exception as e:
#             messagebox.showerror("Error", f"Cannot go back: {e}")
#             return
            
#         root = self.master
#         while not isinstance(root, tk.Tk) and hasattr(root, "master"):
#             root = getattr(root, "master", root)
#             if root is None:
#                 break
                
#         if root is None:
#             messagebox.showerror("Error", "Root window not found.")
#             return
            
#         for w in list(root.winfo_children()):
#             w.destroy()
#         Dashboard(root)