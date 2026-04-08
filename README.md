# Dashboard Service

## Orchestration Layer for M-PESA Analytics Platform

![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)

---

## 📋 Overview

The **Dashboard Service** acts as the orchestration layer for the M-PESA Analytics Platform.

It aggregates responses from multiple backend microservices into a single optimized response consumed by the React dashboard frontend.

Instead of requiring the frontend to make multiple API requests, this service:

✅ Reduces frontend complexity  
✅ Improves dashboard load speed  
✅ Enables graceful degradation  
✅ Centralizes aggregation logic  
✅ Mirrors production SaaS dashboard architectures

---

## 🏗️ Architecture
┌─────────────────────────────────────────────────────────────┐
│ React Dashboard │
│ (http://localhost:3000) │
└─────────────────────────┬───────────────────────────────────┘
│
│ GET /dashboard/overview
│ Header: X-Tenant-ID: {tenant_id}
▼
┌─────────────────────────────────────────────────────────────┐
│ Dashboard Service │
│ (Port: 8006) │
│ Orchestration / Aggregation Layer │
└─────────────────────────┬───────────────────────────────────┘
│
┌─────────────────┼─────────────────┐
│ │ │
│ (parallel) │ (parallel) │ (parallel)
▼ ▼ ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ Analytics │ │ Cashflow │ │ Tenant │
│ Service │ │ Service │ │ Service │
│ (Port 8000) │ │ (Port 8003) │ │ (Port 8002) │
└───────────────┘ └───────────────┘ └───────────────┘

text

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Dashboard Aggregation** | Combines data from analytics, cashflow, and tenant services into one response |
| **Parallel Async Calls** | Fetches all data simultaneously for optimal performance (3-5x faster than sequential) |
| **Tenant Isolation** | All requests are tenant-scoped via `X-Tenant-ID` header |
| **Graceful Degradation** | Handles service failures without breaking the UI - returns empty objects for failed services |
| **Health Checks** | Built-in health endpoint for container orchestration (Kubernetes ready) |
| **CORS Enabled** | Ready for cross-origin requests from your React frontend |
| **Async/Await** | Fully async FastAPI implementation for high concurrency |
| **Timeout Protection** | 10-second timeout per downstream request prevents hanging |

---

## 📊 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/` | Service information and health status | No |
| `GET` | `/health` | Health check for container orchestration | No |
| `GET` | `/dashboard/overview` | Complete dashboard data (summary + cashflow) | Yes (X-Tenant-ID header) |

### Example Request

```bash
curl -H "X-Tenant-ID: 550e8400-e29b-41d4-a716-446655440000" \
     http://localhost:8006/dashboard/overview
Example Response (All Services Healthy)
json
{
  "summary": {
    "total_transactions": 42,
    "total_amount": 125000.00,
    "average_transaction": 2976.19,
    "active_days": 24,
    "status": "healthy"
  },
  "cashflow": {
    "total_inflow": 85000,
    "total_outflow": 45000,
    "net_cashflow": 40000,
    "trend": [
      {"date": "2026-04-01", "inflow": 12000, "outflow": 8000},
      {"date": "2026-04-02", "inflow": 15000, "outflow": 9000}
    ],
    "status": "healthy"
  },
  "timestamp": "2026-04-08T10:30:00Z",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
  "response_time_ms": 245
}
Example Response (Service Unavailable)
json
{
  "summary": {
    "status": "unavailable",
    "message": "Analytics service temporarily unavailable",
    "total_transactions": 0,
    "total_amount": 0,
    "average_transaction": 0,
    "active_days": 0
  },
  "cashflow": {
    "status": "healthy",
    "total_inflow": 85000,
    "total_outflow": 45000,
    "net_cashflow": 40000
  },
  "timestamp": "2026-04-08T10:30:00Z",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440000"
}
🚀 Quick Start
Prerequisites
Python 3.12+

pip

Running microservices:

analytics-service (port 8000)

cashflow-analyzer (port 8003)

tenant-service (port 8002) - optional

Installation
bash
# Clone the repository
git clone https://github.com/Black-opps/dashboard-service.git
cd dashboard-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn src.main:app --reload --port 8006
Docker
bash
# Build the image
docker build -t dashboard-service .

# Run the container
docker run -p 8006:8006 dashboard-service
Testing the Service
bash
# Health check
curl http://localhost:8006/health

# Service info
curl http://localhost:8006/

# Dashboard overview (requires tenant header)
curl -H "X-Tenant-ID: test-tenant-001" \
     http://localhost:8006/dashboard/overview
🔧 Configuration
Environment Variables
Create a .env file in the project root:

env
# Service URLs (required)
ANALYTICS_SERVICE_URL=http://localhost:8000
CASHFLOW_SERVICE_URL=http://localhost:8003
TENANT_SERVICE_URL=http://localhost:8002

# Service Configuration
SERVICE_PORT=8006
DEBUG=true
LOG_LEVEL=INFO

# Timeouts (seconds)
DEFAULT_TIMEOUT=10
LONG_TIMEOUT=30
📈 Performance
Metric	Value
Parallel Fetching	All services called simultaneously
Default Timeout	10 seconds
Expected Response Time	200-500ms (with all services healthy)
Concurrent Requests	Limited by FastAPI/uvicorn (high)
🛡️ Error Handling Matrix
Scenario	Behavior	Response
All services healthy	Returns full data	status: "healthy" for all
Analytics service down	Returns empty summary	summary.status: "unavailable"
Cashflow service down	Returns empty cashflow	cashflow.status: "unavailable"
Tenant service down	Proceeds without tenant features	Tenant data omitted
Timeout (10s)	Returns partial data	Timed-out services show "unavailable"
Invalid tenant ID	Returns empty data	All services return empty objects
📦 Dependencies
Package	Version	Purpose
fastapi	0.115.6	Web framework
uvicorn	0.34.0	ASGI server
httpx	0.28.1	Async HTTP client
pydantic	2.10.4	Data validation
pydantic-settings	2.7.0	Settings management
python-dotenv	1.0.1	Environment variables
🔗 Related Repositories
Repository	Description	Port
mpesa-analytics-api	API Gateway	8000
auth-service	Authentication	8001
tenant-service	Multi-tenancy	8002
cashflow-analyzer	Cashflow analytics	8003
billing-service	Subscription billing	8005
webhook-service	Event delivery	8008
🤝 Contributing
Fork the repository

Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

Development Guidelines
Follow PEP 8 style guide

Use type hints for all functions

Write docstrings for public methods

Add tests for new features

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👤 Author
Jonathan Wambugu

GitHub: @Black-opps

LinkedIn: Jonathan Wambugu

X (Twitter): @Mucheru_Jay

🙏 Acknowledgments
Built as part of the M-PESA Analytics Platform microservices architecture

Inspired by Stripe's API gateway pattern and Shopify's service mesh

Powered by FastAPI and the Python ecosystem

Thanks to all contributors and the open-source community

📞 Support
For issues, questions, or contributions, please open an issue on GitHub.

Part of the M-PESA Analytics Platform - A multi-tenant fintech SaaS solution for transaction analytics.

Built with ❤️ using FastAPI and Python
