from pydantic import BaseModel
from app.domain.UserRole import UserRole

class CreateUserRequest(BaseModel):
    role: UserRole
    email: str