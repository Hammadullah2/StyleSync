import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()
BUCKET = os.environ.get("S3_BUCKET_NAME", "stylesync-mlops-data")
s3 = boto3.client('s3')

print(f"Configuring bucket: {BUCKET}")

try:
    # 1. Disable Block Public Access
    print("Disabling Block Public Access...")
    s3.put_public_access_block(
        Bucket=BUCKET,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        }
    )
    print("Block Public Access disabled.")

    # 2. Put Bucket Policy
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{BUCKET}/*"
            }
        ]
    }

    print("Applying Public Read Policy...")
    s3.put_bucket_policy(
        Bucket=BUCKET,
        Policy=json.dumps(policy)
    )
    print("Bucket is now PUBLIC.")

except Exception as e:
    print(f"Error: {e}")
