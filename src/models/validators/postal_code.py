import re

# Translation tables
lower_to_number = {"i": "1", "o": "0", "q": "9", "s": "5", "t": "7"}
upper_to_number = {"I": "1", "G": "6", "Z": "2", "O": "0", "B": "8", "S": "5", "T": "7"}
number_to_upper = {"1": "I", "6": "G", "2": "Z", "0": "O", "8": "B", "5": "S", "7": "T"}


def validate_postal_code(v: str) -> str:
    if v is None:
        return v

    # Remove any spaces or hyphens
    v = re.sub(r"[ -]", "", v if v is not None else "")

    # Make sure the length is 6; otherwise, return None
    if len(v) != 6:
        return None

    # Apply translations
    result = []
    for i, char in enumerate(v):
        if i in [1, 3, 5]:
            char = lower_to_number.get(char, char)
            char = upper_to_number.get(char, char)
        elif i in [0, 2, 4]:
            char = number_to_upper.get(char, char)
        result.append(char)

    translated_result = "".join(result)

    # Ensure space between 3rd and 4th character
    final_result = f"{translated_result[:3]} {translated_result[3:]}"

    return final_result
