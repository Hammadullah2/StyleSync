# #!/bin/bash

# # activate venv inside shell script
# source .venv/bin/activate

# export MLFLOW_S3_ENDPOINT_URL=https://s3.amazonaws.com
# export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
# export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}


# echo "MLflow tracking server running at http://127.0.0.1:5000"

# mlflow server \
#     --host 0.0.0.0 \
#     --port 5000 \
#     --backend-store-uri sqlite:///mlflow.db \
#     --default-artifact-root s3://stylesync-mlops-data/style-sync/mlflow/


#!/bin/bash

# activate venv
source .venv/bin/activate

# LOAD ENV VARIABLES FROM .env

export $(grep -v '^#' .env | xargs)
echo "Loaded environment variables from .env"

# EXPORT AWS + MLFLOW CONFIG
export MLFLOW_S3_ENDPOINT_URL="https://s3.amazonaws.com"

# These MUST be set in the environment
: "${AWS_ACCESS_KEY_ID:?AWS_ACCESS_KEY_ID is not set}"
: "${AWS_SECRET_ACCESS_KEY:?AWS_SECRET_ACCESS_KEY is not set}"

# START MLFLOW SERVER
echo "Starting MLflow tracking server at http://127.0.0.1:5000"

mlflow server \
    --host 0.0.0.0 \
    --port 5000 \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root s3://stylesync-mlops-data/style-sync/mlflow/
