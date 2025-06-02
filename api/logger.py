import os
import gspread
from datetime import datetime
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

# Load environment variables
load_dotenv()

SHEET_ID = "1QfLOqsYzYl9pUJU8hD4SVRb6vFLClBY5nnYyeBoMAp4"
JSON_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON_PATH")

# Check if JSON path is loaded correctly
if not JSON_PATH or not os.path.exists(JSON_PATH):
    raise FileNotFoundError(f"Service account JSON not found at: {JSON_PATH}")

# Define scopes
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Authenticate
creds = Credentials.from_service_account_file(JSON_PATH, scopes=SCOPES)
client = gspread.authorize(creds)

# Open spreadsheet
sheet = client.open_by_key(SHEET_ID).get_worksheet(0)

# Log function
def log_to_sheet(user_id: str, user_msg: str, bot_reply: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user_id, user_msg, bot_reply, "TRUE"])