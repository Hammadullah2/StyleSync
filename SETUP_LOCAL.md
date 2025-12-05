# Local Development Setup - StyleSync

## 🖥️ Running StyleSync on Your Local Computer

This guide walks you through setting up and running StyleSync on Windows, macOS, or Linux.

---

## Prerequisites

- **Python 3.9+** (3.11 recommended)
- **Node.js 18+**
- **Git**
- **AWS Account** (for S3 access)
- **Google API Key** (for Gemini)

---

## Step 1: Clone Repository

```bash
git clone https://github.com/Hammadullah2/StyleSync.git
cd StyleSync
```

---

## Step 2: Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
# Copy the example
cp .env.example .env
```

Edit `.env` with your API keys:

```bash
GOOGLE_API_KEY=your_gemini_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
S3_BUCKET_NAME=stylesync-mlops-data
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT="StyleSync"
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
```

---

## Step 3: Backend Setup

### Windows (PowerShell)

```powershell
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run data ingestion (one-time)
python src/ingest.py

# Start backend
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

### macOS/Linux (Bash)

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run data ingestion (one-time)
python src/ingest.py

# Start backend
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

**Backend is running at**: `http://localhost:8000`

---

## Step 4: Frontend Setup

Open a **new terminal** (keep backend running):

### Windows (PowerShell)

```powershell
cd src/frontend
npm install
npm run dev
```

### macOS/Linux (Bash)

```bash
cd src/frontend
npm install
npm run dev
```

**Frontend is running at**: `http://localhost:3001`

---

## Step 5: Access Application

1. Open browser: `http://localhost:3001`
2. Click the chat widget (bottom right)
3. Try: "red shoes" or "trendy summer dress"

---

## Step 6: Start Monitoring (Optional)

Open a **third terminal**:

```bash
docker compose up -d
```

**Grafana**: `http://localhost:3000` (user: `GrafanaUser`, password: see `.env`)  
**Prometheus**: `http://localhost:9090`

---

## Project Structure

```
StyleSync/
├── src/
│   ├── app.py              # FastAPI backend
│   ├── ingest.py           # Data ingestion
│   ├── guardrails/         # Input/output validation
│   ├── metrics.py          # Prometheus metrics
│   └── frontend/           # Next.js app
├── chroma_db/              # Vector database (created after ingest)
├── .env                    # Environment variables (create this)
├── requirements.txt        # Python dependencies
└── docker-compose.yml      # Monitoring stack
```

---

## Common Commands

### Run Tests

```bash
# Activate venv first
python -m pytest -q --cov=src
```

### Restart Backend

```bash
# Stop: Ctrl+C in backend terminal
# Start again:
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

### Restart Frontend

```bash
# Stop: Ctrl+C in frontend terminal
# Start again:
cd src/frontend
npm run dev
```

### Check API Health

```bash
curl http://localhost:8000/health
```

---

## Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`  
**Fix**: Activate virtual environment first
```bash
# Windows
.\.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

---

### ChromaDB not found

**Error**: `No collection 'style_sync' found`  
**Fix**: Run data ingestion
```bash
python src/ingest.py
```

---

### Frontend build errors

**Error**: `Cannot find module 'next'`  
**Fix**: Install Node modules
```bash
cd src/frontend
npm install
```

---

### Port already in use

**Error**: `Address already in use: port 8000`  
**Fix**: Kill existing process

**Windows**:
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**macOS/Linux**:
```bash
lsof -ti:8000 | xargs kill -9
```

---

## Development Workflow

1. **Make code changes**
2. **Backend auto-reloads** (if using `--reload` flag)
3. **Frontend auto-reloads** (Next.js default)
4. **Run tests**: `python -m pytest`
5. **Commit & push**: `git commit -am "message" && git push`

---

## Next Steps

- Read [README.md](README.md) for architecture details
- Read [EVALUATION.md](EVALUATION.md) for performance insights
- Read [SECURITY.md](SECURITY.md) for security practices
- Deploy to EC2: See [DEPLOYMENT_EC2.md](DEPLOYMENT_EC2.md)

---

**Setup Time**: 15-20 minutes  
**Difficulty**: Beginner-Friendly ✓
