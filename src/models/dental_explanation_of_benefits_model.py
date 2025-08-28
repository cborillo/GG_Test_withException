from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from src.models.validators.validate_patient_first_name import (
    validate_patient_first_name,
)


class Procedure(BaseModel):
    date_of_service: Optional[date] = Field(
        default=None,
        description="Date of service",
    )
    procedure_code: Optional[str] = Field(
        default=None,
        description="The code associated with the procedure or service",
        example="27215",
    )
    tooth_code: Optional[str] = Field(
        default=None,
        description="The international tooth number or code associated with the procedure",
        example="35",
    )
    tooth_surface: Optional[str] = Field(
        default=None,
        description="The surfaces of the tooth that are involved in the procedure",
        example="MOD",
    )
    dentist_fee: Optional[float] = Field(
        default=None,
        description="The dentist fee for the procedure or service",
        example=400.00,
    )
    lab_fee: Optional[float] = Field(
        default=None,
        description="The fee charged by the laboratory for the service",
        example=12.30,
    )
    total_charges: Optional[float] = Field(
        default=None,
        description="The total expense for the service",
        example=412.30,
    )
    cob_amount: Optional[float] = Field(
        default=None,
        description="Amount of the service that is covered by the coordination of benefits",
        example=120.30,
    )


class DentalExplanationOfBenefits(BaseModel):
    service_lines: List[Procedure] = []
    patient_first_name: Optional[str] = Field(
        default=None,
        description="Patient's first name",
        example="John",
    )
    total_cob_amount: Optional[float] = Field(
        default=0.00,
        description="Total amount of the claim that is covered by the coordination of benefits",
        example=323.40,
    )

    @field_validator("patient_first_name")
    @classmethod
    def validate_patient_first_name(cls, v):
        return validate_patient_first_name(v)
