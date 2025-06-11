import csv
import re
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get path from .env
goals_path_str = os.getenv("GOALS_PATH")
if not goals_path_str:
    raise ValueError("GOALS_PATH is not set in environment variables.")

GOALS_PATH = Path(goals_path_str).resolve()

# Load goal data
goal_data = []
with GOALS_PATH.open(encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        goal_data.append(row)

# Match and return goal link
def get_goal_link(user_input: str) -> str | None:
    for row in goal_data:
        if re.search(row["trigger_word"], user_input):
            return row["url"]
    return None
