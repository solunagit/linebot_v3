import csv
import re

# Load CSV file
def load_faq_data(file_path):
    faq_list = []
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            faq_list.append({
                "trigger": row["trigger_word"].strip(),
                "response": row["response"].strip()
            })
    return faq_list

# Match message text against trigger
def match_faq(user_input: str, faq_list: list) -> str:
    for faq in faq_list:
        pattern = re.escape(faq["trigger"])
        if re.search(pattern, user_input, flags=re.IGNORECASE):
            return faq["response"]
    return ""

print(match_faq("営業時間", load_faq_data('faq.csv')))