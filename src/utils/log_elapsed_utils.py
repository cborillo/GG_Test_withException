import time

from src.utils.logger_utils import log_message

def log_elapsed(start_time, message, correlation_id):
    end_time = time.time()
    elapsed_time = end_time - start_time

    msg = f'{message}. Elapsed time: {elapsed_time:.4f} seconds'
    
    log_message(
        'info', msg, correlation_id)
        