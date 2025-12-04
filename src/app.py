import os
import boto3
import io
import base64
import torch
import open_clip
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from langsmith import traceable
import traceback

# Guardrails
from src.guardrails import InputGuardrails, OutputGuardrails

# Metrics
from src.metrics import create_metrics_tracker, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

load_dotenv()

# Configuration
CHROMA_DB_DIR = "./chroma_db"
MODEL_NAME = "ViT-B-32"
CHECKPOINT = "laion2b_s34b_b79k"
S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "stylesync-mlops-data")

app = FastAPI(title="Style Sync API")

# --- 1. Initialize Models (Global for now) ---
print("Initializing models...")

# OpenCLIP for Embedding Query
model, _, preprocess = open_clip.create_model_and_transforms(MODEL_NAME, pretrained=CHECKPOINT)
tokenizer = open_clip.get_tokenizer(MODEL_NAME)

class OpenCLIPEmbedder:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        
    def embed_documents(self, texts):
        with torch.no_grad():
            text = self.tokenizer(texts)
            text_features = self.model.encode_text(text)
            text_features /= text_features.norm(dim=-1, keepdim=True)
            return text_features.tolist()
    
    def embed_query(self, text):
        return self.embed_documents([text])[0]

embedding_function = OpenCLIPEmbedder(model, tokenizer)

# Chroma Vector Store
vectorstore = Chroma(
    collection_name="style_sync",
    embedding_function=embedding_function,
    persist_directory=CHROMA_DB_DIR
)

# S3 Client
s3_client = boto3.client('s3')

# Gemini
# Ensure GOOGLE_API_KEY is in env
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

print("Initialization complete.")

# --- 2. Helper Functions ---

@traceable(name="fetch_image_from_s3")
def get_image_base64(s3_uri: str) -> str:
    """Downloads image from S3 and converts to Base64."""
    try:
        # Parse S3 URI (s3://bucket/key)
        parts = s3_uri.replace("s3://", "").split("/", 1)
        bucket = parts[0]
        key = parts[1]
        
        response = s3_client.get_object(Bucket=bucket, Key=key)
        image_bytes = response['Body'].read()
        
        return base64.b64encode(image_bytes).decode('utf-8')
    except Exception as e:
        print(f"Error fetching image {s3_uri}: {e}")
        return None

@traceable(name="determine_filters")
def determine_filters(query: str) -> dict:
    """Logic Router: Determine filters based on query keywords."""
    conditions = []
    query_lower = query.lower()
    
    # Trend Logic
    if "trendy" in query_lower or "new" in query_lower or "latest" in query_lower:
        conditions.append({"year": {"$gte": 2022}})
        
    # Season Logic
    if "summer" in query_lower:
        conditions.append({"season": "Summer"})
    elif "winter" in query_lower:
        conditions.append({"season": "Winter"})
    elif "fall" in query_lower or "autumn" in query_lower:
        conditions.append({"season": "Fall"})
    elif "spring" in query_lower:
        conditions.append({"season": "Spring"})
        
    if not conditions:
        return None
    elif len(conditions) == 1:
        return conditions[0]
    else:
        return {"$and": conditions}

@traceable(name="retrieve_documents")
def retrieve_documents(query: str, filters: dict, k: int = 3):
    return vectorstore.similarity_search(
        query, 
        k=k,
        filter=filters if filters else None
    )

@traceable(name="generate_fashion_advice")
def generate_fashion_advice(query: str, images_data: List[str]):
    if not images_data:
        return "I couldn't find any matching items in the catalog."
        
    # Construct Multimodal Message
    message_content = [
        {"type": "text", "text": f"User Query: {query}\n\nHere are some images from our catalog. Please analyze them and provide fashion advice or answer the user's request based on these specific items. Refer to them as 'the suggested items'. Be helpful and stylish in your tone."}
    ]
    
    for b64 in images_data:
        message_content.append({
            "type": "image_url", 
            "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
        })
        
    msg = HumanMessage(content=message_content)
    
    try:
        ai_response = llm.invoke([msg])
        return ai_response.content
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "I found some items, but I'm having trouble analyzing them right now."

# --- 3. API Endpoints ---

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    recommended_items: List[dict]

# Logging Setup
import logging
logging.basicConfig(filename='api_debug.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', force=True)

# Initialize guardrails
input_guardrails = InputGuardrails()
output_guardrails = OutputGuardrails()

@traceable(name="chat_endpoint_flow")
async def chat_endpoint_flow(request: ChatRequest):
    logging.info("Entering chat_endpoint_flow")
    query = request.query
    logging.info(f"Received query: {query}")
    
    # INPUT GUARDRAILS: Validate query before processing
    is_valid, message, details = input_guardrails.validate(query)
    if not is_valid:
        logging.warning(f"Input blocked by guardrails: {message}")
        return ChatResponse(
            response=message,
            recommended_items=[]
        )
    
    # 1. Logic Router
    try:
        filters = determine_filters(query)
        logging.info(f"Applied filters: {filters}")
    except Exception as e:
        logging.error(f"Error in determine_filters: {e}")
        raise

    # 2. Retrieval
    try:
        results = retrieve_documents(query, filters)
        logging.info(f"Retrieved {len(results)} documents")
    except Exception as e:
        logging.error(f"Error in retrieve_documents: {e}")
        raise
    
    # 3. S3-Gemini Bridge
    images_data = []
    recommended_items = []
    
    logging.info("Processing results...")
    for doc in results:
        try:
            s3_uri = doc.metadata.get('s3_uri')
            if not s3_uri and doc.metadata.get('id'):
                s3_uri = f"s3://{S3_BUCKET}/style-sync/raw/fashion/images/{doc.metadata.get('id')}.jpg"
            
            if s3_uri:
                logging.info(f"Fetching image: {s3_uri}")
                b64_image = get_image_base64(s3_uri)
                if b64_image:
                    images_data.append(b64_image)
                    recommended_items.append({
                        "productDisplayName": doc.metadata.get("productDisplayName"),
                        "s3_uri": s3_uri,
                        "metadata": doc.metadata
                    })
                else:
                    logging.warning(f"Failed to fetch image: {s3_uri}")
        except Exception as e:
            logging.error(f"Error processing doc {doc.metadata.get('id')}: {e}")
    
    # 4. Generate Response
    try:
        logging.info("Generating response...")
        response_text = generate_fashion_advice(query, images_data)
        logging.info("Response generated.")
    except Exception as e:
        logging.error(f"Error in generate_fashion_advice: {e}")
        raise
    
    # OUTPUT GUARDRAILS: Moderate response before returning
    is_safe, moderated_response, mod_details = output_guardrails.moderate(
        response_text, 
        [item.get("metadata", {}) for item in recommended_items]
    )
    if not is_safe:
        logging.warning(f"Output moderated by guardrails: {mod_details}")
        response_text = moderated_response

    return ChatResponse(
        response=response_text,
        recommended_items=recommended_items
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    logging.info("Hit /chat endpoint")
    metrics_tracker = create_metrics_tracker()
    metrics_tracker.start_request()
    
    try:
        # Track guardrail check
        is_valid, _, details = input_guardrails.validate(request.query)
        rule = details.get('pii_types', [details.get('matched_pattern', 'unknown')])[0] if details else 'none'
        metrics_tracker.track_guardrail('input', str(rule), is_valid)
        
        result = await chat_endpoint_flow(request)
        metrics_tracker.end_request('success')
        return result
    except Exception as e:
        metrics_tracker.end_request('error')
        logging.error("Exception caught in chat_endpoint:", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
