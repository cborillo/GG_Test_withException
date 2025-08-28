optional_fields = [
    "spouse_insurance_company",
    "spouse_plan_contract_number",
    "spouse_certificate_number",
    "spouse_date_of_birth",
    "submit_unpaid_portion",
    "amount_paid_by_another_plan",
    "name_of_accredited_school",
    "HCSA",
    "HCSA_only",
    "physician_referral",
]

boolean_fields = [
    "covered_under_any_other_plan",
    "submit_unpaid_portion",
    "HCSA",
    "HCSA_only",
    "physician_referral",
]

spouse_fields = [
    "spouse_insurance_company",
    "spouse_plan_contract_number",
    "spouse_certificate_number",
    "spouse_date_of_birth",
]


claim_confirmation_form_additional_information = f"""
- `patient_name` is the first name of the patient.
- `internal_reference_number` usually starts with H. It is a unique identifier for the claim.
- `provider_not_listed_claim_confirmation_number` is an 8-digit unique identifier for the claim.
- {optional_fields} are optional to the form and may not be present in all claims.
- {boolean_fields} are boolean fields in the form, indicating with 'YES' and 'NO'.
- `name_of_accredited_school` will only be present if the relationship is Child.
- Always have {spouse_fields} in the output, even if they are not present in the form. If they are not present, return null.
- `name_of_accredited_school` should always be a school name or null.
- Look for keywords like 'YES' and 'NO' to extract boolean values.
- Please extract the values for the 'HCSA' and 'HCSA_only' fields with precision. Ensure that the values for these fields are not confused with one another.
- All field - value pairs should be in a same line. Do not look for values in the next line.
- The field `plan_member` should only contain the plan member's last name. A plan members last name will be the last word of the "Plan Member" field.
"""
