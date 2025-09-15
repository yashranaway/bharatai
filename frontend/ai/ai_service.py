import pandas as pd
import numpy as np
from .recommendation_engine import RecommendationEngine
from .demand_forecasting import DemandForecaster

class AIService:
    def __init__(self, inventory_manager, order_manager):
        self.inventory_manager = inventory_manager
        self.order_manager = order_manager
        self.recommendation_engine = RecommendationEngine(inventory_manager, order_manager)
        self.demand_forecaster = DemandForecaster(order_manager, inventory_manager)
    
    def get_product_recommendations(self, customer_name, recommendation_type="collaborative", top_n=5):
        """
        Get product recommendations for a customer
        
        Args:
            customer_name (str): Name of the customer
            recommendation_type (str): Type of recommendation ("collaborative", "content", "popular")
            top_n (int): Number of recommendations to return
            
        Returns:
            list: List of recommended products
        """
        if recommendation_type == "collaborative":
            return self.recommendation_engine.get_collaborative_recommendations(customer_name, top_n)
        elif recommendation_type == "content":
            # For content-based, we need a product ID, so we'll use the first product from customer's history
            orders_df = self.order_manager.get_orders_df()
            customer_orders = orders_df[orders_df['Customer'] == customer_name]
            
            if not customer_orders.empty:
                # Get first product from customer's first order
                first_order = customer_orders.iloc[0]
                items = first_order['Items']
                item_name = items.split(', ')[0].split(' (')[0]
                
                inventory_df = self.inventory_manager.get_inventory_df()
                product = inventory_df[inventory_df['Name'].str.contains(item_name, case=False, na=False)]
                
                if not product.empty:
                    product_id = product.iloc[0]['ID']
                    return self.recommendation_engine.get_content_based_recommendations(product_id, top_n)
            
            # Fallback to popular products
            return self.recommendation_engine.get_popular_products(top_n)
        elif recommendation_type == "popular":
            return self.recommendation_engine.get_popular_products(top_n)
        else:
            return self.recommendation_engine.get_collaborative_recommendations(customer_name, top_n)
    
    def get_demand_forecast(self, product_name=None, days_ahead=7):
        """
        Get demand forecast for products
        
        Args:
            product_name (str, optional): Name of specific product. If None, forecasts for all products.
            days_ahead (int): Number of days to forecast ahead
            
        Returns:
            dict: Forecast data
        """
        if product_name:
            forecast = self.demand_forecaster.forecast_demand(product_name, days_ahead)
            return {
                'product_name': product_name,
                'forecast': forecast,
                'total_demand': sum(forecast)
            }
        else:
            # Forecast for all products
            inventory_df = self.inventory_manager.get_inventory_df()
            forecasts = {}
            
            for _, product in inventory_df.iterrows():
                product_name = product['Name']
                forecast = self.demand_forecaster.forecast_demand(product_name, days_ahead)
                forecasts[product_name] = {
                    'forecast': forecast,
                    'total_demand': sum(forecast)
                }
            
            return forecasts
    
    def get_inventory_recommendations(self, days_ahead=7):
        """
        Get inventory restocking recommendations
        
        Args:
            days_ahead (int): Number of days to plan for
            
        Returns:
            list: List of inventory recommendations
        """
        return self.demand_forecaster.get_inventory_recommendations(days_ahead)
    
    def get_seasonal_trends(self):
        """
        Get seasonal trend analysis
        
        Returns:
            dict: Seasonal trend data
        """
        return self.demand_forecaster.get_seasonal_trends()
    
    def get_ai_insights(self, customer_name=None):
        """
        Get comprehensive AI insights
        
        Args:
            customer_name (str, optional): Name of customer for personalized insights
            
        Returns:
            dict: Comprehensive AI insights
        """
        insights = {
            'trending_products': self.recommendation_engine.get_popular_products(5),
            'seasonal_trends': self.get_seasonal_trends(),
            'inventory_recommendations': self.get_inventory_recommendations(7)
        }
        
        if customer_name:
            insights['personalized_recommendations'] = {
                'collaborative': self.get_product_recommendations(customer_name, "collaborative", 3),
                'popular': self.get_product_recommendations(customer_name, "popular", 3)
            }
        
        # Add demand forecasts
        inventory_df = self.inventory_manager.get_inventory_df()
        forecasts = {}
        
        for _, product in inventory_df.head(3).iterrows():  # Limit to top 3 for performance
            product_name = product['Name']
            forecast = self.demand_forecaster.forecast_demand(product_name, 7)
            forecasts[product_name] = forecast
        
        insights['demand_forecasts'] = forecasts
        
        return insights

# Example usage
if __name__ == "__main__":
    # This would be used in the main application
    print("AI Service module loaded successfully")