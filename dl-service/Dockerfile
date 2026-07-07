FROM python:3.11-slim

WORKDIR /app

# opencv/scikit-image/easyocr 런타임에 필요한 시스템 라이브러리
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser

# HF Spaces Docker SDK 기본 포트
EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
