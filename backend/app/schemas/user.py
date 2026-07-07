from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    """Request body for creating a user account."""

    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    """Request body for authenticating an existing user."""

    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Public user fields returned by the API."""

    id: int
    email: EmailStr
    full_name: str
