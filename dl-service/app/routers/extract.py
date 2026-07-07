from fastapi import APIRouter, Depends, UploadFile

from app.core.security import verify_internal_token
from app.ocr_engine import extract_text
from app.schemas import OcrExtractResponse

router = APIRouter(prefix="/extract", tags=["ocr"])


@router.post("/text", response_model=OcrExtractResponse, dependencies=[Depends(verify_internal_token)])
async def extract(file: UploadFile) -> OcrExtractResponse:
    image_bytes = await file.read()
    items = extract_text(image_bytes)
    return OcrExtractResponse(items=items)
