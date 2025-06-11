import csv
import re
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get FAQ CSV path from .env and resolve it
faq_path_str = os.getenv("FAQ_PATH")
if not faq_path_str:
    raise ValueError("FAQ_PATH is not set in environment variables.")

FAQ_PATH = Path(faq_path_str).resolve()

# Load FAQ data
faq_data = []
with FAQ_PATH.open(encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        faq_data.append(row)

# Search and return matching FAQ response
def get_faq_response(user_input: str) -> str | None:
    for entry in faq_data:
        if re.search(entry["trigger_word"], user_input):
            return entry["response"]
    return None
