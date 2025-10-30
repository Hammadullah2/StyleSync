# StyleSync – A Multi-Modal Fashion Recommendation System

A production-ready MLOps system to classify fashion attributes and power a multi-modal style advisor.

---

## 🏛️ Architecture

This diagram shows the complete MLOps workflow for **Milestone 1**, from data ingestion to a monitored inference API.

```mermaid
flowchart LR
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
