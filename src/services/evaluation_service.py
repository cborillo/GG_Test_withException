import logging
import time
from typing import List

from langchain_community.callbacks import OpenAICallbackHandler, get_openai_callback
from langchain_openai import AzureChatOpenAI

from ..config import config
from ..prompts.evaluation_prompt import get_evaluation_prompt
from ..utils import api_utils
from ..utils.json_utils import extract_json


@api_utils.retry_with_exponential_backoff
def evaluate(images: List[str], classification: str, extraction) -> tuple[dict, OpenAICallbackHandler]:
    logging.info("Starting evaluation...")
    start_time = time.time()

    llm = AzureChatOpenAI(
        max_tokens=4096, azure_ad_token=config.AZURE_AD_TOKEN, temperature=0.2,
        default_headers={
            'Ocp-Apim-Subscription-Key': config.AZURE_OPENAI_APIM_SUBS_KEY}
    )
    prompt = get_evaluation_prompt(images, classification, extraction)

    with get_openai_callback() as cb:
        response = llm.invoke(prompt)
        logging.info(cb)

    end_time = time.time()
    elapsed_time = end_time - start_time

    logging.info(
        f"Time taken to evaluate extraction: {elapsed_time:.4f} seconds")

    try:
        result = extract_json(response.content)
    except ValueError:
        result = {}
    return result, cb
