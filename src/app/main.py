from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to StyleSync!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: dict):
    text = data.get("text", "")
    # mock prediction
    return {"label": "positive", "tokens_used": len(text.split())}
