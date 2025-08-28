prescription_drug_authorization_form_additional_information = f"""
- For `contract_number` field, extract plan contract number, also called plan number, group number or policy number, from the form. The value must be a string composed of digits. If not filled, return None.
- For `member_certificate_number` field, extract plan member certificate number, also called certificate number, from the form. The value must be a string composed of digits. If not filled, return None.
"""