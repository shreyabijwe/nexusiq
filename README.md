# NexusIQ — Retail & Supply Chain Decision Intelligence Platform

An AI-powered business intelligence platform that helps companies monitor sales,
optimize inventory, predict demand, track logistics, detect anomalies,
and generate executive insights.

![Dashboard](screenshots/dashboard.png)

## Live Demo
🌐 [https://nexusiq-six.vercel.app](https://nexusiq-six.vercel.app)
- Login with: `admin` / `admin123`

## Screenshots

### Sales Analytics
![Sales](screenshots/sales.png)

### Inventory Management
![Inventory](screenshots/inventory.png)

### Logistics Tracker
![Logistics](screenshots/logistics.png)

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React, Tailwind CSS, Recharts |
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| Auth | JWT Authentication |
| ML | scikit-learn, numpy, pandas |
| Deployment | Vercel, Docker |

## Features
- 📊 Real-time KPI Dashboard — revenue, orders, customers, shipments
- 💰 Sales Analytics — monthly revenue trends, order status, top products
- 📦 Inventory Management — stock levels, warehouse distribution, reorder alerts
- 🚚 Logistics Tracker — carrier performance, shipment status tracking
- 🤖 AI Demand Forecasting — 3-month revenue predictions using linear regression
- 🔍 Anomaly Detection — Z-score based revenue spike/drop detection
- 📋 Executive Summary — auto-generated business insights
- 🔐 JWT Authentication — secure login system

## Dataset
- 10,000 orders across 2 years
- 500 customers, 200 products, 50 suppliers
- 4 warehouses, 5 carriers
- Generated with Python Faker library

## Project Structure
nexusiq/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI route handlers
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── database.py   # Database connection
│   │   └── main.py       # FastAPI app entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/          # Axios API calls
│   │   ├── components/   # Reusable components
│   │   └── pages/        # Dashboard pages
├── data/
│   └── generate_data.py  # Synthetic data generator
└── docker-compose.yml
## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/login | JWT Authentication |
| GET | /api/sales/summary | Sales KPIs |
| GET | /api/sales/monthly-revenue | Revenue by month |
| GET | /api/sales/top-products | Top 10 products |
| GET | /api/inventory/summary | Inventory KPIs |
| GET | /api/inventory/all | All products with stock |
| GET | /api/logistics/summary | Logistics KPIs |
| GET | /api/analytics/demand-forecast | ML demand forecast |
| GET | /api/analytics/anomaly-detection | Anomaly detection |
| GET | /api/analytics/executive-summary | AI executive summary |

## Local Setup
```bash
# Clone the repo
git clone https://github.com/shreyabijwe/nexusiq.git

# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Skills Demonstrated
- Full-stack development (React + FastAPI)
- Database design and SQL (PostgreSQL)
- REST API development
- Machine learning (forecasting, anomaly detection)
- Data engineering (ETL, synthetic data generation)
- Authentication (JWT)
- Deployment (Docker, Vercel)
- Business intelligence & analytics