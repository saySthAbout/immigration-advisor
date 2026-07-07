"""HF Space로 배포된 AI 서비스(ML/DL/LLM)에 대한 공통 내부 통신 클라이언트.

PRD 비기능 요구사항 "결합도 최소화(하나의 서비스가 다운되어도 나머지는 독립
동작)"를 실제로 지키기 위해, 각 호출을 짧은 타임아웃 + 명시적 예외로 감싼다.
라우터 쪽에서 이 예외를 잡아 "그 기능만 실패"로 처리하고 전체 요청을
500으로 죽이지 않도록 한다.
"""

import httpx

from app.core.config import settings


class InternalServiceError(Exception):
    """다운스트림 AI 서비스 호출 실패(타임아웃/네트워크 오류/5xx 등)."""


class InternalServiceClient:
    def __init__(self, base_url: str, timeout: float = 15.0):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    async def post(self, path: str, json: dict) -> dict:
        headers = {"Authorization": f"Bearer {settings.internal_service_token}"}
        try:
            async with httpx.AsyncClient(base_url=self._base_url, timeout=self._timeout) as client:
                response = await client.post(path, json=json, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as exc:
            raise InternalServiceError(
                f"{self._base_url}{path} 응답 오류: {exc.response.status_code}"
            ) from exc
        except httpx.HTTPError as exc:
            raise InternalServiceError(f"{self._base_url}{path} 호출 실패: {exc}") from exc
