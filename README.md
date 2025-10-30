StyleSync – A Multi-Modal Fashion Recommendation SystemA production-ready MLOps system to classify fashion attributes and power a multi-modal style advisor.🏛️ ArchitectureThis diagram shows the complete MLOps workflow for Milestone 1, from data ingestion to a monitored inference API.flowchart LR
  subgraph Cloud
    S3["S3 / MinIO\nImages + Metadata"]
    EC2["EC2 / VM\nInference Host"]
  end

  S3 --> Ingest["Data ingestion\n(download, validate)"]
  Ingest --> Preprocess["Preprocessing\n(resize, augment, split)"]
  Preprocess --> Training["Training\n(transfer learning: ResNet50 / EfficientNet)"]
  Training --> MLflow["MLflow\nTracking & Registry"]
  MLflow --> Model["Model artifact\n(model_v1)"]
  Model --> Build["Build Docker image"]
  Build --> Inference["Inference API\n(FastAPI /predict)"]
  Inference --> UI["Streamlit UI\n(Find Similar, Style Advisor)"]
  Inference --> Prom["Prometheus + Grafana\nMonitoring"]
  Inference --> Evidently["Evidently\nDrift dashboard"]
🚀 Quick-startClone the repository:git clone [https://github.com/](https://github.com/)<your-username>/<your-repo-name>.git
cd <your-repo-name>
Install dependencies and set up the environment:make dev
Run the application:make run
The API will be available at http://localhost:8000/docs.🛠️ Make TargetsThis project uses make to standardize common development tasks.TargetDescriptionmake devSets up the local development environment and installs dependencies from requirements.txt.make lintRuns ruff and black to lint and format all code.make testRuns all pytest unit tests and generates a coverage report.make dockerBuilds the production Docker image.make runRuns the FastAPI application locally using uvicorn.make cleanRemoves temporary files (e..g, __pycache__, .pytest_cache).📊 Monitoring Dashboards(Placeholder: Add screenshots of your Grafana and Evidently dashboards here as required by D5)☁️ Cloud Deployment(Placeholder: Add details about your AWS/GCP/Azure services, setup instructions, and screenshots as required by D9)❓ FAQQ: I'm on Windows. How do I run make?A: make is not installed on Windows by default. You have a few options:WSL (Recommended): Use Windows Subsystem for Linux (WSL2) which provides a full Linux environment.Chocolatey: You can install make via the Chocolatey package manager: choco install make.Manual Commands: Look inside the Makefile and run the corresponding commands directly (e.g., pip install -r requirements.txt instead of make dev).Q: The pre-commit hooks failed my commit. What do I do?A: This is expected! The hooks (like ruff or black) often fix your files for you. Simply git add the files they changed and try your git commit again.Q: I'm getting a ModuleNotFoundError when I run make test.A: You probably forgot to install the dependencies. Run make dev first to set up your environment and install everything in requirements.txt.
