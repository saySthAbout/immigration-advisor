from fastapi import APIRouter, Depends

from app.core.security import verify_internal_token
from app.schemas import JobFieldRecommendationRequest, JobFieldRecommendationResponse
from app.training.job_recommender import recommend_job_fields

router = APIRouter(prefix="/predict", tags=["job"])


@router.post(
    "/job-field-recommendation",
    response_model=JobFieldRecommendationResponse,
    dependencies=[Depends(verify_internal_token)],
)
def predict_job_field_recommendation(request: JobFieldRecommendationRequest) -> JobFieldRecommendationResponse:
    results = recommend_job_fields(request.iso3, top_n=request.top_n)
    return JobFieldRecommendationResponse(iso3=request.iso3, recommendations=results)
