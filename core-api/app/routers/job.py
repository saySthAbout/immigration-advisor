from fastapi import APIRouter, HTTPException

from app.clients.base import InternalServiceError
from app.clients.ml_client import recommend_job_fields
from app.schemas.job import JobFieldRecommendationRequest, JobFieldRecommendationResponse

router = APIRouter(prefix="/job", tags=["job"])


@router.post("/recommend", response_model=JobFieldRecommendationResponse)
async def recommend(request: JobFieldRecommendationRequest) -> JobFieldRecommendationResponse:
    try:
        result = await recommend_job_fields(request.iso3, top_n=request.top_n)
    except InternalServiceError as exc:
        raise HTTPException(503, f"직군 추천 서비스에 일시적으로 연결할 수 없습니다: {exc}") from exc
    return JobFieldRecommendationResponse(**result)
