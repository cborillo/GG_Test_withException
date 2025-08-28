from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ClaimInfo(BaseModel):
    internal_reference_number: Optional[str] = Field(
        default=None,
        description="Internal reference # of the claim",
        example="H0050012345678",
    )
    provider_not_listed_claim_confirmation_number: Optional[str] = Field(
        default=None,
        description="Provider not listed claim confirmation # of the claim",
        example="12345678",
    )
    date_submitted: Optional[date] = Field(
        default=None,
        description="Date submitted of the claim",
    )
    covered_under_any_other_plan: Optional[bool] = Field(
        default=False,
        description="Are you, your spouse, or dependants covered under any other plan for these expenses?",
        example=True,
    )
    submit_unpaid_portion: Optional[bool] = Field(
        default=False,
        description="Do you want to submit an unpaid portion of the claim that has already been submitted and processed under another plan?",
        example=True,
    )
    HCSA: Optional[bool] = Field(
        default=False,
        description="Use your Health Care Spending Account to reimburse any unpaid portion of this claim",
        example=True,
    )
    HCSA_only: Optional[bool] = Field(
        default=False,
        description="Submit your eligible expenses directly to your Health Care Spending Account",
        example=False,
    )
    physician_referral: Optional[bool] = Field(
        default=False,
        description="Did you receive a physician's referral for this expense?",
        example=False,
    )
    service_date: Optional[date] = Field(
        default=None,
        description="Service date of the claim",
    )
    total_charges: Optional[float] = Field(
        default=None,
        description="Total charges in the form",
        example=123.45,
    )
    amount_paid_by_another_plan: Optional[float] = Field(
        default=None,
        description="Amount paid by another plan in the form",
        example=123.45,
    )


class PlanInfo(BaseModel):
    plan_sponsor: Optional[str] = Field(
        default=None,
        description="Plan sponsor of the claim",
        example="Testing Inc.",
    )
    plan_member: Optional[str] = Field(
        default=None,
        description="Plan member of the claim",
        example="John Doe",
    )
    plan_contract_number: Optional[str] = Field(
        default=None,
        description="Plan contract # of the claim",
        example="123456",
    )
    member_certificate_number: Optional[str] = Field(
        default=None,
        description="Member certificate # of the claim",
        example="1234567",
    )


class PatientInfo(BaseModel):
    patient_name: Optional[str] = Field(
        default=None,
        description="Patient first name in the form",
        example="John",
    )
    date_of_birth: Optional[date] = Field(
        default=None,
        description="Date of birth of the patient",
    )
    relationship: Optional[str] = Field(
        default=None,
        description="Patient relationship to the plan member",
        example="Member",
    )
    name_of_accredited_school: Optional[str] = Field(
        default=None,
        description="Name of accredited school",
        example="Main St. High School",
    )


class SpouseInfo(BaseModel):
    spouse_insurance_company: Optional[str] = Field(
        default=None,
        description="Name of spouse's insurance company",
        example="Manulife",
    )
    spouse_plan_contract_number: Optional[str] = Field(
        default=None,
        description="Spouse's plan contract #",
        example="123456",
    )
    spouse_certificate_number: Optional[str] = Field(
        default=None,
        description="Spouse's certificate #",
        example="12345678",
    )
    spouse_date_of_birth: Optional[date] = Field(
        default=None,
        description="Spouse's date of birth",
    )


class ClaimConfirmationForm(BaseModel):
    claim_info: ClaimInfo
    plan_info: PlanInfo
    patient_info: PatientInfo
    spouse_info: Optional[SpouseInfo] = None
