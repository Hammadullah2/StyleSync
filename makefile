VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PRECOMMIT := $(VENV)/bin/pre-commit
RM := rm -rf
FIND := find . -name "__pycache__" -type d -exec rm -rf {} +

.PHONY: dev venv install-deps pre-commit fastapi react evidently mlflow start-servers test lint docker run-docker audit clean

# Default dev command
dev: venv install-deps pre-commit start-servers

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(PYTHON) -m pip install --upgrade pip

# Install dependencies
install-deps:
	@echo "Installing dependencies..."
	@$(PIP) install -r requirements.txt

# Install pre-commit hooks
pre-commit:
	@echo "Installing pre-commit hooks..."
	@$(PRECOMMIT) install || true

# Run tests with coverage
test:
	@echo "Running tests..."
	@$(PYTHON) -m pytest -q --cov=src

# Lint and format check
lint:
	@echo "Running lint and format checks..."
	@$(PYTHON) -m ruff check .
	@$(PYTHON) -m black --check .

# Start FastAPI server
fastapi:
	@echo "Starting FastAPI server at http://127.0.0.1:8000 ..."
	@$(PYTHON) -m uvicorn src.app.main:app --reload --port 8000

react:
	@echo "Starting React development server at http://localhost:3000 ..."
	@cd src/frontend && npm run dev

# Start Evidently server
evidently:
	@echo "Starting Evidently monitoring report..."
	@$(PYTHON) src/app/monitoring/evidently_report.py serve

mlflow:
	@echo "Starting MLflow on localhost:5000 ..."
	@bash mlflow.sh

# Start both servers concurrently
start-servers:
	@$(MAKE) -j3 fastapi react evidently

# Build Docker image
docker:
	@echo "Building Docker image 'stylesync:local'..."
	@docker build -t stylesync:local .

# Run Docker container
run-docker:
	@echo "Running Docker container on port 8000..."
	@docker run --rm -p 8000:8000 stylesync:local

# Security audit
audit:
	@echo "Running dependency security audit..."
	@$(PYTHON) -m pip_audit --strict --requirement requirements.txt || true

# Clean environment
clean:
	@echo "Cleaning environment..."
	@$(RM) $(VENV)
	@$(FIND)
