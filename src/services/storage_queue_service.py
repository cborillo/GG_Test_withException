import json
import base64

from src.config import config
from azure.storage.queue import QueueClient


def send_message_to_storage_queue(storage_connection_string, case_id,
                                  document_id, file_name_extracted, container, failed_destination_container,
                                  correlation_id, ingested_timestamp):
    """
    Send message to Azure Storage Queue.

    Args:
        storage_connection_string: Azure storage connection string
        case_id: Case identifier
        document_id: Document identifier
        file_name_extracted: Name of the extracted file
        container: Storage container name
        failed_destination_container: Failed container name
        correlation_id: Correlation identifier
        ingested_timestamp: Timestamp when document was ingested
    """
    try:
        message_data = {
            'ingested_timestamp': ingested_timestamp,
            'case_id': case_id,
            'document_id': document_id,
            'file_name': file_name_extracted,
            'container': container,
            'failed_ocr_container': failed_destination_container,
            'correlation_id': correlation_id
        }

        # Create QueueClient using the storage connection string
        queue_client = QueueClient.from_connection_string(
            conn_str=storage_connection_string,
            queue_name=config.AZURE_STORAGE_SEND_QUEUE
        )

        message_text = json.dumps(message_data)
        encoded_message = base64.b64encode(
            message_text.encode('utf-8')).decode('utf-8')

        # Send the message to storage queue
        queue_client.send_message(encoded_message)
    except Exception as storage_queue_err:
        raise
