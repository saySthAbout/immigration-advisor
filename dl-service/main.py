from fastapi import FastAPI

from app.routers import classify_doc, extract

app = FastAPI(title="AI Immigration Advisor - DL Service", version="0.1.0")

app.include_router(extract.router)
app.include_router(classify_doc.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
