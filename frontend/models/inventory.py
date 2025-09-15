import pandas as pd
from datetime import datetime

class InventoryManager:
    def __init__(self):
        # Initialize with default inventory data
        self.inventory_data = [
            {
                "ID": 1,
                "Name": "Wheat Flour",
                "Category": "Grains",
                "Price (₹)": 25.00,
                "Quantity": 100,
                "Supplier": "ABC Supplier",
                "Description": "High-quality wheat flour for daily cooking",
                "Last Updated": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "ID": 2,
                "Name": "Rice",
                "Category": "Grains",
                "Price (₹)": 45.00,
                "Quantity": 50,
                "Supplier": "XYZ Supplier",
                "Description": "Basmati rice, 1kg pack",
                "Last Updated": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "ID": 3,
                "Name": "Sugar",
                "Category": "Sweeteners",
                "Price (₹)": 40.00,
                "Quantity": 75,
                "Supplier": "PQR Supplier",
                "Description": "Refined sugar, 1kg pack",
                "Last Updated": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "ID": 4,
                "Name": "Cooking Oil",
                "Category": "Oil",
                "Price (₹)": 120.00,
                "Quantity": 30,
                "Supplier": "ABC Supplier",
                "Description": "Refined sunflower oil, 1L pack",
                "Last Updated": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "ID": 5,
                "Name": "Tea",
                "Category": "Beverages",
                "Price (₹)": 60.00,
                "Quantity": 40,
                "Supplier": "LMN Supplier",
                "Description": "Premium tea leaves, 250g pack",
                "Last Updated": datetime.now().strftime("%Y-%m-%d")
            }
        ]
    
    def get_inventory_df(self):
        """Return inventory as a pandas DataFrame"""
        return pd.DataFrame(self.inventory_data)
    
    def add_product(self, name, category, price, quantity, supplier, description):
        """Add a new product to inventory"""
        new_id = max([item["ID"] for item in self.inventory_data]) + 1 if self.inventory_data else 1
        
        new_product = {
            "ID": new_id,
            "Name": name,
            "Category": category,
            "Price (₹)": price,
            "Quantity": quantity,
            "Supplier": supplier,
            "Description": description,
            "Last Updated": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.inventory_data.append(new_product)
    
    def update_quantity(self, product_id, new_quantity):
        """Update the quantity of a product"""
        for item in self.inventory_data:
            if item["ID"] == product_id:
                item["Quantity"] = new_quantity
                item["Last Updated"] = datetime.now().strftime("%Y-%m-%d")
                return True
        return False
    
    def get_low_stock_items(self, threshold=10):
        """Get items with low stock"""
        low_stock = [item for item in self.inventory_data if item["Quantity"] <= threshold]
        return low_stock
