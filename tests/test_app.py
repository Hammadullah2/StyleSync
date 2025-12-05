"""
Unit tests for FastAPI app
"""
import pytest
from fastapi.testclient import TestClient

# Skip tests that require full app initialization
pytest.importorskip("botocore")

from src.app import app

client = TestClient(app)


def test_health():
    """Test health endpoint."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_metrics():
    """Test metrics endpoint returns Prometheus metrics."""
    r = client.get("/metrics")
    assert r.status_code == 200
    # Check for Prometheus metric format
    assert "python_gc" in r.text or "llm" in r.text
