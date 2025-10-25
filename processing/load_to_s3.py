import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_s3_client():
    return boto3.client(
        service_name='s3',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
    )

def upload_file_to_s3(local_file, bucket_name, key):
    s3_client = get_s3_client()
    try:
        s3_client.upload_file(local_file, bucket_name, key)
        print(f"✅ Upload successful: {key} to bucket {bucket_name}")
        return True
    except ClientError as e:
        print(f"❌ Upload failed: {e}")
        return False

def generate_timestamped_filename(base_name="stages_structured", extension="jsonl"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.{extension}"

def main():
    local_file = "../data/structured/stages_structured.jl"
    bucket_name = os.getenv("AWS_S3_BUCKET_NAME")

    if not local_file or not os.path.exists(local_file):
        print(f"❌ Local file does not exist: {local_file}")
        return

    # Upload timestamped backup
    timestamped_key = generate_timestamped_filename()
    upload_file_to_s3(local_file, bucket_name, timestamped_key)

    # Overwrite the "latest" file
    latest_key = "stages_structured_latest.jsonl"
    upload_file_to_s3(local_file, bucket_name, latest_key)

if __name__ == "__main__":
    main()
