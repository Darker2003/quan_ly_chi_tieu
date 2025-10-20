# MoneyFlow - Quick Start Guide

This guide will help you get the MoneyFlow backend API up and running in minutes.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation Steps

### 1. Clone or Navigate to the Project

```bash
cd e:\Dat\FSB\msapython_final
```

### 2. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and update the following (optional for development):
```env
JWT_SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///./moneyflow.db
```

### 5. Run the Server

**Option A: Using the run script**
```bash
python run_server.py
```

**Option B: Using uvicorn directly**
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
```

The server will start at: **http://localhost:8001**

### 6. Access API Documentation

Once the server is running, open your browser and navigate to:

- **Swagger UI:** http://localhost:8001/api/docs
- **ReDoc:** http://localhost:8001/api/redoc

## Testing the API

### Run All Tests

```bash
pytest -v
```

### Run Specific Test Module

```bash
pytest tests/test_auth.py -v
pytest tests/test_transactions.py -v
pytest tests/test_categories.py -v
pytest tests/test_analytics.py -v
```

### Run with Coverage Report

```bash
pytest --cov=backend --cov-report=html
```

## Quick API Examples

### 1. Register a New User

```bash
curl -X POST "http://localhost:8001/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2024-05-26T10:00:00"
  }
}
```

### 2. Login

```bash
curl -X POST "http://localhost:8001/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### 3. Get Categories (Authenticated)

```bash
curl -X GET "http://localhost:8001/api/categories/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 4. Create a Transaction

```bash
curl -X POST "http://localhost:8001/api/transactions/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50000,
    "description": "Lunch at restaurant",
    "date": "2024-05-26",
    "type": "expense",
    "category_id": 1,
    "notes": "Team lunch"
  }'
```

### 5. Get Financial Summary

```bash
curl -X GET "http://localhost:8001/api/analytics/summary" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 6. Get Dashboard Data

```bash
curl -X GET "http://localhost:8001/api/analytics/dashboard" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Default Categories

The system comes with pre-configured categories:

**Expense Categories:**
- Ăn uống (Food & Dining)
- Di chuyển (Transportation)
- Mua sắm (Shopping)
- Hóa đơn (Bills)
- Giải trí (Entertainment)
- Y tế (Healthcare)
- Giáo dục (Education)
- Nhà ở (Housing)
- Khác (Other)

**Income Categories:**
- Lương (Salary)
- Thưởng (Bonus)
- Đầu tư (Investment)
- Quà tặng (Gifts)
- Thu nhập khác (Other Income)

## Project Structure

```
msapython_final/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── security.py          # Authentication & security
│   └── routers/
│       ├── auth.py          # Authentication endpoints
│       ├── categories.py    # Category endpoints
│       ├── transactions.py  # Transaction endpoints
│       ├── analytics.py     # Analytics endpoints
│       └── users.py         # User profile endpoints
├── tests/
│   ├── conftest.py          # Test configuration
│   ├── test_auth.py         # Authentication tests
│   ├── test_categories.py   # Category tests
│   ├── test_transactions.py # Transaction tests
│   └── test_analytics.py    # Analytics tests
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
├── requirements.txt         # Python dependencies
├── pytest.ini              # Pytest configuration
├── README.md               # Project documentation
├── TEST_REPORT.md          # Test results report
└── QUICKSTART.md           # This file
```

## Common Issues & Solutions

### Issue: Port 8001 already in use

**Solution:** Change the port in `run_server.py` or kill the process using port 8001:

```bash
# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8001 | xargs kill -9
```

### Issue: Database locked error

**Solution:** Close any other connections to the database or delete `moneyflow.db` and restart:

```bash
rm moneyflow.db
python run_server.py
```

### Issue: Import errors

**Solution:** Make sure you're in the virtual environment and all dependencies are installed:

```bash
pip install -r requirements.txt
```

## Next Steps

1. ✅ Backend API is complete and tested
2. 📝 Implement Django frontend (see PRD for requirements)
3. 🔗 Integrate frontend with FastAPI backend
4. 🚀 Deploy to production

## Support

For issues or questions:
1. Check the [README.md](README.md) for detailed documentation
2. Review the [TEST_REPORT.md](TEST_REPORT.md) for test coverage
3. Check API documentation at http://localhost:8001/api/docs

## License

This project is part of the MoneyFlow personal finance management system.

