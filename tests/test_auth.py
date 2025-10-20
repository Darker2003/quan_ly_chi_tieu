"""
Tests for authentication endpoints - REQ-F-001 to REQ-F-005
"""

import pytest
from fastapi import status


class TestUserRegistration:
    """Test user registration - REQ-F-001"""

    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "full_name": "New User",
                "password": "securepassword123",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["full_name"] == "New User"

    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "full_name": "Another User",
                "password": "password123",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"].lower()

    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "invalid-email",
                "full_name": "Test User",
                "password": "password123",
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_short_password(self, client):
        """Test registration with short password"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                "full_name": "Test User",
                "password": "12345",
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUserLogin:
    """Test user login - REQ-F-003"""

    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "testpassword123"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "test@example.com"

    def test_login_wrong_password(self, client, test_user):
        """Test login with wrong password"""
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "wrongpassword"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post(
            "/api/auth/login",
            json={"email": "nonexistent@example.com", "password": "password123"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestPasswordManagement:
    """Test password management - REQ-F-004, REQ-F-018"""

    def test_change_password_success(self, client, auth_headers):
        """Test successful password change - REQ-F-018"""
        response = client.post(
            "/api/auth/change-password",
            headers=auth_headers,
            json={"old_password": "testpassword123", "new_password": "newpassword123"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["success"] is True

        # Verify can login with new password
        login_response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "newpassword123"},
        )
        assert login_response.status_code == status.HTTP_200_OK

    def test_change_password_wrong_old_password(self, client, auth_headers):
        """Test password change with wrong old password"""
        response = client.post(
            "/api/auth/change-password",
            headers=auth_headers,
            json={"old_password": "wrongpassword", "new_password": "newpassword123"},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_reset_request(self, client, test_user):
        """Test password reset request - REQ-F-004"""
        response = client.post(
            "/api/auth/password-reset-request", json={"email": "test@example.com"}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["success"] is True


class TestLogout:
    """Test logout - REQ-F-005"""

    def test_logout_success(self, client, auth_headers):
        """Test successful logout"""
        response = client.post("/api/auth/logout", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["success"] is True


class TestAuthentication:
    """Test authentication requirements"""

    def test_access_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token"""
        response = client.get("/api/auth/me")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_access_protected_endpoint_with_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token"""
        response = client.get(
            "/api/auth/me", headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user(self, client, auth_headers):
        """Test getting current user info"""
        response = client.get("/api/auth/me", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test User"
