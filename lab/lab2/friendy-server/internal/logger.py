import logging
import os
from uvicorn.logging import DefaultFormatter
log_level = None

def create_logger(logger_name):
    global log_level
    # Configure the logger with custom format
    formatter = DefaultFormatter(
        fmt="%(levelprefix)s %(asctime)s  [%(name)s] %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create a logger with the specified name
    logger = logging.getLogger(logger_name)
    log_level = os.getenv("log", default="info")
    if log_level == "warning":
        logger.setLevel(logging.WARNING)
    if log_level == "debug":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Create a StreamHandler and set the formatter
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger

def get_log_level():
    return log_level