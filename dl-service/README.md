---
title: Immigration Advisor DL Service
emoji: 🛂
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# AI Immigration Advisor - DL Service

AI Immigration Advisor MSA의 DL(OCR) 엔진. Core API(Cloudtype)에서만 호출하는
내부 서비스로, 모든 요청은 `Authorization: Bearer <INTERNAL_SERVICE_TOKEN>` 헤더가
필요하다(Space Repository secret으로 설정).

## 엔드포인트

- `POST /extract/text` (multipart 파일 업로드) - EasyOCR(사전학습, 별도 학습 없음)로
  이미지에서 텍스트와 각 텍스트의 신뢰도를 추출
- `POST /classify/document-type` (multipart 파일 업로드) - 문서 종류(id/passport/
  drvlic/other) 분류. MIDV-500(4클래스 x 1개국 x 30장, 총 120장)으로 학습한
  RandomForest(사전학습 MobileNetV3-Small 특징 위에 학습)

> **분류기 정확도에 대한 주의**: hold-out 정확도가 100%로 나오는데, 클래스당
> 데이터가 국가 1개 x 30장뿐이라(같은 문서 템플릿을 여러 촬영조건으로 찍은 것) 이
> 수치는 일반화 성능이 아니라 "실제 라벨 있는 이미지로 학습 파이프라인이 동작한다"는
> 것만 보여준다. 실사용 정확도를 높이려면 클래스당 국가 다양성을 늘려야 한다.

## 로컬 학습/실행

```bash
pip install -r requirements.txt
python -m app.training.train_document_classifier
uvicorn main:app --reload
```
