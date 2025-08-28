class Constants:
    LOG_LEVELS = ["fatal", "error", "warn", "info", "debug"]
    RATE_LIMIT_STATUS = 429
    RATE_LIMIT_ERROR_MESSAGE = 'exceeded call rate limit'
    RATE_LIMIT_ERROR_MESSAGE_GPT4o = 'exceeded the throughput limit'
    ALLOWED_IMG_TYPES = ["pdf", "png", "jpeg", "jpg", "tiff", "tif"]
    ALLOWED_IMG_TYPES_STRING = ", ".join(ALLOWED_IMG_TYPES)
    FIRST_RETRY_INTERVAL_IN_MS = 5000
    RETRY_MAX_NUMBER_OF_ATTEMPTS = 3
    FAILED_TO_MOVE_DOCUMENT_MESSAGE = "Failed to move document from source blob container to destination after failed OCR Process"
