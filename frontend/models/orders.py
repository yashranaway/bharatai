import pandas as pd
from datetime import datetime, timedelta

class OrderManager:
    def __init__(self):
        # Initialize with default orders data
        self.orders_data = [
            {
                "Order ID": "ORD001",
                "Customer": "Ramesh Kirana",
                "Items": "Wheat Flour (5kg), Rice (2kg)",
                "Total (₹)": 215.00,
                "Status": "Delivered",
                "Order Date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
                "Delivery Date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            },
            {
                "Order ID": "ORD002",
                "Customer": "Suresh Store",
                "Items": "Sugar (3kg), Tea (1 pack)",
                "Total (₹)": 180.00,
                "Status": "In Transit",
                "Order Date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
                "Delivery Date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
            },
            {
                "Order ID": "ORD003",
                "Customer": "Mahesh Retail",
                "Items": "Cooking Oil (2L)",
                "Total (₹)": 240.00,
                "Status": "Processing",
                "Order Date": datetime.now().strftime("%Y-%m-%d"),
                "Delivery Date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
            }
        ]
    
    def get_orders_df(self):
        """Return orders as a pandas DataFrame"""
        return pd.DataFrame(self.orders_data)
    
    def add_order(self, customer, items, total):
        """Add a new order"""
        new_id = f"ORD{len(self.orders_data) + 1:03d}"
        
        new_order = {
            "Order ID": new_id,
            "Customer": customer,
            "Items": items,
            "Total (₹)": total,
            "Status": "Processing",
            "Order Date": datetime.now().strftime("%Y-%m-%d"),
            "Delivery Date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        }
        
        self.orders_data.append(new_order)
        return new_id
    
    def update_order_status(self, order_id, status):
        """Update order status"""
        for order in self.orders_data:
            if order["Order ID"] == order_id:
                order["Status"] = status
                return True
        return False
    
    def get_pending_orders(self):
        """Get orders that are not yet delivered"""
        pending = [order for order in self.orders_data if order["Status"] != "Delivered"]
        return pending
