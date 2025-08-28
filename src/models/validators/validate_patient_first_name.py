def validate_patient_first_name(v: str | None) -> str:
    if v is None:
        return v
    return v.upper()
