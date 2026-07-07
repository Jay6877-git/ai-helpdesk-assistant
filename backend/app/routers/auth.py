from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserRegister, UserResponse
from app.services.user_service import user_service
from app.db.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(
        user: UserRegister,
        db: Session = Depends(get_db)
):
    """Create a new user account and return its public profile fields."""
    return user_service.register_user(user, db)
