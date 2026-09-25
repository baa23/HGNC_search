"""
This file contains the function (and module/data structure) needed to set-up logger

"""
import logging.config
from HGNC_search.settings import LOGGING_CONFIG

def setup_logging():
    """
    This function will apply the logging configuration to setup logging for the application
    """

    logging.config.dictConfig(LOGGING_CONFIG)