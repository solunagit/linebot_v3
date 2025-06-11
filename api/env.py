import os

def is_staging() -> bool:
    return os.getenv("ENV", "production") == "staging"
