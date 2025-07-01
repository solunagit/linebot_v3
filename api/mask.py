import re

MASK_TEXT = "＊＊＊"

PHONE_REGEX = re.compile(r'[\d\uFF10-\uFF19]+(?:-[\d\uFF10-\uFF19]+)+')


def mask_sensitive_info(text: str) -> str:
    # Mask full phone numbers first
    masked_text = PHONE_REGEX.sub(MASK_TEXT, text)
    return masked_text
