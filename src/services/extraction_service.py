from __future__ import annotations

import logging
import time

from langchain_community.callbacks import OpenAICallbackHandler, get_openai_callback
from langchain_openai import AzureChatOpenAI

from ..config import config
from ..prompts.extraction_prompt import get_extraction_prompt
from ..utils import api_utils
from ..utils.image_utils import rotate_image
from ..utils.model_utils import get_pydantic_model


@api_utils.retry_with_exponential_backoff
def extract(
    images: list[str],
    classification: str,
    ocr_result: dict,
) -> tuple[dict, OpenAICallbackHandler]:
    logging.info("Starting extraction...")
    
    start_time = time.time()
    rotated_image = rotate_image(images[0], ocr_result["rotation_angle"])
    pydantic_model = get_pydantic_model(classification)
    prompt = get_extraction_prompt([rotated_image], classification, ocr_result)
    llm = AzureChatOpenAI(
        max_tokens=2000,   #extend the max_tokens from 1600 to 2000 for certain receipts with long content
        azure_ad_token=config.AZURE_AD_TOKEN,
        temperature=0,
        default_headers={
            "Ocp-Apim-Subscription-Key": config.AZURE_OPENAI_APIM_SUBS_KEY,
        },
    )
    structured_llm = llm.with_structured_output(pydantic_model)

    with get_openai_callback() as cb:
        response = structured_llm.invoke(prompt)
        logging.info(cb)

    end_time = time.time()
    elapsed_time = end_time - start_time

    logging.info(f"Time taken to extract images: {elapsed_time:.4f} seconds")

    return response, cb
