from datetime import datetime, timezone
from pymongo import MongoClient
from ..config import config

# Initialize the MongoDB client

mongo_connection_string = config.AZURE_COSMOS_CONSTR
environment = config.ENVIRONMENT

database_name = "idp"
collection_name_realtime = "realtime"
collection_name_diagnostics = "diagnostics"

client = MongoClient(mongo_connection_string)
database = client[database_name]
collection = database[collection_name_realtime]
collection_diagnostics = database[collection_name_diagnostics]


def create_realtime_analytic(confidence: dict) -> None:
    """Stores a confidence value in a MongoDB collection for real-time analytics and reporting.

    This function generates a unique document ID and current timestamp, then stores a document containing
    the confidence value, ID, and timestamp in a specified MongoDB collection.

    Args:
    ----
        confidence (float): The confidence value to be stored in the database.

    Raises:
    ------
        pymongo.errors.PyMongoError: If an error occurs while inserting the document into the collection.

    Example:
    -------
        >>> create_realtime_analytic(0.95)
        Document with ID f47ac10b-58cc-4372-a567-0e02b2c3d479 created successfully.

    """
    # Create the document to be stored in MongoDB
    document = {
        "confidence": confidence.get("average_confidence_level"),
        "timestamp": datetime.now(timezone.utc),
    }

    # Store the document in the MongoDB collection
    result = collection.insert_one(document)

    print(f"Realtime analytic with ID {result.inserted_id} created successfully.")


def create_realtime_diagnostic(case_id: str, document_id: str, correlation_id: str, elapsed_time: str, is_success: bool, error_message: str, is_ocr_success: bool = False) -> None:
    # Create the document to be stored in MongoDB
    document = {
        "environment": environment,
        "case_id": case_id,
        "document_id": document_id,
        "correlation_id":  correlation_id,
        "elapsed_time_seconds": elapsed_time,
        "is_ocr_success": is_ocr_success,
        "is_success": is_success,
        "error_message": error_message,
        "timestamp": datetime.now(timezone.utc)
    }

    # Store the document in the MongoDB collection
    result = collection_diagnostics.insert_one(document)

    print(
        f"Realtime diagnostics with ID {result.inserted_id} created successfully.")
    
    return True
