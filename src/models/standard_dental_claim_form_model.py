from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from src.models.validators.phone_number import validate_phone_number
from src.models.validators.postal_code import validate_postal_code
from src.models.validators.validate_patient_first_name import (
    validate_patient_first_name,
)


class DentalClaimInfo(BaseModel):
    group_number: Optional[str] = Field(
        default=None,
        description="The group policy/plan number of the employee, plan member or subscriber. ",
        example="0102003",
    )
    certificate_number: Optional[str] = Field(
        default=None,
        description="The certificate/ID number of the employee, plan member or subscriber.",
        example="1234567",
    )
    member_last_name: Optional[str] = Field(
        default=None,
        description="The last name of the employee, plan member or subscriber.",
        example="Smith",
    )
    estimate: Optional[bool] = Field(
        default=False,
        description="Whether or not the claim is for estimation only",
        example=False,
    )
    CDA_number: Optional[str] = Field(
        default=None,
        description="The Canadian Dental Association number of the dentist.",
        example="341467700",
    )
    provider_first_name: Optional[str] = Field(
        default=None,
        description="The first name of the dentist.",
        example="John",
    )
    provider_last_name: Optional[str] = Field(
        default=None,
        description="The last name of the dentist.",
        example="Wick",
    )
    provider_postal_code: Optional[str] = Field(
        default=None,
        description="The postal code of the dentist address.",
        example="N3T 3J6",
    )
    provider_phone_number: Optional[str] = Field(
        default=None,
        description="The phone number of the dentist.",
        example="519-123-4567",
    )
    patient_first_name: Optional[str] = Field(
        default=None,
        description="The first name of the patient.",
        example="Jack",
    )
    assigned: Optional[bool] = Field(
        default=False,
        description="Whether or not the plan member/subscriber has assigned the benefits to the dentist with a valid signature.",
        example=False,
    )
    office_verification: Optional[bool] = Field(
        default=False,
        description="Whether or not the office is verified.",
        example=False,
    )
    dental_accident: Optional[bool] = Field(
        default=False,
        description="There are checkboxes asking if the claim is due to a dental accident, set to True only if 'yes' checked. The information is usually in the patient information section of the form.",
        example=False,
    )
    signature: Optional[bool] = Field(
        default=False,
        description="Whether or not a valid signature from the plan member/subscriber is present.",
        example=False,
    )
    HCSA: Optional[bool] = Field(
        default=False,
        description="Whether or not the plan member/subscriber wants to reimburse claim with their Health Care Spending Account (HCSA).",
        example=False,
    )
    HCSA_only: Optional[bool] = Field(
        default=False,
        description="Whether or not the plan member/subscriber wants to reimburse claim only with their Health Care Spending Account (HCSA).",
        example=False,
    )
    initial_placement: Optional[bool] = Field(
        default=False,
        description="There is an ask if the claim is for the initial placement, set to True if checked. The information is usually in the patient information section of the form.",
        example=True,
    )
    initial_placement_date: Optional[date] = Field(
        default=None,
        description="The date of the initial placement. Only look for it when initial_placement is True.",
    )
    COB: Optional[bool] = Field(
        default=False,
        description="There is an ask if any dental benefits or service provided are covered by another plan, set to True if checked. The information is usually in the patient information section of the form.",
        example=False,
    )
    total_submitted_charges: Optional[float] = Field(
        default=None,
        description="The total fee submitted by the dentist for the claim.",
        example=456.70,
    )

    @field_validator("provider_postal_code")
    def validate_provider_postal_code(cls, v):
        return validate_postal_code(v)

    @field_validator("provider_phone_number")
    def validate_provider_phone_number(cls, v):
        return validate_phone_number(v)
    
    @field_validator("patient_first_name")    
    @classmethod
    def validate_patient_first_name(cls, v):
        return validate_patient_first_name(v)


class ServiceLines(BaseModel):
    service_date: Optional[date] = Field(
        default=None,
        description="Date of service often found next to the procedure code",
    )
    procedure_code: Optional[str] = Field(
        default=None,
        description="The code associated with the procedure",
        example="27215",
    )
    tooth_code: Optional[str] = Field(
        default=None,
        description="The international tooth number or code associated with the service",
        example="35",
    )
    tooth_surface: Optional[str] = Field(
        default=None,
        description="The surfaces of the tooth that are involved in the service",
        example="MOD",
    )
    dentist_fee: Optional[float] = Field(
        default=None,
        description="The dentist's fee for the service",
        example=200.00,
    )
    lab_fee: Optional[float] = Field(
        default=None,
        description="The fee charged by the laboratory for the service",
        example=12.30,
    )
    total_charges: Optional[float] = Field(
        default=None,
        description="The total charges for the service",
        example=300.00,
    )


class SpouseInfo(BaseModel):
    spouse_policy_number: Optional[str] = Field(
        description="The policy number, group number or plan number in the patient information section",
        example="01023005",
    )
    spouse_certificate_number: Optional[str] = Field(
        description="The certificate number of the spouse in the patient information section",
        example="123456",
    )
    spouse_insurance_company: Optional[str] = Field(
        description="The insurance company name in the patient information section",
        example="Sun Life Financial",
    )


class PlanMemberInfo(BaseModel):
    group_policy_plan_number: Optional[str] = Field(
        description="The group policy plan number of the employee",
        example="01023006",
    )
    cert_sin_or_id_number: Optional[str] = Field(
        description="The certificate, social insurance, or identification number of the employee",
        example="123456",
    )


class PatientInfo(BaseModel):
    first_name: Optional[str] = Field(
        description="The first name of the patient found at the beginning of the form",
    )
    is_accident: Optional[bool] = Field(
        False,
        description="Whether or not treatment required is the result of an accident",
    )
    signature: Optional[bool] = Field(False, description="Whether or not ")


class StandardDentalClaimForm(BaseModel):
    claim_info: DentalClaimInfo
    spouse_info: Optional[SpouseInfo] = None
    service_lines: List[ServiceLines] = []
