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


# Data models
class Product(BaseModel):
    id: int
    name: str
    masterCategory: str
    subCategory: str
    baseColour: str
    season: str
    year: int
    image_url: str


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


@app.get("/products", response_model=List[Product])
def list_products():
    """Get products with pre-signed S3 URLs"""
    response = []

    if merged_df.empty:
        # Return dummy products
        for i in range(20):
            response.append(
                Product(
                    id=i,
                    name=f"Fashion Item {i}",
                    masterCategory=["Apparel", "Footwear", "Accessories"][i % 3],
                    subCategory="Sample",
                    baseColour=["Blue", "Black", "White"][i % 3],
                    season=["Summer", "Winter"][i % 2],
                    year=2024,
                    image_url=f"https://picsum.photos/300/200?random={i}",
                )
            )
        return response

    # Real data from S3
    for category, group in merged_df.groupby("masterCategory"):
        subset = group.head(8)
        for _, row in subset.iterrows():
            try:
                s3_key = f"style-sync/raw/fashion/images/{row['filename']}"
                url = s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": os.getenv("S3_BUCKET"), "Key": s3_key},
                    ExpiresIn=3600,
                )
            except Exception as e:
                print(f"Error loading product image: {e}")
                url = f"https://picsum.photos/300/200?random={row['id']}"

            response.append(
                Product(
                    id=row["id"],
                    name=row["productDisplayName"],
                    masterCategory=row["masterCategory"],
                    subCategory=row["subCategory"],
                    baseColour=row["baseColour"],
                    season=row["season"],
                    year=int(row["year"]),
                    image_url=url,
                )
            )
    return response


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
