import os
import boto3
import pandas as pd
import io
from PIL import Image
import torch
import open_clip
from langchain_chroma import Chroma
from tqdm import tqdm
from dotenv import load_dotenv
import logging
import concurrent.futures

load_dotenv()

# Configuration
S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "stylesync-mlops-data")
CHROMA_DB_DIR = "./chroma_db"
BATCH_SIZE = 32
MODEL_NAME = "ViT-B-32"
CHECKPOINT = "laion2b_s34b_b79k"
MAX_WORKERS = 8

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ingestion.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

missing_logger = logging.getLogger('missing_images')
missing_handler = logging.FileHandler('missing_images.log')
missing_logger.addHandler(missing_handler)
missing_logger.setLevel(logging.WARNING)

def get_s3_client():
    return boto3.client('s3')

def load_styles_csv(s3_client, bucket):
    logger.info("Loading styles.csv from S3...")
    try:
        # User confirmed data is in raw folder
        obj = s3_client.get_object(Bucket=bucket, Key="style-sync/raw/fashion/styles.csv")
        df = pd.read_csv(obj['Body'], on_bad_lines='skip')
        logger.info(f"Loaded {len(df)} rows.")
        return df
    except Exception as e:
        logger.error(f"Failed to load styles.csv: {e}")
        raise

def process_metadata(df):
    logger.info("Processing metadata...")
    df['rich_caption'] = df.apply(
        lambda x: f"{x['productDisplayName']} {x['usage']} {x['season']} {x['baseColour']}", 
        axis=1
    )
    # Construct S3 URI
    df['s3_uri'] = df['id'].apply(lambda x: f"s3://{S3_BUCKET}/style-sync/raw/fashion/images/{x}.jpg")
    return df

def init_model():
    logger.info(f"Loading OpenCLIP model: {MODEL_NAME}...")
    model, _, preprocess = open_clip.create_model_and_transforms(MODEL_NAME, pretrained=CHECKPOINT)
    model.eval()
    return model, preprocess

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

def ingest():
    s3 = get_s3_client()
    
    try:
        df = load_styles_csv(s3, S3_BUCKET)
    except:
        return

    df = process_metadata(df)
    
    model, preprocess = init_model()
    tokenizer = open_clip.get_tokenizer(MODEL_NAME)
    embedding_function = OpenCLIPEmbedder(model, tokenizer)
    
    vectorstore = Chroma(
        collection_name="style_sync",
        embedding_function=embedding_function,
        persist_directory=CHROMA_DB_DIR
    )
    
    existing_ids = set(vectorstore.get()['ids'])
    logger.info(f"Found {len(existing_ids)} existing items.")
    
    df['id_str'] = df['id'].astype(str)
    df_to_process = df[~df['id_str'].isin(existing_ids)]
    logger.info(f"Items to process: {len(df_to_process)}")
    
    if len(df_to_process) == 0:
        logger.info("Nothing new to ingest.")
        return

    # LIMIT FOR TESTING (Optional)
    # df_to_process = df_to_process.head(100)

    def process_image_s3(row):
        image_id = row['id']
        s3_key = f"style-sync/raw/fashion/images/{image_id}.jpg"
        try:
            response = s3.get_object(Bucket=S3_BUCKET, Key=s3_key)
            image_bytes = response['Body'].read()
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            return {"id": image_id, "image": image, "row": row, "status": "success"}
        except s3.exceptions.NoSuchKey:
            return {"id": image_id, "status": "missing", "error": "NoSuchKey"}
        except Exception as e:
            return {"id": image_id, "status": "failed", "error": str(e)}

    for i in tqdm(range(0, len(df_to_process), BATCH_SIZE), desc="Ingesting Batches"):
        batch_df = df_to_process.iloc[i:i+BATCH_SIZE]
        
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(process_image_s3, row) for _, row in batch_df.iterrows()]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
        
        ids = []
        metadatas = []
        embeddings = []
        texts = []
        
        for res in results:
            if res['status'] == 'success':
                try:
                    image = res['image']
                    image_input = preprocess(image).unsqueeze(0)
                    
                    with torch.no_grad():
                        image_features = model.encode_image(image_input)
                        image_features /= image_features.norm(dim=-1, keepdim=True)
                    
                    ids.append(str(res['id']))
                    metadatas.append(res['row'].to_dict())
                    texts.append(res['row']['rich_caption'])
                    embeddings.append(image_features.squeeze().tolist())
                    
                except Exception as e:
                    logger.error(f"Error embedding {res['id']}: {e}")
            elif res['status'] == 'missing':
                missing_logger.warning(f"Missing image: {res['id']}")
            else:
                logger.error(f"Failed to fetch {res['id']}: {res.get('error')}")

        if embeddings:
            vectorstore.add_texts(
                texts=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
    logger.info("Ingestion complete.")

if __name__ == "__main__":
    ingest()
