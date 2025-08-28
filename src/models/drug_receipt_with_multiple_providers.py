from typing import List, Optional

from pydantic import BaseModel, Field

from src.models.drug_receipt_model import DrugReceipt


class DrugReceiptWithMultipleProviders(BaseModel):
    drug_receipts: Optional[List[DrugReceipt]] = Field(
        default=None,
        description="List of drug receipts",
    )
