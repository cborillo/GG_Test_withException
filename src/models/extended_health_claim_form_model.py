from typing import Optional

from pydantic import BaseModel, Field


class PlanMemberInformation(BaseModel):
    contract_number: Optional[str] = Field(
        default=None,
        description="The contract number of the member, it also called plan number or group number or policy number",
        example="123456",
    )
    member_certificate_number: Optional[str] = Field(
        default=None,
        description="The certificate number of the member",
        example="123456",
    )
    member_last_name: Optional[str] = Field(
        default=None,
        description="The last name of the plan member",
        example="Smith",
    )
    HCSA: bool = Field(
        default=False,
        description="Whether or not the plan member/subscriber wants to reimburse claim partially with their Health Care Spending Account (HCSA), it usually indicated by checking Yes or No checkbox at HCSA section",
        example=True,
    )
    HCSA_only: Optional[bool] = Field(
        default=False,
        description="Whether or not the plan member/subscriber wants to reimburse claim only with their Health Care Spending Account (HCSA), it usually indicated by checking Yes or No checkbox at HCSA Only section",
        example=False,
    )
    COB: bool = Field(
        default=False,
        description="If Coordination of benefits (COB) applies to this claim. It is usually indicated by checking Yes or No checkbox of the question with the text 'Are you, your spouse or dependents covered under any other plan...' or equivalent words.",
        example=True,
    )

class SpouseInformation(BaseModel):
    spouse_plan_member_certificate_number: Optional[str] = Field(
        default=None,
        description="The certificate number of the spouse",
        example="85743099",
    )
    spouse_plan_contract_number: Optional[str] = Field(
        default=None,
        description="The contract number of the spouse",
        example="123456",
    )
    spouse_insurance_company: Optional[str] = Field(
        default=None,
        description="The insurance company of the spouse",
        example="Sun Life Financial",
    )


class ExtendedHealthClaimFormPageOne(BaseModel):
    plan_member_information: PlanMemberInformation
    spouse_information: Optional[SpouseInformation] = None


