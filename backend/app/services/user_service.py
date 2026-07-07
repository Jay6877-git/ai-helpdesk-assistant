from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserRegister, UserResponse

class UserService:
    def register_user(self, user: UserRegister, db: Session) -> UserResponse:
        new_user = User(
            email=user.email,
            full_name=user.full_name,
            password_hash= user.password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return UserResponse(
            id = new_user.id,
            email = new_user.email,
            full_name = new_user.full_name
        )

user_service = UserService()