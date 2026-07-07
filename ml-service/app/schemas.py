from pydantic import BaseModel


class VisaProbabilityRequest(BaseModel):
    continent: str
    education_of_employee: str
    has_job_experience: str  # "Y" | "N"
    requires_job_training: str  # "Y" | "N"
    region_of_employment: str
    full_time_position: str  # "Y" | "N"
    no_of_employees: int
    yr_of_estab: int
    prevailing_wage: float
    unit_of_wage: str  # "Year" | "Month" | "Week" | "Hour"


class VisaProbabilityResponse(BaseModel):
    approval_probability: float
    predicted_status: str  # "Certified" | "Denied"


class CountryRecommendationRequest(BaseModel):
    origin_continent: str  # "Asia" | "Europe" | "North America" | "South America" | "Africa" | "Oceania"
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
