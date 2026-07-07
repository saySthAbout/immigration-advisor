"""EasyVisa.csv 기반 비자 승인 확률(case_status) 분류 모델 학습.

Random Forest / XGBoost / LightGBM 3개를 학습해 hold-out F1/ROC-AUC로 비교하고,
가장 성능이 좋은 모델만 서빙용으로 저장한다(CatBoost는 이미 3개로 충분한 비교가
되고 의존성을 늘리고 싶지 않아 제외했다 - 필요하면 나중에 추가 비교 가능).

전처리(단위 통일, 컬럼 인코딩)는 전부 sklearn Pipeline 안에 포함시켜서
학습/서빙 시점의 인코딩 불일치가 나지 않도록 한다 - 저장된 파이프라인 하나만
로드하면 원본 컬럼 그대로 넣어서 바로 추론할 수 있다.
"""

import json

import joblib
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier

from app.feature_config import CATEGORICAL_FEATURES, MODEL_DIR, MODEL_PATH, NUMERIC_FEATURES, SUMMARY_PATH, TARGET
from app.training.preprocess_easyvisa import PROCESSED_PATH, preprocess


def _build_pipeline(classifier) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ],
        remainder="passthrough",  # NUMERIC_FEATURES는 그대로 통과
    )
    return Pipeline(steps=[("preprocess", preprocessor), ("classifier", classifier)])


def train() -> None:
    if not PROCESSED_PATH.exists():
        preprocess()
    df = pd.read_csv(PROCESSED_PATH)

    features = CATEGORICAL_FEATURES + NUMERIC_FEATURES
    X = df[features]
    y = (df[TARGET] == "Certified").astype(int)  # 1 = Certified(승인), 0 = Denied(거부)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    candidates = {
        "random_forest": RandomForestClassifier(n_estimators=300, max_depth=12, random_state=42),
        "xgboost": XGBClassifier(
            n_estimators=300, max_depth=6, learning_rate=0.05, random_state=42, eval_metric="logloss"
        ),
        "lightgbm": LGBMClassifier(n_estimators=300, max_depth=8, learning_rate=0.05, random_state=42, verbose=-1),
    }

    results = {}
    best_name, best_pipeline, best_f1 = None, None, -1.0
    for name, clf in candidates.items():
        pipeline = _build_pipeline(clf)
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        y_proba = pipeline.predict_proba(X_test)[:, 1]
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_proba)
        results[name] = {"f1": round(f1, 4), "roc_auc": round(auc, 4)}
        print(f"\n=== {name} ===")
        print(classification_report(y_test, y_pred, target_names=["Denied", "Certified"]))
        print(f"ROC-AUC: {auc:.4f}")

        if f1 > best_f1:
            best_name, best_pipeline, best_f1 = name, pipeline, f1

    print(f"\n최고 성능 모델: {best_name} (F1={best_f1:.4f}) -> {MODEL_PATH}")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_pipeline, MODEL_PATH)
    SUMMARY_PATH.write_text(
        json.dumps(
            {
                "best_model": best_name,
                "results": results,
                "features": features,
                "n_train": len(X_train),
                "n_test": len(X_test),
                "class_balance": y.value_counts(normalize=True).round(4).to_dict(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    train()
