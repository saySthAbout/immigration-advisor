"""EasyVisa.csv 전처리.

원본 데이터의 알려진 이슈 두 가지를 정리한다:
1. prevailing_wage가 unit_of_wage(Year/Month/Week/Hour)별로 단위가 달라 그대로 비교할 수
   없다 - 연봉 기준(annual_wage)으로 환산한 파생 컬럼을 추가한다.
2. no_of_employees에 음수 값이 섞여 있다(데이터 입력 오류로 보임) - 절대값으로 정리한다.
"""

from pathlib import Path

import pandas as pd

RAW_PATH = Path(__file__).resolve().parents[3] / "dataset" / "EasyVisa.csv"
PROCESSED_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "easyvisa_clean.csv"

WAGE_TO_ANNUAL_MULTIPLIER = {"Year": 1, "Month": 12, "Week": 52, "Hour": 2080}


def preprocess() -> pd.DataFrame:
    df = pd.read_csv(RAW_PATH)

    n_negative = (df["no_of_employees"] < 0).sum()
    if n_negative:
        print(f"no_of_employees 음수 {n_negative}건을 절대값으로 정리합니다.")
        df["no_of_employees"] = df["no_of_employees"].abs()

    df["annual_wage"] = df["prevailing_wage"] * df["unit_of_wage"].map(WAGE_TO_ANNUAL_MULTIPLIER)

    df.to_csv(PROCESSED_PATH, index=False)
    print(f"{len(df)}행 저장: {PROCESSED_PATH}")
    return df


if __name__ == "__main__":
    preprocess()
