"""
Tests for analytics and reporting - REQ-F-013 to REQ-F-016
"""

import pytest
from fastapi import status
from datetime import date, timedelta


class TestFinancialSummary:
    """Test financial summary - REQ-F-013"""

    def test_get_summary_current_month(
        self, client, auth_headers, db_session, test_user
    ):
        """Test getting financial summary for current month"""
        from backend.models import Transaction, Category

        expense_cat = (
            db_session.query(Category).filter(Category.name == "Ăn uống").first()
        )
        income_cat = db_session.query(Category).filter(Category.name == "Lương").first()

        # Create test transactions
        transactions = [
            Transaction(
                amount=1000000,
                description="Salary",
                date=date.today(),
                type="income",
                category_id=income_cat.id,
                user_id=test_user.id,
            ),
            Transaction(
                amount=50000,
                description="Food",
                date=date.today(),
                type="expense",
                category_id=expense_cat.id,
                user_id=test_user.id,
            ),
            Transaction(
                amount=30000,
                description="Transport",
                date=date.today(),
                type="expense",
                category_id=expense_cat.id,
                user_id=test_user.id,
            ),
        ]
        db_session.add_all(transactions)
        db_session.commit()

        response = client.get("/api/analytics/summary", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_income"] == 1000000
        assert data["total_expense"] == 80000
        assert data["balance"] == 920000

    def test_get_summary_custom_date_range(
        self, client, auth_headers, db_session, test_user
    ):
        """Test getting summary for custom date range"""
        from backend.models import Transaction, Category

        category = db_session.query(Category).filter(Category.name == "Ăn uống").first()

        today = date.today()
        last_week = today - timedelta(days=7)

        # Transaction within range
        t1 = Transaction(
            amount=50000,
            description="Recent",
            date=today,
            type="expense",
            category_id=category.id,
            user_id=test_user.id,
        )
        # Transaction outside range
        t2 = Transaction(
            amount=30000,
            description="Old",
            date=last_week - timedelta(days=1),
            type="expense",
            category_id=category.id,
            user_id=test_user.id,
        )
        db_session.add_all([t1, t2])
        db_session.commit()

        response = client.get(
            f"/api/analytics/summary?start_date={last_week}&end_date={today}",
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_expense"] == 50000  # Only recent transaction


class TestCategoryBreakdown:
    """Test category breakdown - REQ-F-014"""

    def test_get_category_breakdown(self, client, auth_headers, db_session, test_user):
        """Test getting category breakdown for pie chart"""
        from backend.models import Transaction, Category

        cat1 = db_session.query(Category).filter(Category.name == "Ăn uống").first()
        cat2 = db_session.query(Category).filter(Category.name == "Di chuyển").first()

        transactions = [
            Transaction(
                amount=60000,
                description="Food 1",
                date=date.today(),
                type="expense",
                category_id=cat1.id,
                user_id=test_user.id,
            ),
            Transaction(
                amount=40000,
                description="Food 2",
                date=date.today(),
                type="expense",
                category_id=cat1.id,
                user_id=test_user.id,
            ),
            Transaction(
                amount=50000,
                description="Transport",
                date=date.today(),
                type="expense",
                category_id=cat2.id,
                user_id=test_user.id,
            ),
        ]
        db_session.add_all(transactions)
        db_session.commit()

        response = client.get("/api/analytics/category-breakdown", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Should have 2 categories
        assert len(data) >= 2

        # Find food category
        food_cat = next(c for c in data if c["category_name"] == "Ăn uống")
        assert food_cat["amount"] == 100000
        assert food_cat["percentage"] > 0

    def test_category_breakdown_by_type(
        self, client, auth_headers, db_session, test_user
    ):
        """Test category breakdown filtered by type"""
        from backend.models import Transaction, Category

        expense_cat = (
            db_session.query(Category).filter(Category.name == "Ăn uống").first()
        )
        income_cat = db_session.query(Category).filter(Category.name == "Lương").first()

        transactions = [
            Transaction(
                amount=50000,
                description="Expense",
                date=date.today(),
                type="expense",
                category_id=expense_cat.id,
                user_id=test_user.id,
            ),
            Transaction(
                amount=1000000,
                description="Income",
                date=date.today(),
                type="income",
                category_id=income_cat.id,
                user_id=test_user.id,
            ),
        ]
        db_session.add_all(transactions)
        db_session.commit()

        response = client.get(
            "/api/analytics/category-breakdown?type=expense", headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Should only have expense categories
        for category in data:
            assert category["type"] == "expense"


class TestMonthlyComparison:
    """Test monthly comparison - REQ-F-015"""

    def test_get_monthly_comparison(self, client, auth_headers, db_session, test_user):
        """Test getting monthly comparison for bar chart"""
        from backend.models import Transaction, Category

        expense_cat = (
            db_session.query(Category).filter(Category.name == "Ăn uống").first()
        )
        income_cat = db_session.query(Category).filter(Category.name == "Lương").first()

        today = date.today()

        # Current month transactions
        t1 = Transaction(
            amount=1000000,
            description="Salary",
            date=today,
            type="income",
            category_id=income_cat.id,
            user_id=test_user.id,
        )
        t2 = Transaction(
            amount=50000,
            description="Food",
            date=today,
            type="expense",
            category_id=expense_cat.id,
            user_id=test_user.id,
        )
        db_session.add_all([t1, t2])
        db_session.commit()

        response = client.get(
            "/api/analytics/monthly-comparison?months=3", headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert isinstance(data, list)
        if len(data) > 0:
            assert "month" in data[0]
            assert "year" in data[0]
            assert "total_income" in data[0]
            assert "total_expense" in data[0]
            assert "balance" in data[0]


class TestTrendData:
    """Test trend data - REQ-F-016"""

    def test_get_trend_data(self, client, auth_headers, db_session, test_user):
        """Test getting trend data for line chart"""
        from backend.models import Transaction, Category

        category = db_session.query(Category).filter(Category.name == "Ăn uống").first()

        today = date.today()

        # Create transactions on different days
        for i in range(5):
            transaction = Transaction(
                amount=10000 * (i + 1),
                description=f"Day {i}",
                date=today - timedelta(days=i),
                type="expense",
                category_id=category.id,
                user_id=test_user.id,
            )
            db_session.add(transaction)
        db_session.commit()

        start_date = today - timedelta(days=7)
        response = client.get(
            f"/api/analytics/trend?start_date={start_date}&end_date={today}",
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 5

        for item in data:
            assert "date" in item
            assert "amount" in item
            assert "type" in item


class TestDashboard:
    """Test complete dashboard - combines all analytics"""

    def test_get_dashboard_data(self, client, auth_headers, db_session, test_user):
        """Test getting complete dashboard data"""
        from backend.models import Transaction, Category

        expense_cat = (
            db_session.query(Category).filter(Category.name == "Ăn uống").first()
        )
        income_cat = db_session.query(Category).filter(Category.name == "Lương").first()

        # Create sample data
        transactions = [
            Transaction(
                amount=1000000,
                description="Salary",
                date=date.today(),
                type="income",
                category_id=income_cat.id,
                user_id=test_user.id,
            ),
            Transaction(
                amount=50000,
                description="Food",
                date=date.today(),
                type="expense",
                category_id=expense_cat.id,
                user_id=test_user.id,
            ),
        ]
        db_session.add_all(transactions)
        db_session.commit()

        response = client.get("/api/analytics/dashboard", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verify all components are present
        assert "summary" in data
        assert "category_breakdown" in data
        assert "monthly_comparison" in data
        assert "trend_data" in data

        # Verify summary data
        assert data["summary"]["total_income"] == 1000000
        assert data["summary"]["total_expense"] == 50000
        assert data["summary"]["balance"] == 950000
