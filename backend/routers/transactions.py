"""
Transaction management router - REQ-F-006 to REQ-F-010
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import date
from ..database import get_db
from ..models import User, Transaction, Category
from ..schemas import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    MessageResponse,
    TransactionType,
)
from ..security import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    category_id: Optional[int] = Query(None),
    type: Optional[TransactionType] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get all transactions with filtering - REQ-F-007, REQ-F-010
    """
    query = db.query(Transaction).filter(
        Transaction.user_id == current_user.id, Transaction.is_deleted == False
    )

    # Apply filters - REQ-F-010
    if category_id:
        query = query.filter(Transaction.category_id == category_id)

    if type:
        query = query.filter(Transaction.type == type.value)

    if start_date:
        query = query.filter(Transaction.date >= start_date)

    if end_date:
        query = query.filter(Transaction.date <= end_date)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Transaction.description.ilike(search_pattern),
                Transaction.notes.ilike(search_pattern),
            )
        )

    # Order by date descending (newest first) - REQ-F-007
    transactions = (
        query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()
    )

    return [TransactionResponse.from_orm(t) for t in transactions]


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get a specific transaction
    """
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == current_user.id,
            Transaction.is_deleted == False,
        )
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )

    return TransactionResponse.from_orm(transaction)


@router.post(
    "/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED
)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new transaction - REQ-F-006
    """
    # Verify category exists and belongs to user or is default
    category = (
        db.query(Category)
        .filter(
            Category.id == transaction_data.category_id,
            or_(Category.user_id == current_user.id, Category.is_default == True),
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    # Verify transaction type matches category type
    if category.type != transaction_data.type.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category type ({category.type}) does not match transaction type ({transaction_data.type.value})",
        )

    new_transaction = Transaction(
        amount=transaction_data.amount,
        description=transaction_data.description,
        date=transaction_data.date,
        type=transaction_data.type.value,
        category_id=transaction_data.category_id,
        notes=transaction_data.notes,
        user_id=current_user.id,
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return TransactionResponse.from_orm(new_transaction)


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a transaction - REQ-F-008
    """
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == current_user.id,
            Transaction.is_deleted == False,
        )
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )

    # Update fields
    if transaction_data.amount is not None:
        transaction.amount = transaction_data.amount

    if transaction_data.description is not None:
        transaction.description = transaction_data.description

    if transaction_data.date is not None:
        transaction.date = transaction_data.date

    if transaction_data.type is not None:
        transaction.type = transaction_data.type.value

    if transaction_data.category_id is not None:
        # Verify new category exists
        category = (
            db.query(Category)
            .filter(
                Category.id == transaction_data.category_id,
                or_(Category.user_id == current_user.id, Category.is_default == True),
            )
            .first()
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )

        transaction.category_id = transaction_data.category_id

    if transaction_data.notes is not None:
        transaction.notes = transaction_data.notes

    db.commit()
    db.refresh(transaction)

    return TransactionResponse.from_orm(transaction)


@router.delete("/{transaction_id}", response_model=MessageResponse)
async def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a transaction - REQ-F-009
    Using soft delete for data integrity
    """
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == current_user.id,
            Transaction.is_deleted == False,
        )
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )

    # Soft delete
    transaction.is_deleted = True
    db.commit()

    return MessageResponse(message="Transaction deleted successfully", success=True)
