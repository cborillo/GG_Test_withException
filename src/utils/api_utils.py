import random
import time

from typing import Any, Callable, Optional
from azure.core.exceptions import ServiceResponseError, ServiceRequestError, HttpResponseError
from openai import RateLimitError
from ..config import config


def str_to_bool(value):
    """Convert a string to a boolean.

    Args:
    ----
        value (str): The string to convert.

    Returns:
    -------
        bool: The converted boolean value.

    """
    return value.lower() in ("true", "1", "t", "y", "yes")


def retry_with_exponential_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1,
    max_delay: float = 16,
    exponential_base: float = 2,
    jitter: bool = True,
    errors: tuple = (RateLimitError,),
) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        retries = 0

        while True:
            try:
                return func(*args, **kwargs)

            except errors as e:
                retries += 1
                if retries > max_retries:
                    raise

                delay = get_retry_after(e) or min(
                    base_delay * (exponential_base ** (retries - 1)),
                    max_delay,
                )

                if jitter:
                    # 10% jitter
                    delay *= 1 + random.random() * 0.1

                time.sleep(delay)

            except Exception:
                raise

    return wrapper


def retry_with_exponential_backoff_ocr(
    func: Callable,
    max_retries: int = 4,
    base_delay: float = 4,
    max_delay: float = 32,
    exponential_base: float = 2,
    jitter: bool = True,
    errors: tuple = (RateLimitError, ServiceResponseError, ServiceRequestError, HttpResponseError),
) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        retries = 0

        while True:
            try:
                return func(*args, **kwargs)

            except errors as e:
                retries += 1
                if retries > max_retries:
                    raise

                delay = get_retry_after(e) or min(
                    base_delay * (exponential_base ** (retries - 1)),
                    max_delay,
                )

                if jitter:
                    # 10% jitter
                    delay *= 1 + random.random() * 0.1

                time.sleep(delay)

            except Exception:
                raise

    return wrapper


def get_retry_after(error: Exception) -> Optional[float]:
    if hasattr(error, "headers") and "Retry-After" in error.headers:
        return float(error.headers["Retry-After"])
    return None


def error_code(error_msg: str):
    return 429 if config.ERROR_RATE_LIMIT_CODE_STRING in error_msg or config.ERROR_RATE_LIMIT_STRING in error_msg else 500
