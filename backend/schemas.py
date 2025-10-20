"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class TransactionType(str, Enum):
    """Transaction type enumeration"""

    INCOME = "income"
    EXPENSE = "expense"


# User Schemas
class UserBase(BaseModel):
    """Base user schema"""

    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """User creation schema - REQ-F-001"""

    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """User login schema - REQ-F-003"""

    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """User update schema - REQ-F-017"""

    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class PasswordChange(BaseModel):
    """Password change schema - REQ-F-018"""

    old_password: str
    new_password: str = Field(..., min_length=6, max_length=100)


class PasswordReset(BaseModel):
    """Password reset schema - REQ-F-004"""

    email: EmailStr


class UserResponse(UserBase):
    """User response schema"""

    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response"""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# Category Schemas
class CategoryBase(BaseModel):
    """Base category schema"""

    name: str = Field(..., min_length=1, max_length=50)
    type: TransactionType


class CategoryCreate(CategoryBase):
    """Category creation schema - REQ-F-012"""

    pass


class CategoryUpdate(BaseModel):
    """Category update schema - REQ-F-012"""

    name: Optional[str] = Field(None, min_length=1, max_length=50)
    type: Optional[TransactionType] = None


class CategoryResponse(CategoryBase):
    """Category response schema"""

    id: int
    is_default: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Transaction Schemas
class TransactionBase(BaseModel):
    """Base transaction schema"""

    amount: float = Field(..., gt=0)
    description: str = Field(..., min_length=1, max_length=200)
    date: date
    type: TransactionType
    category_id: int
    notes: Optional[str] = Field(None, max_length=500)


class TransactionCreate(TransactionBase):
    """Transaction creation schema - REQ-F-006"""

    pass


class TransactionUpdate(BaseModel):
    """Transaction update schema - REQ-F-008"""

    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, min_length=1, max_length=200)
    date: Optional[date] = None
    type: Optional[TransactionType] = None
    category_id: Optional[int] = None
    notes: Optional[str] = Field(None, max_length=500)


class TransactionResponse(TransactionBase):
    """Transaction response schema"""

    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    category: CategoryResponse

    class Config:
        from_attributes = True


class TransactionFilter(BaseModel):
    """Transaction filter schema - REQ-F-010"""

    category_id: Optional[int] = None
    type: Optional[TransactionType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    search: Optional[str] = None


# Analytics Schemas
class FinancialSummary(BaseModel):
    """Financial summary schema - REQ-F-013"""

    total_income: float
    total_expense: float
    balance: float
    period_start: date
    period_end: date


class CategoryBreakdown(BaseModel):
    """Category breakdown for pie chart - REQ-F-014"""

    category_name: str
    category_id: int
    amount: float
    percentage: float
    type: TransactionType


class MonthlyComparison(BaseModel):
    """Monthly comparison for bar chart - REQ-F-015"""

    month: str
    year: int
    total_income: float
    total_expense: float
    balance: float


class TrendData(BaseModel):
    """Trend data for line chart - REQ-F-016"""

    date: date
    amount: float
    type: TransactionType


class AnalyticsResponse(BaseModel):
    """Complete analytics response"""

    summary: FinancialSummary
    category_breakdown: List[CategoryBreakdown]
    monthly_comparison: List[MonthlyComparison]
    trend_data: List[TrendData]


# Generic Response
class MessageResponse(BaseModel):
    """Generic message response"""

    message: str
    success: bool = True
