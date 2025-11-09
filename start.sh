#!/bin/bash
echo "Starting full MLOps stack..."

# Start MLflow (port 5000)
nohup bash -c 'MLFLOW_TRACKING_INSECURE_HTTP=true mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 --port 5000' > mlflow.log 2>&1 &

# Start Prometheus (port 9090)
nohup bash -c 'prometheus --config.file=/app/prometheus.yml --web.listen-address=:9090' > prometheus.log 2>&1 &

# Start Evidently (port 7000)
nohup bash -c 'evidently ui' > evidently.log 2>&1 &

# Start Grafana (port 3000)
nohup bash -c 'docker run -d --name grafana -p 3000:3000 grafana/grafana' > grafana.log 2>&1 &

sleep infinity
