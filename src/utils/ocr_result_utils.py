def build_extracted_data(response_status_code, case_id, document_id, message):
    if response_status_code == 200:
        return_value = {
            'case_id': case_id,
            'document_id': document_id,
            'ocr_result': {
                'status': 'success',
                'analyzeResult': message
            }
        }
    else: 
        return_value = {
            'case_id': case_id,
            'document_id': document_id,
            'ocr_result': {
                'status': 'failed',
                'message': message
            }
        }
    
    return return_value