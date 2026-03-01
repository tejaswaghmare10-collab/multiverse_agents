from fastapi import APIRouter, Depends
from auth import get_current_user
from models import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


# ─── Get Current User (Protected) ─────────────────────────────────────────────

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current logged in user"
)
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    Protected route — requires a valid JWT token in the Authorization header.
    Header format: Authorization: Bearer <token>
    """
    return current_user