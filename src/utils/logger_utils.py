import datetime
import json
import logging
import os

from src.constants import Constants


def log_message(level, message, correlation_id="", case_id="", document_id=""):
    datenow = datetime.datetime.now().astimezone().isoformat()

    if level in Constants.LOG_LEVELS:
        log = getattr(logging, level)
        severity_number = Constants.LOG_LEVELS.index(level)
    else:
        log = getattr(logging, 'info')
        severity_number = Constants.LOG_LEVELS.index('info')

    log_message = {
        'Timestamp': datenow,
        'Resource': {
            'mfc_ver': 1,
            'ci_num': os.getenv('CI'),
            'top_level_ci_num': os.getenv('CI'),
            'owning_segment': 'can',
            'pii_flag': 'false',
            'sec_flag': 'false',
            'app_name': 'idp-docext-svc',
            'app_comp': 'api'
        },
        'Body': {
            'timestamp': datenow,
            'severityNumber': severity_number,
            'level': level,
            'correlation_id': correlation_id,
            'case_id': case_id,
            'document_id': document_id,
            'message': json.dumps(message)
        }
    }

    log(log_message)
