from fastapi import Depends, HTTPException, Cookie
from sqlalchemy.orm import Session

from app.api.dto.request.CreateUserRequest import CreateUserRequest
from app.api.dto.request.LoginRequest import LoginRequest
from app.database.database import get_db
from app.domain.User import User
from app.domain.UserRepository import UserRepository


class AuthService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.user_repository = UserRepository(db)

    def create_user(self, request: CreateUserRequest) -> User:
        existing_user = self.user_repository.get_by_email(request.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
        user = User(email=request.email, role=request.role)
        return self.user_repository.create(user)

    def login(self, request: LoginRequest) -> User:
        user = self.user_repository.get_by_email(request.email)
        if not user:
            raise HTTPException(status_code=401, detail="존재하지 않는 회원입니다.")
        return user

    def get_current_user(self, x_user_id: str = Cookie(alias="X-User-ID")) -> User:
        if not x_user_id:
            raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

        user = self.user_repository.get_by_id(int(x_user_id))
        if not user:
            raise HTTPException(status_code=401, detail="회원을 찾을 수 없습니다.")

        return user