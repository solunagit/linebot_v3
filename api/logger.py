import os
import gspread
from datetime import datetime
from dotenv import load_dotenv
import json
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials


# Load environment variables
load_dotenv()

SHEET_ID = "1QfLOqsYzYl9pUJU8hD4SVRb6vFLClBY5nnYyeBoMAp4"

# Load JSON from environment variable
json_str = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

if not json_str:
    raise RuntimeError("Missing GOOGLE_SERVICE_ACCOUNT_JSON in environment.")

# Parse JSON and authenticate
info = json.loads(json_str)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(info, scope)
client = gspread.authorize(creds)

# Open spreadsheet
sheet = client.open_by_key(SHEET_ID).get_worksheet(0)

# Log function
def log_to_sheet(user_id: str, user_msg: str, bot_reply: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user_id, user_msg, bot_reply, "TRUE"])