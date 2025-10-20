"""
User profile management router - REQ-F-017 to REQ-F-018
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserUpdate, UserResponse, MessageResponse
from ..security import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user profile
    """
    return UserResponse.from_orm(current_user)


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update user profile - REQ-F-017
    """
    # Check if email is being changed and if it's already taken
    if user_data.email and user_data.email != current_user.email:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use"
            )
        current_user.email = user_data.email

    # Update full name
    if user_data.full_name:
        current_user.full_name = user_data.full_name

    db.commit()
    db.refresh(current_user)

    return UserResponse.from_orm(current_user)


@router.delete("/account", response_model=MessageResponse)
async def delete_account(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Deactivate user account (soft delete)
    """
    current_user.is_active = False
    db.commit()

    return MessageResponse(message="Account deactivated successfully", success=True)
