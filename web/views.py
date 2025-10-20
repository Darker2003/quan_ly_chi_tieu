"""
MoneyFlow Web Views
"""
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
    """Dashboard page"""
    if not request.session.get('access_token'):
        return redirect('login')

    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    try:
        # Get dashboard data
        response = requests.get(
            f"{settings.FASTAPI_BASE_URL}/analytics/dashboard",
            headers=headers
        )

        if response.status_code == 200:
            dashboard_data = response.json()
        else:
            dashboard_data = {}
            messages.error(request, 'Không thể tải dữ liệu dashboard')
    except Exception as e:
        dashboard_data = {}
        messages.error(request, f'Lỗi kết nối: {str(e)}')

    context = {
        'user': request.session.get('user'),
        'dashboard_data': dashboard_data
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

        # Get category breakdown
        breakdown_response = requests.get(
            f"{settings.FASTAPI_BASE_URL}/analytics/category-breakdown",
            headers=headers
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
        'monthly': monthly
    }
    return render(request, 'web/analytics.html', context)
