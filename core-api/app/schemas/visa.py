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
    predicted_status: str
