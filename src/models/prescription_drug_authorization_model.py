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
        description="The certificate number of the member, also called plan member certificate number",
        example="123456",
    )
    member_last_name: Optional[str] = Field(
        default=None,
        description="The last name of the plan member",
        example="Smith",
    )

class PrescriptionDrugAuthorizationForm(BaseModel):
    plan_member_information: PlanMemberInformation
