from typing import List

from pydantic import BaseModel
from src.models.health_receipt_model import HealthReceipt


class HealthReceiptMultipleProviders(BaseModel):
    health_receipts: List[HealthReceipt] = []
