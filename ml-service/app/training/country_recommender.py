"""국가 추천 - 콘텐츠 기반 유사도 스코어링.

country_profiles.csv(build_country_profiles.py 결과물)를 이용해 사용자 프로필과
국가 프로필 간 가중합 점수를 계산한다. user<->country 매칭에 대한 실제 정답
라벨이 어디에도 없어서(지도학습 불가) 학습된 분류기가 아니라 명시적인 가중치
기반 콘텐츠 스코어링으로 설계했다 - 가중치의 근거는 각 피처 docstring 참고.

sklearn Pipeline으로 감싸지 않은 이유: 이건 "학습된 모델"이 아니라 정규화 +
가중합 규칙이라서 fit할 파라미터가 없다. 대신 정규화 기준(min/max)은
country_profiles.csv 자체에서 매번 다시 계산하지 않도록 저장해둔다.
"""

import json
from pathlib import Path

import pandas as pd

PROCESSED_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "country_profiles.csv"
NORM_STATS_PATH = Path(__file__).resolve().parents[2] / "models" / "country_recommender" / "norm_stats.json"

CONTINENT_TO_COLUMN = {
    "Asia": "migrant_share_asia",
    "Europe": "migrant_share_europe",
    "North America": "migrant_share_north_america",
    "South America": "migrant_share_south_america",
    "Africa": "migrant_share_africa",
    "Oceania": "migrant_share_oceania",
}

# 가중치 근거:
# - diaspora_fit(0.35): 출신 대륙 커뮤니티가 이미 자리잡은 나라일수록 정착/네트워킹이
#   현실적으로 쉽다고 보고 가장 큰 비중을 줬다.
# - openness(0.25): 외국출생인구비율이 높을수록 이민자에 대한 사회적 수용도가
#   높다고 가정.
# - naturalization_ease(0.20): 국적취득률이 높을수록 시민권 취득 경로가 상대적으로
#   원활하다고 가정.
# - momentum(0.20): 최근 순유입 규모가 클수록 이민 문호가 활발히 열려있다는 신호.
DEFAULT_WEIGHTS = {
    "diaspora_fit": 0.35,
    "openness": 0.25,
    "naturalization_ease": 0.20,
    "momentum": 0.20,
}


def _compute_and_cache_norm_stats(df: pd.DataFrame) -> dict:
    stats = {
        col: {"min": float(df[col].min()), "max": float(df[col].max())}
        for col in ["foreign_born_pct", "naturalization_rate_pct", "annual_inflow_thousands"]
    }
    NORM_STATS_PATH.parent.mkdir(parents=True, exist_ok=True)
    NORM_STATS_PATH.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    return stats


def _minmax(value: float, stats: dict) -> float:
    if pd.isna(value) or stats["max"] == stats["min"]:
        return 0.0
    return (value - stats["min"]) / (stats["max"] - stats["min"])


def recommend_countries(origin_continent: str, weights: dict | None = None, top_n: int = 3) -> list[dict]:
    if origin_continent not in CONTINENT_TO_COLUMN:
        raise ValueError(f"origin_continent는 {list(CONTINENT_TO_COLUMN)} 중 하나여야 합니다.")
    weights = weights or DEFAULT_WEIGHTS

    df = pd.read_csv(PROCESSED_PATH)
    stats = _compute_and_cache_norm_stats(df)

    diaspora_col = CONTINENT_TO_COLUMN[origin_continent]
    scored = []
    for _, row in df.iterrows():
        diaspora_fit = row[diaspora_col]
        openness = _minmax(row["foreign_born_pct"], stats["foreign_born_pct"])
        naturalization_ease = _minmax(row["naturalization_rate_pct"], stats["naturalization_rate_pct"])
        momentum = _minmax(row["annual_inflow_thousands"], stats["annual_inflow_thousands"])

        match_score = (
            weights["diaspora_fit"] * diaspora_fit
            + weights["openness"] * openness
            + weights["naturalization_ease"] * naturalization_ease
            + weights["momentum"] * momentum
        )
        scored.append(
            {
                "iso3": row["iso3"],
                "match_score": round(match_score * 100, 1),
                "diaspora_fit": round(diaspora_fit, 3),
                "foreign_born_pct": row["foreign_born_pct"],
                "naturalization_rate_pct": row["naturalization_rate_pct"],
                "annual_inflow_thousands": row["annual_inflow_thousands"],
                "income_group": row["income_group"],
            }
        )

    scored.sort(key=lambda r: r["match_score"], reverse=True)
    return scored[:top_n]


if __name__ == "__main__":
    for continent in CONTINENT_TO_COLUMN:
        print(f"\n=== {continent} 출신 추천 Top 3 ===")
        for rank, result in enumerate(recommend_countries(continent), start=1):
            print(f"{rank}. {result['iso3']} - match_score={result['match_score']}")
