"""
Test dashboard API endpoint
"""

import requests

print("=" * 70)
print("TESTING DASHBOARD API")
print("=" * 70)

# Login
print("\n1. Logging in...")
login_response = requests.post(
    'http://127.0.0.1:8001/api/auth/login',
    json={
        'email': 'lethanh@outlook.com',
        'password': 'password123'
    }
)

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
    exit(1)

login_data = login_response.json()
token = login_data['access_token']
print(f"✅ Login successful")
print(f"   Token: {token[:50]}...")

# Get dashboard data
print("\n2. Getting dashboard data...")
dashboard_response = requests.get(
    'http://127.0.0.1:8001/api/analytics/dashboard',
    headers={'Authorization': f'Bearer {token}'}
)

print(f"   Status Code: {dashboard_response.status_code}")

if dashboard_response.status_code == 200:
    dashboard_data = dashboard_response.json()
    print(f"✅ Dashboard data retrieved successfully")
    print(f"\n📊 Dashboard Data:")
    print(f"   Total Income:  {dashboard_data.get('total_income', 0):>15,.0f} VND")
    print(f"   Total Expense: {dashboard_data.get('total_expense', 0):>15,.0f} VND")
    print(f"   Balance:       {dashboard_data.get('balance', 0):>15,.0f} VND")
    print(f"   Transactions:  {dashboard_data.get('transaction_count', 0):>15,}")
    
    if dashboard_data.get('total_income', 0) == 0:
        print("\n⚠️  WARNING: Dashboard shows 0 income!")
        print("   This means the API is not returning the correct data.")
    else:
        print("\n✅ Dashboard data looks correct!")
else:
    print(f"❌ Failed to get dashboard data: {dashboard_response.status_code}")
    print(dashboard_response.text)

print("=" * 70)

