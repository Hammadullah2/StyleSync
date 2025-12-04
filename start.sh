# #!/bin/bash
# echo "Starting full MLOps stack..."

# # Start MLflow (port 5000)
# nohup bash -c 'MLFLOW_TRACKING_INSECURE_HTTP=true mlflow server \
#   --backend-store-uri sqlite:///mlflow.db \
#   --default-artifact-root ./mlruns \
#   --host 0.0.0.0 --port 5000' > mlflow.log 2>&1 &

# # Start Prometheus (port 9090)
# nohup bash -c 'prometheus --config.file=/app/prometheus.yml --web.listen-address=:9090' > prometheus.log 2>&1 &

# # Start Evidently (port 7000)
# nohup bash -c 'evidently ui' > evidently.log 2>&1 &

# # Start Grafana (port 3000)
# nohup bash -c 'docker run -d --name grafana -p 3000:3000 grafana/grafana' > grafana.log 2>&1 &

# sleep infinity

#!/bin/bash

# 1. Update & install Docker
sudo apt update
sudo apt install -y docker.io docker-compose git

# 2. Add user to docker group
sudo usermod -aG docker $USER

# 3. Clone repo if not exists
if [ ! -d "StyleSync" ]; then
  git clone https://github.com/YOUR_USERNAME/StyleSync.git
fi

cd StyleSync

# 4. Create .env if not exists
if [ ! -f ".env" ]; then
  echo "Enter AWS_ACCESS_KEY_ID:"
  read AWS_ACCESS_KEY_ID
  echo "Enter AWS_SECRET_ACCESS_KEY:"
  read AWS_SECRET_ACCESS_KEY
  echo "Enter AWS_DEFAULT_REGION (e.g. us-east-1):"
  read AWS_DEFAULT_REGION
  echo "Enter S3_BUCKET:"
  read S3_BUCKET

  cat > .env <<EOL
AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
S3_BUCKET=$S3_BUCKET
EOL
fi

# 5. Build and start containers
docker compose build
docker compose up -d

echo "Deployment complete!"
