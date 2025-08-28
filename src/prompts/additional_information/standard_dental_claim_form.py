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

estimate_keywords = [
    "estimate",
    "pre-determination",
    "authorization",
]

standard_dental_claim_form_additonal_information = f"""
- A standard dental claim form could have multiple variations but should all have required fields. If a field is not present at regular location, look for it through the form.
- A standard dental claim form may contain multiple procedures found in table format. Each procedure will be listed line by line and are to be interpreted left to right. If a value is not present, please do not extract the value and instead return null.
- Here is the structure of the procedures table:

| Date of Service | Procedure Code | Intl. Tooth Code | Tooth Surfaces | Dentist's Fee | Laboratory Charge | Total Charges |
|-----------------|----------------|------------------|----------------|---------------|-------------------|---------------|
|                 |                |                  |                |               |                   |               |
|                 |                |                  |                |               |                   |               |

## Instructions for extraction fields:
- Group_number, certificate_number and member_last_name values are usually in the employee section of the form.
- Group_number may have multiple "0"s in the value. This is an important field. Ensure precise and accurate extraction of this value.
- For estimate field, look for keywords or equivalent keywords of {estimate_keywords}. If any of these keywords are found in the additional information section of the form, or shows up as no dates/realistic dates for any of the service lines, set this to True.
- A true office_verification field will have a valid stamp or signature from the dental office on Office Verification. It requires a valid stamp or signature for True.
- For dental_accident field, there are checkboxes in the patient information section asking if the claim is due to an accident. Set to True if 'Yes' checked, otherwise False. It is possible that the checkboxes for the field are not presented in the form. In this case, return False.
- For initial_placement field, there are checkboxes in the patient information section asking if the claim is an initial placement. Set to True if 'Yes' checked, otherwise False. It is possible that the checkboxes for the field are not presented in the form. In this case, return False.
- For COB field, it is a checkbox related field, consider the given checkbox mark is a reliable reference for checkbox value. There are checkboxes in the patient information section asking are any dental benefits or services under any other group insurance or dental plan, W.C.B or Gov't Plan. Set to True if 'Yes' checked, otherwise False. It is possible that the checkboxes for the field are not presented in the form. In this case, return False.
- - For dental_accident and initial_placement, they are checkbox related field, consider OCR result is a reliable reference for checkbox value. There are two checkboxes for each of these fields. Only if 'yes' checked, set to True.
- For signature field, look for a valid signature from the plan member/subscriber. If found, set to True.
- For HCSA and HCSA_only fields, pay attention to the distinction that if the plan member wants to reimburse claim only with HCSA. These two fields are mutually exclusive. The information is usually in additional information section of the form.
- For initial_placement_date, look for the date of initial placement. This information is usually in the additional information section of the form but could be somewhere else.
- For total_submitted_charges, it is usually in the total charges section of the form. Ensure that this value is the sum of all the charges of services in the table.
- A Procedure Code has 5 digits.
- A tooth code should be in {tooth_codes} typically comes right after the Procedure Code.
- For lab_fee field, look for Laboratory Charge of the service. It is likely that lab_fee will be empty. If it is, return null.
- For CDA_number field, it's usually in the dentist section of the form and shows up as an unique number/id.
- Any first or last name can be possibly of foreign origin.
- For spouse_certificate_number field, it is not Patient I.D. No. If the field is not presented in the form, return null.
- For spouse_policy_number field, look for policy number or group number in the patient information section. It must not be same as group_number field value. If field not filled, return null.
- For spouse_insurance_company field, look for insurance company name in the patient information section. If not filled, return null.
- Always look for spouse_info class values in the patient information section of the form.

- Ensure the correct identification of 'dentist', 'plan member', and 'patient' by using the keywords 'dentist', 'plan member', and 'patient' to locate the appropriate values.
-  Divide the top third of the form into three equal horizontal sections:
  - The first section contains the patient's information.
  - The second section contains the provider's information.
  - The third section contains the assignment information.
-  Here is a visual representation of the form for reference:

    ```
    |----------------|-----------|------|----------------------------|--------------|
    | PART 1 DENTIST | Unique No | Spec | Patients Office Account no |              |
    |----------------|-----------|------|----------------------------| [ASSIGN BOX] |
    | Patient info   | Provider info                                 |              |
    |----------------|-----------------------------------------------|--------------|
    ```

Strict rules to follow for the following fields:
    - `patient_first_name`:
        - Found besides the string `PART 1 DENTIST` in the OCR results.
        - Located within the top vertical third and first horizontal third of the form.
        - Found within the first 30% of the OCR results. Do not consider any string after this for this field.
        - Closer to the string "PART 1 DENTIST" than `provider_first_name` in the OCR results.
        - Always appears before `provider_first_name` in the OCR results.
        - Always appears before the string "INSTRUCTIONS FOR CLAIM SUBMISSION" in the OCR results.
            - Do not consider any first name after the string "INSTRUCTIONS FOR CLAIM SUBMISSION"
        - Is the first first name appearing in the OCR results.
        - Always appears one line before the first address in the OCR results.
        - Is not necessarily the same as the "Employee/Plan Member/Subscriber" name located in the "PART 2 · EMPLOYEE/PLAN MEMBER/SUBSCRIBER" section
    - `provider_first_name` and `provider_last_name`:
        - Located within the top vertical third and second horizontal third of the form.
        - Found after `patient_first_name` in the OCR results.
        - Closer to a telephone number and professional designation (e.g., Dr.) than `patient_first_name` in the OCR results.
        - Always appears before "INSTRUCTIONS FOR CLAIM SUBMISSION" in the OCR results.
    - `member_last_name`:
        - Found after the `PART 2 · EMPLOYEE/PLAN MEMBER/SUBSCRIBER` section in the OCR results.
        - Found directly besides the string `2. YOUR NAME (PLEASE PRINT)` in the OCR results.

- For the `claim_info` field `assigned`, examine the top right box of the dental claim form beginning with the text "I hereby assign my beneftis..." and containing the text "Signature of subscriber" and set the value as follows:
    - Set to True if:
        1. A handwritten signature is present in the box. An 'X' is not considered a signature.
        2. "PAY PROVIDER" text is present WITHOUT a signature.
    - Set to False if:
        1. "PAY SUBSCRIBER" text is present (regardless of signature).
        2. A big 'X' or a single slash mark is handwritten in the box.
        3. The box is empty.
        4. Any other condition.
- For the `service_lines` field, carefully looking for all service items and do not miss any of them. 
Carefully double check all return values and make sure they are accurate and correct. Especially for checkboxes and signature required fields.
"""
