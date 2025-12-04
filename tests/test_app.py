from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "Welcome to StyleSync" in r.json()["message"]


# def test_predict():
#     r = client.post("/predict", json={"text": "This is good"})
#     assert r.status_code == 200
#     body = r.json()
#     assert set(body.keys()) == {"label", "tokens_used"}
#     assert body["label"] == "positive"
#     assert body["tokens_used"] == 3


def test_predict():
    dummy_file = ("test.jpg", "fake image bytes", "image/jpeg")

    r = client.post(
        "/predict", files={"file": dummy_file}, data={"text": "This is good"}
    )
    assert r.status_code == 200
