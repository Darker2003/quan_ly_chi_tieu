"""
MoneyFlow Web Views
"""
import json
import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render


def index(request):
    """Home page - redirect to dashboard if logged in, else login"""
    if request.session.get('access_token'):
        return redirect('dashboard')
    return redirect('login')


def login_view(request):
    """Login page"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            response = requests.post(
                f"{settings.FASTAPI_BASE_URL}/auth/login",
                json={"email": email, "password": password}
            )

            if response.status_code == 200:
                data = response.json()
                request.session['access_token'] = data['access_token']
                request.session['user'] = data['user']
                messages.success(request, 'Đăng nhập thành công!')
                return redirect('dashboard')
            else:
                error_data = response.json()
                messages.error(request, error_data.get('detail', 'Đăng nhập thất bại'))
        except Exception as e:
            messages.error(request, f'Lỗi kết nối: {str(e)}')

    return render(request, 'web/login.html')


def register_view(request):
    """Registration page"""
    if request.method == 'POST':
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Mật khẩu không khớp')
            return render(request, 'web/register.html')

        try:
            response = requests.post(
                f"{settings.FASTAPI_BASE_URL}/auth/register",
                json={
                    "email": email,
                    "full_name": full_name,
                    "password": password
                }
            )

            if response.status_code == 200:
                data = response.json()
                request.session['access_token'] = data['access_token']
                request.session['user'] = data['user']
                messages.success(request, 'Đăng ký thành công!')
                return redirect('dashboard')
            else:
                error_data = response.json()
                messages.error(request, error_data.get('detail', 'Đăng ký thất bại'))
        except Exception as e:
            messages.error(request, f'Lỗi kết nối: {str(e)}')

    return render(request, 'web/register.html')


def logout_view(request):
    """Logout"""
    request.session.flush()
    messages.success(request, 'Đã đăng xuất')
    return redirect('login')


def dashboard(request):
    """Dashboard page with optional date range filter"""
    print("DEBUG: Dashboard view called!")
    if not request.session.get('access_token'):
        print("DEBUG: No access token, redirecting to login")
        return redirect('login')

    token = request.session.get('access_token')
    print(f"DEBUG: Token from session: {token[:20] if token else 'None'}...")
    headers = {'Authorization': f'Bearer {token}'}

    # Get date range from request (if provided)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Build params for API request
    params = {}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date

    try:
        # Get dashboard data with optional date range
        print(f"DEBUG: Calling backend API: {settings.FASTAPI_BASE_URL}/analytics/dashboard")
        print(f"DEBUG: Headers: {headers}")
        print(f"DEBUG: Params: {params}")
        
        response = requests.get(
            f"{settings.FASTAPI_BASE_URL}/analytics/dashboard",
            headers=headers,
            params=params
        )

        print(f"DEBUG: Response status: {response.status_code}")
        if response.status_code == 200:
            dashboard_data = response.json()
            print(f"DEBUG: Dashboard data received: {list(dashboard_data.keys())}")
            print(f"DEBUG: Category breakdown: {len(dashboard_data.get('category_breakdown', []))} items")
            print(f"DEBUG: Monthly comparison: {len(dashboard_data.get('monthly_comparison', []))} items")
        else:
            dashboard_data = {}
            print(f"DEBUG: Dashboard API failed: {response.status_code} - {response.text}")
            messages.error(request, 'Không thể tải dữ liệu dashboard')
    except Exception as e:
        dashboard_data = {}
        print(f"DEBUG: Dashboard API error: {str(e)}")
        messages.error(request, f'Lỗi kết nối: {str(e)}')
    
    # FIX: Ensure dashboard_data is not empty
    if not dashboard_data:
        print("DEBUG: dashboard_data is empty, using mock data")
        dashboard_data = {
            'summary': {
                'total_income': 0,
                'total_expense': 0,
                'balance': 0,
                'transaction_count': 0
            },
            'category_breakdown': [],
            'monthly_comparison': [],
            'trend_data': [],
            'recent_transactions': []
        }

    context = {
        'user': request.session.get('user'),
        'dashboard_data': dashboard_data,
        'dashboard_data_json': json.dumps(dashboard_data),
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'web/dashboard.html', context)


def transactions(request):
    """Transactions list page"""
    if not request.session.get('access_token'):
        return redirect('login')

    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    # Get filter parameters
    category_id = request.GET.get('category_id')
    transaction_type = request.GET.get('type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    params = {}
    if category_id:
        params['category_id'] = category_id
    if transaction_type:
        params['type'] = transaction_type
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date

    try:
        # Get transactions
        response = requests.get(
            f"{settings.FASTAPI_BASE_URL}/transactions/",
            headers=headers,
            params=params
        )

        if response.status_code == 200:
            transactions_data = response.json()
        else:
            transactions_data = []
            messages.error(request, 'Không thể tải danh sách giao dịch')

        # Get categories for filter
        cat_response = requests.get(
            f"{settings.FASTAPI_BASE_URL}/categories/",
            headers=headers
        )
        categories = cat_response.json() if cat_response.status_code == 200 else []

    except Exception as e:
        transactions_data = []
        categories = []
        messages.error(request, f'Lỗi kết nối: {str(e)}')

    context = {
        'user': request.session.get('user'),
        'transactions': transactions_data,
        'categories': categories,
        'filters': {
            'category_id': category_id,
            'type': transaction_type,
            'start_date': start_date,
            'end_date': end_date
        }
    }
    return render(request, 'web/transactions.html', context)


def add_transaction(request):
    """Add transaction page"""
    if not request.session.get('access_token'):
        return redirect('login')

    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    if request.method == 'POST':
        try:
            transaction_data = {
                'amount': float(request.POST.get('amount')),
                'description': request.POST.get('description'),
                'date': request.POST.get('date'),
                'type': request.POST.get('type'),
                'category_id': int(request.POST.get('category_id')),
                'notes': request.POST.get('notes', '')
            }

            response = requests.post(
                f"{settings.FASTAPI_BASE_URL}/transactions/",
                headers=headers,
                json=transaction_data
            )

            if response.status_code == 201:
                messages.success(request, 'Thêm giao dịch thành công!')
                return redirect('transactions')
            else:
                error_data = response.json()
                messages.error(request, error_data.get('detail', 'Thêm giao dịch thất bại'))
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')

    # Get categories
    try:
        response = requests.get(
            f"{settings.FASTAPI_BASE_URL}/categories/",
            headers=headers
        )
        categories = response.json() if response.status_code == 200 else []
    except:
        categories = []

    context = {
        'user': request.session.get('user'),
        'categories': categories
    }
    return render(request, 'web/add_transaction.html', context)


def analytics(request):
    """Analytics page"""
    if not request.session.get('access_token'):
        return redirect('login')

    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    try:
        # Get financial summary
        summary_response = requests.get(
            f"{settings.FASTAPI_BASE_URL}/analytics/summary",
            headers=headers
        )
        summary = summary_response.json() if summary_response.status_code == 200 else {}

        # Get category breakdown (only expenses for pie chart)
        breakdown_response = requests.get(
            f"{settings.FASTAPI_BASE_URL}/analytics/category-breakdown",
            headers=headers,
            params={'type': 'expense'}
        )
        breakdown = breakdown_response.json() if breakdown_response.status_code == 200 else []

        # Get monthly comparison
        monthly_response = requests.get(
            f"{settings.FASTAPI_BASE_URL}/analytics/monthly-comparison",
            headers=headers
        )
        monthly = monthly_response.json() if monthly_response.status_code == 200 else []

    except Exception as e:
        summary = {}
        breakdown = []
        monthly = []
        messages.error(request, f'Lỗi kết nối: {str(e)}')

    context = {
        'user': request.session.get('user'),
        'summary': summary,
        'breakdown': breakdown,
        'monthly': monthly,
        'summary_json': json.dumps(summary),
        'breakdown_json': json.dumps(breakdown),
        'monthly_json': json.dumps(monthly)
    }
    return render(request, 'web/analytics.html', context)


def admin_dashboard(request):
    """Admin dashboard page"""
    if not request.session.get('access_token'):
        return redirect('login')

    user = request.session.get('user')
    if not user.get('is_admin'):
        messages.error(request, 'Bạn không có quyền truy cập trang này')
        return redirect('dashboard')

    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    try:
        # Get admin stats
        stats_response = requests.get(
            f"{settings.FASTAPI_BASE_URL}/admin/stats",
            headers=headers
        )

        if stats_response.status_code == 200:
            stats = stats_response.json()
        else:
            stats = {}
            messages.error(request, 'Không thể tải thống kê hệ thống')

        # Get users list
        search = request.GET.get('search', '')
        is_active = request.GET.get('is_active', '')
        is_admin = request.GET.get('is_admin', '')

        params = {}
        if search:
            params['search'] = search
        if is_active:
            params['is_active'] = is_active == 'true'
        if is_admin:
            params['is_admin'] = is_admin == 'true'

        users_response = requests.get(
            f"{settings.FASTAPI_BASE_URL}/admin/users",
            headers=headers,
            params=params
        )

        if users_response.status_code == 200:
            users = users_response.json()
        else:
            users = []
            messages.error(request, 'Không thể tải danh sách người dùng')

    except Exception as e:
        stats = {}
        users = []
        messages.error(request, f'Lỗi kết nối: {str(e)}')

    context = {
        'user': user,
        'stats': stats,
        'users': users,
        'filters': {
            'search': search,
            'is_active': is_active,
            'is_admin': is_admin
        }
    }
    return render(request, 'web/admin_dashboard.html', context)


def admin_user_detail(request, user_id):
    """Admin user detail page"""
    if not request.session.get('access_token'):
        return redirect('login')

    user = request.session.get('user')
    if not user.get('is_admin'):
        messages.error(request, 'Bạn không có quyền truy cập trang này')
        return redirect('dashboard')

    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    if request.method == 'POST':
        # Update user
        data = {
            'full_name': request.POST.get('full_name'),
            'email': request.POST.get('email'),
            'is_active': request.POST.get('is_active') == 'on',
            'is_admin': request.POST.get('is_admin') == 'on'
        }

        try:
            response = requests.put(
                f"{settings.FASTAPI_BASE_URL}/admin/users/{user_id}",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                messages.success(request, 'Cập nhật người dùng thành công!')
                return redirect('admin_user_detail', user_id=user_id)
            else:
                error_data = response.json()
                messages.error(request, error_data.get('detail', 'Cập nhật thất bại'))
        except Exception as e:
            messages.error(request, f'Lỗi kết nối: {str(e)}')

    try:
        # Get user details
        response = requests.get(
            f"{settings.FASTAPI_BASE_URL}/admin/users/{user_id}",
            headers=headers
        )

        if response.status_code == 200:
            user_data = response.json()
        else:
            messages.error(request, 'Không thể tải thông tin người dùng')
            return redirect('admin_dashboard')

    except Exception as e:
        messages.error(request, f'Lỗi kết nối: {str(e)}')
        return redirect('admin_dashboard')

    context = {
        'user': user,
        'user_data': user_data
    }
    return render(request, 'web/admin_user_detail.html', context)


def admin_delete_user(request, user_id):
    """Admin delete user"""
    if not request.session.get('access_token'):
        return redirect('login')

    user = request.session.get('user')
    if not user.get('is_admin'):
        messages.error(request, 'Bạn không có quyền truy cập trang này')
        return redirect('dashboard')

    if request.method == 'POST':
        token = request.session.get('access_token')
        headers = {'Authorization': f'Bearer {token}'}

        try:
            response = requests.delete(
                f"{settings.FASTAPI_BASE_URL}/admin/users/{user_id}",
                headers=headers
            )

            if response.status_code == 200:
                messages.success(request, 'Xóa người dùng thành công!')
            else:
                error_data = response.json()
                messages.error(request, error_data.get('detail', 'Xóa thất bại'))
        except Exception as e:
            messages.error(request, f'Lỗi kết nối: {str(e)}')

    return redirect('admin_dashboard')
