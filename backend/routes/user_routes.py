# backend/routes/user_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.feat1.user_service import UserService
from backend.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])
user_repo = UserRepository()
service = UserService(user_repo)


class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(req: RegisterRequest):
    try:
        created = service.register(req.username, req.password, role=req.role or "customer")
        # never return password_hash
        return {"id": created["id"], "username": created["username"], "role": created["role"]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(req: LoginRequest):
    ok = service.login(req.username, req.password)
    if not ok:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}
