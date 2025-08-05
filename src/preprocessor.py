import re


def clean_text(text: str) -> str:
    """Applies lowercasing, and removes punctuation."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text
