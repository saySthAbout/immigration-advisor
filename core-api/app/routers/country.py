from fastapi import APIRouter, HTTPException

from app.clients.base import InternalServiceError
from app.clients.ml_client import recommend_countries
from app.schemas.country import CountryRecommendationRequest, CountryRecommendationResponse

router = APIRouter(prefix="/country", tags=["country"])


@router.post("/recommend", response_model=CountryRecommendationResponse)
async def recommend(request: CountryRecommendationRequest) -> CountryRecommendationResponse:
    try:
        result = await recommend_countries(request.origin_continent, top_n=request.top_n)
    except InternalServiceError as exc:
        raise HTTPException(503, f"국가 추천 서비스에 일시적으로 연결할 수 없습니다: {exc}") from exc
    return CountryRecommendationResponse(**result)
