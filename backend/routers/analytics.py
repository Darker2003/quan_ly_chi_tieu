"""
Analytics and reporting router - REQ-F-013 to REQ-F-016
"""

from calendar import month_name
from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Category, Transaction, User
from ..schemas import (AnalyticsResponse, CategoryBreakdown, FinancialSummary,
                       MonthlyComparison, TransactionType, TrendData)
from ..security import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=FinancialSummary)
async def get_financial_summary(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get financial summary - REQ-F-013
    Default to current month if no dates provided
    """
    if not start_date or not end_date:
        from datetime import timedelta

        today = date.today()
        start_date = date(today.year, today.month, 1)
        # Get last day of current month
        if today.month == 12:
            end_date = date(today.year, 12, 31)
        else:
            next_month = date(today.year, today.month + 1, 1)
            end_date = next_month - timedelta(days=1)

    # Calculate total income
    total_income = (
        db.query(func.sum(Transaction.amount))
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.type == "income",
            Transaction.is_deleted == False,
            Transaction.date >= start_date,
            Transaction.date <= end_date,
        )
        .scalar()
        or 0.0
    )

    # Calculate total expense
    total_expense = (
        db.query(func.sum(Transaction.amount))
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.type == "expense",
            Transaction.is_deleted == False,
            Transaction.date >= start_date,
            Transaction.date <= end_date,
        )
        .scalar()
        or 0.0
    )

    return FinancialSummary(
        total_income=total_income,
        total_expense=total_expense,
        balance=total_income - total_expense,
        period_start=start_date,
        period_end=end_date,
    )


@router.get("/category-breakdown", response_model=List[CategoryBreakdown])
async def get_category_breakdown(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    type: Optional[TransactionType] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get category breakdown for pie chart - REQ-F-014
    """
    if not start_date or not end_date:
        from datetime import timedelta

        today = date.today()
        start_date = date(today.year, today.month, 1)
        if today.month == 12:
            end_date = date(today.year, 12, 31)
        else:
            next_month = date(today.year, today.month + 1, 1)
            end_date = next_month - timedelta(days=1)

    query = (
        db.query(
            Category.id,
            Category.name,
            Category.type,
            func.sum(Transaction.amount).label("total"),
        )
        .join(Transaction, Transaction.category_id == Category.id)
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.is_deleted == False,
            Transaction.date >= start_date,
            Transaction.date <= end_date,
        )
    )

    if type:
        query = query.filter(Transaction.type == type.value)

    results = query.group_by(Category.id, Category.name, Category.type).all()

    # Calculate total for percentage
    total_amount = sum(r.total for r in results)

    breakdown = []
    for result in results:
        percentage = (result.total / total_amount * 100) if total_amount > 0 else 0
        breakdown.append(
            CategoryBreakdown(
                category_id=result.id,
                category_name=result.name,
                amount=result.total,
                percentage=round(percentage, 2),
                type=TransactionType(result.type),
            )
        )

    return breakdown


@router.get("/monthly-comparison", response_model=List[MonthlyComparison])
async def get_monthly_comparison(
    months: int = Query(6, ge=1, le=24),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get monthly comparison for bar chart - REQ-F-015
    """
    # Get data grouped by year and month
    results = (
        db.query(
            extract("year", Transaction.date).label("year"),
            extract("month", Transaction.date).label("month"),
            Transaction.type,
            func.sum(Transaction.amount).label("total"),
        )
        .filter(Transaction.user_id == current_user.id, Transaction.is_deleted == False)
        .group_by(
            extract("year", Transaction.date),
            extract("month", Transaction.date),
            Transaction.type,
        )
        .order_by(
            extract("year", Transaction.date).desc(),
            extract("month", Transaction.date).desc(),
        )
        .limit(months * 2)
        .all()
    )  # *2 because we have income and expense

    # Organize data by month
    monthly_data = {}
    for result in results:
        key = (int(result.year), int(result.month))
        if key not in monthly_data:
            monthly_data[key] = {
                "year": int(result.year),
                "month": int(result.month),
                "income": 0.0,
                "expense": 0.0,
            }

        if result.type == "income":
            monthly_data[key]["income"] = result.total
        else:
            monthly_data[key]["expense"] = result.total

    # Convert to response format
    comparison = []
    for (year, month), data in sorted(monthly_data.items(), reverse=True)[:months]:
        comparison.append(
            MonthlyComparison(
                month=month_name[month],
                year=year,
                total_income=data["income"],
                total_expense=data["expense"],
                balance=data["income"] - data["expense"],
            )
        )

    return list(reversed(comparison))  # Return in chronological order


@router.get("/trend", response_model=List[TrendData])
async def get_trend_data(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    type: Optional[TransactionType] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get trend data for line chart - REQ-F-016
    """
    if not start_date or not end_date:
        today = date.today()
        start_date = date(today.year, today.month, 1)
        if today.month == 12:
            end_date = date(today.year, 12, 31)
        else:
            end_date = date(today.year, today.month + 1, 1)
            end_date = date(end_date.year, end_date.month, end_date.day - 1)

    query = db.query(
        Transaction.date, Transaction.type, func.sum(Transaction.amount).label("total")
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.is_deleted == False,
        Transaction.date >= start_date,
        Transaction.date <= end_date,
    )

    if type:
        query = query.filter(Transaction.type == type.value)

    results = (
        query.group_by(Transaction.date, Transaction.type)
        .order_by(Transaction.date)
        .all()
    )

    trend = []
    for result in results:
        trend.append(
            TrendData(
                date=result.date, amount=result.total, type=TransactionType(result.type)
            )
        )

    return trend


@router.get("/dashboard", response_model=AnalyticsResponse)
async def get_dashboard_data(
    start_date: Optional[date] = Query(None, description="Start date for dashboard data (default: all time)"),
    end_date: Optional[date] = Query(None, description="End date for dashboard data (default: all time)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get complete dashboard data - combines all analytics
    Supports optional date range filtering
    If no dates provided, shows ALL TIME data
    """
    # Determine date range
    if start_date and end_date:
        # Use provided date range
        filter_start = start_date
        filter_end = end_date
    else:
        # Get ALL transactions (no date filter)
        filter_start = None
        filter_end = None

    # Build base query filters
    base_filters = [
        Transaction.user_id == current_user.id,
        Transaction.is_deleted == False,
    ]

    # Add date filters if provided
    if filter_start:
        base_filters.append(Transaction.date >= filter_start)
    if filter_end:
        base_filters.append(Transaction.date <= filter_end)

    # Calculate total income
    total_income = (
        db.query(func.sum(Transaction.amount))
        .filter(
            *base_filters,
            Transaction.type == "income",
        )
        .scalar()
        or 0.0
    )

    # Calculate total expense
    total_expense = (
        db.query(func.sum(Transaction.amount))
        .filter(
            *base_filters,
            Transaction.type == "expense",
        )
        .scalar()
        or 0.0
    )

    # Get transaction count
    transaction_count = (
        db.query(func.count(Transaction.id))
        .filter(*base_filters)
        .scalar()
        or 0
    )

    # Get actual date range from user's transactions (for display)
    date_range = (
        db.query(
            func.min(Transaction.date),
            func.max(Transaction.date)
        )
        .filter(*base_filters)
        .first()
    )

    display_start = date_range[0] if date_range[0] else date.today()
    display_end = date_range[1] if date_range[1] else date.today()

    # Create summary
    summary = FinancialSummary(
        total_income=total_income,
        total_expense=total_expense,
        balance=total_income - total_expense,
        period_start=display_start,
        period_end=display_end,
        transaction_count=transaction_count,
    )

    # Get category breakdown (use actual date range for display)
    category_breakdown = await get_category_breakdown(
        display_start, display_end, None, current_user, db
    )

    # Get monthly comparison (last 6 months)
    monthly_comparison = await get_monthly_comparison(6, current_user, db)

    # Get trend data (use actual date range for display)
    trend_data = await get_trend_data(display_start, display_end, None, current_user, db)

    return AnalyticsResponse(
        summary=summary,
        category_breakdown=category_breakdown,
        monthly_comparison=monthly_comparison,
        trend_data=trend_data,
    )
