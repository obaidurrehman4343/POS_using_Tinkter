
from backend.database import Database

class ProductService:
    def __init__(self):
        self.db = Database()
    
    def get_all_categories(self):
        """Get all categories"""
        return self.db.get_all_categories()
    
    def add_category(self, name, description=""):
        """Add category with validation"""
        if not name or not name.strip():
            raise ValueError("Category name is required")
        
        if len(name) < 2:
            raise ValueError("Category name must be at least 2 characters")
            
        return self.db.add_category(name, description)
    
    def get_products_by_category(self, category_id):
        """Get products by category"""
        return self.db.get_products_by_category(category_id)
    
    def add_product(self, product_data):
        """Add product with validation"""
        # Required fields validation
        required_fields = ['category_id', 'company', 'type', 'color']
        for field in required_fields:
            if not product_data.get(field):
                raise ValueError(f"{field} is required")
        
        # Price validation
        if product_data.get('sale_price', 0) <= 0:
            raise ValueError("Sale price must be greater than 0")
        
        if product_data.get('purchase_price', 0) < 0:
            raise ValueError("Purchase price cannot be negative")
            
        # Stock validation
        if product_data.get('current_stock', 0) < 0:
            raise ValueError("Stock quantity cannot be negative")
            
        return self.db.add_product(product_data)
    
    def update_product(self, product_id, product_data):
        """Update product with validation"""
        # Same validation as add_product
        required_fields = ['category_id', 'company', 'type', 'color']
        for field in required_fields:
            if not product_data.get(field):
                raise ValueError(f"{field} is required")
        
        if product_data.get('sale_price', 0) <= 0:
            raise ValueError("Sale price must be greater than 0")
            
        return self.db.update_product(product_id, product_data)
    
    def delete_product(self, product_id):
        """Delete product"""
        return self.db.delete_product(product_id)
    
    def get_all_products(self):
        """Get all products"""
        return self.db.get_all_products()
    
    def get_product_by_id(self, product_id):
        """Get product by ID"""
        products = self.db.get_all_products()
        for product in products:
            if product[0] == product_id:
                return product
        return None