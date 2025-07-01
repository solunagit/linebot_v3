# api/mask.py
import re
from fugashi import Tagger

MASK_TEXT = "＊＊＊"

PHONE_REGEX = re.compile(r'[\d\uFF10-\uFF19]+(?:-[\d\uFF10-\uFF19]+)+')

tagger = Tagger()  # UniDic tokenizer

def mask_sensitive_info(text: str) -> str:
    # Mask full phone numbers first
    masked_text = PHONE_REGEX.sub(MASK_TEXT, text)

    # Identify name entities using MeCab (Fugashi)
    name_spans = []
    current = ""
    pos_start = None

    for index, word in enumerate(tagger(text)):
        surface = word.surface
        features = word.feature
        # UniDic labels person names as "人名"
        if features and "人名" in features:
            if current == "":
                pos_start = index  # starting index
                current = surface
            else:
                current += surface
        else:
            if current:
                name_spans.append((pos_start, pos_start + len(current), current))
            current = ""
    # Catch trailing name at end
    if current:
        name_spans.append((pos_start, pos_start + len(current), current))

    # Replace names in reverse order to not mess up indices
    for _, _, name in reversed(name_spans):
        masked_text = masked_text.replace(name, MASK_TEXT)

    return masked_text
