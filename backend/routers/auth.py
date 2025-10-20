"""
Authentication router - REQ-F-001 to REQ-F-005
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..models import User
from ..schemas import (
    MessageResponse,
    PasswordChange,
    PasswordReset,
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)
from ..security import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user - REQ-F-001
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create new user with hashed password - REQ-F-002
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=get_password_hash(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(new_user.id)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, user=UserResponse.from_orm(new_user))


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login user - REQ-F-003
    """
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, user=UserResponse.from_orm(user))


@router.post("/logout", response_model=MessageResponse)
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user - REQ-F-005
    Note: In JWT-based auth, logout is handled client-side by removing the token
    This endpoint is for consistency and can be used for logging/analytics
    """
    return MessageResponse(message="Successfully logged out", success=True)


@router.post("/password-reset-request", response_model=MessageResponse)
async def password_reset_request(data: PasswordReset, db: Session = Depends(get_db)):
    """
    Request password reset - REQ-F-004
    In production, this would send an email with a reset link
    """
    user = db.query(User).filter(User.email == data.email).first()

    # Always return success to prevent email enumeration
    if user:
        # TODO: In production, generate reset token and send email
        # For now, we'll just log it
        reset_token = create_access_token(
            data={"sub": str(user.id), "type": "password_reset"},
            expires_delta=timedelta(hours=1),
        )
        print(f"Password reset token for {user.email}: {reset_token}")

    return MessageResponse(
        message="If the email exists, a password reset link has been sent", success=True
    )


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Change user password - REQ-F-018
    """
    from ..security import verify_password

    # Verify old password
    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect current password"
        )

    # Update password
    current_user.password_hash = get_password_hash(data.new_password)
    db.commit()

    return MessageResponse(message="Password changed successfully", success=True)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    return UserResponse.from_orm(current_user)
