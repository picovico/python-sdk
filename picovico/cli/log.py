import os
import logging
import logging.handlers as log_handlers
from picovico.cli import file_utils


def get_logger(profile_name):
    profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
    log_file = file_utils.get_log_file(profile_name)
    handler = log_handlers.RotatingFileHandler(log_file, backupCount=3)
    #logging.basicConfig(filename=log_file, level=logging.INFO)
    logger = logging.getLogger('pv-cli-{}'.format(profile_name))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
    
def log_actions(profile_name, action, result, **kwargs):
    logger = get_logger(profile_name)
    logger.info('Your Action: {}'.format(action))
    if kwargs:
        logger.info('Action called with: {}'.format(str(kwargs)))
    if result:
        logger.info('Your Result: {}'.format(result))

def flush_log(profile_name):
    profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
    logging.shutdown()
    log_file = file_utils.get_log_file(profile_name)
    if os.path.isfile(log_file):
        os.remove(log_file)
