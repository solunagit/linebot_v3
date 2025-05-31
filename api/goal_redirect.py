import csv
import re

goal_data = []

with open("../data/goals.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        goal_data.append(row)

def get_goal_link(user_input: str) -> str | None:
    for row in goal_data:
        if re.search(row["trigger_word"], user_input):
            return row["url"]
    return None

print(get_goal_link("内見したい"))