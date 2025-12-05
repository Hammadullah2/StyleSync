from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import boto3
import pandas as pd
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

# import io
# from PIL import Image

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="StyleSync API", description="AI Fashion Styling API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    region_name=os.getenv("AWS_DEFAULT_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


class PredictionResult(BaseModel):
    category: str
    subcategory: str
    color: str
    style: str
    confidence: float
    recommendations: List[str]


class StylistAdvice(BaseModel):
    advice: str
    outfit_suggestions: List[str]
    matching_products: List[int]


# Load data (you might want to cache this)
try:
    images_df = pd.read_csv("data/images.csv")
    styles_df = pd.read_csv("data/styles.csv", on_bad_lines="skip", quotechar='"')

    # Merge data
    merged_df = pd.merge(
        images_df,
        styles_df,
        left_on=images_df["filename"].str.replace(".jpg", ""),
        right_on="id",
        how="inner",
    )
except Exception as e:
    print(f"Dummy data: {e}")
    # Create dummy data if files don't exist
    merged_df = pd.DataFrame()


@app.get("/")
def read_root():
    return {"message": "Welcome to StyleSync API!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...), text: str = Form("")):
    """Predict fashion attributes from uploaded image"""
    # Read image
    # image_data = await file.read()
    # image = Image.open(io.BytesIO(image_data))

    # Here you would add your actual ML model prediction
    # For now, return mock predictions

    return {
        "category": "Topwear",
        "subcategory": "Shirts",
        "color": "Blue",
        "style": "Casual",
        "confidence": 0.92,
        "recommendations": [
            "Pair with slim-fit jeans",
            "Add a leather jacket for layering",
            "Accessorize with a silver watch",
        ],
        "user_question": text,
    }


@app.post("/ask")
async def ask_stylist(text: str):
    """Get fashion advice from AI stylist"""
    # Here you would integrate with your RAG/LLM system
    return {
        "advice": f"Based on your query: '{text}', I recommend focusing on layering techniques for the upcoming season. Try combining different textures and neutral colors for a sophisticated look.",
        "outfit_suggestions": [
            "Casual: Denim jacket + White tee + Black jeans",
            "Formal: Blazer + Button-down + Tailored trousers",
            "Evening: Silk dress + Statement jewelry",
        ],
        "matching_products": [1, 5, 12],
    }
