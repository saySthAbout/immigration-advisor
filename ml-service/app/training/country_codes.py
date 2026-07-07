"""국가명 <-> ISO3 매핑 (World Bank 코드북 기준).

build_country_profiles.py와 job_recommender.py가 똑같이 필요로 해서 공용
모듈로 뺐다 - 국가명 표기가 다른 외부 데이터셋(OECD는 국가명, World Bank은
ISO3)을 조인할 때마다 재사용한다.

build_name_to_iso3()는 서빙 경로(job_recommender.py가 요청마다 호출)에서도
쓰이는데, 원본 World Bank CSV는 모노레포 공용 dataset/ 폴더(학습 전용, HF
Space에는 안 딸려감)에만 있다 - 그래서 배포된 컨테이너에는 그 파일이 없어서
FileNotFoundError가 났다. 그래서 이 매핑 결과를 ml-service 자체의
data/processed/country_name_to_iso3.json으로 한 번 구워두고, 서빙 시점에는
그 캐시 파일만 읽도록 분리했다(원본 dataset/ 폴더에 대한 의존을 서빙 경로에서
완전히 제거).
"""

import json
import unicodedata
from pathlib import Path

import pandas as pd

DATASET_DIR = Path(__file__).resolve().parents[3] / "dataset"
NAME_TO_ISO3_CACHE_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "country_name_to_iso3.json"

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


def rebuild_name_to_iso3_cache() -> dict:
    """학습/전처리 시점에만 실행 - 원본 dataset/ 폴더가 있는 로컬에서 한 번
    돌려서 캐시 파일을 갱신한다."""
    wb = pd.read_csv(DATASET_DIR / "API_SP.POP.1564.TO.ZS_DS2_en_csv_v2_4949.csv", skiprows=4)
    mapping = {normalize_name(row["Country Name"]): row["Country Code"] for _, row in wb.iterrows()}
    NAME_TO_ISO3_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    NAME_TO_ISO3_CACHE_PATH.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    return mapping


def build_name_to_iso3() -> dict:
    """서빙 경로에서 쓰는 버전 - dataset/ 원본이 아니라 미리 구워둔 캐시만 읽는다."""
    if not NAME_TO_ISO3_CACHE_PATH.exists():
        return rebuild_name_to_iso3_cache()
    return json.loads(NAME_TO_ISO3_CACHE_PATH.read_text(encoding="utf-8"))


if __name__ == "__main__":
    mapping = rebuild_name_to_iso3_cache()
    print(f"{len(mapping)}개 국가명 매핑 저장: {NAME_TO_ISO3_CACHE_PATH}")
