import requests
from src.utils.logger_utils import log_message
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(3), wait=wait_fixed(30), reraise=True)
def post_with_retries_files(url, correlation_id, headers, files):
    log_message(
        'info', f'Invoked endpoint: {url}', correlation_id)

    response = requests.post(url, headers=headers, files=files)
    response.raise_for_status()
    return response


@retry(stop=stop_after_attempt(3), wait=wait_fixed(30), reraise=True)
def post_with_retries_json(url, correlation_id, headers, payload):
    log_message(
        'info', f'Invoked endpoint: {url}', correlation_id)

    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
    return response


@retry(stop=stop_after_attempt(3), wait=wait_fixed(30), reraise=True)
def patch_with_retries_json(url, correlation_id, headers, payload):
    log_message(
        'info', f'Invoked endpoint: {url}', correlation_id)

    response = requests.patch(url, headers=headers, data=payload)
    response.raise_for_status()
    return response
