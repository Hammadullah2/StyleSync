# # ---------- Base image ----------
# FROM python:3.10-slim

# WORKDIR /app
# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 5000  # MLflow
# EXPOSE 8000  # FastAPI

# # ---------- CMD ----------
# CMD bash -c "\
#   mlflow server --backend-store-uri sqlite:///mlflow.db \
#   --default-artifact-root s3://stylesync-mlops-data/style-sync/mlflow/ \
#   --host 0.0.0.0 --port 5000 & \
#   uvicorn app.main:app --host 0.0.0.0 --port 8000"

# ---- builder ----
FROM python:3.11-slim AS builder
WORKDIR /w

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# ---- runtime ----
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# create non-root user and minimal utils
RUN adduser --disabled-password --gecos "" app && \
    apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/app
COPY --from=builder /w/wheels /wheels
RUN pip install --no-cache /wheels/*

COPY src ./src
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

USER app
CMD ["python", "-m", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
