# Mini Bharat AI Store - Backend API

RESTful API for the Mini Bharat AI Store, an Integrated Retail Intelligence System for Kirana stores.

## Features

- Inventory Management API
- Delivery Booking API
- Credit Scoring API
- User Authentication & Authorization
- PostgreSQL Database Integration (Neon DB)
- RESTful architecture
- Comprehensive documentation

## Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file with the following variables:
   ```env
   PORT=3001
   NODE_ENV=development
   DATABASE_URL=postgresql://neondb_owner:npg_mc3zRWHGX2ph@ep-sparkling-glitter-ade65204-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   JWT_SECRET=your_jwt_secret_key_here
   ```

## Usage

### Development
```bash
npm run dev
```

### Production
```bash
npm start
```

The API will be available at `http://localhost:3001`.

## Database Schema

Refer to [docs/database_schema.md](docs/database_schema.md) for detailed database design.

## API Endpoints

### Authentication

#### Register user
```
POST /api/auth/register
```

#### Login user
```
POST /api/auth/login
```

#### Get user profile
```
GET /api/auth/profile
```

#### Update user role (admin only)
```
PUT /api/auth/role
```

### Inventory Management

#### Get all products
```
GET /api/inventory/products
```

#### Get product by ID
```
GET /api/inventory/products/:id
```

#### Add new product
```
POST /api/inventory/products
```

#### Update product
```
PUT /api/inventory/products/:id
```

#### Delete product
```
DELETE /api/inventory/products/:id
```

#### Add stock
```
POST /api/inventory/products/:productId/add-stock
```

#### Deduct stock
```
POST /api/inventory/products/:productId/deduct-stock
```

#### Get stock level
```
GET /api/inventory/products/:productId/stock-level
```

### Delivery Booking

#### Place order
```
POST /api/delivery/orders
```

#### Get order by ID
```
GET /api/delivery/orders/:id
```

#### Get orders by customer
```
GET /api/delivery/orders/customer/:customerId
```

#### Update order status
```
PUT /api/delivery/orders/:orderId/status
```

#### Get tracking information
```
GET /api/delivery/orders/:orderId/tracking
```

#### Cancel order
```
DELETE /api/delivery/orders/:orderId
```

### Credit Scoring

#### Verify retailer
```
GET /api/credit/retailers/:id
```

#### Add retailer
```
POST /api/credit/retailers
```

#### Update retailer
```
PUT /api/credit/retailers/:id
```

#### Assess credit risk
```
POST /api/credit/assessment/:retailerId
```

#### Get retailer credit info
```
GET /api/credit/retailers/:retailerId/credit-info
```

## Project Structure

```
backend/
├── server.js              # Main server file
├── package.json           # Dependencies and scripts
├── .env                   # Environment variables
├── README.md              # This file
├── docs/                  # Documentation
│   └── database_schema.md # Database schema design
├── migrations/            # Database migrations
│   ├── init_schema.sql    # Initial database schema
│   └── runMigration.js    # Migration runner
├── controllers/           # Request handlers
│   ├── auth.controller.js
│   ├── inventory.controller.js
│   ├── delivery.controller.js
│   └── credit.controller.js
├── models/                # Data models
│   └── postgresql/        # PostgreSQL models
│       ├── BaseModel.js
│       ├── User.js
│       ├── Retailer.js
│       ├── Supplier.js
│       ├── Product.js
│       ├── Order.js
│       ├── DeliveryTracking.js
│       └── CreditAssessment.js
├── routes/                # API routes
│   ├── auth.routes.js
│   ├── inventory.routes.js
│   ├── delivery.routes.js
│   └── credit.routes.js
├── middleware/            # Custom middleware
│   ├── auth.js
│   └── role.js
├── services/              # Business logic
├── utils/                 # Utility functions
└── config/                # Configuration files
    └── database.js
```

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
PORT=3001
NODE_ENV=development
DATABASE_URL=postgresql://neondb_owner:npg_mc3zRWHGX2ph@ep-sparkling-glitter-ade65204-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
JWT_SECRET=mini_bharat_ai_store_secret_key
```

## Requirements

- Node.js 14+
- npm 6+
- PostgreSQL (Neon DB)

