# Mini Bharat AI Store - WhatsApp Interface

A Python-based WhatsApp-style interface for the Mini Bharat AI Store, built with Streamlit.

## Features

- WhatsApp-style chat interface for Kirana store operations
- Inventory management system
- Order placement and tracking
- Business analytics dashboard
- AI-powered recommendations and demand forecasting
- Natural Language Processing for intelligent chat responses
- Left-to-right sidebar navigation layout
- Responsive UI with mobile-friendly design

## Installation

1. Navigate to the whatsapp_interface directory:
   ```bash
   cd whatsapp_interface
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Download the spaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

Run the application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Project Structure

```
whatsapp_interface/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/                 # Data storage (if needed)
├── models/               # Data models
│   ├── inventory.py      # Inventory management
│   └── orders.py         # Order management
├── ui/                   # User interface components
│   └── chat_interface.py # Chat interface implementation
├── ai/                   # AI services
│   ├── ai_service.py     # Main AI service
│   ├── recommendation_engine.py # Product recommendations
│   ├── demand_forecasting.py # Demand forecasting
│   └── nlp_service.py    # Natural Language Processing
└── utils/                # Utility functions
```

## Functionality

### Chat Interface
- WhatsApp-style messaging for store operations
- Natural language processing for intelligent responses
- Intent classification and entity recognition
- Context-aware responses
- Fixed input area at the bottom

### Inventory Management
- View current stock levels
- Add new products to inventory
- Track low stock items
- Category-based organization

### Order Management
- Place orders with suppliers
- Track order status
- View order history
- Delivery date tracking

### Analytics
- Sales overview dashboard
- Top selling products
- Business metrics
- Trend visualization

### AI Insights
- **Product Recommendations**: AI-powered product suggestions based on customer behavior
- **Demand Forecasting**: Predictive analytics for future product demand
- **Inventory Recommendations**: Smart restocking suggestions based on forecasts
- **Seasonal Trends**: Analysis of seasonal purchasing patterns
- **Personalized Insights**: Customer-specific business intelligence

### Natural Language Processing
- **Intent Classification**: Understands user intentions from text input
- **Entity Recognition**: Identifies products, quantities, and other key information
- **Smart Responses**: Generates contextually appropriate responses
- **Continuous Learning**: Adapts to user patterns over time

### Navigation
- Left sidebar for easy navigation between sections
- Quick stats display in sidebar
- Responsive layout for different screen sizes

## Customization

You can customize the interface by modifying:
- `ui/chat_interface.py` - Chat responses and behavior
- `models/inventory.py` - Inventory data structure
- `models/orders.py` - Order management system
- `ai/ai_service.py` - AI algorithms and insights
- `ai/nlp_service.py` - Natural Language Processing logic

## Requirements

- Python 3.7+
- Streamlit 1.39.0
- Pandas 2.2.2
- NumPy 2.1.1
- Scikit-learn 1.5.1
- NLTK 3.8.1
- spaCy 3.7.2