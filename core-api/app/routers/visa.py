from fastapi import APIRouter, HTTPException

from app.clients.base import InternalServiceError
from app.clients.ml_client import predict_visa_probability
from app.schemas.visa import VisaProbabilityRequest, VisaProbabilityResponse

router = APIRouter(prefix="/visa", tags=["visa"])


@router.post("/predict", response_model=VisaProbabilityResponse)
async def predict(request: VisaProbabilityRequest) -> VisaProbabilityResponse:
    try:
        result = await predict_visa_probability(request.model_dump())
    except InternalServiceError as exc:
        # PRD NFR: ML 서비스가 다운돼도 나머지 기능에 영향 없이 이 요청만 실패해야 한다.
        raise HTTPException(503, f"비자 예측 서비스에 일시적으로 연결할 수 없습니다: {exc}") from exc
    return VisaProbabilityResponse(**result)
