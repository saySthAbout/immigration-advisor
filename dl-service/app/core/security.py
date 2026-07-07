from fastapi import Header, HTTPException, status

from app.core.config import settings


async def verify_internal_token(authorization: str = Header(default="")) -> None:
    expected = f"Bearer {settings.internal_service_token}"
    if authorization != expected:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")
