import os
import time
import logging
import logging.handlers
import pathlib

base_dir = pathlib.Path(__file__).parent.parent
log_dir = f'{base_dir}/logs'


def init_logger():
    """
    Initialize the logger.
    :return: None
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)


def get_logger_file(script_name):
    """
    Load the logger.
    :param script_name:
    :return: file logger
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    today = time.strftime("%Y-%m-%d")
    print(base_dir)
    return f"{log_dir}/{script_name}_{today}.log"


def setup_logger(log_level, script_name):
    """
    Setup the logger.
    Parameters:
        log_level (str): The log level to use
        :param log_level:
        :param script_name:
    Returns:
        A logger object for logging messages.
    """
    log_file = get_logger_file(script_name)
    logger = logging.getLogger()
    log_level = log_level.upper()
    if log_level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif log_level == 'INFO':
        logger.setLevel(logging.INFO)
    elif log_level == 'CRITICAL':
        logger.setLevel(logging.CRITICAL)
    else:
        logger.critical(
            f"Invalid log level '{log_level}', defaulting to 'INFO'")
        logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s: %(message)s', datefmt='%I:%M %p')
    if not logger.handlers:
        handler = logging.handlers.TimedRotatingFileHandler(
            log_file, when='midnight', interval=1, backupCount=3)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        formatter = logging.Formatter()
        console_handler = logging.StreamHandler()
        if log_level == 'debug':
            console_handler.setLevel(logging.DEBUG)
        elif log_level == 'info':
            console_handler.setLevel(logging.INFO)
        elif log_level == 'critical':
            console_handler.setLevel(logging.CRITICAL)
        logger.addHandler(console_handler)
    log_files = [f for f in os.listdir(log_dir) if os.path.isfile(
        os.path.join(log_dir, f)) and f.startswith(f"{script_name}_")]
    log_files.sort(key=lambda x: os.path.getmtime(
        os.path.join(log_dir, x)), reverse=True)
    for file in log_files[3:]:
        os.remove(os.path.join(log_dir, file))
    return logger