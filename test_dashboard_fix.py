"""Test the dashboard API with date range support"""
from datetime import date, timedelta

import requests

# Login first (using JSON format)
login_data = {
    "email": "lethanh@outlook.com",
    "password": "password123"
}

print("1. Logging in...")
response = requests.post(
    "http://127.0.0.1:8001/api/auth/login",
    json=login_data
)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Get all-time dashboard data (no date filter)
    print("\n2. Testing dashboard - ALL TIME (no date filter)...")
    response = requests.get("http://127.0.0.1:8001/api/analytics/dashboard", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        summary = data["summary"]
        print(f"   ✅ Total Income: {summary['total_income']:,.0f} VND")
        print(f"   ✅ Total Expense: {summary['total_expense']:,.0f} VND")
        print(f"   ✅ Balance: {summary['balance']:,.0f} VND")
        print(f"   ✅ Period: {summary['period_start']} to {summary['period_end']}")
        print(f"   ✅ Transactions: {summary.get('transaction_count', 'N/A')}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test 2: Get dashboard data for specific month (May 2024)
    print("\n3. Testing dashboard - MAY 2024...")
    params = {
        "start_date": "2024-05-01",
        "end_date": "2024-05-31"
    }
    response = requests.get("http://127.0.0.1:8001/api/analytics/dashboard", headers=headers, params=params)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        summary = data["summary"]
        print(f"   ✅ Total Income: {summary['total_income']:,.0f} VND")
        print(f"   ✅ Total Expense: {summary['total_expense']:,.0f} VND")
        print(f"   ✅ Balance: {summary['balance']:,.0f} VND")
        print(f"   ✅ Period: {summary['period_start']} to {summary['period_end']}")
        print(f"   ✅ Transactions: {summary.get('transaction_count', 'N/A')}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test 3: Get dashboard data for this year (2024)
    print("\n4. Testing dashboard - YEAR 2024...")
    params = {
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }
    response = requests.get("http://127.0.0.1:8001/api/analytics/dashboard", headers=headers, params=params)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        summary = data["summary"]
        print(f"   ✅ Total Income: {summary['total_income']:,.0f} VND")
        print(f"   ✅ Total Expense: {summary['total_expense']:,.0f} VND")
        print(f"   ✅ Balance: {summary['balance']:,.0f} VND")
        print(f"   ✅ Period: {summary['period_start']} to {summary['period_end']}")
        print(f"   ✅ Transactions: {summary.get('transaction_count', 'N/A')}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    print("\n✅ All tests completed!")
else:
    print(f"   ❌ Login failed: {response.text}")

