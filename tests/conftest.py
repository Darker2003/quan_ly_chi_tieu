"""
Pytest configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base, get_db
from backend.main import app
from backend.models import User, Category
from backend.security import get_password_hash

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Seed default categories
    default_categories = [
        {"name": "Ăn uống", "type": "expense"},
        {"name": "Di chuyển", "type": "expense"},
        {"name": "Lương", "type": "income"},
        {"name": "Thưởng", "type": "income"},
    ]

    for cat_data in default_categories:
        category = Category(
            name=cat_data["name"], type=cat_data["type"], is_default=True, user_id=None
        )
        db.add(category)

    db.commit()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override"""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        email="test@example.com",
        full_name="Test User",
        password_hash=get_password_hash("testpassword123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for test user"""
    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_category(db_session, test_user):
    """Create a test category"""
    category = Category(
        name="Test Category", type="expense", user_id=test_user.id, is_default=False
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category
