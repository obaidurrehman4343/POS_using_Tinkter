from backend.database import Database

class CategoryService:
    def __init__(self):
        self.db = Database()
    
    def get_all_categories(self):
        """Get all categories"""
        return self.db.get_all_categories()
    
    def add_category(self, name, description=""):
        """Add category with validation"""
        if not name or not name.strip():
            raise ValueError("Category name cannot be empty")
        
        if len(name.strip()) < 2:
            raise ValueError("Category name must be at least 2 characters")
            
        # Check if category already exists
        categories = self.db.get_all_categories()
        for cat in categories:
            if cat[1].lower() == name.lower():
                raise ValueError(f"Category '{name}' already exists")
                
        return self.db.add_category(name, description)
    
    def get_category_by_name(self, name):
        """Get category ID by name"""
        categories = self.db.get_all_categories()
        for cat in categories:
            if cat[1] == name:
                return cat[0]  # Return category ID
        return None
    
    def get_category_by_id(self, category_id):
        """Get category by ID"""
        categories = self.db.get_all_categories()
        for cat in categories:
            if cat[0] == category_id:
                return cat
        return None