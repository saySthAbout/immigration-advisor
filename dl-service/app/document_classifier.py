from functools import lru_cache
from io import BytesIO
from pathlib import Path

import joblib
from PIL import Image

from app.training.doc_classifier_config import MODEL_PATH
from app.training.feature_extractor import extract_features


@lru_cache
def _load_model():
    if not Path(MODEL_PATH).exists():
        raise FileNotFoundError(
            f"{MODEL_PATH} 가 없습니다. app/training/train_document_classifier.py 를 먼저 실행하세요."
        )
    return joblib.load(MODEL_PATH)


def classify_document(image_bytes: bytes) -> dict:
    image = Image.open(BytesIO(image_bytes))
    model = _load_model()
    features = [extract_features(image)]
    predicted_label = model.predict(features)[0]
    probabilities = dict(zip(model.classes_, model.predict_proba(features)[0].tolist()))
    return {"document_type": predicted_label, "probabilities": probabilities}
