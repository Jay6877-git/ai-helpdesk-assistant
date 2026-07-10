from fastapi import APIRouter, Depends

from app.schemas.user import UserResponse
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/users/me", response_model=UserResponse)
def get_me(
        current_user: UserResponse = Depends(get_current_user),
):
    """Return the profile represented by the bearer token."""
    return current_user
