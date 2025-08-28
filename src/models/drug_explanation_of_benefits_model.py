from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from src.models.validators.drug_quantity_type import validate_drug_quantity_type


class ServiceInfo(BaseModel):
    date_of_service: Optional[date] = Field(
        default=None,
        description="Date of service",
    )
    drug_identification_number: Optional[str] = Field(
        default=None,
        description="Eight digit drug identification number assigned to a drug product, also known as DIN number",
        example="00586676",
    )
    rx_number: Optional[str] = Field(
        default=None,
        description="Seven digit prescription number assigned to a prescription",
        example="1159834",
    )
    drug_quantity: Optional[int] = Field(
        default=None,
        description="The number of units of the drug sold",
        example=1,
    )
    drug_quantity_type: Optional[str] = Field(
        default=None,
        description="Unit of the drug sold (grams, tablets, patches, injections, etc.)",
        example="TAB",
    )
    dispensing_fee: Optional[float] = Field(
        default=None,
        description="Cost of storing and preparing prescription medication",
        example=203.4,
    )
    drug_cost: Optional[float] = Field(
        default=None,
        description="Cost of prescription",
        example=203.4,
    )
    patient_paid: Optional[float] = Field(
        default=None,
        description="Amount paid by patient",
        example=203.4,
    )
    province_paid: Optional[bool] = Field(
        default=False,
        description="Indicates whether or not the drug claim is part of a provincial drug plan",
    )
    dispensing_province: Optional[str] = Field(
        default=None,
        description="Province the drug was dispensed in",
        example="ON",
    )
    total_charge: Optional[float] = Field(
        default=None,
        description="Total charge including the tax of this prescription",
        example=203.4,
    )
    cob_amount: Optional[float] = Field(
        default=None,
        description="Amount of the drug service that is covered by the coordination of benefits",
        example=45.89,
    )

    @field_validator("drug_quantity_type")
    @classmethod
    def validate_quantity_type(cls, v):
        return validate_drug_quantity_type(v)


class DrugExplanationOfBenefits(BaseModel):
    patient_first_name: Optional[str] = Field(
        default=None,
        description="Patient's first name",
        example="John",
    )
    patient_last_name: Optional[str] = Field(
        default=None,
        description="Patient's last name",
        example="Doe",
    )
    service_lines: List[ServiceInfo]=[]
    total_cob_amount: Optional[float] = Field(
        default=None,
        description="Total amount of the claim that is covered by the coordination of benefits",
        example=323.40,
    )
