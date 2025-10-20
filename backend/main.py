"""
MoneyFlow FastAPI Backend Application
Main entry point for the API server
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import settings
from .database import init_db, get_db
from .routers import auth, categories, transactions, analytics, users
from sqlalchemy.orm import Session

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Personal Finance Management API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS - REQ-NF-004
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """
    Initialize database and seed default data on startup
    """
    init_db()

    # Seed default categories - REQ-F-011
    from .models import Category

    db = next(get_db())

    default_categories = [
        # Expense categories
        {"name": "Ăn uống", "type": "expense"},
        {"name": "Di chuyển", "type": "expense"},
        {"name": "Mua sắm", "type": "expense"},
        {"name": "Hóa đơn", "type": "expense"},
        {"name": "Giải trí", "type": "expense"},
        {"name": "Y tế", "type": "expense"},
        {"name": "Giáo dục", "type": "expense"},
        {"name": "Nhà ở", "type": "expense"},
        {"name": "Khác", "type": "expense"},
        # Income categories
        {"name": "Lương", "type": "income"},
        {"name": "Thưởng", "type": "income"},
        {"name": "Đầu tư", "type": "income"},
        {"name": "Quà tặng", "type": "income"},
        {"name": "Thu nhập khác", "type": "income"},
    ]

    for cat_data in default_categories:
        existing = (
            db.query(Category)
            .filter(Category.name == cat_data["name"], Category.is_default == True)
            .first()
        )

        if not existing:
            category = Category(
                name=cat_data["name"],
                type=cat_data["type"],
                is_default=True,
                user_id=None,
            )
            db.add(category)

    db.commit()
    db.close()


@app.get("/")
async def root():
    """
    Root endpoint - health check
    """
    return {
        "message": "MoneyFlow API is running",
        "version": "1.0.0",
        "docs": "/api/docs",
    }


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "environment": settings.environment}


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors
    """
    if settings.debug:
        raise exc

    return JSONResponse(
        status_code=500, content={"message": "Internal server error", "success": False}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        reload=settings.debug,
    )
