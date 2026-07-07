"""학습 스크립트와 서빙 라우터가 공유하는 상수.

라우터가 이 모듈만 가져오면 되고 xgboost/lightgbm 같은 학습 전용 무거운
라이브러리를 서빙 경로에 끌어들이지 않는다(joblib.load 자체는 pickle된
객체의 클래스를 각 라이브러리에서 직접 임포트하므로 requirements.txt에는
계속 필요하지만, 이 모듈 자체는 순수 상수만 담는다).
"""

from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parent.parent / "models" / "visa_classifier"
MODEL_PATH = MODEL_DIR / "model.joblib"
SUMMARY_PATH = MODEL_DIR / "training_summary.json"

CATEGORICAL_FEATURES = [
    "continent",
    "education_of_employee",
    "has_job_experience",
    "requires_job_training",
    "region_of_employment",
    "full_time_position",
]
NUMERIC_FEATURES = ["no_of_employees", "yr_of_estab", "annual_wage"]
TARGET = "case_status"
