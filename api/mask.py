import re

MASK_TEXT = "＊ ＊ ＊"

# Basic Japanese name pattern (improvable)
NAME_REGEX = re.compile(r"[一-龥]{1,2}\s?[一-龥]{1,3}")
PHONE_REGEX = re.compile(r"\b\d{2,4}-\d{2,4}-\d{3,4}\b")

def mask_sensitive_info(text: str) -> str:
    text = NAME_REGEX.sub(MASK_TEXT, text)
    text = PHONE_REGEX.sub(MASK_TEXT, text)
    return text