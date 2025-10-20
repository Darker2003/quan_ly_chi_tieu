"""
Tests for transaction management - REQ-F-006 to REQ-F-010
"""

import pytest
from fastapi import status
from datetime import date, timedelta


class TestTransactionCreation:
    """Test transaction creation - REQ-F-006"""

    def test_create_transaction_success(self, client, auth_headers, db_session):
        """Test successful transaction creation"""
        # Get a default category
        from backend.models import Category

        category = db_session.query(Category).filter(Category.name == "Ăn uống").first()

        response = client.post(
            "/api/transactions/",
            headers=auth_headers,
            json={
                "amount": 50000,
                "description": "Lunch at restaurant",
                "date": str(date.today()),
                "type": "expense",
                "category_id": category.id,
                "notes": "With friends",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["amount"] == 50000
        assert data["description"] == "Lunch at restaurant"
        assert data["type"] == "expense"
        assert data["notes"] == "With friends"

    def test_create_transaction_invalid_category(self, client, auth_headers):
        """Test transaction creation with invalid category"""
        response = client.post(
            "/api/transactions/",
            headers=auth_headers,
            json={
                "amount": 50000,
                "description": "Test",
                "date": str(date.today()),
                "type": "expense",
                "category_id": 99999,
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_transaction_type_mismatch(self, client, auth_headers, db_session):
        """Test transaction with mismatched type and category"""
        from backend.models import Category

        expense_category = (
            db_session.query(Category).filter(Category.name == "Ăn uống").first()
        )

        response = client.post(
            "/api/transactions/",
            headers=auth_headers,
            json={
                "amount": 50000,
                "description": "Test",
                "date": str(date.today()),
                "type": "income",  # Mismatch: income type with expense category
                "category_id": expense_category.id,
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestTransactionRetrieval:
    """Test transaction retrieval - REQ-F-007"""

    def test_get_transactions_list(self, client, auth_headers, db_session, test_user):
        """Test getting list of transactions"""
        # Create test transactions
        from backend.models import Transaction, Category

        category = db_session.query(Category).filter(Category.name == "Ăn uống").first()

        for i in range(3):
            transaction = Transaction(
                amount=10000 * (i + 1),
                description=f"Transaction {i+1}",
                date=date.today() - timedelta(days=i),
                type="expense",
                category_id=category.id,
                user_id=test_user.id,
            )
            db_session.add(transaction)
        db_session.commit()

        response = client.get("/api/transactions/", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        # Should be ordered by date descending (newest first)
        assert data[0]["description"] == "Transaction 1"

    def test_get_single_transaction(self, client, auth_headers, db_session, test_user):
        """Test getting a single transaction"""
        from backend.models import Transaction, Category

        category = db_session.query(Category).filter(Category.name == "Ăn uống").first()

        transaction = Transaction(
            amount=50000,
            description="Test Transaction",
            date=date.today(),
            type="expense",
            category_id=category.id,
            user_id=test_user.id,
        )
        db_session.add(transaction)
        db_session.commit()
        db_session.refresh(transaction)

        response = client.get(
            f"/api/transactions/{transaction.id}", headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == transaction.id
        assert data["description"] == "Test Transaction"


class TestTransactionFiltering:
    """Test transaction filtering - REQ-F-010"""

    def test_filter_by_category(self, client, auth_headers, db_session, test_user):
        """Test filtering transactions by category"""
        from backend.models import Transaction, Category

        cat1 = db_session.query(Category).filter(Category.name == "Ăn uống").first()
        cat2 = db_session.query(Category).filter(Category.name == "Di chuyển").first()

        # Create transactions with different categories
        t1 = Transaction(
            amount=50000,
            description="Food",
            date=date.today(),
            type="expense",
            category_id=cat1.id,
            user_id=test_user.id,
        )
        t2 = Transaction(
            amount=30000,
            description="Transport",
            date=date.today(),
            type="expense",
            category_id=cat2.id,
            user_id=test_user.id,
        )
        db_session.add_all([t1, t2])
        db_session.commit()

        response = client.get(
            f"/api/transactions/?category_id={cat1.id}", headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["description"] == "Food"

    def test_filter_by_type(self, client, auth_headers, db_session, test_user):
        """Test filtering transactions by type"""
        from backend.models import Transaction, Category

        expense_cat = (
            db_session.query(Category).filter(Category.name == "Ăn uống").first()
        )
        income_cat = db_session.query(Category).filter(Category.name == "Lương").first()

        t1 = Transaction(
            amount=50000,
            description="Expense",
            date=date.today(),
            type="expense",
            category_id=expense_cat.id,
            user_id=test_user.id,
        )
        t2 = Transaction(
            amount=1000000,
            description="Income",
            date=date.today(),
            type="income",
            category_id=income_cat.id,
            user_id=test_user.id,
        )
        db_session.add_all([t1, t2])
        db_session.commit()

        response = client.get("/api/transactions/?type=income", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["type"] == "income"

    def test_filter_by_date_range(self, client, auth_headers, db_session, test_user):
        """Test filtering transactions by date range"""
        from backend.models import Transaction, Category

        category = db_session.query(Category).filter(Category.name == "Ăn uống").first()

        # Create transactions on different dates
        today = date.today()
        t1 = Transaction(
            amount=50000,
            description="Today",
            date=today,
            type="expense",
            category_id=category.id,
            user_id=test_user.id,
        )
        t2 = Transaction(
            amount=30000,
            description="Yesterday",
            date=today - timedelta(days=1),
            type="expense",
            category_id=category.id,
            user_id=test_user.id,
        )
        t3 = Transaction(
            amount=20000,
            description="Last week",
            date=today - timedelta(days=7),
            type="expense",
            category_id=category.id,
            user_id=test_user.id,
        )
        db_session.add_all([t1, t2, t3])
        db_session.commit()

        start_date = today - timedelta(days=2)
        response = client.get(
            f"/api/transactions/?start_date={start_date}", headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2  # Should get today and yesterday


class TestTransactionUpdate:
    """Test transaction update - REQ-F-008"""

    def test_update_transaction_success(
        self, client, auth_headers, db_session, test_user
    ):
        """Test successful transaction update"""
        from backend.models import Transaction, Category

        category = db_session.query(Category).filter(Category.name == "Ăn uống").first()

        transaction = Transaction(
            amount=50000,
            description="Original",
            date=date.today(),
            type="expense",
            category_id=category.id,
            user_id=test_user.id,
        )
        db_session.add(transaction)
        db_session.commit()
        db_session.refresh(transaction)

        response = client.put(
            f"/api/transactions/{transaction.id}",
            headers=auth_headers,
            json={"amount": 75000, "description": "Updated description"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["amount"] == 75000
        assert data["description"] == "Updated description"


class TestTransactionDeletion:
    """Test transaction deletion - REQ-F-009"""

    def test_delete_transaction_success(
        self, client, auth_headers, db_session, test_user
    ):
        """Test successful transaction deletion"""
        from backend.models import Transaction, Category

        category = db_session.query(Category).filter(Category.name == "Ăn uống").first()

        transaction = Transaction(
            amount=50000,
            description="To delete",
            date=date.today(),
            type="expense",
            category_id=category.id,
            user_id=test_user.id,
        )
        db_session.add(transaction)
        db_session.commit()
        db_session.refresh(transaction)

        response = client.delete(
            f"/api/transactions/{transaction.id}", headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["success"] is True

        # Verify transaction is soft deleted
        get_response = client.get(
            f"/api/transactions/{transaction.id}", headers=auth_headers
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
