---
title: Immigration Advisor ML Service
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# AI Immigration Advisor - ML Service

AI Immigration Advisor MSA의 ML 추천/예측 엔진. Core API(Cloudtype)에서만 호출하는
내부 서비스로, 모든 요청은 `Authorization: Bearer <INTERNAL_SERVICE_TOKEN>` 헤더가
필요하다(Space Repository secret으로 설정).

## 엔드포인트

- `POST /predict/visa-probability` - EasyVisa.csv(25,480건, 실제 라벨 case_status)로
  학습한 분류 모델(RandomForest, hold-out F1 0.81 / ROC-AUC 0.77) 기반 비자 승인 확률 예측

## 로컬 학습/실행

```bash
pip install -r requirements.txt
python -m app.training.preprocess_easyvisa
python -m app.training.train_visa_classifier
uvicorn main:app --reload
```
