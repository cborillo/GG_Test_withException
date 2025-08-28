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
    "RAMQ",
    "MSI",
    "PEI",
]


drug_receipt_additional_information = f"""
- For `pharmacy_postal_code` field, if the postal code appears below the name of the patient, it is the postal code of the patient, not the pharmacy. DO NOT return the patient's postal code unless it is the same as the pharmacy's postal code. In that case, return the postal code. 
- For the `pharmacy_address` field, if the address appears below the name of the patient, it is the address of the patient, not the pharmacy. DO NOT return the patient's address.
- For `pharmacy_phone_number` field, only output the phone number of pharmacy in XXXXXXXXXX format.
- `patient_first_name` and `patient_last_name` fields are the first and last name of the patient respectively. Patient name is usually next to or below pharmancy information, do not confuse with Doctor's name. One receipt has only one patient.
- For the `rx_number` field, it is a unique seven digit number assigned to a prescription. It is usually (although not always) found at the top of the receipt, preceded by "Rx". It is directly above the patient's name.
- For the `drug_identification_number` field, it is an eight digit drug identification number assigned to a drug product. It is usually found at the top of the receipt, preceded by "DIN".
- For the `drug_quantity field`, the quantity of the drug will be the first whole number written before the drug name. For example, "100 CANDESAR/HC 16/12.5MG PMS" has a quantity of 100. DO NOT use a drug_quantity that appears after the drug name.
- For the `drug_quantity_type` field, if the drug_quantity_type is not in {quantity_types}, return None.
- For the `drug_cost` field, the cost of the drug is usually denoted by the word "COST", or the letter "C" followed by a dollar amount.
- For the `dispensing_fee field`, the dispensing fee is usually denoted by the word "FEE", or the letter "F" followed by a dollar amount.
- For the `province_paid` field, return True if any of the following strings appear in the receipt: {province_plans}. Otherwise, return False.
- For the `days_supply` field, the number of days the prescription is valid for is usually denoted by the word "DAYS", or the letter "D" followed by a number.
- For the `total_charge` field, the total charge is usually denoted by the word "TOTAL", or the letter "T" followed by a dollar amount.
- For the `refills_remaining` field, the number of refills remaining is usually denoted by the word "REFILLS", or the letter "R" followed by a number.
- Do not make up any values that are not present in the receipt.
"""
