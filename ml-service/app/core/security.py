"""core-api <-> ml-service 내부 통신 인증.

외부에는 core-api만 노출되고, 이 서비스는 core-api가 보내는 공유 시크릿
Bearer 토큰(INTERNAL_SERVICE_TOKEN)만 신뢰한다. HF Space Repository Secret과
core-api의 환경변수에 동일한 값이 설정되어 있어야 한다.
"""

from fastapi import Header, HTTPException, status

from app.core.config import settings


async def verify_internal_token(authorization: str = Header(default="")) -> None:
    expected = f"Bearer {settings.internal_service_token}"
    if authorization != expected:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")
