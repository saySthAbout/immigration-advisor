"""학습 스크립트와 서빙 코드가 공유하는 상수만 담은 가벼운 모듈.

document_classifier.py(서빙 경로)가 이 모듈만 가져오면 되고, sklearn 학습
관련 임포트(train_document_classifier.py)를 서빙 경로에 끌어들이지 않는다.
"""

from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parents[2] / "models" / "document_classifier"
MODEL_PATH = MODEL_DIR / "model.joblib"
SUMMARY_PATH = MODEL_DIR / "training_summary.json"

LABELS = ["id", "passport", "drvlic", "other"]
