import re


def validate_phone_number(v: str | None) -> str:
    if v is None:
        return v
    numbers = re.findall(r"\d+", v)
    return "".join(numbers)
