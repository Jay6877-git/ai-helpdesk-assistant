from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.user_service import user_service
from app.schemas.user import UserResponse

# FastAPI reads bearer tokens from the Authorization header and documents
# `/login` as the token endpoint in the generated OpenAPI schema.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
) -> UserResponse:
    """Resolve the authenticated user for routes that require a bearer token."""
    return user_service.current_user(token=token, db=db)

