from app.schemas.user import UserRegister, UserResponse

class UserService:
    def register_user(self, user: UserRegister) -> UserResponse:
        return UserResponse(
            id = 1,
            email = user.email,
            full_name = user.full_name
        )

user_service = UserService()