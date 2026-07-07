from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd
from fastapi import APIRouter, Depends

from app.core.security import verify_internal_token
from app.feature_config import CATEGORICAL_FEATURES, MODEL_PATH, NUMERIC_FEATURES
from app.schemas import VisaProbabilityRequest, VisaProbabilityResponse
from app.training.preprocess_easyvisa import WAGE_TO_ANNUAL_MULTIPLIER

router = APIRouter(prefix="/predict", tags=["visa"])


@lru_cache
def _load_model():
    if not Path(MODEL_PATH).exists():
        raise FileNotFoundError(
            f"{MODEL_PATH} 가 없습니다. app/training/train_visa_classifier.py 를 먼저 실행하세요."
        )
    return joblib.load(MODEL_PATH)


@router.post("/visa-probability", response_model=VisaProbabilityResponse, dependencies=[Depends(verify_internal_token)])
def predict_visa_probability(request: VisaProbabilityRequest) -> VisaProbabilityResponse:
    model = _load_model()

    annual_wage = request.prevailing_wage * WAGE_TO_ANNUAL_MULTIPLIER[request.unit_of_wage]
    row = {
        "continent": request.continent,
        "education_of_employee": request.education_of_employee,
        "has_job_experience": request.has_job_experience,
        "requires_job_training": request.requires_job_training,
        "region_of_employment": request.region_of_employment,
        "full_time_position": request.full_time_position,
        "no_of_employees": abs(request.no_of_employees),
        "yr_of_estab": request.yr_of_estab,
        "annual_wage": annual_wage,
    }
    X = pd.DataFrame([row])[CATEGORICAL_FEATURES + NUMERIC_FEATURES]

    proba_certified = float(model.predict_proba(X)[0, 1])
    predicted_status = "Certified" if proba_certified >= 0.5 else "Denied"

    return VisaProbabilityResponse(approval_probability=round(proba_certified, 4), predicted_status=predicted_status)
