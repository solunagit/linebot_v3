import boto3
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

def upload_log_to_s3(user_id: str, user_msg: str, bot_reply: str) -> None:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    client_id = os.getenv("CLIENT_ID", "admin")
    filename = f"{timestamp}.json"
    s3_path = f"{os.getenv('S3_LOG_PREFIX')}{client_id}/{filename}"

    data = {
        "timestamp": timestamp,
        "user_id": user_id,
        "user_msg": user_msg,
        "bot_reply": bot_reply,
    }

    s3.put_object(
        Bucket=os.getenv("S3_BUCKET_NAME"),
        Key=s3_path,
        Body=json.dumps(data, ensure_ascii=False),
        ServerSideEncryption="AES256"
    )
