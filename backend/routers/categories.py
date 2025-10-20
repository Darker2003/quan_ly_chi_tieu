"""
Category management router - REQ-F-011 to REQ-F-012
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Category, User
from ..schemas import CategoryCreate, CategoryResponse, CategoryUpdate, MessageResponse
from ..security import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get all categories (default + user's custom categories) - REQ-F-011
    """
    # Get default categories and user's custom categories
    categories = (
        db.query(Category)
        .filter((Category.is_default == True) | (Category.user_id == current_user.id))
        .all()
    )

    return [CategoryResponse.from_orm(cat) for cat in categories]


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new custom category - REQ-F-012
    """
    # Check if category with same name already exists for this user
    existing = (
        db.query(Category)
        .filter(
            Category.name == category_data.name, Category.user_id == current_user.id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists",
        )

    new_category = Category(
        name=category_data.name,
        type=category_data.type.value,
        user_id=current_user.id,
        is_default=False,
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return CategoryResponse.from_orm(new_category)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a custom category - REQ-F-012
    """
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    # Check if it's a default category or belongs to another user
    if category.is_default:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify default categories",
        )

    if category.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify another user's category",
        )

    # Update fields
    if category_data.name is not None:
        category.name = category_data.name
    if category_data.type is not None:
        category.type = category_data.type.value

    db.commit()
    db.refresh(category)

    return CategoryResponse.from_orm(category)


@router.delete("/{category_id}", response_model=MessageResponse)
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a custom category - REQ-F-012
    """
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    # Check if it's a default category or belongs to another user
    if category.is_default:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete default categories",
        )

    if category.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete another user's category",
        )

    # Check if category has transactions
    from ..models import Transaction

    has_transactions = (
        db.query(Transaction).filter(Transaction.category_id == category_id).first()
    )

    if has_transactions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with existing transactions",
        )

    db.delete(category)
    db.commit()

    return MessageResponse(message="Category deleted successfully", success=True)
