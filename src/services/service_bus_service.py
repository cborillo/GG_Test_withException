import json

from azure.servicebus import ServiceBusMessage

from src.config import config

def send_message_to_queue(servicebus_client, case_id, 
                          document_id, file_name_extracted, container, failed_destination_container, 
                          correlation_id, ingested_timestamp):
    try:
        message_str = {
            'ingested_timestamp': ingested_timestamp,
            'case_id': case_id,
            'document_id': document_id,
            'file_name': file_name_extracted,
            'container': container,
            'failed_ocr_container': failed_destination_container,
            'correlation_id': correlation_id
        }
        # create a ServiceBusMessage
        message = ServiceBusMessage(json.dumps(message_str))

        # send the message
        with servicebus_client.get_queue_sender(config.AZURE_SERVICE_BUS_SEND_QUEUE) as sender:
            sender.send_messages(message)
    except Exception as sbus_err:
        raise