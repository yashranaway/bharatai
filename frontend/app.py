import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json

# Import custom modules
from ui.chat_interface import chat_interface
from models.inventory import InventoryManager
from models.orders import OrderManager
# Import AI modules
from ai.ai_service import AIService

# Set page config
st.set_page_config(
    page_title="Mini Bharat AI Store",
    page_icon="Store",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'inventory_manager' not in st.session_state:
    st.session_state.inventory_manager = InventoryManager()

if 'order_manager' not in st.session_state:
    st.session_state.order_manager = OrderManager()

# Initialize AI service
if 'ai_service' not in st.session_state:
    st.session_state.ai_service = AIService(
        st.session_state.inventory_manager,
        st.session_state.order_manager
    )

# Main app
def main():
    st.title("Mini Bharat AI Store")
    
    # Create sidebar for navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Go to",
            ["Chat Interface", "Inventory", "Analytics", "Orders", "AI Insights"]
        )
        
        st.divider()
        
        # Quick stats
        st.header("Quick Stats")
        st.metric("Total Products", len(st.session_state.inventory_manager.inventory_data))
        st.metric("Pending Orders", len(st.session_state.order_manager.get_pending_orders()))
        low_stock = st.session_state.inventory_manager.get_low_stock_items()
        st.metric("Low Stock Items", len(low_stock))
        
        st.divider()
        
        # About section
        st.header("About")
        st.markdown("""
        Mini Bharat AI Store is an Integrated Retail Intelligence System that connects Kirana stores, wholesalers, and logistics providers using AI and WhatsApp-like interfaces.
        
        **Features:**
        - Inventory management
        - Order tracking
        - Business analytics
        - AI-powered recommendations
        """)
    
    # Main content area
    if page == "Chat Interface":
        show_chat_interface()
    elif page == "Inventory":
        show_inventory()
    elif page == "Analytics":
        show_analytics()
    elif page == "Orders":
        show_orders()
    elif page == "AI Insights":
        show_ai_insights()

def show_chat_interface():
    st.header("Chat Interface")
    st.markdown("""
    Welcome to the Mini Bharat AI Store - Your intelligent Kirana store assistant!
    
    This WhatsApp-style interface helps you manage your Kirana store operations:
    - Check inventory levels
    - Place orders with suppliers
    - Track deliveries
    - Manage customer interactions
    """)
    
    chat_interface()

def show_inventory():
    st.header("Inventory Management")
    
    # Display current inventory
    inventory_df = st.session_state.inventory_manager.get_inventory_df()
    st.dataframe(inventory_df, use_container_width=True, hide_index=True)
    
    # Low stock alert
    low_stock_items = st.session_state.inventory_manager.get_low_stock_items()
    if low_stock_items:
        st.warning(f"You have {len(low_stock_items)} low stock items:")
        low_stock_df = pd.DataFrame(low_stock_items)
        st.dataframe(low_stock_df[['Name', 'Quantity']], use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Add new product form
    st.subheader("Add New Product")
    with st.form("add_product_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input("Product Name")
            category = st.selectbox("Category", ["Grains", "Pulses", "Oil", "Spices", "Snacks", "Beverages", "Other"])
        
        with col2:
            price = st.number_input("Price (₹)", min_value=0.0, step=0.5)
            quantity = st.number_input("Quantity", min_value=0, step=1)
        
        with col3:
            supplier = st.text_input("Supplier")
            description = st.text_area("Description", height=100)
        
        submitted = st.form_submit_button("Add Product")
        
        if submitted:
            if name and price > 0:
                st.session_state.inventory_manager.add_product(
                    name, category, price, quantity, supplier, description
                )
                st.success(f"Added {name} to inventory!")
                st.rerun()
            else:
                st.error("Please fill in all required fields correctly.")

def show_orders():
    st.header("Order Management")
    
    # Display current orders
    orders_df = st.session_state.order_manager.get_orders_df()
    st.dataframe(orders_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Add new order form
    st.subheader("Place New Order")
    with st.form("add_order_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer = st.text_input("Customer Name")
            items = st.text_area("Items (comma separated)", height=100)
        
        with col2:
            total = st.number_input("Total Amount (₹)", min_value=0.0, step=0.5)
            delivery_date = st.date_input("Expected Delivery Date")
        
        submitted = st.form_submit_button("Place Order")
        
        if submitted:
            if customer and items and total > 0:
                order_id = st.session_state.order_manager.add_order(customer, items, total)
                st.success(f"Order {order_id} placed successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields correctly.")

def show_analytics():
    st.header("Store Analytics")
    
    # Sample analytics data
    st.subheader("Sales Overview")
    sales_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Sales': [12000, 15000, 18000, 14000, 22000, 25000],
        'Orders': [120, 150, 180, 140, 220, 250]
    })
    
    st.line_chart(sales_data.set_index('Month'))
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Sales (This Month)", "₹25,000", "₹3,000")
    with col2:
        st.metric("Total Orders (This Month)", "250", "30")
    
    st.subheader("Top Selling Products")
    top_products = pd.DataFrame({
        'Product': ['Wheat Flour', 'Rice', 'Sugar', 'Oil', 'Spices'],
        'Quantity Sold': [500, 450, 300, 250, 200],
        'Revenue': [12500, 20250, 12000, 15000, 8000]
    })
    
    st.bar_chart(top_products.set_index('Product')['Quantity Sold'])

def show_ai_insights():
    st.header("AI Insights & Recommendations")
    
    # Get AI insights
    ai_insights = st.session_state.ai_service.get_ai_insights()
    
    # Product Recommendations
    st.subheader("Product Recommendations")
    trending_tab, seasonal_tab = st.tabs(["Trending Products", "Seasonal Trends"])
    
    with trending_tab:
        trending_products = ai_insights['trending_products']
        if trending_products:
            trending_df = pd.DataFrame(trending_products)
            st.dataframe(trending_df[['Name', 'Category', 'Price (₹)', 'Quantity']], 
                        use_container_width=True, hide_index=True)
        else:
            st.info("No trending products data available.")
    
    with seasonal_tab:
        seasonal_trends = ai_insights['seasonal_trends']
        if seasonal_trends:
            seasonal_data = []
            for product, data in seasonal_trends.items():
                if 'peak_month' in data:
                    seasonal_data.append({
                        'Product': product,
                        'Peak Month': data['peak_month'],
                        'Low Month': data['low_month']
                    })
            
            if seasonal_data:
                seasonal_df = pd.DataFrame(seasonal_data)
                st.dataframe(seasonal_df, use_container_width=True, hide_index=True)
            else:
                st.info("No seasonal trend data available.")
        else:
            st.info("No seasonal trend data available.")
    
    # Inventory Recommendations
    st.subheader("Inventory Recommendations")
    inventory_recs = ai_insights['inventory_recommendations']
    if inventory_recs:
        recs_df = pd.DataFrame(inventory_recs)
        st.dataframe(recs_df[['product_name', 'current_stock', 'forecasted_demand', 'to_order']], 
                    use_container_width=True, hide_index=True)
        
        # Highlight products that need restocking
        need_restock = [rec for rec in inventory_recs if rec['to_order'] > 0]
        if need_restock:
            st.warning(f"{len(need_restock)} products need restocking:")
            restock_df = pd.DataFrame(need_restock)
            st.dataframe(restock_df[['product_name', 'current_stock', 'to_order']], 
                        use_container_width=True, hide_index=True)
    else:
        st.info("No inventory recommendations available.")
    
    # Demand Forecasts
    st.subheader("Demand Forecasts (Next 7 Days)")
    forecasts = ai_insights['demand_forecasts']
    if forecasts:
        forecast_data = []
        for product, forecast in forecasts.items():
            forecast_data.append({
                'Product': product,
                'Total Forecast': round(sum(forecast)),
                'Avg Daily Demand': round(sum(forecast) / len(forecast), 2)
            })
        
        if forecast_data:
            forecast_df = pd.DataFrame(forecast_data)
            st.dataframe(forecast_df, use_container_width=True, hide_index=True)
        else:
            st.info("No demand forecast data available.")
    else:
        st.info("No demand forecast data available.")

if __name__ == "__main__":
    main()