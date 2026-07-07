from pydantic import BaseModel


class CountryRecommendationRequest(BaseModel):
    origin_continent: str
    top_n: int = 3


class CountryRecommendation(BaseModel):
    iso3: str
    match_score: float
    diaspora_fit: float
    foreign_born_pct: float | None
    naturalization_rate_pct: float | None
    annual_inflow_thousands: float | None
    income_group: str
    cost_of_living_index: float
    local_purchasing_power_index: float


class CountryRecommendationResponse(BaseModel):
    recommendations: list[CountryRecommendation]
