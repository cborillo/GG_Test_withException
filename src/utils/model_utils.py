from __future__ import annotations

import importlib

from deepdiff import DeepDiff

from src.models.health_explanation_of_benefits import HealthExplanationOfBenefits

from ..models import (
    ClaimConfirmationForm,
    DentalExplanationOfBenefits,
    DrugReceipt,
    DrugReceiptWithMultipleProviders,
    ExtendedHealthClaimFormPageOne,
    HealthReceipt,
    HealthReceiptMultipleProviders,
    StandardDentalClaimForm,
    DrugExplanationOfBenefits,
    PrescriptionDrugAuthorizationForm
)


def get_pydantic_model(
    classification,
) -> (
    StandardDentalClaimForm
    | DentalExplanationOfBenefits
    | ExtendedHealthClaimFormPageOne
    | HealthReceipt
    | HealthReceiptMultipleProviders
    | DrugReceipt
    | DrugReceiptWithMultipleProviders
    | ClaimConfirmationForm
    | DrugExplanationOfBenefits
    | PrescriptionDrugAuthorizationForm
):
    """Get the Pydantic model class based on the classification of the form.

    Args:
    ----
        classification (str): The classification of the form.

    Returns:
    -------
        type: The Pydantic model class corresponding to the classification.

    """
    match classification:
        case "Standard Dental Claim Form":
            return StandardDentalClaimForm
        case "Dental Explanation of Benefits":
            return DentalExplanationOfBenefits
        case "Extended Health Claim Form (Page 1)":
            return ExtendedHealthClaimFormPageOne
        case "Health Receipt":
            return HealthReceipt
        case "Health Receipt with Multiple Providers":
            return HealthReceiptMultipleProviders
        case "Health Explanation of Benefits":
            return HealthExplanationOfBenefits
        case "Drug Receipt":
            return DrugReceipt
        case "Drug Receipt with Multiple Providers":
            return DrugReceiptWithMultipleProviders
        case "Drug Explanation of Benefits":
            return DrugExplanationOfBenefits
        case "Claim Confirmation Form":
            return ClaimConfirmationForm
        case "Prescription Drug Authorization Form (Page 1)":
            return PrescriptionDrugAuthorizationForm
        case _:
            msg = f"Unknown classification: {classification}"
            raise ValueError(msg)


def dynamic_import_type(obj):
    obj_type = type(obj)
    module_name = obj_type.__module__
    class_name = obj_type.__name__

    module = importlib.import_module(module_name)
    return getattr(module, class_name)


class DictComparator:
    def __init__(self, reference: dict, other: dict) -> None:
        self.reference = reference
        self.other = other
        self.diff = self._compare_dicts()

    def _compare_dicts(self) -> DeepDiff:
        return DeepDiff(
            self.reference,
            self.other,
            view="tree",
            ignore_string_case=True,
        )

    def get_diff_keys(self) -> list[str]:
        keys = set()

        for changes in self.diff.values():
            for change in changes:
                path = change.path(output_format="list")
                filtered_path = [str(p) for p in path if not isinstance(p, int)]
                keys.add(".".join(filtered_path))

        return sorted(keys)


def document_table_to_markdown(doc_table):
    # Create an empty 2D list to hold the table content
    table = [
        ["" for _ in range(doc_table.column_count)] for _ in range(doc_table.row_count)
    ]

    # Populate the table with cell contents
    for cell in doc_table.cells:
        for i in range(cell.row_span):
            for j in range(cell.column_span):
                table[cell.row_index + i][cell.column_index + j] = cell.content

    # Create the markdown string
    markdown_str = ""

    for row in table:
        markdown_str += "| " + " | ".join(row) + " |\n"

    # Add header separator
    if table:
        header_separator = "|---" * doc_table.column_count + "|\n"
        markdown_str = (
            markdown_str.split("\n", 1)[0]
            + "\n"
            + header_separator
            + markdown_str.split("\n", 1)[1]
        )

    return markdown_str


def extract_paragraphs(document_paragraphs):
    paragraphs = []
    for paragraph in document_paragraphs:
        content = paragraph.content.replace(":selected:", "").replace(":unselected:", "")  # Remove selection marks from content
        paragraphs.append(content)
    return paragraphs


def extract_selection_marks(document_selection_marks):
    selection_marks = []
    for mark in document_selection_marks:
        selection_marks.append(mark.state)
    return selection_marks
