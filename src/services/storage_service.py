import json
from datetime import timezone

from azure.storage.blob import BlobServiceClient


def connect_to_blob_storage(connect_str):
    return BlobServiceClient.from_connection_string(connect_str)


def get_document_from_blob(blob_service_client, container, file_name):
    container_client = blob_service_client.get_container_client(container)
    blob_client = container_client.get_blob_client(file_name)

    # read the binary content of the blob
    binary_content = blob_client.download_blob().readall()

    # decode the bytes to a UTF-8 string
    utf8_content = binary_content.decode('utf-8')

    # deserialize the JSON content
    json_content = json.loads(utf8_content)

    return json_content


def delete_document_from_blob(blob_service_client, container, file_name):
    try:
        container_client = blob_service_client.get_container_client(container)
        blob_client = container_client.get_blob_client(file_name)

        # Delete the blob
        blob_client.delete_blob()
    except Exception as e:
        # Let the exception be rethrown automatically
        raise
    
    
def move_document_between_containers(blob_service_client, source_container, destination_container, case_id, file_name):
    try:
        # Get the source container client and blob client
        source_container_client = blob_service_client.get_container_client(source_container)
        source_blob_client = source_container_client.get_blob_client(file_name)

        # Download the blob content
        binary_content = source_blob_client.download_blob().readall()

        # Get the destination container client and blob client
        destination_container_client = blob_service_client.get_container_client(destination_container)
        destination_blob_client = destination_container_client.get_blob_client(f'{case_id}/{file_name}')

        # Upload the blob to the destination container
        destination_blob_client.upload_blob(binary_content, overwrite=True)

        # Delete the blob from the source container
        source_blob_client.delete_blob()
    except Exception as e:
        raise
    
def create_document_to_container(blob_service_client, destination_container, case_id, file_name, data):
    try:
        # Get the destination container client and blob client
        destination_container_client = blob_service_client.get_container_client(destination_container)
            
        # Create the blob client with the folder path included in the blob name
        blob_client = destination_container_client.get_blob_client(f"{file_name}")
        
        # Convert the data to JSON format
        json_data = json.dumps(data)
        
        # Upload the JSON data to the blob
        blob_client.upload_blob(json_data, overwrite=True)
    except Exception as e:
        raise
