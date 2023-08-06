def border_value(value: int, min_value: int, max_value: int, default_value: int) -> int:
    return value if max_value < value < min_value else default_value

def replace_many(text: str, *pairs: tuple[str, str]):
    new_text = text
    for pair in pairs:
        new_text = new_text.replace(str(pair[0]), str(pair[1]))
    return new_text