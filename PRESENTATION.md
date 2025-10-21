# 🎯 THUYẾT TRÌNH ĐỒ ÁN KẾT THÚC MÔN PYTHON

## 📋 THÔNG TIN ĐỒ ÁN

**Tên đồ án:** MoneyFlow - Hệ Thống Quản Lý Tài Chính Cá Nhân

**Sinh viên thực hiện:** [Tên sinh viên]

**Lớp:** [Tên lớp]

**Giảng viên hướng dẫn:** [Tên giảng viên]

**Thời gian thực hiện:** [Thời gian]

---

## 📑 NỘI DUNG THUYẾT TRÌNH

### 1. GIỚI THIỆU ĐỀ TÀI (3 phút)

#### 1.1. Bối cảnh và Động lực
- **Vấn đề thực tế:**
  - Nhiều người gặp khó khăn trong việc quản lý thu chi cá nhân
  - Thiếu công cụ đơn giản, dễ sử dụng để theo dõi tài chính
  - Khó khăn trong việc phân tích và lập kế hoạch tài chính

- **Mục tiêu đề tài:**
  - Xây dựng ứng dụng web quản lý tài chính cá nhân hoàn chỉnh
  - Áp dụng kiến thức Python đã học vào thực tế
  - Tích hợp công nghệ hiện đại (FastAPI, Django, SQLAlchemy)

#### 1.2. Phạm vi đồ án
- ✅ Quản lý thu chi cá nhân
- ✅ Phân tích và báo cáo tài chính
- ✅ Hệ thống xác thực và phân quyền
- ✅ Giao diện người dùng thân thiện
- ✅ Dashboard quản trị viên

---

### 2. CÔNG NGHỆ SỬ DỤNG (4 phút)

#### 2.1. Kiến trúc hệ thống
```
┌─────────────────────────────────────────────────┐
│           FRONTEND (Django)                      │
│   - Templates (HTML/CSS/JavaScript)              │
│   - Bootstrap 5.3.0                              │
│   - Chart.js 4.4.0                               │
└─────────────────┬───────────────────────────────┘
                  │ HTTP/REST API
┌─────────────────▼───────────────────────────────┐
│           BACKEND (FastAPI)                      │
│   - RESTful API                                  │
│   - JWT Authentication                           │
│   - Business Logic                               │
└─────────────────┬───────────────────────────────┘
                  │ SQLAlchemy ORM
┌─────────────────▼───────────────────────────────┐
│           DATABASE (SQLite)                      │
│   - Users, Transactions, Categories              │
└─────────────────────────────────────────────────┘
```

#### 2.2. Stack công nghệ Backend
| Công nghệ | Phiên bản | Mục đích |
|-----------|-----------|----------|
| **Python** | 3.10+ | Ngôn ngữ lập trình chính |
| **FastAPI** | 0.109.0 | Web framework backend, REST API |
| **SQLAlchemy** | 2.0.25 | ORM - Object Relational Mapping |
| **Pydantic** | 2.5.3 | Data validation và schemas |
| **JWT** | 2.8.0 | Authentication & Authorization |
| **Bcrypt** | 4.1.2 | Mã hóa mật khẩu |
| **Uvicorn** | 0.27.0 | ASGI server |

#### 2.3. Stack công nghệ Frontend
| Công nghệ | Phiên bản | Mục đích |
|-----------|-----------|----------|
| **Django** | 5.0.1 | Web framework frontend |
| **Bootstrap** | 5.3.0 | Responsive UI framework |
| **Chart.js** | 4.4.0 | Biểu đồ và visualization |
| **Bootstrap Icons** | 1.11.0 | Icon library |

#### 2.4. Ưu điểm của kiến trúc
- **Tách biệt Frontend - Backend:** Dễ bảo trì, mở rộng
- **RESTful API:** Chuẩn hóa, có thể tích hợp với mobile app
- **Async/Await:** Hiệu năng cao với FastAPI
- **Type Hints:** Code rõ ràng, ít lỗi với Pydantic

---

### 3. CƠ SỞ DỮ LIỆU (3 phút)

#### 3.1. Sơ đồ ERD
```
┌─────────────────┐
│     USERS       │
├─────────────────┤
│ id (PK)         │
│ email           │
│ password_hash   │
│ full_name       │
│ is_admin        │
│ is_active       │
│ created_at      │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────▼────────┐         ┌─────────────────┐
│  TRANSACTIONS   │    N    │   CATEGORIES    │
├─────────────────┤─────────┤─────────────────┤
│ id (PK)         │    1    │ id (PK)         │
│ user_id (FK)    │         │ name            │
│ category_id (FK)│         │ type            │
│ amount          │         │ is_default      │
│ description     │         │ user_id (FK)    │
│ date            │         └─────────────────┘
│ type            │
│ notes           │
│ is_deleted      │
│ created_at      │
└─────────────────┘
```

#### 3.2. Mô tả các bảng

**Bảng USERS:**
- Lưu thông tin người dùng
- Mật khẩu được mã hóa bằng bcrypt
- Hỗ trợ phân quyền admin

**Bảng CATEGORIES:**
- Danh mục thu/chi (Lương, Ăn uống, Di chuyển...)
- Có danh mục mặc định và danh mục tùy chỉnh
- Phân loại theo type: income/expense

**Bảng TRANSACTIONS:**
- Lưu trữ các giao dịch thu/chi
- Soft delete (is_deleted) để giữ lịch sử
- Liên kết với user và category

---

### 4. CHỨC NĂNG CHÍNH (8 phút)

#### 4.1. Hệ thống Xác thực (Authentication)

**Đăng ký tài khoản:**
```python
# Backend: backend/routers/auth.py
@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Kiểm tra email đã tồn tại
    # Hash password với bcrypt
    # Tạo user mới
    # Tạo categories mặc định
```

**Đăng nhập:**
```python
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm, db: Session):
    # Xác thực email/password
    # Tạo JWT access token
    # Trả về token cho client
```

**Bảo mật:**
- ✅ Password hashing với bcrypt (cost factor: 12)
- ✅ JWT token với expiration time
- ✅ Protected routes với dependency injection
- ✅ CORS configuration

#### 4.2. Quản lý Giao dịch (Transactions)

**Thêm giao dịch:**
- Form nhập liệu với validation
- Chọn loại (Thu/Chi), danh mục, số tiền, ngày
- Ghi chú tùy chọn

**Xem danh sách giao dịch:**
- Hiển thị dạng bảng với phân trang
- Lọc theo: loại, danh mục, khoảng thời gian
- Tìm kiếm theo mô tả

**Sửa/Xóa giao dịch:**
- Chỉnh sửa thông tin giao dịch
- Soft delete để giữ lịch sử

**Code minh họa:**
```python
# Backend API endpoint
@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate category thuộc về user
    # Tạo transaction mới
    # Lưu vào database
    return new_transaction
```

#### 4.3. Dashboard và Phân tích

**Tổng quan tài chính:**
- 📊 Tổng thu nhập
- 📊 Tổng chi tiêu  
- 📊 Số dư hiện tại
- 📊 Số lượng giao dịch

**Biểu đồ phân tích:**

1. **Biểu đồ tròn - Chi tiêu theo danh mục:**
```javascript
// Chart.js implementation
const categoryChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: categories,
        datasets: [{
            data: amounts,
            backgroundColor: colors
        }]
    }
});
```

2. **Biểu đồ cột - So sánh 6 tháng:**
- Thu nhập vs Chi tiêu theo tháng
- Dễ dàng nhận biết xu hướng

3. **Biểu đồ đường - Xu hướng giao dịch:**
- Theo dõi biến động theo thời gian

**Tính năng lọc theo thời gian:**
- ✅ Tất cả thời gian (mặc định)
- ✅ Tháng này
- ✅ Tháng trước
- ✅ Năm nay
- ✅ Tùy chỉnh khoảng thời gian

**Code Backend:**
```python
@router.get("/dashboard", response_model=AnalyticsResponse)
async def get_dashboard_data(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Tính toán tổng thu/chi
    # Lấy dữ liệu biểu đồ
    # Trả về analytics response
```

#### 4.4. Quản lý Danh mục (Categories)

**Danh mục mặc định:**
- Thu nhập: Lương, Thưởng, Đầu tư, Khác
- Chi tiêu: Ăn uống, Di chuyển, Mua sắm, Giải trí, Hóa đơn, Khác

**Danh mục tùy chỉnh:**
- Người dùng tạo danh mục riêng
- Chỉnh sửa, xóa danh mục (không xóa được danh mục mặc định)

#### 4.5. Dashboard Quản trị (Admin)

**Thống kê hệ thống:**
- 👥 Tổng số người dùng
- 👤 Người dùng hoạt động
- 💰 Tổng giao dịch
- 👨‍💼 Số admin

**Quản lý người dùng:**
- Xem danh sách tất cả users
- Lọc theo vai trò (Admin/User)
- Xem chi tiết thông tin user
- Chỉnh sửa thông tin user
- Cấp/Thu hồi quyền admin
- Xóa user

**Bảo mật:**
- Chỉ admin mới truy cập được
- Middleware kiểm tra quyền admin

```python
# Security check
async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Không có quyền truy cập"
        )
    return current_user
```

---

### 5. GIAO DIỆN NGƯỜI DÙNG (3 phút)

#### 5.1. Thiết kế UI/UX

**Nguyên tắc thiết kế:**
- ✅ **Responsive:** Tương thích mọi thiết bị (Desktop, Tablet, Mobile)
- ✅ **Intuitive:** Dễ sử dụng, không cần hướng dẫn
- ✅ **Consistent:** Thống nhất về màu sắc, font chữ, layout
- ✅ **Accessible:** Hỗ trợ người dùng khuyết tật

**Màu sắc:**
- Primary: #0d6efd (Xanh dương - Tin cậy)
- Success: #198754 (Xanh lá - Thu nhập)
- Danger: #dc3545 (Đỏ - Chi tiêu)
- Warning: #ffc107 (Vàng - Cảnh báo)

#### 5.2. Các trang chính

1. **Trang đăng nhập/đăng ký**
   - Form đơn giản, rõ ràng
   - Validation real-time
   - Thông báo lỗi thân thiện

2. **Dashboard**
   - Cards hiển thị số liệu tổng quan
   - Biểu đồ trực quan
   - Bộ lọc thời gian linh hoạt

3. **Trang giao dịch**
   - Bảng danh sách với phân trang
   - Bộ lọc đa tiêu chí
   - Modal thêm/sửa giao dịch

4. **Trang báo cáo**
   - Biểu đồ phân tích chi tiết
   - Export dữ liệu (future feature)

5. **Admin Dashboard**
   - Thống kê hệ thống
   - Quản lý users
   - Bảng điều khiển admin

---

### 6. DEMO SẢN PHẨM (5 phút)

#### 6.1. Kịch bản Demo

**Bước 1: Đăng ký và Đăng nhập**
1. Truy cập http://127.0.0.1:8000
2. Đăng ký tài khoản mới
3. Đăng nhập vào hệ thống

**Bước 2: Thêm giao dịch**
1. Thêm giao dịch thu nhập (Lương tháng 10)
2. Thêm giao dịch chi tiêu (Ăn sáng, Xăng xe)
3. Xem danh sách giao dịch

**Bước 3: Xem Dashboard**
1. Xem tổng quan tài chính
2. Xem biểu đồ chi tiêu theo danh mục
3. Thử nghiệm bộ lọc thời gian:
   - Lọc "Tháng này"
   - Lọc "Năm nay"
   - Tùy chỉnh khoảng thời gian

**Bước 4: Quản lý danh mục**
1. Xem danh mục mặc định
2. Thêm danh mục tùy chỉnh
3. Sử dụng danh mục mới trong giao dịch

**Bước 5: Admin Dashboard** (nếu là admin)
1. Truy cập trang quản trị
2. Xem thống kê hệ thống
3. Quản lý người dùng
4. Cấp quyền admin cho user khác

---

### 7. DỮ LIỆU TEST (2 phút)

#### 7.1. Dữ liệu mẫu

**Hệ thống đã tạo sẵn:**
- ✅ **51 users** với thông tin người Việt thực tế
- ✅ **26,675 giao dịch** từ 05/2024 đến 05/2025
- ✅ Dữ liệu phản ánh thực tế tài chính người Việt

**Đặc điểm dữ liệu:**
- Thu nhập trung bình: ~17.3 triệu VNĐ/tháng
- Tỷ lệ chi tiêu: ~10% thu nhập
- Phân bố theo thành phố: Hà Nội, TP.HCM, Đà Nẵng...
- Nghề nghiệp đa dạng: Kỹ sư, Giáo viên, Bác sĩ, Kinh doanh...

#### 7.2. Tài khoản test

**Admin account:**
```
Email: lethanh@outlook.com
Password: password123
```

**Regular user:**
```
Email: [bất kỳ user nào trong 51 users]
Password: password123
```

---

### 8. KIỂM THỬ VÀ CHẤT LƯỢNG (3 phút)

#### 8.1. Unit Testing

**Backend Tests:**
- ✅ 40 test cases
- ✅ Coverage: Authentication, Transactions, Categories, Analytics
- ✅ Framework: pytest

**Chạy tests:**
```bash
cd backend
pytest tests/ -v
```

**Kết quả:**
```
================================ 40 passed ================================
```

#### 8.2. Các test case chính

**Authentication Tests:**
- ✅ Đăng ký user mới
- ✅ Đăng ký với email trùng
- ✅ Đăng nhập thành công
- ✅ Đăng nhập sai mật khẩu
- ✅ Access protected routes

**Transaction Tests:**
- ✅ Tạo giao dịch thu/chi
- ✅ Lấy danh sách giao dịch
- ✅ Lọc theo loại, danh mục
- ✅ Cập nhật giao dịch
- ✅ Xóa giao dịch (soft delete)

**Analytics Tests:**
- ✅ Tính toán tổng thu/chi
- ✅ Phân tích theo danh mục
- ✅ So sánh theo tháng
- ✅ Dashboard data

#### 8.3. Manual Testing

**Đã test:**
- ✅ Responsive design trên nhiều thiết bị
- ✅ Cross-browser compatibility
- ✅ Performance với 26K+ transactions
- ✅ Security (SQL injection, XSS)
- ✅ User experience flow

---

### 9. HƯỚNG DẪN CÀI ĐẶT (2 phút)

#### 9.1. Yêu cầu hệ thống
- Python 3.10 trở lên
- pip (Python package manager)
- Git (optional)

#### 9.2. Các bước cài đặt

**Bước 1: Clone repository**
```bash
git clone <repository-url>
cd msapython_final
```

**Bước 2: Tạo virtual environment**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

**Bước 3: Cài đặt dependencies**
```bash
pip install -r requirements.txt
```

**Bước 4: Khởi tạo database**
```bash
python -c "from backend.database import init_db; init_db()"
```

**Bước 5: Chạy servers**
```bash
python run_both_servers.py
```

**Bước 6: Truy cập ứng dụng**
- Frontend: http://127.0.0.1:8000
- Backend API: http://127.0.0.1:8001
- API Docs: http://127.0.0.1:8001/api/docs

---

### 10. KẾT QUẢ ĐẠT ĐƯỢC (3 phút)

#### 10.1. Chức năng hoàn thành

✅ **Backend API (FastAPI):**
- Authentication & Authorization (JWT)
- CRUD operations cho Users, Transactions, Categories
- Analytics & Reporting endpoints
- Admin management APIs
- Data validation với Pydantic
- Error handling & logging

✅ **Frontend (Django):**
- Responsive UI với Bootstrap 5
- Interactive charts với Chart.js
- Form validation
- Session management
- Admin dashboard
- Date range filtering

✅ **Database:**
- SQLite với SQLAlchemy ORM
- Proper relationships & constraints
- Migration scripts
- Sample data generation

✅ **Testing:**
- 40 unit tests (100% pass)
- Manual testing completed
- Performance tested với 26K+ records

#### 10.2. Kiến thức Python đã áp dụng

**Core Python:**
- ✅ OOP (Classes, Inheritance)
- ✅ Type Hints & Annotations
- ✅ Async/Await
- ✅ List/Dict Comprehensions
- ✅ Decorators
- ✅ Context Managers
- ✅ Exception Handling

**Libraries & Frameworks:**
- ✅ FastAPI (Web framework)
- ✅ Django (Web framework)
- ✅ SQLAlchemy (ORM)
- ✅ Pydantic (Validation)
- ✅ Pytest (Testing)
- ✅ JWT (Authentication)
- ✅ Bcrypt (Security)

**Best Practices:**
- ✅ Clean Code principles
- ✅ RESTful API design
- ✅ MVC/MVT architecture
- ✅ Dependency Injection
- ✅ Environment variables
- ✅ Git version control

---

### 11. THÁCH THỨC VÀ GIẢI PHÁP (2 phút)

#### 11.1. Các thách thức gặp phải

**Thách thức 1: Tích hợp FastAPI + Django**
- **Vấn đề:** Hai framework chạy trên hai ports khác nhau
- **Giải pháp:** 
  - Sử dụng CORS để cho phép cross-origin requests
  - Tạo script `run_both_servers.py` để chạy đồng thời
  - Frontend gọi Backend qua REST API

**Thách thức 2: Dashboard không hiển thị dữ liệu**
- **Vấn đề:** Dashboard mặc định lọc theo tháng hiện tại (không có data)
- **Giải pháp:**
  - Thay đổi logic để hiển thị ALL TIME data mặc định
  - Thêm date range filter để user tùy chọn
  - Fix bug trong `get_category_breakdown` và `get_trend_data`

**Thách thức 3: Performance với dữ liệu lớn**
- **Vấn đề:** 26K+ transactions có thể làm chậm queries
- **Giải pháp:**
  - Sử dụng pagination
  - Indexing trên database
  - Optimize SQL queries với SQLAlchemy
  - Lazy loading cho relationships

**Thách thức 4: Bảo mật**
- **Vấn đề:** Protect sensitive data và prevent attacks
- **Giải pháp:**
  - Password hashing với bcrypt
  - JWT token authentication
  - Input validation với Pydantic
  - SQL injection prevention với ORM
  - CORS configuration

---

### 12. HƯỚNG PHÁT TRIỂN (2 phút)

#### 12.1. Tính năng mở rộng

**Ngắn hạn:**
- 📱 Mobile responsive improvements
- 📊 Export reports (PDF, Excel)
- 🔔 Notifications & Reminders
- 💾 Backup & Restore data
- 🌙 Dark mode
- 🌐 Multi-language support

**Trung hạn:**
- 📈 Budget planning & tracking
- 🎯 Financial goals setting
- 📧 Email notifications
- 📱 Mobile app (React Native/Flutter)
- 🔄 Recurring transactions
- 💳 Bank integration (API)

**Dài hạn:**
- 🤖 AI-powered insights & predictions
- 👥 Family/Group accounts
- 💰 Investment tracking
- 📊 Advanced analytics & ML
- ☁️ Cloud deployment
- 🔐 Two-factor authentication

#### 12.2. Cải tiến kỹ thuật

**Backend:**
- Migrate to PostgreSQL/MySQL
- Implement caching (Redis)
- Add background tasks (Celery)
- Microservices architecture
- GraphQL API

**Frontend:**
- Migrate to React/Vue.js
- Progressive Web App (PWA)
- Real-time updates (WebSocket)
- Better state management

**DevOps:**
- Docker containerization
- CI/CD pipeline
- Cloud deployment (AWS/Azure/GCP)
- Monitoring & logging
- Load balancing

---

### 13. KẾT LUẬN (2 phút)

#### 13.1. Tổng kết

**Đồ án đã hoàn thành:**
- ✅ Xây dựng thành công ứng dụng web quản lý tài chính cá nhân
- ✅ Áp dụng đầy đủ kiến thức Python đã học
- ✅ Tích hợp nhiều công nghệ hiện đại
- ✅ Tạo dữ liệu test thực tế (51 users, 26K+ transactions)
- ✅ Viết và pass 40 unit tests
- ✅ Hoàn thiện documentation

**Kỹ năng đạt được:**
- 💻 Lập trình Python nâng cao
- 🌐 Web development (Backend + Frontend)
- 🗄️ Database design & ORM
- 🔐 Authentication & Security
- 📊 Data visualization
- 🧪 Testing & Quality Assurance
- 📝 Documentation & Presentation

**Giá trị thực tế:**
- Sản phẩm có thể sử dụng thực tế
- Giải quyết vấn đề quản lý tài chính cá nhân
- Có thể mở rộng thành sản phẩm thương mại

#### 13.2. Cảm nhận cá nhân

**Những điều học được:**
- Hiểu sâu về kiến trúc web application
- Kỹ năng debug và problem solving
- Làm việc với documentation
- Time management trong dự án lớn

**Khó khăn:**
- Tích hợp nhiều công nghệ mới
- Debug các lỗi phức tạp
- Tối ưu performance
- Viết documentation đầy đủ

**Thành công:**
- Hoàn thành đúng deadline
- Sản phẩm chạy ổn định
- Code quality tốt
- User experience tốt

---

## 📚 TÀI LIỆU THAM KHẢO

1. **FastAPI Documentation:** https://fastapi.tiangolo.com/
2. **Django Documentation:** https://docs.djangoproject.com/
3. **SQLAlchemy Documentation:** https://docs.sqlalchemy.org/
4. **Bootstrap Documentation:** https://getbootstrap.com/docs/
5. **Chart.js Documentation:** https://www.chartjs.org/docs/
6. **Python Official Documentation:** https://docs.python.org/3/

---

## 🙏 LỜI CẢM ƠN

- **Thầy/Cô giảng viên:** Cảm ơn sự hướng dẫn và hỗ trợ nhiệt tình
- **Gia đình:** Động viên và tạo điều kiện để hoàn thành đồ án
- **Bạn bè:** Góp ý và test sản phẩm

---

## ❓ HỎI & ĐÁP

**Sẵn sàng trả lời các câu hỏi từ hội đồng!**

---

**CẢM ƠN QUÝ THẦY CÔ ĐÃ LẮNG NGHE!** 🎉

