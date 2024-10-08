"""
Logging utilities for application-wide use.

This module provides a custom logging filter and an initialization function for
setting up loggers with specific configurations.

Classes:
    AppFilter: A custom logging filter that adds attributes and filters log messages.

Functions:
    init_log(logger_name="root"): Initializes and configures a logger instance.
"""

import logging


class AppFilter(logging.Filter):
    """
    A custom logging filter that sets additional attributes on the log record and
    filters log messages based on specific criteria.

    This filter can modify log records by adding custom attributes such as `app_name`,
    which can later be used in log formatting. It also filters out log messages that
    do not meet specific conditions (e.g., those that do not start with a certain
    string).

    Methods:
        filter(record: logging.LogRecord) -> bool:
            Sets custom attributes on the log record and filters messages.
            Returns True if the log message passes the filter, otherwise False.
    """

    def filter(self, record):
        """
        Modifies the log record by adding custom attributes and filters log messages.
        This method sets custom values, such as `app_name`, on the log record, which
        can be used in the log formatting. It filters messages based on their content,
        allowing only those that start with a specified string (empty string .

        Args:
            record (logging.LogRecord): The log record to be filtered.

        Returns:
            bool: True if the log message passes the filter, False otherwise.
        """

        return record.getMessage().startswith("")


def init_log(logger_name="root"):
    """
    Initializes a logger with the specified name and adds a custom filter to it.

    This function configures the logging system with the DEBUG level and attaches
    the `AppFilter` to the logger for filtering log messages. The logger will use
    the default "root" logger if no name is provided.

    Args:
        logger_name (str): The name of the logger to initialize (default is "root").

    Returns:
        logging.Logger: The initialized logger with the custom filter.
    """
    logging.basicConfig(
        level=logging.DEBUG,
    )
    logger = logging.getLogger(logger_name)
    logger.addFilter(AppFilter())
    return logger
