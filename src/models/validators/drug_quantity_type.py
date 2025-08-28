from src.prompts.additional_information.drug_receipt import quantity_types


def validate_drug_quantity_type(quantity_type: str) -> str:
    if quantity_type:
        return quantity_type if quantity_type.upper() in quantity_types else None
    else:
        return None
