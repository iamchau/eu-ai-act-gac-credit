# Scoring API image — thesis / portfolio slice (not bank production).
# Model file is gitignored: use docker-compose (mount ./artifacts) or copy model.joblib into build context before `docker build`.
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY requirements-serving.txt .
RUN pip install --no-cache-dir -r requirements-serving.txt

COPY src/ ./src/
COPY serving/ ./serving/
COPY params.yaml ./params.yaml

# Optional: bake model + schema into image (uncomment after train if you want a self-contained image)
# COPY artifacts/model.joblib ./artifacts/model.joblib
# COPY artifacts/feature_schema.json ./artifacts/feature_schema.json

EXPOSE 8080
CMD ["uvicorn", "serving.app:app", "--host", "0.0.0.0", "--port", "8080"]
