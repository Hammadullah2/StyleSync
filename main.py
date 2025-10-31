from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

# Define the app
app = FastAPI(
    title="StyleSync API",
    description="API for the Multi-Modal Fashion Recommendation System.",
    version="1.0",
)


# ---
# 1. Health Check Endpoint
# This is required for the Dockerfile HEALTHCHECK
# ---
class HealthResponse(BaseModel):
    status: str


@app.get(
    "/health",
    tags=["Monitoring"],
    summary="Perform a Health Check",
    response_model=HealthResponse,
)
def get_health():
    """
    Provides a simple health check endpoint to confirm the API is running.
    """
    return HealthResponse(status="ok")


# ---
# 2. Prediction Endpoint (Placeholder)
# This is the core "/predict" for your Attribute Classifier
# ---
class PredictionResponse(BaseModel):
    filename: str
    content_type: str
    predicted_attributes: dict


@app.post(
    "/predict",
    tags=["Attribute Classifier"],
    summary="Classify Fashion Attributes from Image",
    response_model=PredictionResponse,
)
async def predict(file: UploadFile = File(...)):
    """
    Receives an image file and returns its predicted attributes.

    **(This is a placeholder for Milestone 1)**
    """
    # Placeholder logic:
    # In your real app, you would do:
    # contents = await file.read()
    # image = Image.open(io.BytesIO(contents))
    # attributes = model.predict(image)

    # For now, just return dummy data
    dummy_attributes = {
        "articleType": "T-Shirt",
        "baseColour": "Blue",
        "pattern": "Solid",
        "sleeve_length": "Short",
    }

    return PredictionResponse(
        filename=file.filename,
        content_type=file.content_type,
        predicted_attributes=dummy_attributes,
    )


# ---
# 3. Root Endpoint
# ---
@app.get("/", tags=["General"])
def read_root():
    """
    A simple root endpoint to confirm the API is alive.
    """
    return {"message": "Welcome to the StyleSync API"}
