import os
from functools import lru_cache
from time import time

from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


class Config:
    AZURE_APPSEC_HEADERS = {
        "Content-Type": "application/json",
        "Cache-control": "no-store",
        "Pragma": "no-cache",
        "X-Content-Type-Options": "nosniff",
        "Content-Security-Policy": "default-src 'self'; form-action 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content",
        "X-Permitted-Cross-Domain-Policies": "none",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=63072000; includeSubDomains;",
    }
    AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_APIM_SUBS_KEY = os.getenv("AZURE_OPENAI_APIM_SUBS_KEY")
    AZURE_OPENAI_SCOPE = "https://cognitiveservices.azure.com/.default"
    AZURE_COSMOS_CONSTR = os.getenv("AZURE_COSMOS_CONSTR")
    AZURE_FORM_RECOGNIZER_API_KEY = os.getenv("AZURE_FORM_RECOGNIZER_API_KEY")
    AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    AZURE_SERVICE_BUS_SEND_QUEUE = "claimdocument-processing-completed"
    AZURE_STORAGE_SEND_QUEUE = "claimdocument-strque-processing-completed"
    ERROR_RATE_LIMIT_STRING = "exceeded the throughput limit"
    ERROR_RATE_LIMIT_CODE_STRING = "Error code: 429"
    ENVIRONMENT = os.getenv("ENV")
    APIM_BACKEND_CLIENTID = os.getenv("APIM_BACKEND_CLIENTID")

    @property
    def AZURE_AD_TOKEN(self):
        return self._get_fresh_token()

    @lru_cache(maxsize=1)
    def _get_azure_ad_token(self):
        token = DefaultAzureCredential().get_token(self.AZURE_OPENAI_SCOPE)
        return token.token, token.expires_on

    def _get_fresh_token(self, token_refresh_margin_minutes: int = 5):
        token, expiry = self._get_azure_ad_token()
        if time() > expiry - token_refresh_margin_minutes * 60:
            self._get_azure_ad_token.cache_clear()
            token, _ = self._get_azure_ad_token()
        return token


config = Config()
