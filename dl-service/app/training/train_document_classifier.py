"""문서 종류 분류기 학습 (여권/신분증/운전면허증/기타).

MIDV-500(github.com/fcakyon/midv500, MIT license)에서 4개 클래스 x 1개국
샘플만 받아 썼다 - 전체 데이터셋은 50개 클래스 x 500개 클립의 원본 영상까지
포함해 총 30GB+라, 클래스당 30장(3장 x 10개 촬영조건)만 골라 640px 이하
JPEG로 변환해 저장했다(원본 tif/영상은 다운로드 직후 삭제). 데이터가 매우
적어서(4클래스 x 30장 = 120장, 클래스당 국가 1개뿐) 이 분류기는 실사용
정확도보다는 "실제 라벨 있는 이미지로 학습한 DL 컴포넌트가 있다"는 것을
보여주는 보조 기능으로 취급해야 한다 - 운영에서 정확도가 기대에 못 미치면
클래스당 국가 다양성을 늘리는 게 최우선 개선 포인트다.
"""

import json
from pathlib import Path

import joblib
import numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from app.training.doc_classifier_config import LABELS, MODEL_DIR, MODEL_PATH, SUMMARY_PATH
from app.training.feature_extractor import extract_features

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "midv500"


def _load_dataset() -> tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    for label in LABELS:
        label_dir = RAW_DIR / label
        for image_path in label_dir.rglob("*.jpg"):
            img = Image.open(image_path)
            X.append(extract_features(img))
            y.append(label)
    return np.array(X), np.array(y)


def train() -> None:
    X, y = _load_dataset()
    print(f"총 {len(X)}장, 클래스별 개수: {dict(zip(*np.unique(y, return_counts=True)))}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    report = classification_report(y_test, y_pred, output_dict=True)
    print(classification_report(y_test, y_pred))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    SUMMARY_PATH.write_text(
        json.dumps(
            {
                "labels": LABELS,
                "n_total": len(X),
                "n_train": len(X_train),
                "n_test": len(X_test),
                "classification_report": report,
                "caveat": "클래스당 국가 1개, 30장뿐이라 실사용 정확도 지표라기보다는 파이프라인 검증용",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"모델 저장: {MODEL_PATH}")


if __name__ == "__main__":
    train()
