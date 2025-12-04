# StyleSync - Setup & Running Guide

This guide helps teammates set up and run the StyleSync RAG Fashion Advisor locally.

---

## Prerequisites

- **Python 3.11+**
- **Docker Desktop** (for monitoring)
- **Git**

---

## 1. Clone & Setup

```bash
git clone https://github.com/Hammadullah2/StyleSync.git
cd StyleSync
git checkout llmops

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

---

## 2. Environment Variables

Create a `.env` file in the project root:

```env
# Google Gemini API
GOOGLE_API_KEY=your_google_api_key

# AWS S3 (for images)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
S3_BUCKET_NAME=stylesync-mlops-data

# LangSmith (optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=StyleSync
LANGCHAIN_API_KEY=your_langsmith_key

# Grafana (for monitoring)
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=your_password
```

---

## 3. Download ChromaDB

The vector database needs to be downloaded from S3:

```bash
python download_db.py
```

This creates the `chroma_db/` folder with pre-indexed fashion items.

---

## 4. Run the API

```bash
uvicorn src.app:app --port 8000 --reload
```

**Access:**
- Swagger UI: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics

---

## 5. Test the API

### Via Swagger UI
1. Go to http://localhost:8000/docs
2. Click on `/chat` → **Try it out**
3. Enter: `{"query": "red shoes for summer"}`
4. Click **Execute**

### Via Script
```bash
python test_api_local.py
```

---

## 6. Monitoring (Optional)

Start Prometheus and Grafana:

```bash
docker-compose up -d prometheus grafana
```

**Access:**
| Service | URL | Credentials |
|---------|-----|-------------|
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin / (from .env) |

### Setup Grafana Dashboard
1. Login to Grafana
2. **Connections → Data Sources → Add → Prometheus**
3. URL: `http://prometheus:9090`
4. Click **Save & Test**
5. Create dashboard with queries like:
   - `sum(llm_requests_total)`
   - `guardrail_checks_total`

---

## 7. Run Tests

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=term-missing
```

---

## Project Structure

```
StyleSync/
├── src/
│   ├── app.py              # FastAPI app
│   ├── ingest.py           # Data ingestion
│   ├── metrics.py          # Prometheus metrics
│   └── guardrails/         # Input/Output guardrails
├── tests/                  # Unit tests
├── grafana/                # Grafana provisioning
├── prometheus.yml          # Prometheus config
├── docker-compose.yml      # Docker services
└── chroma_db/              # Vector database (after download)
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Fashion advice with product recommendations |
| `/health` | GET | Health check |
| `/metrics` | GET | Prometheus metrics |

---

## Troubleshooting

### Port 8000 in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Use different port
uvicorn src.app:app --port 8001
```

### ChromaDB not found
```bash
python download_db.py
```

### Docker not running
Start Docker Desktop first, then:
```bash
docker-compose up -d prometheus grafana
```

---

## Need Help?

- Check `guardrails_report.md` for guardrail documentation
- Check `monitoring_report.md` for monitoring setup
- Check `prompt_report.md` for prompt engineering details
