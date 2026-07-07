from fastapi import FastAPI

from app.routers import visa_proba

app = FastAPI(title="AI Immigration Advisor - ML Service", version="0.1.0")

app.include_router(visa_proba.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
