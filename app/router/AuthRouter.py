from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.AuthService import AuthService
from app.api.dto.request.CreateUserRequest import CreateUserRequest
from app.api.dto.request.LoginRequest import LoginRequest

router = APIRouter()

@router.post("/users")
def create_user(request: CreateUserRequest, auth_service: AuthService = Depends(AuthService)):
    user = auth_service.create_user(request)
    return {"message": "회원가입 완료", "user_id": user.id, "email": user.email}

@router.post("/login")
def login(request: LoginRequest, response: Response, auth_service: AuthService = Depends(AuthService)):
    user = auth_service.login(request)
    response.set_cookie(key="X-User-ID", value=str(user.id), httponly=True)
    return {"message": "Login successful", "user_id": user.id}