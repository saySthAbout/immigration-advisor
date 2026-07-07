FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# HF Spaces는 기본적으로 non-root(uid 1000)로 컨테이너를 실행한다.
RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser

# HF Spaces Docker SDK 기본 포트
EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
