from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
from jose import jwt
from app.schemas import LoginRequest, TokenResponse
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


def create_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    return jwt.encode(
        {"sub": username, "exp": expire},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    if (
        body.username != settings.admin_username
        or body.password != settings.admin_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Noto'g'ri login yoki parol",
        )
    return TokenResponse(access_token=create_token(body.username))
