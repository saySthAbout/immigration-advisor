from pydantic import BaseModel


class JobFieldRecommendationRequest(BaseModel):
    iso3: str
    top_n: int = 5


class JobFieldRecommendation(BaseModel):
    skill_group_name: str
    skill_group_category: str
    net_migration_per_10k: float


class JobFieldRecommendationResponse(BaseModel):
    iso3: str
    recommendations: list[JobFieldRecommendation]
