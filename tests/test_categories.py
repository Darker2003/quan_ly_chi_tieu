"""
Tests for category management - REQ-F-011 to REQ-F-012
"""

import pytest
from fastapi import status


class TestCategoryRetrieval:
    """Test category retrieval - REQ-F-011"""

    def test_get_categories_includes_defaults(self, client, auth_headers, db_session):
        """Test that default categories are returned"""
        response = client.get("/api/categories/", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Should have default categories
        assert len(data) >= 4
        category_names = [cat["name"] for cat in data]
        assert "Ăn uống" in category_names
        assert "Lương" in category_names

    def test_get_categories_includes_user_custom(
        self, client, auth_headers, test_category
    ):
        """Test that user's custom categories are returned"""
        response = client.get("/api/categories/", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        category_names = [cat["name"] for cat in data]
        assert "Test Category" in category_names


class TestCategoryCreation:
    """Test category creation - REQ-F-012"""

    def test_create_category_success(self, client, auth_headers):
        """Test successful category creation"""
        response = client.post(
            "/api/categories/",
            headers=auth_headers,
            json={"name": "Custom Category", "type": "expense"},
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Custom Category"
        assert data["type"] == "expense"
        assert data["is_default"] is False

    def test_create_duplicate_category(self, client, auth_headers, test_category):
        """Test creating category with duplicate name"""
        response = client.post(
            "/api/categories/",
            headers=auth_headers,
            json={"name": "Test Category", "type": "expense"},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestCategoryUpdate:
    """Test category update - REQ-F-012"""

    def test_update_category_success(self, client, auth_headers, test_category):
        """Test successful category update"""
        response = client.put(
            f"/api/categories/{test_category.id}",
            headers=auth_headers,
            json={"name": "Updated Category"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Category"

    def test_update_default_category_forbidden(self, client, auth_headers, db_session):
        """Test that default categories cannot be updated"""
        from backend.models import Category

        default_cat = (
            db_session.query(Category).filter(Category.is_default == True).first()
        )

        response = client.put(
            f"/api/categories/{default_cat.id}",
            headers=auth_headers,
            json={"name": "Modified Default"},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestCategoryDeletion:
    """Test category deletion - REQ-F-012"""

    def test_delete_category_success(self, client, auth_headers, db_session, test_user):
        """Test successful category deletion"""
        from backend.models import Category

        category = Category(
            name="To Delete", type="expense", user_id=test_user.id, is_default=False
        )
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)

        response = client.delete(f"/api/categories/{category.id}", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["success"] is True

    def test_delete_default_category_forbidden(self, client, auth_headers, db_session):
        """Test that default categories cannot be deleted"""
        from backend.models import Category

        default_cat = (
            db_session.query(Category).filter(Category.is_default == True).first()
        )

        response = client.delete(
            f"/api/categories/{default_cat.id}", headers=auth_headers
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_category_with_transactions(
        self, client, auth_headers, db_session, test_user
    ):
        """Test that categories with transactions cannot be deleted"""
        from backend.models import Category, Transaction
        from datetime import date

        category = Category(
            name="With Transactions",
            type="expense",
            user_id=test_user.id,
            is_default=False,
        )
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)

        # Add a transaction
        transaction = Transaction(
            amount=50000,
            description="Test",
            date=date.today(),
            type="expense",
            category_id=category.id,
            user_id=test_user.id,
        )
        db_session.add(transaction)
        db_session.commit()

        response = client.delete(f"/api/categories/{category.id}", headers=auth_headers)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
