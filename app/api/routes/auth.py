from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import UserRegister, UserLogin, UserResponse, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.supabase import db
from app.api.deps import get_current_user
from typing import Dict, Any

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserRegister):
    existing_user = await db.get_user_by_email(user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah terdaftar. Silakan gunakan email lain atau login."
        )

    # Initial avatar
    initials = "".join([part[0].upper() for part in user_in.name.split()[:2]]) or "AP"

    user_data = {
        "name": user_in.name,
        "email": user_in.email,
        "hashed_password": get_password_hash(user_in.password),
        "role": "Pendamping",
        "avatar_initials": initials
    }

    created_user = await db.create_user(user_data)
    token = create_access_token({"sub": created_user["email"], "id": created_user["id"]})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse(**created_user)
    }

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    user = await db.get_user_by_email(credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email atau kata sandi salah."
        )

    if not verify_password(credentials.password, user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email atau kata sandi salah."
        )

    token = create_access_token({"sub": user["email"], "id": user["id"]})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse(**user)
    }

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    return UserResponse(**current_user)
