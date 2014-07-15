"""
Helper functions for configuring loggers.
"""

import logging

from .settings import app_config

def configure_sqlalchemy_logger(format_string, level):
    logger = logging.getLogger('sqlalchemy.engine')
    logger.setLevel(level)
    logger.addHandler(get_stderr_handler(format_string, level))

def get_stderr_handler(format_string, level):
    "Returns a standard error handler with provided format and level"
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(*format_string))
    return handler

def get_app_stderr_handler():
    "Returns a configured stderr_handler"
    return get_stderr_handler(app_config.STDERR_LOG_FORMAT, app_config.APP_LOG_LEVEL)

def get_stderr_logger():
    "Returns a Logger object with a configured stderr_handler"
    logger = logging.getLogger()
    logger.handlers = []
    logger.setLevel(app_config.APP_LOG_LEVEL)
    logger.addHandler(get_app_stderr_handler())
    return logger
