from typing import List, Optional
from pydantic import BaseModel, Field
from src.models.health_receipt_model import ServiceInfo


class ExtendedServiceInfo(ServiceInfo):
    cob_amount: Optional[float] = Field(
        default=None,
        description="Amount of the health expense that is covered by the coordination of benefits",
        example=45.89,
    )


class HealthExplanationOfBenefits(BaseModel):
    health_expenses: List[ExtendedServiceInfo] = []
    total_cob_amount: Optional[float] = Field(
        default=None,
        description="Total amount of the claim that is covered by the coordination of benefits",
        example=120.49,
    )
