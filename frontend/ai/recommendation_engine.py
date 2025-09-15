import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import json

class RecommendationEngine:
    def __init__(self, inventory_manager, order_manager):
        self.inventory_manager = inventory_manager
        self.order_manager = order_manager
        self.product_similarity_matrix = None
        self.product_ids = None
        
    def _prepare_product_features(self):
        """Prepare product features for content-based filtering"""
        inventory_df = self.inventory_manager.get_inventory_df()
        
        # Combine category and description for feature extraction
        inventory_df['features'] = inventory_df['Category'] + ' ' + inventory_df['Description']
        
        return inventory_df
    
    def _compute_product_similarities(self):
        """Compute similarity matrix between products based on features"""
        inventory_df = self._prepare_product_features()
        
        # Use TF-IDF to vectorize product features
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(inventory_df['features'])
        
        # Compute cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        self.product_similarity_matrix = similarity_matrix
        self.product_ids = inventory_df['ID'].tolist()
        
        return similarity_matrix
    
    def get_content_based_recommendations(self, product_id, top_n=5):
        """Get content-based recommendations for a product"""
        if self.product_similarity_matrix is None:
            self._compute_product_similarities()
        
        # Find the index of the product
        try:
            idx = self.product_ids.index(product_id)
        except ValueError:
            return []
        
        # Get similarity scores for this product
        sim_scores = list(enumerate(self.product_similarity_matrix[idx]))
        
        # Sort products based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N similar products (excluding the product itself)
        sim_scores = sim_scores[1:top_n+1]
        
        # Get product indices
        product_indices = [i[0] for i in sim_scores]
        
        # Get product IDs
        recommended_ids = [self.product_ids[i] for i in product_indices]
        
        # Get product details
        inventory_df = self.inventory_manager.get_inventory_df()
        recommendations = inventory_df[inventory_df['ID'].isin(recommended_ids)].to_dict('records')
        
        return recommendations
    
    def get_collaborative_recommendations(self, customer_name, top_n=5):
        """Get collaborative filtering recommendations based on similar customers"""
        orders_df = self.order_manager.get_orders_df()
        
        # Create a customer-product matrix
        # First, we need to parse the items in each order
        customer_product_data = []
        
        for _, order in orders_df.iterrows():
            # Parse items string (simplified parsing)
            items = order['Items']
            # In a real implementation, you would parse this more robustly
            # For now, we'll just use the items as a string
            customer_product_data.append({
                'Customer': order['Customer'],
                'Items': items
            })
        
        # For collaborative filtering, we'll use a simple approach:
        # Find customers with similar order patterns
        
        # Get the target customer's orders
        target_customer_orders = orders_df[orders_df['Customer'] == customer_name]
        
        if target_customer_orders.empty:
            # If no history, return popular items
            return self.get_popular_products(top_n)
        
        # Find other customers
        other_customers = orders_df[orders_df['Customer'] != customer_name]['Customer'].unique()
        
        # Simple similarity based on item overlap
        similarities = []
        
        target_items = set()
        for _, order in target_customer_orders.iterrows():
            # Parse items (simplified)
            items = order['Items']
            target_items.update(items.split(','))
        
        for customer in other_customers:
            customer_orders = orders_df[orders_df['Customer'] == customer]
            customer_items = set()
            
            for _, order in customer_orders.iterrows():
                items = order['Items']
                customer_items.update(items.split(','))
            
            # Calculate Jaccard similarity
            intersection = len(target_items.intersection(customer_items))
            union = len(target_items.union(customer_items))
            
            if union > 0:
                similarity = intersection / union
                similarities.append((customer, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Get products from similar customers that the target customer hasn't bought
        recommended_products = []
        inventory_df = self.inventory_manager.get_inventory_df()
        
        for customer, similarity in similarities[:3]:  # Top 3 similar customers
            customer_orders = orders_df[orders_df['Customer'] == customer]
            
            for _, order in customer_orders.iterrows():
                items = order['Items']
                # Parse and recommend items (simplified)
                item_names = [item.split(' (')[0] for item in items.split(', ')]
                
                for item_name in item_names:
                    # Find product in inventory
                    product = inventory_df[inventory_df['Name'].str.contains(item_name, case=False, na=False)]
                    if not product.empty:
                        product_record = product.iloc[0].to_dict()
                        # Check if target customer already bought this
                        already_bought = False
                        for _, target_order in target_customer_orders.iterrows():
                            if item_name in target_order['Items']:
                                already_bought = True
                                break
                        
                        if not already_bought and product_record not in recommended_products:
                            recommended_products.append(product_record)
                            
                            if len(recommended_products) >= top_n:
                                break
                
                if len(recommended_products) >= top_n:
                    break
            
            if len(recommended_products) >= top_n:
                break
        
        return recommended_products[:top_n]
    
    def get_popular_products(self, top_n=5):
        """Get popular products based on order frequency"""
        orders_df = self.order_manager.get_orders_df()
        inventory_df = self.inventory_manager.get_inventory_df()
        
        # Count product occurrences
        product_counts = defaultdict(int)
        
        for _, order in orders_df.iterrows():
            items = order['Items']
            # Parse items (simplified)
            item_names = [item.split(' (')[0] for item in items.split(', ')]
            
            for item_name in item_names:
                product_counts[item_name] += 1
        
        # Sort by count
        sorted_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Get product details
        popular_products = []
        for product_name, count in sorted_products[:top_n]:
            product = inventory_df[inventory_df['Name'].str.contains(product_name, case=False, na=False)]
            if not product.empty:
                product_record = product.iloc[0].to_dict()
                product_record['order_count'] = count
                popular_products.append(product_record)
        
        return popular_products
    
    def get_trending_products(self, days=30, top_n=5):
        """Get trending products based on recent orders"""
        # In a real implementation with a proper database, we would filter by date
        # For now, we'll return popular products as a proxy
        return self.get_popular_products(top_n)

if __name__ == "__main__":
    # This is just for testing
    print("Recommendation Engine module loaded successfully")