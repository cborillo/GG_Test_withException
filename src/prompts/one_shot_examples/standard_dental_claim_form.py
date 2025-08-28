standard_dental_claim_form_one_ocr = """
Canadian Dental Association
Canadian Life and Health Insurance Association Inc.
STANDARD DENTAL CLAIM FORM
PART 1 DENTIST
OFFICE NO.
7026
UNIQUE NO. 222417231
SPEC.
PATIENT'S OFFICE ACCOUNT NO:
127154
I hereby assign my benefits payable from this claim to the named dentist and authorize payment directly to him/her
P
A
T
1
E
N
T
BROOME, Mr. Lucas
368 Tooth Ave
Collierview
ON L4N8R3
D
Dr. John Doe
E
N
T
555 Paris Dr W #201
Barrie, ON
L4N8G5
S
T
Fax (000) 000-0000
PHONE NO. (705) 711-1122
SIGNATURE OF SUBSCRIBER
For dentist's use only - for additional information, diagnosis, procedures,
or special consideration.
PLEASE SEE WHAT FIRST
CARRIER IS PAYING
Duplicate Form
Date of Service
Pro-
Day
Mo.
Yr
cedure
Code
33121
23314 15
18/JUN/24
18/JUN/24
Intl.
Tooth
Code
15
Tooth
Sur-
faces
Dentist's ATTACHED
Laboratory Charge
Fee
883.00
396.00
DOBL
I understand that the fees listed in this claim may not be covered by or may exceed my plan benefits. I understand that I am financially responsible to my dentist for the entire treatment. I acknowledge that the total fee of $ charged to me for services rendered. 1 2 79 . 00 is accurate and has been I authorize release of the information contained in this claim form to my insuring company / plan administrator. I also authorize the communication of information related to the coverage of services described in this form to the named dentist.
SIGNATURE OF PATIENT (PARENT/GUARDIAN)
Office Verificasont
BAHRAM ESFANDIARI. D.D.S.
Total Charges
For Carrier Use
883.00
Allowed Amount
Inc
%
Patient's Share
396.00
Cheque No.
Date
Deductible
Patient Pays
Plan Pays
This is an accurate statement of services performed and the total fee due and payable, E & OE.
TOTAL FEE SUBMITTED
1279.00
Claim No.
INSTRUCTIONS FOR CLAIM SUBMISSION
Being a standard form, this cannot include specific instructions on where it should be sent, depending on who is the carrier for your plan. You can obtain details from either your plan booklet, your certificate or from your employer.
If your plan requires submission directly to the carrier, please send this form with only parts 1, 2, and 3 completed to the carrier's appropriate claims office. *If your plan requires submission directly to your employer, please direct this form to your personnel office/plan administrator who will complete part 4 and forward the form to the carrier.
PART 2 - EMPLOYEE/PLAN MEMBER/SUBSCRIBER
1. Group Policy/Plan No.
0205043
Division Section No.
2. Your Name
(Please Print)
Ms. Justina BIEMAN
Employer
Your Cert. No.
or ID. No.
4444444
Name of Insuring Agency or Plan OTIP
Your Date of Birth
25/MAR/1980
Day
Month
Year
PART 3 - PATIENT INFORMATION
1. Patient: Relationship to employee/
Plan member/Subscriber
Date of Birth
Day/Mth/Year
If child indicate
If student, indicate school
Spouse
09/MAR/1974
Student
Handicapped
3. Is any treatment required as the result of an accident?
If yes, give date and details separately.
No
×
Yes
4. If denture, crown or bridge, is this initial placement?
Give date of prior placement and reason for replacement
No
Yes
Patient ID. No.
4444444
2. Are any dental benefits or services provided under any other Group Insurance or Dental plan, W.C.B. or Gov't Plan? No
Yes
5. Is any treatment required for orthodontic purposes?
No
6. | authorize the release of any information or records requested in respect of this claim to the insurerplan administrator and certify that the information given is true, correet and complete to the best of my knowledge.
Yes
Policy No.
25320
Name of other Insuring Agency or Plan
Spouse Date of Birth
09/MAR/1974 Sun Life of Canada
SIGNATURE OF EMPLOYEE/PLAN MEMBER/SUBSCRIBER
DATE
18/JUN/24
Day Month Year
PART 4 - POLICY HOLDER/EMPLOYER (for completion only if applicable. SEE ABOVE*)
DAY
MONTH
YEAR
4. Contract holder
1. Date coverage commenced 2. Date dependent covered 3. Date terminated
DAY
DATE
MONTH
YEAR
AUTHORIZED SIGNATURE
(POSITION OR TITLE)
C 12/03 ABELSoft Corporation.
All information recorded on this form is confidential
"""

standard_dental_claim_form_extraction = {
    "dentist_info": {
        "first_name": "John",
        "last_name": "Doe",
        "unique_number": "222417231",
        "postal_code": "L4N8G5",
        "assigned": True,
        "office_verification": True,
    },
    "spouse_info": {
            "spouse_policy_number": "25320",
            "spouse_certificate_number": None,
            "spouse_insurance_company": "Sun Life of Canada",
        },
    "service_lines": [
        {
            "date_of_service": "2024-06-18",
            "procedure_code": "33121",
            "tooth_code": "15",
            "tooth_surfaces": None,
            "dentists_fee": "883.00",
            "laboratory_charge": None,
            "total_charges": "883.00",
        },
        {
            "date_of_service": "2024-06-18",
            "procedure_code": "23314",
            "tooth_code": "15",
            "tooth_surfaces": "DOBL",
            "dentists_fee": "396.00",
            "laboratory_charge": None,
            "total_charges": "396.00",
        },
    ],
    "plan_member_info": {
        "group_policy_plan_number": "0205043",
        "cert_sin_or_id_number": "4444444",
    },
    "patient_info": {"first_name": "Lucas", "is_accident": False, "signature": True},
    "total_fee_submitted": 1279.0,
}

standard_dental_claim_form_one_shot = f"""
OCR one shot example:
```json
{standard_dental_claim_form_one_ocr}
```

One shot result:
```
{standard_dental_claim_form_extraction}
```
"""
