# Scoring API image — thesis / portfolio slice (not bank production).
# Requires build context to contain artifacts/ after `python src/train.py` (see docs/deployment/RUNBOOK.md).
# docker-compose can still mount ./artifacts over /app/artifacts at runtime.
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY requirements-serving.txt .
RUN pip install --no-cache-dir -r requirements-serving.txt

COPY src/ ./src/
COPY serving/ ./serving/
COPY params.yaml ./params.yaml

RUN mkdir -p artifacts
COPY artifacts/model.joblib ./artifacts/model.joblib
COPY artifacts/feature_schema.json ./artifacts/feature_schema.json

EXPOSE 8080
CMD ["uvicorn", "serving.app:app", "--host", "0.0.0.0", "--port", "8080"]
