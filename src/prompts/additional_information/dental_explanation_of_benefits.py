tooth_codes = [
    "00",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "38",
    "41",
    "42",
    "43",
    "44",
    "45",
    "46",
    "47",
    "48",
    "51",
    "52",
    "53",
    "54",
    "55",
    "61",
    "62",
    "63",
    "64",
    "65",
    "71",
    "72",
    "73",
    "74",
    "75",
    "81",
    "82",
    "83",
    "84",
    "85",
]


dental_explanation_of_benefits_additional_information = f"""
- For total_cob_amount, it is usually referred as 'total payable to insured', 'total benefit to dentist' or equivalent terms. It is coming from the total sum of 'BENEFIT' columns in procedure table, so if the value is not found directly, return the sum of 'BENEFIT' columns in the procedure table.
- A procedure is a single service line in the explanation of benefits. It is usually found in a table format.
- A tooth code should be in {tooth_codes} typically comes right after the Procedure Code.
- A date_of_service must be formatted as YYYY-MM-DD (e.g., "2024-03-15"). Convert all date formats including MM/DD/YYYY, DD/MM/YYYY, YYYY/MM/DD, textual dates like "MAR, 27, 25", "Nov/19/24", or space-separated formats like "25 02 01" (YY MM DD).
- tooth_surface, dentist_fee, lab_fee are optional for an explanation of benefits form, if not presented, return None. Eligible fee is not dentist fee, it is the fee that is covered by the insurance.

**CRITICAL SERVICE LINE EXTRACTION RULES: - All rules must be followed**
- Use the given table information (if available) to extract correct same row values for a procedure. 
- `total_charges` is usually referred as 'charges' in the procedure table, do not take eligible fee as total charges. `cob_amount` is usually referred as 'benefit' in the procedure table.
- `total_charges` and `cob_amount` should be extracted from the same row in the procedure table. You must only look for these values from the horizontal right of the procedure_code. Never retrive any values that are not in the same row as the procedure_code.
- If there are duplicate procedures, treat them as separate service lines and read values independently.

Ensure accuracy by not fabricating any values not present in the receipt.
"""
