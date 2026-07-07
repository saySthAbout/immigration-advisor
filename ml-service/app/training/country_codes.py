"""국가명 <-> ISO3 매핑 (World Bank 코드북 기준).

build_country_profiles.py와 job_recommender.py가 똑같이 필요로 해서 공용
모듈로 뺐다 - 국가명 표기가 다른 외부 데이터셋(OECD는 국가명, World Bank은
ISO3)을 조인할 때마다 재사용한다.
"""

import unicodedata
from pathlib import Path

import pandas as pd

DATASET_DIR = Path(__file__).resolve().parents[3] / "dataset"

# World Bank 국가명과 다른 데이터셋(OECD, Kaggle)의 국가명 표기가 다른 경우만
# 수동 매핑한다.
NAME_ALIASES = {
    "czech republic": "czechia",
    "turkiye": "turkiye",
    "turkey": "turkiye",
    "korea": "korea, rep.",
    "south korea": "korea, rep.",
    "slovak republic": "slovak republic",
    "slovakia": "slovak republic",
}


def normalize_name(name: str) -> str:
    name = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode("ascii")
    name = name.strip().lower()
    return NAME_ALIASES.get(name, name)


def build_name_to_iso3() -> dict:
    wb = pd.read_csv(DATASET_DIR / "API_SP.POP.1564.TO.ZS_DS2_en_csv_v2_4949.csv", skiprows=4)
    return {normalize_name(row["Country Name"]): row["Country Code"] for _, row in wb.iterrows()}
