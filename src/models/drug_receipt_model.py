from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from src.models.validators.drug_quantity_type import validate_drug_quantity_type
from src.models.validators.postal_code import validate_postal_code


class PharmacyInfo(BaseModel):
    pharmacy_name: Optional[str] = Field(
        default=None,
        description="The name of the pharmacy, exclude the pharmacy store number",
        example="Shopper's Drug Mart",
    )
    pharmacy_store_number: Optional[str] = Field(
        default=None,
        description="The store number of the pharmacy, usually start with #",
        example="0875",
    )
    pharmacy_address: Optional[str] = Field(
        default=None,
        description="The pharmacy's address",
        example="123 Main Street",
    )
    pharmacy_city: Optional[str] = Field(
        default=None,
        description="The pharmacy's city",
        example="Toronto",
    )
    pharmacy_province: Optional[str] = Field(
        default=None,
        description="The pharmacy's province",
        example="ON",
    )
    pharmacy_postal_code: Optional[str] = Field(
        default=None,
        description="Postal Code of pharmacy's address",
        example="N3T 3J6",
    )
    pharmacy_phone_number: Optional[str] = Field(
        default=None,
        description="Pharmacy's phone number in XXXXXXXXXX format",
        example="8448573188",
    )

    @field_validator("pharmacy_postal_code")
    @classmethod
    def validate_pharmacy_postal_code(cls, v):
        return validate_postal_code(v)


class ServiceInfo(BaseModel):
    patient_first_name: Optional[str] = Field(
        default=None, description="Patient's first name", example="Mike"
    )
    patient_last_name: Optional[str] = Field(
        default=None, description="Patient's last name", example="Johnson"
    )
    date_of_service: Optional[date] = Field(
        default=None,
        description="Date of service",
    )
    days_supply: Optional[int] = Field(
        default=None,
        description="Number of days the prescription is valid for",
        example=30,
    )
    drug_identification_number: Optional[str] = Field(
        default=None,
        description="Eight digit drug identification number assigned to a drug product",
        example="00586676",
    )
    refills_remaining: Optional[int] = Field(
        default=None,
        description="Number of refills remaining on the prescription",
        example=1,
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
    total_charge: Optional[float] = Field(
        default=None,
        description="Total charge including the tax of this prescription",
        example=203.4,
    )

    @field_validator("drug_quantity_type")
    @classmethod
    def validate_quantity_type(cls, v):
        return validate_drug_quantity_type(v)

    # TODO: Add validation for province_paid (depends on SME)


class DrugReceipt(BaseModel):
    pharmacy_info: PharmacyInfo
    services: List[ServiceInfo] = []
