from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.dto.request.CreateUserRequest import CreateUserRequest
from app.api.dto.request.LoginRequest import LoginRequest
from app.domain.User import User
from app.domain.UserRepository import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def create_user(self, request: CreateUserRequest) -> User:
        existing_user = self.user_repository.get_by_email(request.email)
        if existing_user:
            raise ValueError("이미 존재하는 이메일입니다.")
        user = User(email=request.email, role=request.role)
        return self.user_repository.create(user)

    def login(self, request: LoginRequest) -> User:
        user = self.user_repository.get_by_email(request.email)
        if not user:
            raise HTTPException(status_code=401, detail="존재하지 않는 회원입니다.")
        return user