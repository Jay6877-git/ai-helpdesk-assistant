from fastapi import APIRouter
from app.schemas.user import UserRegister, UserResponse
from app.services.user_service import user_service

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserRegister):
    return user_service.register_user(user)
