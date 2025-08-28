from src.prompts.additional_information.health_receipt import health_service_lines

health_explanation_of_benefits_additional_information = f"""
- For cob_amount, extract the amount of the coordination of benefit that is paid for the given health expense.
- For total_cob_amount, extract the total amount of the health benefit claim that is paid.
- For the `service_code` field, extract the service name from the receipt and map it to the closest equivalent service name in the following array: {health_service_lines}. For example, if the service is identified as "Massage Therapy", the closest equivalent servcie in the array is "Massage Therapist".
"""
