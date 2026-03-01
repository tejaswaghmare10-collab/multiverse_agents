from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from bson import ObjectId

from database import get_users_collection
from models import RegisterRequest, LoginRequest, TokenResponse, UserResponse, MessageResponse
from auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ─── Register ──────────────────────────────────────────────────────────────────

@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def register(data: RegisterRequest):
    users = get_users_collection()

    # Check if email already exists
    existing = await users.find_one({"email": data.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password and save user
    new_user = {
        "email": data.email,
        "password": hash_password(data.password),
        "created_at": datetime.utcnow(),
    }

    await users.insert_one(new_user)

    return {"message": "User registered successfully. Please login."}


# ─── Login ─────────────────────────────────────────────────────────────────────

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and get JWT token"
)
async def login(data: LoginRequest):
    users = get_users_collection()

    # Find user by email
    user = await users.find_one({"email": data.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    user_id = str(user["_id"])
    token = create_access_token(user_id=user_id, email=user["email"])

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "email": user["email"],
            "created_at": user["created_at"],
        }
    }