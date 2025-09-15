# Mini Bharat AI Store

An Integrated Retail Intelligence System that connects Kirana stores, wholesalers, and logistics providers using AI and WhatsApp-like interfaces.
# Video Demo - https://drive.google.com/file/d/1eCX6ZNYm6yAG4zWa83MaFXX8ElARqzm1/view?usp=sharing

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Frontend      │    │     Backend      │    │    Database      │
│  (Streamlit)    │◄──►│  (Node.js/Express)│◄──►│ (PostgreSQL)     │
│                 │    │                  │    │                  │
│ • Chat Interface│    │ • RESTful API    │    │ • Products       │
│ • NLP Processing│    │ • Auth System    │    │ • Orders         │
│ • AI Insights   │    │ • Inventory Mgmt │    │ • Users          │
└─────────────────┘    │ • Order Tracking │    │ • Credit Data    │
                       │ • Credit Scoring │    └──────────────────┘
                       └──────────────────┘
```


### Using Docker (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd bharatai

# Build and start all services
docker-compose up --build

# Access the application:
# Frontend: http://localhost:8501
# Backend API: http://localhost:3001
```

### Local Development
```bash
# Start backend
cd backend
npm install
npm start

# Start frontend (in another terminal)
cd frontend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```


## Project Structure

```
bharatai/
├── backend/              # Node.js/Express API
│   ├── controllers/      # Request handlers
│   ├── models/           # Database models
│   ├── routes/           # API routes
│   └── config/           # Configuration files
├── frontend/             # Streamlit frontend
│   ├── ai/               # AI services
│   ├── models/           # Data models
│   └── ui/               # UI components
├── docker-compose.yml    # Docker orchestration
├── DEPLOYMENT_GUIDE.md   # Deployment instructions
├── RUNNING.md            # Instructions for running the system
├── test_system.py        # System testing script
└── tasks.md             # Project task tracking
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

### Inventory
- `GET /api/inventory/products` - Get all products
- `GET /api/inventory/products/:id` - Get product by ID
- `POST /api/inventory/products` - Add new product
- `PUT /api/inventory/products/:id` - Update product
- `DELETE /api/inventory/products/:id` - Delete product
- `POST /api/inventory/products/:id/add-stock` - Add stock
- `POST /api/inventory/products/:id/deduct-stock` - Deduct stock
- `GET /api/inventory/products/:id/stock-level` - Get stock level


## Monitoring

Run the monitoring script:
```bash
node monitoring.js --continuous --interval 30
```

## Authors

- **Aditya Garud** - *Initial work* - [yashranaway](https://github.com/yashranaway)


## Acknowledgments
- Built with Node.js, Express, PostgreSQL, Python, Streamlit, and spaCy
- Inspired by the need to modernize Kirana store operations in India
