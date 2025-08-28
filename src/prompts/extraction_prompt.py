from ..utils.image_utils import append_images_to_messages
from .additional_information.dental_explanation_of_benefits import (
    dental_explanation_of_benefits_additional_information,
)
from .additional_information.health_explanation_of_benefits import (
    health_explanation_of_benefits_additional_information,
)
from .additional_information.extended_health_claim_form import (
    extended_health_claim_form_page_1_additional_information,
)
from .additional_information.health_receipt import health_receipt_additional_information
from .additional_information.drug_receipt import drug_receipt_additional_information
from .additional_information.drug_explanation_of_benefits import (
    drug_explanation_of_benefits_additional_information,
)
from .additional_information.standard_dental_claim_form import (
    standard_dental_claim_form_additonal_information,
)
from .additional_information.claim_confirmation_form import (
    claim_confirmation_form_additional_information,
)
from .additional_information.prescription_drug_authorization_form import (
    prescription_drug_authorization_form_additional_information,
)
from .one_shot_examples.dental_explanation_of_benefits import (
    dental_explanation_of_benefits_one_shot,
)
from .one_shot_examples.health_explanation_of_benefits import (
    health_explanation_of_benefits_one_shot,
)
from .one_shot_examples.extended_health_claim_form import (
    extended_health_claim_form_page_1_one_shot,
)
from .one_shot_examples.health_receipt import (
    health_receipt_one_shot,
)
from .one_shot_examples.health_receipt_multiple_providers import (
    health_receipt_multiple_providers_one_shot,
)
from .one_shot_examples.claim_confirmation_form import claim_confirmation_form_one_shot
from .one_shot_examples.standard_dental_claim_form import (
    standard_dental_claim_form_one_shot,
)
from .one_shot_examples.drug_receipt import drug_receipt_one_shot
from .one_shot_examples.drug_explanation_of_benefits import (
    drug_explanation_of_benefits_one_shot,
)
from .one_shot_examples.prescription_drug_authorization_form import (
    prescription_drug_authorization_form_one_shot,
)


def get_extraction_prompt(images: list, classification: str, ocr_result: dict):
    context = get_additional_context(classification)
    styles = ocr_result.get("styles", "")
    languages = ocr_result.get("languages", "")
    paragraphs = ocr_result.get("paragraphs", "")
    selection_marks = ocr_result.get("selection_marks", [])
    tables = ocr_result.get("tables", [])

    system_message = f"""
    You are an AI assistant that extracts information from health-related documents written in French or English for an insurance company. Your task is to extract relevant data from {classification} images.

    Extract all relevant information, including but not limited to provider information, service information, and any other pertinent details.

    Return the extracted information as JSON output. If any fields or key/value pairs appear to be blank, do not attempt to extract the value. Instead, omit it from the returned JSON output.

    The following is an OCR result for the provided image. Use this OCR result with the provided image for the extraction.
    
    Styles:
    ```
    {styles}
    ```

    Languages:
    ```
    {languages}
    ```

    Paragraphs
    ```
    {paragraphs}
    ```
    
    Checkbox Marks:
    ```
    {selection_marks}
    ```

    Tables:
    ```
    {tables}

    The following is additional information and a one-shot example to help you with the extraction process.

    Additional Information:
    ```
    {context.additional_information}
    ```

    One-Shot JSON Example:
    ```
    {context.one_shot_example}
    ```

    Adapt your extraction based on the specific content and format of the document you're analyzing.
    """

    messages = [
        {
            "role": "system",
            "content": system_message,
        },
    ]

    return append_images_to_messages(images, messages)


class AdditionalContext:
    def __init__(self, one_shot_example, additional_information) -> None:
        self.one_shot_example = one_shot_example
        self.additional_information = additional_information


def get_additional_context(classification: str):
    match classification:
        case "Standard Dental Claim Form":
            return AdditionalContext(
                one_shot_example=standard_dental_claim_form_one_shot,
                additional_information=standard_dental_claim_form_additonal_information,
            )
        case "Dental Explanation of Benefits":
            return AdditionalContext(
                one_shot_example=dental_explanation_of_benefits_one_shot,
                additional_information=dental_explanation_of_benefits_additional_information,
            )
        case "Extended Health Claim Form (Page 1)":
            return AdditionalContext(
                one_shot_example=extended_health_claim_form_page_1_one_shot,
                additional_information=extended_health_claim_form_page_1_additional_information,
            )
        case "Health Receipt":
            return AdditionalContext(
                one_shot_example=health_receipt_one_shot,
                additional_information=health_receipt_additional_information,
            )
        case "Health Receipt with Multiple Providers":
            return AdditionalContext(
                one_shot_example=health_receipt_multiple_providers_one_shot,
                additional_information=health_receipt_additional_information,
            )
        case "Health Explanation of Benefits":
            return AdditionalContext(
                one_shot_example=health_explanation_of_benefits_one_shot,
                additional_information=health_explanation_of_benefits_additional_information,
            )
        case "Drug Receipt":
            return AdditionalContext(
                one_shot_example=drug_receipt_one_shot,
                additional_information=drug_receipt_additional_information,
            )
        case "Drug Receipt with Multiple Providers":
            return AdditionalContext(one_shot_example="", additional_information="")
        case "Drug Explanation of Benefits":
            return AdditionalContext(
                one_shot_example=drug_explanation_of_benefits_one_shot,
                additional_information=drug_explanation_of_benefits_additional_information,
            )
        case "Claim Confirmation Form":
            return AdditionalContext(
                one_shot_example=claim_confirmation_form_one_shot,
                additional_information=claim_confirmation_form_additional_information,
            )
        case "Prescription Drug Authorization Form (Page 1)":
            return AdditionalContext(
                one_shot_example=prescription_drug_authorization_form_one_shot,
                additional_information=prescription_drug_authorization_form_additional_information,
            )
        case _:
            msg = f"Unknown classification: {classification}"
            raise ValueError(msg)
