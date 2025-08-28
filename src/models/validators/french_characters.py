import unicodedata


def convert_french_characters(v: str | None) -> str:
    if v is None:
        return v
    nfkd_form = unicodedata.normalize("NFKD", v)
    only_ascii = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return only_ascii
