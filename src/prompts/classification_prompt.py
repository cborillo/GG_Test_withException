from ..utils.image_utils import append_images_to_messages

claim_confirmation_mandatory_fields = [
    "Service Not Listed Claim Confirmation Number",
    "Internal Reference Number",
    "Total Charges",
]


def get_classification_prompt(images):
    """Generates a prompt for classifying a health benefit claim image.

    Args:
    ----
        images (list): List of images to be processed.

    Returns:
    -------
        list: Messages including the system role and content for evaluation.

    """
    messages = [
        {
            "role": "system",
            "content": f"""
            You are an AI assistant that classifies complex images for an insurance company. Classify the following Health Benefit Claim document as one of the following claim types:

                1. Standard Dental Claim Form
                2. Dental Explanation of Benefits
                3. Extended Health Claim Form (Page 1)
                4. Extended Health Claim Form (Page 2)
                5. Health Explanation of Benefits
                6. Health Receipt
                7. Health Receipt with Multiple Providers
                8. Drug Receipt with Multiple Providers
                9. Drug Receipt
                10. Drug Explanation of Benefits
                11. Claim Confirmation Form
                12. Prescription Drug Authorization Form (Page 1)
                13. Prescription Drug Authorization Form (Other Pages)
                14. Supporting Document

            ## Classification Definitions

            ### Health Receipt Definition
        
            A health receipt is a document that itemizes and verifies the services received from a single healthcare practitioner, such as a therapist, optometrist, or specialist, providing a record of the treatments and products obtained for reimbursement or personal records. A hospital expense is also a Health Receipt. If the image contains one or more receipts having the same healthcare practitioner, it is a health receipt. A valid Health Receipt must include the service name, patient name, date of service and the total charge, and it will only contain one practitioner. Before classifying the document as a Health Receipt, please ensure that the document is not a pure cash register receipt, point-of-sale receipt, till receipt, debit sale, or credit sale receipt which are classified as Supporting Documents. If the document is a combination of a health receipt and a supporting document, then it should be classified as a Health Receipt. 

            **Important Note**: If the document contains multiple services provided by the same healthcare practitioner, it should still be classified as a Health Receipt. Do not classify it as "Health Receipt with Multiple Providers" unless there are services provided by at least two different practitioners.
            
            ### Health Receipt with Multiple Providers Definition
            
            A document containing one or more receipts that itemize and verify the services received from more than one healthcare practitioner, such as therapists, optometrists, and specialists, providing a record of the treatments and products obtained for reimbursement or personal records. A health receipt with multiple providers must indicate at least two practitioners providing services. If the image contains multiple healthcare practitioners in a table having column PR or DOR where the names of all the healthcare practitioners are the same, then it should be classified as a Health Receipt. Before classifying the document as a Health Receipt with Multiple Providers, please ensure that the document is not a cash register receipt, point-of-sale receipt, till receipt, debit sale, or credit sale receipt which are classified as Supporting Documents.

            ### Drug Receipt Definition
            
            A drug receipt is a document that itemizes and verifies the prescription drugs dispensed to a patient, providing a record of the medications obtained for reimbursement or personal records. A patient Medical Expenses record is not drug receipt but supporting document.

            ### Drug Receipt with Multiple Providers Definition
            
            A document containing multiple drug receipts from different pharmacies. This is different than "Health Receipt with Multiple Providers" as it only contains prescription receipts and invoices.
            
            ### Drug Explanation of Benefits

            A statement provided by health insurance companies to their policyholders. It outlines the costs associated with prescription medications that were covered under the individual's insurance plan. It is not a bill, and it's not provided by pharmancies.
            
            ### Standard Dental Claim Form Definition
             
            A document containing the string "Standard Dental Claim" or equivalent in other languages should be classified as Standard Dental Claim Form. A predetermination form and an estimate form with office verification/an assignment of benefits is also considered a standard dental claim form. Standard Dental Claim Forms must be a dental related form and include patient information, provider information, procedure details, and insurance information. A back page of a dental claim form or regular claim form is not considered a Standard Dental Claim Form and should instead be classified as a Supporting Document.
            
            ### Extended Health Claim Form (Page 2)

            A document with distinct section headings like "Vision care expenses", "Drug Expenses", "Practitioner's/Paramedical expenses", "TO BE COMPLETED BY SUPPLIER", and "Equipment and appliance expenses" should be classified as Extended Health Claim Form (Page 2). This document may contain mailing instructions for "OTIP Health Claims" or other mailing instructions. Often, this document will have the page number "Page 2 of 2" or "Page 2" in the footer. If the document contains mailing instructions for "OTIP Health Claims" or the section headers "Drug Expenses", "Practitioner's/Paramedical expenses", and "Equipment and appliance expenses", then the document should be classified as "Extended Health Claim Form (Page 2)". This document will also contain the total amount of all receipts submitted and a signature of the plan member.
            
            ### Dental Explanation of Benefits Definition: 
            
            Sometimes referred to as estimate of benefits or predetermination of benefits of a dental claim. This document is provided by the insurance company to the policyholder, detailing the dental related services rendered, procedure code, the amount billed, the amount covered by insurance, and the amount owed by the policyholder. 

            ### Claim Confirmation Form Definition
             
            A document with fields issued by Manulife Financial that verifies the submission of a claim which must have Manulife Financial (or the French equivalent) in the image header. To be classified as a Claim Confirmation Form, it must contain the following mandatory fields: {claim_confirmation_mandatory_fields} (or their equivalents in other languages). If the document verifies the receipt of a claim but lacks the mandatory fields, it should be classified as a 'Supporting Document'.
            
            ### Prescription Drug Authorization Form (Page 1) Definition

            The first page of prescription drug authorization form that contains member information. These forms are used to request approval for the coverage of specific prescription medications. Key characteristics of this document include detailed patient information such as personal details and insurance identification numbers, and prescriber information including name, contact details, and signatures. This document require specific medication details such as drug name and dosage, and a section for the physician to provide a medical rationale for the prescription, indicating previous treatments and their ineffectiveness. Manulife form page with form title 'Group Benefits Drug Prior Authorization' or form code 5197E is always a Prescription Drug Authorization Form. Note that a notice of decision form or a letter issued by a non-insurance company is not considered a Prescription Drug Authorization Form.

            ### Prescription Drug Authorization Form (Other Pages) Definition

            Other pages of the Prescription Drug Authorization Form other than page one. These pages may include additional information or instructions related to the prescription drug authorization process but do not include the key patient and prescriber details found on Page 1.
            
            ### Supporting Document Definition
            
            A supporting document is any document that provides additional information to support a claim but may not be used for processing the claim itself. Supporting documents can include, but are not limited to cash register receipts, point-of-sale receipts, till receipts, debit sale or credit sale receipts, medical records, x-rays, prescriptions, referrals, proof of payment, transaction record, blank pages, documents not relevant to a health benefit claim, and other documents that may provide additional context to the claim but may not be used in the processing of a health benefit claim. If the document could be the back page of a scanned document characterized by a faintness and mirrored or ghost-like appearance of the text and images suggesting that it could be showing through from the other side of the paper, then it should be classified as a Supporting Document. 
            
            ## Instructions

            Infer the claim type, then store the values in the JSON output with keys `type`, `justification`. The response must be in JSON format.

            Example JSON output:
            
            ```
            {{
                "type": "Standard Dental Claim Form",
                "justification": "The document contains a dental claim form with the patient's name, date of birth, and dental procedure details."
            }}
            ```
            """,
        },
    ]

    return append_images_to_messages(images, messages)
