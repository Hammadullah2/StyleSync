# ---------- Base image ----------
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000  # MLflow
EXPOSE 8000  # FastAPI

# ---------- CMD ----------
CMD bash -c "\
  mlflow server --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root s3://stylesync-mlops-data/style-sync/mlflow/ \
  --host 0.0.0.0 --port 5000 & \
  uvicorn app.main:app --host 0.0.0.0 --port 8000"
