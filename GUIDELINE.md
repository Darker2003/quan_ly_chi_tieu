# MoneyFlow - Personal Finance Management System
## Complete User & Admin Guideline

---

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Getting Started](#getting-started)
3. [User Features](#user-features)
4. [Admin Features](#admin-features)
5. [API Documentation](#api-documentation)
6. [Technical Details](#technical-details)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 System Overview

**MoneyFlow** is a comprehensive personal finance management system built with:
- **Backend**: FastAPI (Python) - RESTful API on port 8001
- **Frontend**: Django - Web application on port 8000
- **Database**: SQLite with realistic Vietnamese financial data
- **Authentication**: JWT-based secure authentication
- **UI**: Bootstrap 5 with Vietnamese localization

### Key Features
✅ User authentication and authorization  
✅ Transaction management (income & expenses)  
✅ Category-based organization  
✅ Financial analytics and reporting  
✅ Admin dashboard for user management  
✅ Responsive design for all devices  
✅ Vietnamese language interface  

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Virtual environment activated

### Installation & Setup

1. **Activate Virtual Environment**
   ```bash
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

2. **Install Dependencies** (if not already installed)
   ```bash
   pip install -r requirements.txt
   ```

3. **Create Environment File**
   ```bash
   # Copy .env.example to .env
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   ```

4. **Initialize Database**
   ```bash
   python -c "from backend.database import init_db; init_db()"
   ```

5. **Populate Vietnamese Data**
   ```bash
   python data/populate_vietnamese_data.py
   ```

6. **Run Django Migrations**
   ```bash
   python manage.py migrate
   ```

7. **Start Both Servers**
   ```bash
   python run_both_servers.py
   ```

8. **Access the Application**
   - Frontend: http://127.0.0.1:8000
   - Backend API: http://127.0.0.1:8001
   - API Documentation: http://127.0.0.1:8001/api/docs

### Default Test Accounts

**Admin Account:**
- Email: `lethanh@outlook.com`
- Password: `password123`

**Regular Users:** (50+ Vietnamese users available)
- Email: `vuvanthanh@moneyflow.vn`
- Email: `buitu460@moneyflow.vn`
- Email: `lamlan@yahoo.com`
- Password for all: `password123`

---

## 👤 User Features

### 1. Authentication

#### Registration
1. Navigate to http://127.0.0.1:8000
2. Click "Đăng ký ngay" (Register now)
3. Fill in:
   - Full Name (Họ và tên)
   - Email
   - Password (minimum 6 characters)
4. Click "Đăng Ký" (Register)

#### Login
1. Navigate to http://127.0.0.1:8000/login/
2. Enter email and password
3. Click "Đăng Nhập" (Login)

### 2. Dashboard

**Overview Statistics:**
- Total Income (Tổng Thu Nhập)
- Total Expenses (Tổng Chi Tiêu)
- Current Balance (Số Dư)

**Visual Analytics:**
- Expense breakdown by category (pie chart)
- 6-month comparison (bar chart)
- Recent transactions list

**Access:** Click "Dashboard" in navigation menu

### 3. Transaction Management

#### Add Transaction
1. Click "Giao Dịch" → "Thêm Giao Dịch" or use the "+" button
2. Fill in transaction details:
   - **Amount** (Số tiền): Enter amount in VND
   - **Type** (Loại): Select Income or Expense
   - **Category** (Danh mục): Choose from available categories
   - **Date** (Ngày): Select transaction date
   - **Description** (Mô tả): Add details (optional)
   - **Notes** (Ghi chú): Additional notes (optional)
3. Click "Thêm Giao Dịch" (Add Transaction)

#### View Transactions
1. Click "Giao Dịch" (Transactions) in navigation
2. View all transactions in a table format
3. Use filters to narrow down:
   - **Type**: Income/Expense/All
   - **Category**: Select specific category
   - **Date Range**: From date - To date
4. Click "Lọc" (Filter) to apply filters

**Transaction Information Displayed:**
- Date
- Description
- Category
- Type (Income/Expense)
- Amount in VND

### 4. Analytics & Reports

**Access:** Click "Báo Cáo" (Reports) in navigation

**Available Reports:**

1. **Financial Summary**
   - Total income
   - Total expenses
   - Net balance
   - Savings rate

2. **Category Breakdown**
   - Pie chart showing expense distribution
   - Percentage by category
   - Top spending categories

3. **Monthly Comparison**
   - Bar chart comparing last 6 months
   - Income vs Expense trends
   - Month-over-month growth

### 5. Categories

**Default Categories:**

**Income Categories:**
- Lương (Salary)
- Thưởng (Bonus)
- Đầu tư (Investment)
- Thu nhập khác (Other income)

**Expense Categories:**
- Ăn uống (Food & Dining)
- Đi lại (Transportation)
- Mua sắm (Shopping)
- Giải trí (Entertainment)
- Hóa đơn (Bills)
- Y tế (Healthcare)
- Giáo dục (Education)
- Chi tiêu khác (Other expenses)

---

## 🔐 Admin Features

### Accessing Admin Dashboard

**Requirements:**
- Must have admin privileges (`is_admin = True`)
- Login with admin account

**Access:** Click "Quản Trị" (Admin) in navigation menu (only visible to admins)

### Admin Dashboard Overview

**System Statistics Cards:**
1. **Total Users** (Tổng Người Dùng) - All registered users
2. **Active Users** (Đang Hoạt Động) - Currently active accounts
3. **Inactive Users** (Không Hoạt Động) - Deactivated accounts
4. **Admin Users** (Quản Trị Viên) - Users with admin privileges

**Financial Statistics:**
- Total Transactions across all users
- Total Income (system-wide)
- Total Expenses (system-wide)
- Net Balance

### User Management

#### View All Users
The admin dashboard displays a comprehensive user table with:
- User ID
- Full Name
- Email
- Role (Admin/User badge)
- Status (Active/Inactive)
- Transaction Count
- Total Income
- Total Expenses
- Registration Date
- Action buttons (Edit/Delete)

#### Filter Users
Use the filter form to narrow down users:
1. **Search** (Tìm kiếm): Search by name or email
2. **Status** (Trạng thái): All/Active/Inactive
3. **Role** (Vai trò): All/Admin/User
4. Click "Lọc" (Filter) to apply

#### Edit User
1. Click "Sửa" (Edit) button next to any user
2. Modify user information:
   - Full Name
   - Email
   - Active Status (checkbox)
   - Admin Rights (checkbox)
3. Click "Lưu Thay Đổi" (Save Changes)

**User Detail Page Shows:**
- User statistics (ID, created date, updated date)
- Transaction count
- Total income and expenses
- Current balance
- Role and status badges

**Restrictions:**
- Cannot deactivate your own account
- Cannot remove your own admin privileges
- Cannot delete your own account

#### Delete User
1. Click "Xóa" (Delete) button next to any user
2. Confirm deletion in the modal dialog
3. User and all their data will be permanently deleted

**Warning:** This action cannot be undone!

### Setting Admin Users

**Method 1: Using Admin Dashboard**
1. Login as admin
2. Navigate to Admin Dashboard
3. Click "Sửa" (Edit) on target user
4. Check "Quyền quản trị viên" (Admin Rights)
5. Click "Lưu Thay Đổi" (Save Changes)

**Method 2: Using Command Line**
```bash
python set_admin.py <email>
```

**Examples:**
```bash
# Set user as admin
python set_admin.py user@example.com

# List all admin users
python set_admin.py --list
```

---

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8001/api
```

### Interactive API Docs
Access Swagger UI at: http://127.0.0.1:8001/api/docs

### Authentication Endpoints

**Register User**
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

**Login**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {...}
}
```

### Transaction Endpoints

**Create Transaction**
```http
POST /api/transactions
Authorization: Bearer <token>
Content-Type: application/json

{
  "amount": 500000,
  "description": "Lunch",
  "type": "expense",
  "category_id": 1,
  "date": "2025-01-15"
}
```

**Get All Transactions**
```http
GET /api/transactions?skip=0&limit=100
Authorization: Bearer <token>
```

### Admin Endpoints

**Get All Users (Admin Only)**
```http
GET /api/admin/users?skip=0&limit=100&search=&is_active=true
Authorization: Bearer <admin_token>
```

**Update User (Admin Only)**
```http
PUT /api/admin/users/{user_id}
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "full_name": "Updated Name",
  "email": "newemail@example.com",
  "is_active": true,
  "is_admin": false
}
```

**Get System Statistics (Admin Only)**
```http
GET /api/admin/stats
Authorization: Bearer <admin_token>
```

---

## 🔧 Technical Details

### Project Structure
```
msapython_final/
├── backend/
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── transactions.py  # Transaction management
│   │   ├── categories.py    # Category management
│   │   ├── analytics.py     # Analytics endpoints
│   │   ├── users.py         # User profile endpoints
│   │   └── admin.py         # Admin endpoints
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── security.py          # Authentication & authorization
│   ├── database.py          # Database configuration
│   └── main.py              # FastAPI application
├── web/
│   ├── templates/web/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── transactions.html
│   │   ├── add_transaction.html
│   │   ├── analytics.html
│   │   ├── admin_dashboard.html
│   │   └── admin_user_detail.html
│   ├── views.py             # Django views
│   └── urls.py              # URL routing
├── data/
│   ├── generated_users.json # 50 Vietnamese users
│   └── populate_vietnamese_data.py
├── moneyflow.db             # SQLite database
├── run_both_servers.py      # Start both servers
├── set_admin.py             # Admin management script
└── requirements.txt         # Python dependencies
```

### Database Schema

**Users Table:**
- id (Primary Key)
- email (Unique)
- password_hash
- full_name
- created_at
- updated_at
- is_active
- is_admin

**Transactions Table:**
- id (Primary Key)
- amount
- description
- date
- type (income/expense)
- category_id (Foreign Key)
- user_id (Foreign Key)
- notes
- created_at
- is_deleted

**Categories Table:**
- id (Primary Key)
- name
- type (income/expense)
- is_default
- user_id (Foreign Key, nullable for default categories)

### Security Features
- JWT token-based authentication
- Bcrypt password hashing
- Role-based access control (Admin/User)
- CORS protection
- Session management
- Token expiration (30 minutes)

---

## 🐛 Troubleshooting

### Common Issues

**1. Servers won't start**
```bash
# Check if ports are already in use
netstat -ano | findstr :8000
netstat -ano | findstr :8001

# Kill processes if needed
taskkill /PID <process_id> /F
```

**2. Database errors**
```bash
# Reinitialize database
python -c "from backend.database import init_db; init_db()"
```

**3. Admin column missing**
```bash
# Run migration
python migrate_add_admin.py
```

**4. Can't login**
- Verify email and password
- Check if user exists in database
- Ensure backend server is running
- Check browser console for errors

**5. Transactions not showing**
- Verify you're logged in
- Check date filters
- Ensure backend API is accessible
- Check browser network tab for API errors

### Getting Help

**Check Logs:**
- Backend logs in terminal running `run_both_servers.py`
- Browser console (F12) for frontend errors
- Network tab for API request/response details

**Verify Setup:**
```bash
# Test backend
curl http://127.0.0.1:8001/api/

# Test database
python -c "from backend.database import SessionLocal; from backend.models import User; db = SessionLocal(); print(f'Users: {db.query(User).count()}'); db.close()"
```

---

## 📊 Sample Data

The system comes pre-populated with:
- **50 Vietnamese users** with realistic profiles
- **26,675 transactions** spanning May 2024 - May 2025
- **Realistic spending patterns** based on Vietnamese income classes
- **All Vietnamese Unicode characters** properly supported

**Income Classes:**
- Low: 5-10M VND/month
- Lower-Middle: 10-20M VND/month
- Middle: 20-40M VND/month
- Upper-Middle: 40-60M VND/month
- High: 60-80M VND/month

---

## 🎓 Best Practices

### For Users
1. **Regular Updates**: Add transactions daily for accurate tracking
2. **Use Categories**: Properly categorize all transactions
3. **Review Analytics**: Check monthly reports to understand spending patterns
4. **Set Goals**: Use balance tracking to monitor savings progress

### For Admins
1. **Regular Monitoring**: Check system statistics regularly
2. **User Management**: Review and manage inactive accounts
3. **Security**: Limit admin privileges to trusted users only
4. **Backups**: Regularly backup the database file
5. **Audit**: Monitor user activities and transaction patterns

---

## 📝 License & Credits

**MoneyFlow Personal Finance Management System**
- Built with FastAPI, Django, and Bootstrap 5
- Vietnamese localization and realistic data generation
- Comprehensive admin dashboard for user management

**Version:** 1.0.0  
**Last Updated:** January 2025

---

## 🚀 Quick Reference

**Start Application:**
```bash
python run_both_servers.py
```

**Access Points:**
- Frontend: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8001/api/docs
- Admin: http://127.0.0.1:8000/admin/

**Default Admin:**
- Email: lethanh@outlook.com
- Password: password123

**Set New Admin:**
```bash
python set_admin.py user@example.com
```

---

**Happy Financial Management! 💰📊**

