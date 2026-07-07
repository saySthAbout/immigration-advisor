# AI Immigration Advisor

> ML, DL, LLM을 결합한 MSA(마이크로서비스 아키텍처) 기반 이민 어드바이저 플랫폼

## 프로젝트 개요

사용자의 학력·경력·어학 점수 등을 바탕으로 맞춤형 이민 국가를 추천하고, 비자 승인
확률을 예측하며, 여권/증명서 OCR 자동 입력과 RAG 기반 AI 이민 상담을 제공하는
종합 이민 어드바이저 플랫폼입니다. 독립적인 ML/DL/LLM 마이크로서비스로 구성해
서비스 간 결합도를 낮추고, 클라우드 네이티브 환경에서의 배포·확장성을 확보하는
것을 목표로 합니다.

| 구분 | 내용 |
| --- | --- |
| 서비스 형태 | AI 기반 맞춤형 이민 국가 추천 및 비자 승인 확률 예측 플랫폼 |
| 아키텍처 | MSA - Core API(Cloudtype) + ML/DL/LLM 3개 독립 서비스(Hugging Face Spaces) |
| 핵심 가치 | 데이터 기반 이민 의사결정 지원 (추천 · 예측 · 상담 · 서류 자동화) |

## 핵심 기능

1. **AI 국가 추천** - 프로필 기반 맞춤 이민 국가 Top 3 추천
2. **비자 승인 확률 예측** - 특정 비자 유형에 대한 합격 가능성 예측 및 부족 조건 피드백
3. **서류 OCR 자동 입력** - 여권/졸업증명서/경력증명서 자동 인식 및 폼 매핑
4. **RAG 기반 AI 상담** - 공식 이민정책 자료 기반 스트리밍 챗봇
5. **국가별 생활비 예측** - 이주 시 예상 생활비 및 취업 가능 직군 예측
6. **이민 준비 체크리스트 자동 생성** - 타겟 국가/비자 결정 시 동적 체크리스트 생성

## 아키텍처

```
[React Frontend] -> [Core API (FastAPI, Cloudtype)] -> [ML Service (Hugging Face)]
                                                      -> [DL/OCR Service (Hugging Face)]
                                                      -> [LLM/RAG Service (Hugging Face)]
```

Core API만 외부에 노출되며, 3개 AI 서비스는 공유 시크릿 Bearer 토큰
(`INTERNAL_SERVICE_TOKEN`)으로 인증된 내부 통신만 허용합니다. 한 서비스가
다운되어도 나머지 서비스는 독립적으로 동작하도록 설계되었습니다(loosely coupled).

## 기술 스택

| 영역 | 기술 스택 |
| --- | --- |
| Frontend | React (TypeScript), Stitch 디자인 |
| Core API | FastAPI, Cloudtype 배포 |
| Machine Learning | Scikit-Learn, XGBoost, LightGBM |
| Deep Learning (OCR) | EasyOCR + MIDV 데이터 기반 문서 분류기 |
| LLM / RAG | LangChain, FAISS |
| 배포 | Cloudtype (Core API) + Hugging Face Spaces (ML/DL/LLM) |

## 프로젝트 구조

```
immigration-advisor/
├── docs/                  PRD, 워크플로 문서, Stitch 디자인 시스템/화면 export
├── dataset/               원본 데이터셋 (용량 문제로 git 미포함, .gitignore 처리)
├── frontend/               React + TypeScript
├── core-api/               FastAPI 게이트웨이 - Cloudtype 배포
├── ml-service/             국가 추천 · 비자 승인 확률 · 생활비 예측 - Hugging Face Space
├── dl-service/             여권/서류 OCR - Hugging Face Space
├── llm-service/            RAG 상담 챗봇 · 체크리스트 생성 - Hugging Face Space
└── scripts/                각 서비스를 Hugging Face Space로 배포하는 헬퍼 스크립트
```

`ml-service`, `dl-service`, `llm-service`는 각각 독립적인 Hugging Face Space git
저장소로도 동작하도록 별도의 내부 git 저장소를 가집니다(이 모노레포는 GitHub용
소스 트리 전체를 추적하고, 각 서비스 폴더에서 개별적으로 자신의 HF Space
원격 저장소로 push합니다).

## 현재 진행 상황

- [x] PRD 작성 및 데이터셋 수집 (66개 파일 - `EasyVisa.csv`만 실제 케이스 단위 라벨 보유)
- [x] `ml-service`: EasyVisa.csv 기반 비자 승인 확률 분류 모델 학습 (RandomForest,
      hold-out F1 0.81 / ROC-AUC 0.77) 및 FastAPI 서빙 엔드포인트 구현
- [x] `ml-service`를 실제 Hugging Face Space에 배포 (Docker SDK, private)
- [x] `ml-service` 국가 추천(DIOC/World Bank/OECD/Kaggle 조인 + 콘텐츠 기반
      유사도 스코어링) 및 직군 추천(LinkedIn Skill Migration 실데이터 랭킹) 기능
- [x] `core-api` 스캐폴딩 (프로필 CRUD, 3개 ml-service 엔드포인트 프록시) 및
      실제 배포된 ml-service와의 엔드투엔드 연동 검증 (로컬 core-api ->
      Hugging Face의 실제 ml-service까지 curl로 확인)
- [ ] `core-api`를 Cloudtype에 실제 배포 (DB 애드온 연결 등 대시보드 작업 필요)
- [ ] `dl-service` (OCR), `llm-service` (RAG 챗봇)
- [ ] Frontend 연동

## 시작하기

### ml-service
```bash
cd ml-service
pip install -r requirements.txt
python -m app.training.preprocess_easyvisa
python -m app.training.train_visa_classifier
python -m app.training.country_codes         # 국가명<->ISO3 캐시 생성
python -m app.training.build_country_profiles
uvicorn main:app --reload
```

### core-api
```bash
cd core-api
pip install -r requirements.txt
cp .env.example .env   # DATABASE_URL, INTERNAL_SERVICE_TOKEN, ML_SERVICE_URL 채우기
alembic upgrade head
uvicorn app.main:app --reload
```
