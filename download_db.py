import boto3
import os
import zipfile
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "stylesync-mlops-data")
KEY = "style-sync/artifacts/chroma_db.zip"
LOCAL_ZIP = "chroma_db.zip"
EXTRACT_DIR = "."

def download_and_extract():
    s3 = boto3.client('s3')
    
    print(f"Downloading {KEY} from {S3_BUCKET}...")
    try:
        s3.download_file(S3_BUCKET, KEY, LOCAL_ZIP)
        print("Download complete.")
        
        print(f"Extracting to {EXTRACT_DIR}...")
        with zipfile.ZipFile(LOCAL_ZIP, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)
        print("Extraction complete.")
        
        # Optional: cleanup
        # os.remove(LOCAL_ZIP)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    download_and_extract()
