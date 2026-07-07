from pydantic import BaseModel


class OcrTextItem(BaseModel):
    text: str
    confidence: float


class OcrExtractResponse(BaseModel):
    items: list[OcrTextItem]


class DocumentClassificationResponse(BaseModel):
    document_type: str
    probabilities: dict[str, float]
