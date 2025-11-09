from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert "ok" in r.json()


def test_predict():
    r = client.post("/predict", json={"text": "This is good"})
    assert r.status_code == 200
    body = r.json()
    assert set(body.keys()) == {"label", "tokens_used"}
