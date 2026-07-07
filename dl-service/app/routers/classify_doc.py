from fastapi import APIRouter, Depends, UploadFile

from app.core.security import verify_internal_token
from app.document_classifier import classify_document
from app.schemas import DocumentClassificationResponse

router = APIRouter(prefix="/classify", tags=["document"])


@router.post(
    "/document-type", response_model=DocumentClassificationResponse, dependencies=[Depends(verify_internal_token)]
)
async def classify(file: UploadFile) -> DocumentClassificationResponse:
    image_bytes = await file.read()
    result = classify_document(image_bytes)
    return DocumentClassificationResponse(**result)
