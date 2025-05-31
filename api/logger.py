import os
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

SHEET_ID = "1QfLOqsYzYl9pUJU8hD4SVRb6vFLClBY5nnYyeBoMAp4"
JSON_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON_PATH")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_PATH, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

def log_to_sheet(user_id: str, user_msg: str, bot_reply: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user_id, user_msg, bot_reply, "TRUE"])

print(log_to_sheet("1234567890", "Hello", "Hello sir"))