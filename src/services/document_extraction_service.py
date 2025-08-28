import os
import base64
import datetime
import io
import json
import mimetypes
import time
import filetype

from azure.servicebus import ServiceBusClient
from werkzeug.datastructures import FileStorage

from ..config import config
from ..constants import Constants
from ..utils.logger_utils import log_message
from ..utils.ocr_result_utils import build_extracted_data
from ..utils.log_elapsed_utils import log_elapsed
from . import db_service
from .storage_service import (
    get_document_from_blob,
    move_document_between_containers,
    create_document_to_container,
)
from .service_bus_service import send_message_to_queue
from .storage_queue_service import send_message_to_storage_queue


def process_document_extraction(req: dict, trigger_type: str, blob_service_client, extract_main_func):
    """
    Common function to process document extraction for both Service Bus and Storage Queue triggers.

    Args:
        req: Request data containing file information
        trigger_type: Type of trigger ("service_bus" or "storage_queue")
        blob_service_client: Azure blob storage client
        extract_main_func: Function to call for main extraction logic
    """
    log_message(
        "info", f"{trigger_type.title()} trigger to extract data through GPT4o. Request: {req}", ""
    )

    servicebus_client = ServiceBusClient.from_connection_string(
        os.getenv("AZURE_SHARED_SBUS_SEND_CONN")
    )

    # Parse request data
    filename_split = req.get("file_name").split("_")
    filename_correlation_id = filename_split[len(filename_split) - 1]
    filename_split_dot = req.get("file_name").split(".")
    filename_without_filetype = filename_split_dot[0]
    file_name_extracted = f"{filename_without_filetype}_extracted.json"

    correlation_id = filename_correlation_id.split(".")[0]

    ingested_timestamp = req.get("timestamp")
    ingested_timestamp_object = datetime.datetime.fromtimestamp(
        ingested_timestamp)
    case_id = req.get("case_id")
    document_id = req.get("document_id")
    file_name = req.get("file_name")
    container = req.get("container")
    failed_destination_container = req.get("failed_ocr_container")

    try:
        # Get document from blob storage
        json_content = get_document_from_blob(
            blob_service_client, container, file_name)

        log_message(
            "info",
            f"Successfully got document from blob container. Ingested dateTime: {ingested_timestamp_object.isoformat()}",
            correlation_id,
        )

        # Convert the base64 encoded image to a BytesIO object
        image_bytes = base64.b64decode(json_content.get("file"))
        image_file = io.BytesIO(image_bytes)
        image_kind = filetype.guess(image_bytes)

        file_type = image_kind.extension
        file_mime_type = mimetypes.guess_type(f"file.{file_type}")[0]
        file = FileStorage(image_file, filename=file_name,
                           content_type=file_mime_type)

        # Execute extraction
        try:
            response = extract_main_func(file, correlation_id)
            response_body = json.loads(response.get_body().decode("utf-8"))

            extracted_data = build_extracted_data(
                response.status_code, case_id, document_id, response_body
            )
            log_elapsed(
                ingested_timestamp,
                "Successfully extracted by LLM"
                if response.status_code == 200
                else "Failed to extract via LLM",
                correlation_id,
            )
        except Exception as extract_main_exception:
            extracted_data = build_extracted_data(
                500, case_id, document_id, str(extract_main_exception)
            )
            log_elapsed(
                ingested_timestamp,
                f"Failed to extract via LLM. Error: {str(extract_main_exception)}",
                correlation_id,
            )

        # Create extracted data in storage account container and log elapsed time
        create_document_to_container(
            blob_service_client, container, case_id, file_name_extracted, extracted_data
        )
        log_elapsed(
            ingested_timestamp,
            f"Successfully created OCR extracted data JSON blob on container: {container}",
            correlation_id,
        )

        # Send message to appropriate queue based on trigger type
        if trigger_type == "service_bus":
            send_message_to_queue(
                servicebus_client,
                case_id,
                document_id,
                file_name_extracted,
                container,
                failed_destination_container,
                correlation_id,
                ingested_timestamp,
            )
            log_elapsed(
                ingested_timestamp,
                f"Successfully sent message to Azure ServiceBus queue: {config.AZURE_SERVICE_BUS_SEND_QUEUE}",
                correlation_id,
            )
        elif trigger_type == "storage_queue":
            storage_conn_str = os.getenv("SHARED_STORAGE_CONN")
            send_message_to_storage_queue(
                storage_conn_str,
                case_id,
                document_id,
                file_name_extracted,
                container,
                failed_destination_container,
                correlation_id,
                ingested_timestamp,
            )
            log_elapsed(
                ingested_timestamp,
                f"Successfully sent message to Azure Storage queue: {config.AZURE_STORAGE_SEND_QUEUE}",
                correlation_id,
            )

    except Exception as err:
        handle_extraction_error(err, ingested_timestamp, correlation_id, case_id, document_id,
                                container, failed_destination_container, file_name, trigger_type,
                                blob_service_client)


def handle_extraction_error(err: Exception, ingested_timestamp: float, correlation_id: str,
                            case_id: str, document_id: str, container: str,
                            failed_destination_container: str, file_name: str, trigger_type: str,
                            blob_service_client):
    """Handle extraction errors with proper logging and diagnostics."""
    try:
        err_msg = str(err)
        end_time = time.time()
        elapsed_time = end_time - ingested_timestamp
        elapsed_string = f"{elapsed_time:.4f}"

        log_message(
            "error",
            f"Main exception error: {err_msg}",
            correlation_id,
            case_id,
            document_id,
        )
        log_message(
            "info",
            f"Elapsed time from ingestion to main exception handling: {elapsed_string} seconds",
            correlation_id,
        )

        db_service.create_realtime_diagnostic(
            case_id, document_id, correlation_id, elapsed_string, False, err_msg
        )

        try:
            move_document_between_containers(
                blob_service_client,
                container,
                failed_destination_container,
                case_id,
                file_name,
            )
        except Exception:
            log_message(
                "error", Constants.FAILED_TO_MOVE_DOCUMENT_MESSAGE, correlation_id
            )
    except Exception as innerErr:
        err_msg = str(innerErr)
        try:
            end_time = time.time()
            elapsed_time = end_time - ingested_timestamp
            elapsed_string = f"{elapsed_time:.4f}"

            log_message(
                "error", f"Inner exception error: {err_msg}", correlation_id
            )
            log_message(
                "info",
                f"Elapsed time from ingestion to inner exception handling: {elapsed_string} seconds",
                correlation_id,
            )

            db_service.create_realtime_diagnostic(
                case_id, document_id, correlation_id, elapsed_string, False, err_msg
            )

            try:
                move_document_between_containers(
                    blob_service_client,
                    container,
                    failed_destination_container,
                    case_id,
                    file_name,
                )
            except Exception:
                log_message(
                    "error",
                    Constants.FAILED_TO_MOVE_DOCUMENT_MESSAGE,
                    correlation_id,
                )
        except Exception:
            log_message(
                "error",
                f"Extract {trigger_type} endpoint failed to process document. Please check other logs."
            )
