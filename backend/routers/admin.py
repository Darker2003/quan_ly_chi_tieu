"""
Admin router for user management
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from ..database import get_db
from ..models import User, Transaction
from ..schemas import (
    UserAdminResponse,
    UserAdminUpdate,
    MessageResponse,
)
from ..security import get_current_admin_user, get_password_hash

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=List[UserAdminResponse])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_admin: Optional[bool] = None,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Get all users with statistics (admin only)
    """
    query = db.query(User)

    # Apply filters
    if search:
        query = query.filter(
            or_(
                User.full_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
            )
        )

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if is_admin is not None:
        query = query.filter(User.is_admin == is_admin)

    # Get users with pagination
    users = query.offset(skip).limit(limit).all()

    # Build response with statistics
    result = []
    for user in users:
        # Get transaction statistics
        income_total = (
            db.query(func.sum(Transaction.amount))
            .filter(Transaction.user_id == user.id, Transaction.type == "income")
            .scalar()
            or 0
        )

        expense_total = (
            db.query(func.sum(Transaction.amount))
            .filter(Transaction.user_id == user.id, Transaction.type == "expense")
            .scalar()
            or 0
        )

        transaction_count = (
            db.query(func.count(Transaction.id))
            .filter(Transaction.user_id == user.id)
            .scalar()
            or 0
        )

        user_data = UserAdminResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
            is_admin=user.is_admin,
            transaction_count=transaction_count,
            total_income=float(income_total),
            total_expense=float(expense_total),
        )
        result.append(user_data)

    return result


@router.get("/users/{user_id}", response_model=UserAdminResponse)
async def get_user_by_id(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Get specific user details (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Get transaction statistics
    income_total = (
        db.query(func.sum(Transaction.amount))
        .filter(Transaction.user_id == user.id, Transaction.type == "income")
        .scalar()
        or 0
    )

    expense_total = (
        db.query(func.sum(Transaction.amount))
        .filter(Transaction.user_id == user.id, Transaction.type == "expense")
        .scalar()
        or 0
    )

    transaction_count = (
        db.query(func.count(Transaction.id))
        .filter(Transaction.user_id == user.id)
        .scalar()
        or 0
    )

    return UserAdminResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_active=user.is_active,
        is_admin=user.is_admin,
        transaction_count=transaction_count,
        total_income=float(income_total),
        total_expense=float(expense_total),
    )


@router.put("/users/{user_id}", response_model=UserAdminResponse)
async def update_user(
    user_id: int,
    user_data: UserAdminUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Update user information (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Prevent admin from deactivating themselves
    if user.id == current_admin.id and user_data.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account",
        )

    # Prevent admin from removing their own admin status
    if user.id == current_admin.id and user_data.is_admin is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove your own admin status",
        )

    # Check if email is being changed and if it's already taken
    if user_data.email and user_data.email != user.email:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use"
            )
        user.email = user_data.email

    # Update fields
    if user_data.full_name is not None:
        user.full_name = user_data.full_name

    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    if user_data.is_admin is not None:
        user.is_admin = user_data.is_admin

    db.commit()
    db.refresh(user)

    # Get statistics
    income_total = (
        db.query(func.sum(Transaction.amount))
        .filter(Transaction.user_id == user.id, Transaction.type == "income")
        .scalar()
        or 0
    )

    expense_total = (
        db.query(func.sum(Transaction.amount))
        .filter(Transaction.user_id == user.id, Transaction.type == "expense")
        .scalar()
        or 0
    )

    transaction_count = (
        db.query(func.count(Transaction.id))
        .filter(Transaction.user_id == user.id)
        .scalar()
        or 0
    )

    return UserAdminResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_active=user.is_active,
        is_admin=user.is_admin,
        transaction_count=transaction_count,
        total_income=float(income_total),
        total_expense=float(expense_total),
    )


@router.delete("/users/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Delete user permanently (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Prevent admin from deleting themselves
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account",
        )

    db.delete(user)
    db.commit()

    return MessageResponse(message="User deleted successfully", success=True)


@router.get("/stats")
async def get_admin_stats(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Get overall system statistics (admin only)
    """
    total_users = db.query(func.count(User.id)).scalar() or 0
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar() or 0
    admin_users = db.query(func.count(User.id)).filter(User.is_admin == True).scalar() or 0
    total_transactions = db.query(func.count(Transaction.id)).scalar() or 0
    total_income = db.query(func.sum(Transaction.amount)).filter(Transaction.type == "income").scalar() or 0
    total_expense = db.query(func.sum(Transaction.amount)).filter(Transaction.type == "expense").scalar() or 0

    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": total_users - active_users,
        "admin_users": admin_users,
        "total_transactions": total_transactions,
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "net_balance": float(total_income - total_expense),
    }

