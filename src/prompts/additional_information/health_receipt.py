health_service_lines = [
    "Chiropractor",
    "Massage Therapist",
    "Naturopath",
    "Osteopath",
    "Psychologist",
    "Speech Therapist",
    "Acupuncturist",
    "Athletic Therapist",
    "Audiologist",
    "Cataract Contact Lenses",
    "Chiropodist",
    "Christian Science Practitioner",
    "Clinical Counsellor",
    "Dietician",
    "Elective Contact Lenses",
    "Eye Exam",
    "Frames",
    "Frames Repair",
    "Glasses",
    "Glasses Repair",
    "Homeopath",
    "Kinesiologist",
    "Laser Eye Surgery",
    "Lenses",
    "Marriage and Family Therapist",
    "Nutritionist",
    "Occupational Therapist",
    "Orthotherapist",
    "Podiatrist",
    "Prescription Safety Glasses",
    "Prescription Sun Glasses",
    "Psychiatrist",
    "Psychoanalyst",
    "Psychotherapy",
    "Physiotherapist",
    "Reflexologist",
    "Safety Glasses",
    "Shiatsu Therapist",
    "Social Worker",
    "Sun Glasses",
    "Visual Training",
    "Ambulance",
]


no_sub_service_lines = [
    "Eye Exam",
    "Visual Training",
    "Glasses",
    "Elective Contact Lenses",
    "Frames",
    "Lenses",
]


health_related_keywords = [
    "Initial",
    "Subsequent",
    "Laser Therapy",
    "X-ray",
    "Surgery",
    "Surgical Trays",
    "Group",
    "Marriage Counselling",
    "Family Counselling",
    "Report Fees-Eligible",
    "Nutritional Supplements",
    "Diagnostic Testing",
]

sub_service_mapping = {
    "Ambulance": "L",
}


health_receipt_additional_information = f"""
- For the `provider_province` field, return the full standard province name. For example, if you find "BC", return "British Columbia".
- The `provider_registration_number` refers to the provider's registration number or license number.
- The `provider_first_name` and `provider_last_name` fields are sometimes located next to their registration number.
- For `provider_postal_code` field, looking for postal code of the provider or clinic. If the postal code appears next to the name of the patient, it is the postal code of the patient, not the provider. DO NOT return the patient's postal code.
- For `provider_phone_number` field, looking for phone number of the provider or clinic, and only output the phone number of provider in XXXXXXXXXX format.
- For the `patient_first_name` field, extract only the patient's first name from the receipt. Do not extract full name.
- Every service in the receipt should be considered as a separate `ServiceInfo` object.
- For the `service_code` field, extract the service name from the receipt and map it to the closest equivalent service name in the following array: {health_service_lines}. For example, if the service is identified as "Massage Therapy", the closest equivalent servcie in the array is "Massage Therapist". A service having 0 total charge should also be considered as a service code.
- If there are other items with expense in the receipt that are not a treatment, still consider them as separate service. For example, if the receipt contains "Medicine" item along with other treatment, consider it as a separate service and use the item name as the service code.
- For the `sub_service_code` field, follow these instruction:
    1. If the service code is a key in this dictionary {sub_service_mapping}, then use the corresponding value in the dictionary as the sub service code.
    2. If the corresponding service code is a paramedical treatment, then the default value is 'subsequent', otherwise the default value is None.
    3. Look for following keywords or equivalent words in the content: {health_related_keywords}, ignoring letter cases. If any keywords or equivalent words are found, return the keyword in the list.
"""
