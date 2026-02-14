import re

def normalize_company_key(text: str) -> str:
    text = text.strip().upper()
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^A-Z0-9_]", "", text)
    return text
