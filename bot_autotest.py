import hmac
import hashlib
import base64
import json
import requests
import os
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")  # Must exist
TARGET_URL = "http://127.0.0.1:8000/api/callback"  # Local webhook

# 📝 Customize your test message here:
body_json = {
  "destination": "U8dba1234c56789abcdef0123456789ab",
  "events": [
    {
      "type": "message",
      "message": {
        "type": "text",
        "id": "14330791261644",
        "text": "ping"
      },
      "timestamp": 1716440000000,
      "source": {
        "type": "user",
        "userId": "U4f5b6c7d8e9f01234567890abcdef123"
      },
      "replyToken": "dummy-reply-token",#1caa9876543210987654321098765432
      "mode": "active"
    }
  ]
}


# Generate correct signature
body_str = json.dumps(body_json, separators=(',', ':'))
hash = hmac.new(CHANNEL_SECRET.encode('utf-8'), body_str.encode('utf-8'), hashlib.sha256).digest()
signature = base64.b64encode(hash)  #.decode()

# Headers
headers = {
    "Content-Type": "application/json",
    "X-Line-Signature": signature
}
print(signature, body_str)
# Send request
response = requests.post(TARGET_URL, headers=headers, data=body_str)

print(f"[STATUS] {response.status_code}")
print(f"[RESPONSE] {response.text}")
