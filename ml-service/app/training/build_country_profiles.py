"""국가 추천용 국가 피처 매트릭스 구축.

country_status(비자 승인) 같은 개별 라벨이 없어서 지도학습이 불가능하다 - 대신
아래 4개 소스를 국가(ISO3) 단위로 조인해 "국가 프로필" 테이블을 만들고,
콘텐츠 기반 유사도 스코어링(build_country_recommender.py)의 입력으로 쓴다.

1. DIOC 2015/16 (DIOC_2015_16_File_A_1.csv) - 목적지 국가 x 출신 대륙별 이주민 수.
   fborn==1(외국 출생)만 집계해 목적지 국가별 "기존 이주민이 어느 대륙 출신인지"
   비중을 계산한다. EasyVisa의 continent 카테고리와 바로 연결되는 신호다.
2. World Bank 인구 지표 - 청년인구비율/생산가능인구비율 + 소득 그룹(IncomeGroup).
3. OECD 국제이주 데이터베이스 3종(연도별 국가 단위 와이드 테이블, 국가명 표기라
   World Bank 코드북으로 ISO3에 매핑):
   - Stocks of foreign-born population.xlsx -> 외국 출생 인구 비율(최신 연도)
   - Acquisition of nationality.xlsx -> 외국인 대비 국적 취득률(최신 연도) - 시민권
     취득 난이도의 근사 지표
   - Inflows of foreign population.xlsx -> 최근 연도 순유입 규모(천 명) - 최근
     이민 활발도 신호

DIOC가 다루는 35개 OECD 목적지 국가만 최종 국가 유니버스로 쓴다(실질적으로 이민
목적지로 추천할 만한 국가 범위와 일치).
"""

import re
import unicodedata
from pathlib import Path

import pandas as pd

DATASET_DIR = Path(__file__).resolve().parents[3] / "dataset"
PROCESSED_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "country_profiles.csv"

REGION_TO_CONTINENT = {
    "AFRI": "Africa",
    "ASIA": "Asia",
    "EURO": "Europe",
    "NOAM": "North America",
    "OCEA": "Oceania",
    "SCAC": "South America",
}

# World Bank 국가명과 OECD 파일 국가명 표기가 다른 경우만 수동 매핑한다.
NAME_ALIASES = {
    "czech republic": "czechia",
    "turkiye": "turkiye",
    "turkey": "turkiye",
    "korea": "korea, rep.",
    "south korea": "korea, rep.",
    "slovak republic": "slovak republic",
}


def _normalize_name(name: str) -> str:
    name = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode("ascii")
    name = name.strip().lower()
    return NAME_ALIASES.get(name, name)


def _build_name_to_iso3() -> dict:
    wb = pd.read_csv(DATASET_DIR / "API_SP.POP.1564.TO.ZS_DS2_en_csv_v2_4949.csv", skiprows=4)
    return {_normalize_name(row["Country Name"]): row["Country Code"] for _, row in wb.iterrows()}


def _is_year_like(value) -> bool:
    try:
        return 1990 <= float(value) <= 2035
    except (TypeError, ValueError):
        return False


def _latest_numeric(row: pd.Series, year_cols: list) -> float | None:
    for col in reversed(year_cols):  # 최신 연도부터 역순으로 찾는다
        val = row[col]
        if pd.notna(val) and str(val).strip() not in {"..", "."}:
            try:
                return float(val)
            except (TypeError, ValueError):
                continue
    return None


def _parse_oecd_wide_table(path: Path, name_to_iso3: dict) -> pd.DataFrame:
    """국가명 + 연도별 절대값(+ 선택적으로 '% of ...' 비율 행)로 된 OECD 와이드
    테이블을 {iso3: {"value": 최신 절대값, "pct": 최신 비율(없으면 NaN)}} 로 정리."""
    sheet_name = pd.ExcelFile(path).sheet_names[0]
    df = pd.ExcelFile(path).parse(sheet_name)

    header_row_idx = next(
        i for i, row in df.iterrows() if sum(_is_year_like(v) for v in row) >= 3
    )
    year_cols = [c for c in df.columns if _is_year_like(df.loc[header_row_idx, c])]

    records = {}
    rows = df.iloc[header_row_idx + 1 :].reset_index(drop=True)
    i = 0
    while i < len(rows):
        label = rows.iloc[i, 0]
        if pd.isna(label) or "%" in str(label) or "table" in str(label).lower():
            i += 1
            continue

        iso3 = name_to_iso3.get(_normalize_name(label))
        value = _latest_numeric(rows.iloc[i], year_cols)
        pct = None
        if i + 1 < len(rows) and "%" in str(rows.iloc[i + 1, 0]):
            pct = _latest_numeric(rows.iloc[i + 1], year_cols)
            i += 1

        if iso3:
            records[iso3] = {"value": value, "pct": pct}
        i += 1

    return pd.DataFrame.from_dict(records, orient="index")


def build() -> pd.DataFrame:
    name_to_iso3 = _build_name_to_iso3()

    # 1. DIOC: 목적지 국가별 출신 대륙 비중
    dioc = pd.read_csv(DATASET_DIR / "DIOC_2015_16_File_A_1.csv")
    dioc = dioc[(dioc["fborn"] == 1) & (dioc["regionb"] != "UNK")]
    by_region = dioc.groupby(["country", "regionb"])["number"].sum().unstack(fill_value=0)
    by_region = by_region.div(by_region.sum(axis=1), axis=0)  # 국가별 비중 정규화
    by_region.columns = [f"migrant_share_{REGION_TO_CONTINENT[c].lower().replace(' ', '_')}" for c in by_region.columns]
    profiles = by_region.copy()
    profiles.index.name = "iso3"

    # 2. World Bank 인구 지표 + 소득 그룹
    youth = pd.read_csv(DATASET_DIR / "API_SP.POP.0014.TO.ZS_DS2_en_csv_v2_4596.csv", skiprows=4)
    working_age = pd.read_csv(DATASET_DIR / "API_SP.POP.1564.TO.ZS_DS2_en_csv_v2_4949.csv", skiprows=4)
    year_cols_wb = [c for c in youth.columns if _is_year_like(c)]
    profiles["youth_population_pct"] = youth.set_index("Country Code").apply(
        lambda r: _latest_numeric(r, year_cols_wb), axis=1
    )
    profiles["working_age_population_pct"] = working_age.set_index("Country Code").apply(
        lambda r: _latest_numeric(r, year_cols_wb), axis=1
    )
    meta = pd.read_csv(DATASET_DIR / "Metadata_Country_API_SP.POP.1564.TO.ZS_DS2_en_csv_v2_4949.csv")
    profiles["income_group"] = meta.set_index("Country Code")["IncomeGroup"]

    # 3. OECD 국제이주 데이터베이스 3종
    foreign_born = _parse_oecd_wide_table(DATASET_DIR / "Stocks of foreign-born population.xlsx", name_to_iso3)
    profiles["foreign_born_pct"] = foreign_born["pct"]

    naturalization = _parse_oecd_wide_table(DATASET_DIR / "Acquisition of nationality.xlsx", name_to_iso3)
    profiles["naturalization_rate_pct"] = naturalization["pct"]

    inflows = _parse_oecd_wide_table(DATASET_DIR / "Inflows of foreign population.xlsx", name_to_iso3)
    profiles["annual_inflow_thousands"] = inflows["value"]

    profiles = profiles.reset_index().rename(columns={"index": "iso3"})
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    profiles.to_csv(PROCESSED_PATH, index=False)
    print(f"{len(profiles)}개국 프로필 저장: {PROCESSED_PATH}")
    print(f"결측치 컬럼별 개수:\n{profiles.isna().sum()}")
    return profiles


if __name__ == "__main__":
    build()
