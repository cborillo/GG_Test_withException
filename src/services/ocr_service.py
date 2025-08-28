from __future__ import annotations

import base64
import logging
import time
from typing import TYPE_CHECKING

import pandas as pd

from azure.core.exceptions import ServiceResponseError, ServiceRequestError
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from src.utils.model_utils import (
    document_table_to_markdown,
    extract_paragraphs,
    extract_selection_marks,
)

from ..config import config
from ..utils import api_utils


if TYPE_CHECKING:
    from ..models import Classification


@api_utils.retry_with_exponential_backoff_ocr
def ocr(base64_image: str, classification: Classification) -> dict:
    """
    Perform optical character recognition on the provided image.
    """

    ocr_result = {}
    logging.info("Starting optical character recognition...")
    start_time = time.time()

    # Decode the base64-encoded file to get the file bytes
    file_bytes = base64.b64decode(base64_image)
    document_intelligence_client = DocumentAnalysisClient(
        endpoint=config.AZURE_FORM_RECOGNIZER_ENDPOINT,
        credential=AzureKeyCredential(config.AZURE_FORM_RECOGNIZER_API_KEY),
    )
    ocr_model = classification.get_ocr_model()

    try:
        poller = document_intelligence_client.begin_analyze_document(
            ocr_model, file_bytes)
    except (ServiceResponseError, ServiceRequestError) as e:
        raise
    
    result = poller.result()

    page = result.pages[0]
    ocr_result["styles"] = result.styles
    ocr_result["languages"] = result.languages
    ocr_result["paragraphs"] = extract_paragraphs(result.paragraphs)
    ocr_result["selection_marks"] = extract_selection_marks(
        page.selection_marks)
    ocr_result["rotation_angle"] = page.angle
    ocr_result["confidences"] = (
        pd.Series(
            [word.confidence for page in result.pages for word in page.words])
        .describe()
        .round(2)
        .to_dict()
    )

    # Extract and convert tables to Markdown
    tables = []
    for table in result.tables:
        md_table = document_table_to_markdown(table)
        tables.append(md_table)

    ocr_result["tables"] = tables

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(
        f"Time taken to perform optical character recognition: {elapsed_time:.4f} seconds",
    )
    return ocr_result
