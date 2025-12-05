# EC2 Deployment Guide - StyleSync

## 🚀 Quick Start: Deploy to AWS EC2

This guide walks you through deploying StyleSync to an AWS EC2 instance, making it publicly accessible.

---

## Prerequisites

- AWS Account with EC2 access
- Local copy of StyleSync code
- `.env` file with all API keys configured

---

## Step 1: Launch EC2 Instance

### 1.1 Create Instance

1. Go to **AWS Console → EC2 → Launch Instance**
2. **Configuration**:
   - **Name**: `stylesync-prod`
   - **AMI**: Ubuntu Server 22.04 LTS
   - **Instance Type**: `t3.medium` (2 vCPU, 4 GB RAM) - minimum for ML models
   - **Key Pair**: Create new or select existing (download `.pem` file)
   - **Storage**: 30 GB gp3

### 1.2 Configure Security Group

Create security group `stylesync-sg` with these rules:

| Type | Port | Source | Description |
|------|------|--------|-------------|
| SSH | 22 | My IP | Your IP only (for SSH) |
| HTTP | 80 | 0.0.0.0/0 | Redirect to 3001 (later) |
| Custom TCP | 3001 | 0.0.0.0/0 | Next.js Frontend |
| Custom TCP | 8000 | 0.0.0.0/0 | FastAPI Backend |
| Custom TCP | 3000 | My IP | Grafana (optional) |

**Note**: In production, you'd proxy backend through frontend (port 8000 = internal only)

### 1.3 Launch & Get Public IP

- Click **Launch Instance**
- Note the **Public IPv4 Address** (e.g., `18.XXX.XXX.XXX`)

---

## Step 2: Connect to EC2

### Option A: SSH from Windows (PowerShell)

```powershell
# Set permissions (first time only)
icacls "path\to\your-key.pem" /inheritance:r
icacls "path\to\your-key.pem" /grant:r "%USERNAME%:R"

# Connect
ssh -i "path\to\your-key.pem" ubuntu@18.XXX.XXX.XXX
```

### Option B: EC2 Instance Connect (Browser)

- Go to EC2 Console → Select Instance → Click **Connect** → Use EC2 Instance Connect

---

## Step 3: Install Dependencies on EC2

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Install Git
sudo apt install git -y

# Verify installations
python3.11 --version
node --version
npm --version
```

---

## Step 4: Transfer Code to EC2

### Option A: Git Clone (Recommended)

```bash
# On EC2
cd ~
git clone https://github.com/Hammadullah2/StyleSync.git
cd StyleSync
```

### Option B: SCP from Local Machine

```powershell
# On your local Windows machine
scp -i "path\to\your-key.pem" -r C:\Users\hammad\StyleSync ubuntu@18.XXX.XXX.XXX:~/
```

---

## Step 5: Configure Environment Variables

```bash
# On EC2
cd ~/StyleSync
nano .env
```

Paste your `.env` contents:
```bash
GOOGLE_API_KEY=your_key_here
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
S3_BUCKET_NAME=stylesync-mlops-data
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT="StyleSync"
LANGCHAIN_API_KEY=your_key_here
```

Save: `Ctrl+X`, `Y`, `Enter`

---

## Step 6: Set Up Backend

```bash
# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run ingestion (one-time, downloads data from S3)
python src/ingest.py
# This will take 5-10 minutes depending on dataset size
```

---

## Step 7: Set Up Frontend

```bash
cd src/frontend
npm install
cd ../..
```

---

## Step 8: Start Services with Screen (Background)

### 8.1 Start Backend

```bash
# Create screen session for backend
screen -S backend

# Activate venv and start
source .venv/bin/activate
uvicorn src.app:app --host 0.0.0.0 --port 8000

# Detach from screen: Ctrl+A, then D
```

### 8.2 Start Frontend

```bash
# Create screen session for frontend
screen -S frontend

# Start Next.js
cd src/frontend
npm run dev -- --hostname 0.0.0.0

# Detach from screen: Ctrl+A, then D
```

### 8.3 Start Monitoring (Optional)

```bash
# Only if you want Grafana/Prometheus
screen -S monitoring
docker compose up -d
# Detach: Ctrl+A, then D
```

---

## Step 9: Access Your Application

### Frontend
```
http://18.XXX.XXX.XXX:3001
```

### Backend API
```
http://18.XXX.XXX.XXX:8000/health
```

### Test Chat Widget
1. Open frontend URL in browser
2. Click chat widget (bottom right)
3. Ask: "red shoes"
4. Should see recommendations!

---

## Managing Screen Sessions

### View Running Sessions
```bash
screen -ls
```

### Reattach to Session
```bash
screen -r backend    # View backend logs
screen -r frontend   # View frontend logs
```

### Kill Session
```bash
screen -X -S backend quit
screen -X -S frontend quit
```

---

## Step 10: Make It Persistent (Auto-Start on Reboot)

### Create systemd service for Backend

```bash
sudo nano /etc/systemd/system/stylesync-backend.service
```

Paste:
```ini
[Unit]
Description=StyleSync Backend API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/StyleSync
Environment="PATH=/home/ubuntu/StyleSync/.venv/bin"
ExecStart=/home/ubuntu/StyleSync/.venv/bin/uvicorn src.app:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable stylesync-backend
sudo systemctl start stylesync-backend
sudo systemctl status stylesync-backend
```

### Create systemd service for Frontend

```bash
sudo nano /etc/systemd/system/stylesync-frontend.service
```

Paste:
```ini
[Unit]
Description=StyleSync Frontend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/StyleSync/src/frontend
ExecStart=/usr/bin/npm run dev -- --hostname 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable stylesync-frontend
sudo systemctl start stylesync-frontend
sudo systemctl status stylesync-frontend
```

Now services will auto-start on EC2 reboot!

---

## Troubleshooting

### Backend Not Starting
```bash
# Check logs
sudo journalctl -u stylesync-backend -f

# Common issues:
# - Missing .env file
# - ChromaDB not initialized (run ingest.py first)
# - Port 8000 already in use
```

### Frontend Not Starting
```bash
# Check logs
sudo journalctl -u stylesync-frontend -f

# Common issues:
# - npm packages not installed
# - Port 3001 already in use
```

### Can't Access from Browser
```bash
# Check security group allows port 3001
# Check service is running: sudo systemctl status stylesync-frontend
# Check frontend is binding to 0.0.0.0: netstat -tulpn | grep 3001
```

### ChromaDB Missing
```bash
# Re-run ingestion
source .venv/bin/activate
python src/ingest.py
```

---

## Cost Estimate

**t3.medium (2 vCPU, 4GB RAM, 30GB Storage)**
- **On-Demand**: ~$30-35/month (24/7)
- **Reserved Instance**: ~$20/month (1-year commitment)

**Free Tier**: t2.micro (750 hrs/month) too small for ML models

---

## Next Steps (Production Hardening)

Once basic setup works, consider:

1. **Domain Name**: Register domain, point to EC2 IP
2. **HTTPS**: Set up Let's Encrypt SSL certificate
3. **Nginx Reverse Proxy**: Hide backend port 8000
4. **CI/CD**: Auto-deploy on git push
5. **Monitoring**: Set up CloudWatch alarms

See `DEPLOYMENT_PRODUCTION.md` (future) for advanced setup.

---

## Quick Commands Reference

```bash
# Check if services are running
sudo systemctl status stylesync-backend
sudo systemctl status stylesync-frontend

# Restart services
sudo systemctl restart stylesync-backend
sudo systemctl restart stylesync-frontend

# View logs
sudo journalctl -u stylesync-backend -f
sudo journalctl -u stylesync-frontend -f

# Update code from GitHub
cd ~/StyleSync
git pull origin main
sudo systemctl restart stylesync-backend
sudo systemctl restart stylesync-frontend
```

---

**Deployment Date**: 2025-12-05  
**Estimated Setup Time**: 30-45 minutes  
**Difficulty**: Beginner-Friendly ✓
