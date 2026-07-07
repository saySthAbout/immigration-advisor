"""EasyOCR 래퍼 - 별도 학습 없이 사전학습된 텍스트 검출/인식 모델을 그대로 쓴다.

body_guide 프로젝트가 MediaPipe의 사전학습 Pose 모델을 그대로 재사용했던 것과
같은 패턴 - 여권/신분증 텍스트 추출 자체를 처음부터 학습시키는 건 비현실적이고,
이미 검증된 OCR 엔진을 감싸는 게 맞다. PaddleOCR 대신 EasyOCR을 골랐다 -
paddlepaddle 프레임워크 없이 PyTorch(어차피 문서분류기 특징추출에도 씀)만으로
동작해서 이미지가 더 가볍다.
"""

from functools import lru_cache
from io import BytesIO

import easyocr
import numpy as np
from PIL import Image


@lru_cache
def _get_reader() -> easyocr.Reader:
    return easyocr.Reader(["en"], gpu=False, verbose=False)


def extract_text(image_bytes: bytes) -> list[dict]:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    reader = _get_reader()
    results = reader.readtext(np.array(image))
    return [
        {"text": text, "confidence": round(float(confidence), 4)}
        for _bbox, text, confidence in results
    ]
