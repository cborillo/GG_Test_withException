from __future__ import annotations

import logging
import time

from langchain_community.callbacks import OpenAICallbackHandler, get_openai_callback
from langchain_openai import AzureChatOpenAI

from ..config import config
from ..models import Classification
from ..prompts.classification_prompt import get_classification_prompt
from ..utils import api_utils


@api_utils.retry_with_exponential_backoff
def classify(images: list[str]) -> tuple[Classification, OpenAICallbackHandler]:
    logging.info("Starting classification...")
    start_time = time.time()

    prompt = get_classification_prompt(images)
    llm = AzureChatOpenAI(
        max_tokens=400, azure_ad_token=config.AZURE_AD_TOKEN, temperature=0,
        default_headers={
            'Ocp-Apim-Subscription-Key': config.AZURE_OPENAI_APIM_SUBS_KEY}
    )
    structured_llm = llm.with_structured_output(Classification)

    with get_openai_callback() as cb:
        response = structured_llm.invoke(prompt)
        logging.info(cb)

    end_time = time.time()
    elapsed_time = end_time - start_time

    logging.info(f"Time taken to classify images: {elapsed_time:.4f} seconds")

    return response, cb
