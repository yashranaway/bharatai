import nltk
import requests
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re
import os

# Download required NLTK data (this would typically be done during setup)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class NLPService:
    def __init__(self):
        # Load NLTK stopwords
        self.stop_words = set(stopwords.words('english'))
        
        # Backend API URL
        self.backend_url = os.getenv('BACKEND_URL', 'http://localhost:3001/api')
        
        # Define intent patterns
        self.intent_patterns = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'inventory_query': ['stock', 'inventory', 'quantity', 'how many', 'available', 'in stock'],
            'order_request': ['order', 'purchase', 'buy', 'place order', 'want to buy'],
            'delivery_query': ['delivery', 'track', 'status', 'when', 'arrive'],
            'help_request': ['help', 'what can you do', '功能', 'how to']
        }
        
        # Define entity types we're interested in
        self.entity_types = {
            'PRODUCT': ['wheat', 'flour', 'rice', 'sugar', 'oil', 'tea', 'coffee', 'salt', 'spices'],
            'QUANTITY': ['kg', 'kilogram', 'gram', 'g', 'liter', 'l', 'pack', 'box', 'unit'],
            'NUMBER': [str(i) for i in range(1, 100)]
        }
    
    def process_text(self, text):
        """
        Process text with NLTK tokenization
        """
        try:
            tokens = word_tokenize(text.lower())
            return tokens
        except Exception as e:
            print(f"Error in tokenization: {e}")
            # Fallback to simple split if NLTK fails
            return text.lower().split()
    
    def extract_entities(self, text):
        """
        Extract entities from text using custom rules
        """
        tokens = self.process_text(text)
        
        # Extract custom entities
        custom_entities = self._extract_custom_entities(text)
        
        return {
            'custom_entities': custom_entities,
            'tokens': tokens
        }
    
    def _extract_custom_entities(self, text):
        """
        Extract custom entities using rule-based approach
        """
        entities = []
        text_lower = text.lower()
        
        # Extract product entities
        for product in self.entity_types['PRODUCT']:
            if product in text_lower:
                start = text_lower.find(product)
                entities.append({
                    'text': product,
                    'label': 'PRODUCT',
                    'start': start,
                    'end': start + len(product)
                })
        
        # Extract quantity entities
        quantity_pattern = r'(\d+)\s*(kg|kilogram|gram|g|liter|l|pack|box|unit)s?'
        matches = re.finditer(quantity_pattern, text_lower)
        for match in matches:
            entities.append({
                'text': match.group(0),
                'label': 'QUANTITY',
                'start': match.start(),
                'end': match.end()
            })
        
        return entities
    
    def classify_intent(self, text):
        """
        Classify the intent of the user input
        """
        text_lower = text.lower()
        
        # Check for exact matches first
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    return intent
        
        # Use NLTK for more sophisticated analysis
        tokens = self.process_text(text)
        
        # Extract keywords (excluding stopwords)
        keywords = [token.lower() for token in tokens 
                   if token.lower() not in self.stop_words and token.isalpha()]
        
        # Score intents based on keyword matches
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                # Check for partial matches
                if any(pattern_word in keywords for pattern_word in pattern.split()):
                    score += 1
            intent_scores[intent] = score
        
        # Return the intent with the highest score
        if intent_scores:
            return max(intent_scores, key=intent_scores.get)
        
        # Default intent
        return 'general_query'
    
    def generate_response(self, text):
        """
        Generate a response based on the intent and entities
        """
        intent = self.classify_intent(text)
        entities = self.extract_entities(text)
        
        # Generate response based on intent
        if intent == 'greeting':
            return "Hello! Welcome to Mini Bharat AI Store. How can I help you with your Kirana store operations today?"
        
        elif intent == 'inventory_query':
            product_entities = [ent for ent in entities['custom_entities'] if ent['label'] == 'PRODUCT']
            if product_entities:
                product = product_entities[0]['text']
                # Check actual inventory from backend
                stock_info = self._get_product_stock(product)
                return stock_info
            else:
                # Get all products from backend
                all_products = self._get_all_products()
                return all_products
        
        elif intent == 'order_request':
            product_entities = [ent for ent in entities['custom_entities'] if ent['label'] == 'PRODUCT']
            quantity_entities = [ent for ent in entities['custom_entities'] if ent['label'] == 'QUANTITY']
            
            if product_entities and quantity_entities:
                product = product_entities[0]['text']
                quantity = quantity_entities[0]['text']
                # Place order through backend
                order_result = self._place_order(product, quantity)
                return order_result
            elif product_entities:
                product = product_entities[0]['text']
                return f"How much {product} would you like to order?"
            else:
                return "What product would you like to order and how much?"
        
        elif intent == 'delivery_query':
            return "I can help you track your deliveries. Please provide your order ID or customer name."
        
        elif intent == 'help_request':
            return """I can help you with several Kirana store operations:
            1. Check inventory levels - Ask about stock quantities
            2. Place orders with suppliers - Help with purchasing
            3. View sales analytics - Get business insights
            4. Track deliveries - Monitor order status
            
            Try asking questions like:
            - "How much wheat flour do I have in stock?"
            - "Place an order for 10kg of rice"
            - "Show me my inventory"
            """
        
        else:
            return "I understand. Let me help you with that. For Kirana store operations, I recommend checking your stock levels first. What specific information do you need?"
    
    def _get_product_stock(self, product_name):
        """
        Get product stock information from backend API
        """
        try:
            # First, get all products to find the matching product
            response = requests.get(f"{self.backend_url}/inventory/products", timeout=5)
            if response.status_code == 200:
                products = response.json().get('data', [])
                # Find product that matches the name
                for product in products:
                    if product_name.lower() in product['name'].lower():
                        return f"{product['name']}: {product['quantity']} units available (₹{product['price']} each)"
                
                return f"I couldn't find {product_name} in your inventory. Would you like to add it?"
            else:
                return "Unable to fetch inventory information at the moment. Backend may be down."
        except requests.exceptions.ConnectionError:
            return "Cannot connect to backend server. Please make sure the API is running on port 3001."
        except requests.exceptions.Timeout:
            return "Request timed out. Please try again."
        except Exception as e:
            return f"Error fetching inventory: {str(e)}"
    
    def _get_all_products(self):
        """
        Get all products from backend API
        """
        try:
            response = requests.get(f"{self.backend_url}/inventory/products", timeout=5)
            if response.status_code == 200:
                products = response.json().get('data', [])
                if products:
                    product_list = "\n".join([f"• {p['name']}: {p['quantity']} units (₹{p['price']})" for p in products[:10]])
                    return f"Your inventory:\n{product_list}\n\nTotal items: {len(products)}"
                else:
                    return "Your inventory is empty. Would you like to add some products?"
            else:
                return "Unable to fetch inventory information at the moment. Backend may be down."
        except requests.exceptions.ConnectionError:
            return "Cannot connect to backend server. Please make sure the API is running on port 3001."
        except requests.exceptions.Timeout:
            return "Request timed out. Please try again."
        except Exception as e:
            return f"Error fetching inventory: {str(e)}"
    
    def _place_order(self, product_name, quantity):
        """
        Place an order through the backend API
        """
        try:
            # First, get all products to find the matching product
            response = requests.get(f"{self.backend_url}/inventory/products", timeout=5)
            if response.status_code == 200:
                products = response.json().get('data', [])
                # Find product that matches the name
                for product in products:
                    if product_name.lower() in product['name'].lower():
                        # Extract numeric quantity
                        quantity_num = re.findall(r'\d+', quantity)
                        if quantity_num:
                            quantity_num = int(quantity_num[0])
                            # Deduct stock from inventory
                            deduct_response = requests.post(
                                f"{self.backend_url}/inventory/products/{product['id']}/deduct-stock",
                                json={"quantity": quantity_num},
                                timeout=5
                            )
                            if deduct_response.status_code == 200:
                                return f"Successfully placed order for {quantity} of {product['name']}. Stock updated!"
                            else:
                                return f"Failed to place order for {product['name']}. Error: {deduct_response.json().get('message', 'Unknown error')}"
                        else:
                            return f"Invalid quantity specified for {product['name']}."
                
                return f"I couldn't find {product_name} in your inventory. Would you like to add it first?"
            else:
                return "Unable to fetch inventory information at the moment. Backend may be down."
        except requests.exceptions.ConnectionError:
            return "Cannot connect to backend server. Please make sure the API is running on port 3001."
        except requests.exceptions.Timeout:
            return "Request timed out. Please try again."
        except Exception as e:
            return f"Error placing order: {str(e)}"

# Initialize NLP service
nlp_service = NLPService()

if __name__ == "__main__":
    # Test the NLP service
    print("NLP Service initialized successfully")