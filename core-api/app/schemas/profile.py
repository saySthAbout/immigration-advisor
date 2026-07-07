from pydantic import BaseModel


class ProfileCreateRequest(BaseModel):
    age: int
    education_level: str
    years_of_experience: float
    language_score: float | None = None
    origin_continent: str
    desired_country: str | None = None


class ProfileResponse(BaseModel):
    id: int
    age: int
    education_level: str
    years_of_experience: float
    language_score: float | None
    origin_continent: str
    desired_country: str | None

    class Config:
        from_attributes = True
