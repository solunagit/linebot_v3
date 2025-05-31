import csv
import re

import csv
import re

faq_data = []

with open("../data/faq.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        faq_data.append(row)

def get_faq_response(user_input: str) -> str | None:
    for entry in faq_data:
        if re.search(entry["trigger_word"], user_input):
            return entry["response"]
    return None

print(get_faq_response("営業時間"))