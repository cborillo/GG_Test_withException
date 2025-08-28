from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from src.models.validators.french_characters import convert_french_characters
from src.models.validators.phone_number import validate_phone_number
from src.models.validators.postal_code import validate_postal_code


class ProviderInfo(BaseModel):
    provider_registration_number: Optional[str] = Field(
        default=None,
        description="Provider's registration number, a unique string composed of numbers and letters.",
        example="007360",
    )
    provider_first_name: Optional[str] = Field(
        default=None,
        description="Provider's first name",
        example="Jodi",
    )
    provider_last_name: Optional[str] = Field(
        default=None,
        description="Provider's last name",
        example="Brown",
    )
    provider_province: Optional[str] = Field(
        default=None,
        description="Province of service provider's address, return the full standard province name",
        example="British Columbia",
    )
    provider_postal_code: Optional[str] = Field(
        default=None,
        description="Postal Code of service provider's address",
        example="N3T 3J6",
    )
    provider_phone_number: Optional[str] = Field(
        default=None,
        description="Provider's phone number",
        example="844 8573188",
    )
    under_supervision: bool = Field(
        default=False,
        description="If the provider is under supervision, looking for the keyword 'supervision'",
        example=False,
    )

    @field_validator("provider_postal_code")
    def validate_provider_postal_code(cls, v):
        return validate_postal_code(v)

    @field_validator("provider_province")
    def validate_provider_province(cls, v):
        return convert_french_characters(v)

    @field_validator("provider_phone_number")
    def validate_provider_phone_number(cls, v):
        return validate_phone_number(v)


class ServiceInfo(BaseModel):
    patient_first_name: Optional[str] = Field(
        default=None, description="Patient's first name", example="Mike"
    )
    date_of_service: Optional[date] = Field(
        default=None,
        description="Date of service often found next to the procedure code",
    )
    service_code: Optional[str] = Field(
        default=None,
        description="The service name",
        example="Acupuncture",
    )
    sub_service_code: Optional[str] = Field(
        default="Subsequent",
        description="The sub service category",
        example="Subsequent",
    )
    minutes: Optional[int] = Field(
        default=None,
        description="the length of service, shown as a minute. If the receipt shows the length in hour, convert to correct minutes, if the receipt doesn't tell length, return None",
        example=60,
    )
    no_of_occur: int = Field(1, description="always return 1", example=1)
    phys_reference: bool = Field(
        default=False,
        description="if the service is referred by a physician, return True, otherwise return False.",
        example=False,
    )
    total_charge: Optional[float] = Field(
        default=None,
        description="total charge including the tax of this service",
        example=203.4,
    )


class HealthReceipt(BaseModel):
    provider_info: ProviderInfo
    health_expenses: List[ServiceInfo] = []
