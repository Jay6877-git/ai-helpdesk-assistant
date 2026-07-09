from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserRegister, UserResponse
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token

class UserService:
    """Business logic for user account operations."""

    def register_user(self, user: UserRegister, db: Session) -> UserResponse:
        """Persist a new user and return the API response model."""
        new_user = User(
            email=user.email,
            full_name=user.full_name,
            password_hash= hash_password(user.password)
        )

        # Commit first so the database assigns primary-key values, then refresh
        # the model instance before building the response.
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return UserResponse(
            id = new_user.id,
            email = new_user.email,
            full_name = new_user.full_name
        )

    def login_user(self, email: str, password: str, db: Session) -> dict:
        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        token = create_access_token(data={"sub": str(user.id)})

        return {
            "access_token": token,
            "token_type": "bearer"
        }


    def current_user(self, token: str, db: Session) -> UserResponse:
        payload = decode_access_token(token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        return UserResponse(
            id = user.id,
            email = user.email,
            full_name = user.full_name
        )


user_service = UserService()
