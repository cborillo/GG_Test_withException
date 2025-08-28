quantity_types = [
    "CAP",
    "TAB",
    "GM",
    "G",
    "ML",
    "INJ",
    "PAT",
    "EPI",
    "SYR",
    "VL",
    "KIT",
    "SPY",
    "PACK",
    "PK",
    "PKT",
    "PC",
    "INH",
    "NDL",
    "LAN",
    "STR",
    "STRIP",
]


province_plans = [
    "ABC",
    "ODB",
    "Pharmacare",
    "PNET",
    "DPIN",
]

drug_explanation_of_benefits_additional_information = f"""
- For the 'patient_first_name' field, it is the first name of the patient taking the drug service.
- For the 'patient_last_name' field, it is the last name of the patient taking the drug service.
- If patient's last name is not present in the form, consider plan member's last name as patient's last name.
- For the 'rx_number' field, it is a unique seven digit number assigned to a prescription. 
- For the 'drug_identification_number' field, it is an eight digit drug identification number assigned to a drug product. It is usually preceded by "DIN".
- For the 'drug_quantity_type' field, if the drug_quantity_type is not in {quantity_types}, return None.
- For the 'province_paid' field, return True if any of the following strings appear in the receipt: {province_plans}. Otherwise, return False.
- For the 'total_charge' field, return a charge for each prescription that includes the tax.
- For cob_amount, extract the amount of the coordination of benefit that is paid for the given drug service.
- For 'cob_amount', it is typically the last dollar amount of each service line unless otherwise specified.
- For 'total_cob_amount' field, extract the total amount of 'cob_amount' in each service line.
- Do not make up any values that are not present in the receipt.
"""