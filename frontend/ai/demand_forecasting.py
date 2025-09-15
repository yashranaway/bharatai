import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
from datetime import datetime, timedelta
import json

class DemandForecaster:
    def __init__(self, order_manager, inventory_manager):
        self.order_manager = order_manager
        self.inventory_manager = inventory_manager
        self.models = {}
        
    def _prepare_time_series_data(self, product_name):
        """Prepare time series data for a specific product"""
        orders_df = self.order_manager.get_orders_df()
        
        # Parse orders to extract product quantities
        product_orders = []
        
        for _, order in orders_df.iterrows():
            order_date = datetime.strptime(order['Order Date'], '%Y-%m-%d')
            items = order['Items']
            
            # Parse items to find the product
            item_list = items.split(', ')
            for item in item_list:
                if product_name in item:
                    # Extract quantity (simplified)
                    quantity = 1  # Default quantity
                    if '(' in item and ')' in item:
                        try:
                            quantity_str = item.split('(')[1].split(')')[0]
                            if quantity_str.endswith('kg'):
                                quantity = float(quantity_str.replace('kg', ''))
                            elif quantity_str.endswith('L'):
                                quantity = float(quantity_str.replace('L', ''))
                            elif quantity_str.endswith('pack'):
                                quantity = 1
                            else:
                                quantity = float(quantity_str)
                        except:
                            quantity = 1
                    
                    product_orders.append({
                        'date': order_date,
                        'quantity': quantity
                    })
        
        # Convert to DataFrame and group by date
        if product_orders:
            df = pd.DataFrame(product_orders)
            df = df.groupby('date').agg({'quantity': 'sum'}).reset_index()
            df = df.sort_values('date')
            return df
        else:
            return pd.DataFrame(columns=['date', 'quantity'])
    
    def _create_features(self, df):
        """Create features for the forecasting model"""
        if df.empty:
            return pd.DataFrame()
        
        # Create time-based features
        df = df.copy()
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_month'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
        
        return df
    
    def train_forecast_model(self, product_name):
        """Train a forecasting model for a specific product"""
        # Prepare data
        ts_data = self._prepare_time_series_data(product_name)
        
        if ts_data.empty or len(ts_data) < 2:
            # Not enough data to train a model
            return None
        
        # Create features
        df = self._create_features(ts_data)
        
        if df.empty:
            return None
        
        # Prepare features and target
        feature_cols = ['day_of_week', 'day_of_month', 'month', 'days_since_start']
        X = df[feature_cols]
        y = df['quantity']
        
        # Create and train model
        # Using a polynomial regression for better fitting
        model = Pipeline([
            ('poly', PolynomialFeatures(degree=2)),
            ('linear', LinearRegression())
        ])
        
        model.fit(X, y)
        
        # Store model
        self.models[product_name] = {
            'model': model,
            'feature_cols': feature_cols,
            'start_date': df['date'].min(),
            'mae': mean_absolute_error(y, model.predict(X))
        }
        
        return model
    
    def forecast_demand(self, product_name, days_ahead=7):
        """Forecast demand for a product for the next N days"""
        # Check if we have a trained model
        if product_name not in self.models:
            # Try to train a model
            model = self.train_forecast_model(product_name)
            if model is None:
                # If we can't train a model, return average demand
                ts_data = self._prepare_time_series_data(product_name)
                if not ts_data.empty:
                    avg_demand = ts_data['quantity'].mean()
                    return [avg_demand] * days_ahead
                else:
                    # If no data, return a default value
                    inventory_df = self.inventory_manager.get_inventory_df()
                    product = inventory_df[inventory_df['Name'].str.contains(product_name, case=False, na=False)]
                    if not product.empty:
                        # Return a fraction of current stock as default forecast
                        current_stock = product.iloc[0]['Quantity']
                        return [current_stock * 0.1] * days_ahead
                    else:
                        return [10] * days_ahead  # Default value
        
        # Get the trained model
        model_info = self.models[product_name]
        model = model_info['model']
        feature_cols = model_info['feature_cols']
        start_date = model_info['start_date']
        
        # Generate future dates
        last_date = datetime.now()
        future_dates = [(last_date + timedelta(days=i)) for i in range(1, days_ahead + 1)]
        
        # Create features for future dates
        future_df = pd.DataFrame({'date': future_dates})
        future_df = self._create_features(future_df)
        
        # Make predictions
        X_future = future_df[feature_cols]
        predictions = model.predict(X_future)
        
        # Ensure non-negative predictions
        predictions = np.maximum(predictions, 0)
        
        return predictions.tolist()
    
    def get_inventory_recommendations(self, days_ahead=7):
        """Get inventory recommendations for all products"""
        inventory_df = self.inventory_manager.get_inventory_df()
        recommendations = []
        
        for _, product in inventory_df.iterrows():
            product_name = product['Name']
            current_stock = product['Quantity']
            
            # Forecast demand
            forecast = self.forecast_demand(product_name, days_ahead)
            total_forecast = sum(forecast)
            
            # Calculate recommended restocking
            recommended_stock = total_forecast * 1.2  # Add 20% buffer
            to_order = max(0, recommended_stock - current_stock)
            
            recommendations.append({
                'product_id': product['ID'],
                'product_name': product_name,
                'current_stock': current_stock,
                'forecasted_demand': total_forecast,
                'recommended_stock': recommended_stock,
                'to_order': to_order
            })
        
        return recommendations
    
    def get_seasonal_trends(self):
        """Analyze seasonal trends in product demand"""
        inventory_df = self.inventory_manager.get_inventory_df()
        seasonal_analysis = {}
        
        for _, product in inventory_df.iterrows():
            product_name = product['Name']
            ts_data = self._prepare_time_series_data(product_name)
            
            if not ts_data.empty and len(ts_data) > 2:
                # Group by month to see seasonal patterns
                ts_data['month'] = ts_data['date'].dt.month
                monthly_avg = ts_data.groupby('month')['quantity'].mean()
                
                seasonal_analysis[product_name] = {
                    'monthly_avg': monthly_avg.to_dict(),
                    'peak_month': monthly_avg.idxmax(),
                    'low_month': monthly_avg.idxmin()
                }
        
        return seasonal_analysis

if __name__ == "__main__":
    # This is just for testing
    print("Demand Forecaster module loaded successfully")