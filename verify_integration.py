#!/usr/bin/env python3
"""
Final verification script for Mini Bharat AI Store integration
"""

import requests
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_backend_api():
    """Verify backend API is running and accessible"""
    try:
        backend_base_url = os.getenv("BACKEND_URL", "http://localhost:3001/api")
        response = requests.get(f"{backend_base_url}/health")
        if response.status_code == 200 and response.json().get("status") == "OK":
            print("Backend API: RUNNING")
            return True
        else:
            print("Backend API: NOT RESPONDING")
            return False
    except Exception as e:
        print(f"Backend API: ERROR - {str(e)}")
        return False

def verify_database_connection():
    """Verify database connection through API"""
    try:
        backend_base_url = os.getenv("BACKEND_URL", "http://localhost:3001/api")
        response = requests.get(f"{backend_base_url}/inventory/products")
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "data" in data:
                print(f"Database Connection: CONNECTED ({data.get('count', 0)} products)")
                return True
            else:
                print("Database Connection: ERROR - Invalid response")
                return False
        else:
            print("Database Connection: ERROR - HTTP error")
            return False
    except Exception as e:
        print(f"Database Connection: ERROR - {str(e)}")
        return False

def verify_frontend_interface():
    """Verify frontend interface is accessible"""
    try:
        # Just check if the port is listening
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8501))
        sock.close()
        if result == 0:
            print("Frontend Interface: AVAILABLE")
            return True
        else:
            print("Frontend Interface: NOT AVAILABLE")
            return False
    except Exception as e:
        print(f"Frontend Interface: ERROR - {str(e)}")
        return False

def verify_nlp_functionality():
    """Verify NLP functionality"""
    try:
        # Import and test NLP service
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend'))
        from ai.nlp_service import nlp_service
        
        # Test intent classification
        test_sentence = "How much wheat flour do I have in stock?"
        intent = nlp_service.classify_intent(test_sentence)
        
        if intent == "inventory_query":
            print("NLP Functionality: WORKING")
            return True
        else:
            print("NLP Functionality: NOT WORKING")
            return False
    except Exception as e:
        print(f"NLP Functionality: ERROR - {str(e)}")
        return False

def verify_api_integration():
    """Verify API integration in NLP service"""
    try:
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend'))
        from ai.nlp_service import nlp_service
        
        # Test API integration
        response = nlp_service._get_all_products()
        if "Your inventory" in response or "inventory is empty" in response:
            print("API Integration: CONNECTED")
            return True
        else:
            print("API Integration: NOT CONNECTED")
            return False
    except Exception as e:
        print(f"API Integration: ERROR - {str(e)}")
        return False

def main():
    """Main verification function"""
    print("Mini Bharat AI Store - Integration Verification")
    print("=" * 50)
    
    # Run all verification checks
    checks = [
        verify_backend_api,
        verify_database_connection,
        verify_frontend_interface,
        verify_nlp_functionality,
        verify_api_integration
    ]
    
    results = []
    for check in checks:
        results.append(check())
    
    print("\n" + "=" * 50)
    if all(results):
        print("ALL SYSTEMS INTEGRATED SUCCESSFULLY!")
        print("Frontend and Backend are fully connected")
        print("NLP service is working with real-time data")
        print("Chatbot is ready for production use")
    else:
        print("SOME INTEGRATIONS NEED ATTENTION")
        print("Please check the error messages above")
    
    print("=" * 50)

if __name__ == "__main__":
    main()