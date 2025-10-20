"""
Configuration settings for MoneyFlow FastAPI backend
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # Application
    app_name: str = "MoneyFlow API"
    debug: bool = True
    environment: str = "development"

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    jwt_secret_key: str = "your-jwt-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database
    database_url: str = "sqlite:///./moneyflow.db"

    # Server
    fastapi_host: str = "127.0.0.1"
    fastapi_port: int = 8001

    # CORS
    allowed_origins: List[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]

    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    email_from: str = "noreply@moneyflow.com"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
