"""
Chatbot API endpoints for financial advice and analysis
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from ..database import get_db
from ..security import get_current_user
from ..models import User
from ..chatbot_service import chatbot

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


class ChatMessage(BaseModel):
    """Chat message request model"""
    message: str
    days: Optional[int] = 30  # Number of days to analyze (default 30)


class ChatResponse(BaseModel):
    """Chat response model"""
    success: bool
    response: str
    financial_summary: Optional[dict] = None
    error: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(
    chat_message: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with the financial AI bot
    
    Args:
        chat_message: The user's message and analysis period
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        AI response with financial analysis and advice
    """
    try:
        # Validate days parameter
        if chat_message.days < 1 or chat_message.days > 365:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Days parameter must be between 1 and 365"
            )
        
        # Get AI response
        result = chatbot.chat_with_user(
            db=db,
            user_id=current_user.id,
            message=chat_message.message,
            days=chat_message.days
        )
        
        if not result['success']:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get('error', 'Unknown error occurred')
            )
        
        return ChatResponse(
            success=True,
            response=result['response'],
            financial_summary=result.get('financial_summary')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        ) from e


@router.get("/financial-summary")
async def get_financial_summary(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get financial summary for the user
    
    Args:
        days: Number of days to analyze (default 30)
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Financial summary data
    """
    try:
        if days < 1 or days > 365:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Days parameter must be between 1 and 365"
            )
        
        financial_data = chatbot.get_user_financial_data(
            db=db,
            user_id=current_user.id,
            days=days
        )
        
        return {
            "success": True,
            "data": financial_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting financial summary: {str(e)}"
        ) from e


@router.get("/spending-analysis")
async def get_spending_analysis(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get spending pattern analysis
    
    Args:
        days: Number of days to analyze (default 30)
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Spending analysis and recommendations
    """
    try:
        if days < 1 or days > 365:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Days parameter must be between 1 and 365"
            )
        
        financial_data = chatbot.get_user_financial_data(
            db=db,
            user_id=current_user.id,
            days=days
        )
        
        spending_analysis = chatbot.analyze_spending_patterns(financial_data)
        budget_recommendations = chatbot.get_budget_recommendations(financial_data)
        
        return {
            "success": True,
            "spending_analysis": spending_analysis,
            "budget_recommendations": budget_recommendations,
            "financial_data": financial_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing spending: {str(e)}"
        ) from e


@router.get("/quick-advice")
async def get_quick_financial_advice(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get quick financial advice without chat interaction
    
    Args:
        days: Number of days to analyze (default 30)
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Quick financial advice
    """
    try:
        if days < 1 or days > 365:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Days parameter must be between 1 and 365"
            )
        
        financial_data = chatbot.get_user_financial_data(
            db=db,
            user_id=current_user.id,
            days=days
        )
        
        advice = chatbot.generate_financial_advice(financial_data)
        
        return {
            "success": True,
            "advice": advice,
            "financial_summary": {
                "total_income": financial_data['total_income'],
                "total_expense": financial_data['total_expense'],
                "net_balance": financial_data['net_balance'],
                "period": financial_data['period']
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating advice: {str(e)}"
        ) from e

@router.post("/clear-history")
async def clear_conversation_history(
    current_user: User = Depends(get_current_user)
):
    """Xóa lịch sử trò chuyện của user"""
    try:
        chatbot_service._clear_history(current_user.id)
        return {
            "success": True,
            "message": "Đã xóa lịch sử trò chuyện"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing history: {str(e)}"
        ) from e
