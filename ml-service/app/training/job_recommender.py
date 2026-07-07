"""취업 가능 직군 추천 - LinkedIn 'Skill Migration' 실데이터 기반 순위.

country_recommender.py와 같은 이유로 학습된 모델이 아니라 순위 매기기다:
각 국가의 스킬 그룹별 net_per_10K(LinkedIn 회원 1만 명당 순유입) 자체가
"그 나라가 해당 직군의 숙련 인력을 순유입으로 얼마나 끌어들이고 있는지"를
바로 보여주는 실측 지표라, 이걸 다시 다른 피처로 예측하는 회귀 모델을 만드는
건 cost_of_living과 같은 이유로 불필요하다 - 값 자체가 이미 원하는 답이다.
양수가 클수록 그 직군의 숙련 인력이 해당 국가로 순유입되고 있다는 뜻이라
(=취업 수요가 있다는 신호), 상위 스킬 그룹을 그대로 "취업 가능 직군 추천"으로
반환한다.
"""

from pathlib import Path

import pandas as pd

from app.training.country_codes import build_name_to_iso3, normalize_name

RAW_PATH = Path(__file__).resolve().parents[2] / "data" / "raw" / "job_market" / "skill_migration_public.csv"
LATEST_YEAR_COL = "net_per_10K_2019"


def recommend_job_fields(iso3: str, top_n: int = 5) -> list[dict]:
    df = pd.read_csv(RAW_PATH)
    name_to_iso3 = build_name_to_iso3()
    df["iso3"] = df["country_name"].apply(lambda n: name_to_iso3.get(normalize_name(n)))

    country_rows = df[(df["iso3"] == iso3) & df[LATEST_YEAR_COL].notna()]
    if country_rows.empty:
        return []

    top = country_rows.sort_values(LATEST_YEAR_COL, ascending=False).head(top_n)
    return [
        {
            "skill_group_name": row["skill_group_name"],
            "skill_group_category": row["skill_group_category"],
            "net_migration_per_10k": round(row[LATEST_YEAR_COL], 2),
        }
        for _, row in top.iterrows()
    ]


if __name__ == "__main__":
    for iso3 in ["CAN", "DEU", "AUS", "USA"]:
        print(f"\n=== {iso3} 취업 가능 직군 Top 5 (순유입 기준) ===")
        for rank, result in enumerate(recommend_job_fields(iso3), start=1):
            print(
                f"{rank}. {result['skill_group_name']} ({result['skill_group_category']}) "
                f"- net={result['net_migration_per_10k']}/만명"
            )
