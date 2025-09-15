#!/usr/bin/env python3
"""
Test script to verify the Mini Bharat AI Store system
"""

import sys
import os
import requests
import time

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_backend_api():
    """Test backend API connectivity"""
    try:
        print("Testing backend API connectivity...")
        response = requests.get("http://localhost:3001/api/health", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "OK":
            print("✅ Backend API: RUNNING")
            return True
        else:
            print("❌ Backend API: NOT RESPONDING")
            return False
    except Exception as e:
        print(f"❌ Backend API: ERROR - {str(e)}")
        return False

def test_database_connection():
    """Test database connection through API"""
    try:
        print("Testing database connection...")
        response = requests.get("http://localhost:3001/api/inventory/products", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "data" in data:
                print(f"✅ Database Connection: CONNECTED ({data.get('count', 0)} products)")
                return True
            else:
                print("❌ Database Connection: ERROR - Invalid response")
                return False
        else:
            print("❌ Database Connection: ERROR - HTTP error")
            return False
    except Exception as e:
        print(f"❌ Database Connection: ERROR - {str(e)}")
        return False

def test_nlp_service():
    """Test NLP service functionality"""
    try:
        print("Testing NLP service...")
        # Import and test NLP service
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend'))
        from frontend.ai.nlp_service import nlp_service
        
        # Test intent classification
        test_sentence = "How much wheat flour do I have in stock?"
        intent = nlp_service.classify_intent(test_sentence)
        
        if intent == "inventory_query":
            print("✅ NLP Functionality: WORKING")
            return True
        else:
            print("❌ NLP Functionality: NOT WORKING")
            return False
    except Exception as e:
        print(f"❌ NLP Functionality: ERROR - {str(e)}")
        return False

def test_ai_service():
    """Test AI service functionality"""
    try:
        print("Testing AI service...")
        # Import and test AI service
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend'))
        from frontend.models.inventory import InventoryManager
        from frontend.models.orders import OrderManager
        from frontend.ai.ai_service import AIService
        
        # Initialize managers
        inventory_manager = InventoryManager()
        order_manager = OrderManager()
        
        # Initialize AI service
        ai_service = AIService(inventory_manager, order_manager)
        
        # Test AI insights
        insights = ai_service.get_ai_insights("Ramesh Kirana")
        
        if isinstance(insights, dict) and 'trending_products' in insights:
            print("✅ AI Service: WORKING")
            return True
        else:
            print("❌ AI Service: NOT WORKING")
            return False
    except Exception as e:
        print(f"❌ AI Service: ERROR - {str(e)}")
        return False

def main():
    """Main test function"""
    print("Mini Bharat AI Store - System Test")
    print("=" * 40)
    
    # Run all tests
    tests = [
        test_backend_api,
        test_database_connection,
        test_nlp_service,
        test_ai_service
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"Test failed with exception: {str(e)}")
            results.append(False)
        print()  # Add a blank line between tests
    
    print("=" * 40)
    if all(results):
        print("🎉 ALL SYSTEMS ARE WORKING CORRECTLY!")
        print("The Mini Bharat AI Store is ready for production use.")
    else:
        print("⚠️  SOME SYSTEMS NEED ATTENTION")
        print("Please check the error messages above")
    
    print("=" * 40)

if __name__ == "__main__":
    main()