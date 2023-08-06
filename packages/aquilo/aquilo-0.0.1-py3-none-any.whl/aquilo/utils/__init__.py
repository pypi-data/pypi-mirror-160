def has_special_char(text: str) -> bool:
    return any(c for c in text if not c.isalnum() and not c.isspace())
