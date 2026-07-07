from app.clients.base import InternalServiceClient
from app.core.config import settings

ml_client = InternalServiceClient(settings.ml_service_url)


async def predict_visa_probability(payload: dict) -> dict:
    return await ml_client.post("/predict/visa-probability", json=payload)


async def recommend_countries(origin_continent: str, top_n: int = 3) -> dict:
    return await ml_client.post(
        "/predict/country-recommendation",
        json={"origin_continent": origin_continent, "top_n": top_n},
    )


async def recommend_job_fields(iso3: str, top_n: int = 5) -> dict:
    return await ml_client.post("/predict/job-field-recommendation", json={"iso3": iso3, "top_n": top_n})
