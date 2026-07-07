from fastapi import APIRouter, Depends, HTTPException

from app.core.security import verify_internal_token
from app.schemas import CountryRecommendationRequest, CountryRecommendationResponse
from app.training.country_recommender import recommend_countries

router = APIRouter(prefix="/predict", tags=["country"])


@router.post(
    "/country-recommendation",
    response_model=CountryRecommendationResponse,
    dependencies=[Depends(verify_internal_token)],
)
def predict_country_recommendation(request: CountryRecommendationRequest) -> CountryRecommendationResponse:
    try:
        results = recommend_countries(request.origin_continent, top_n=request.top_n)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return CountryRecommendationResponse(recommendations=results)
