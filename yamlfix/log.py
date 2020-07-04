"""
Utility module for configuring logging
"""

from logging import (
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
    getLogger,
    StreamHandler,
    Logger,
    Handler,
)
from sys import stdout
from typing import NewType

LogLevel = NewType("LogLevel", int)
LOGGER = getLogger(__name__)
DEBUG_LVL = LogLevel(DEBUG)
INFO_LVL = LogLevel(INFO)
WARNING_LVL = LogLevel(WARNING)
ERROR_LVL = LogLevel(ERROR)
CRITICAL_LVL = LogLevel(CRITICAL)


def configure_logger(
    logger: Logger, level: LogLevel = INFO_LVL, handler: Handler = None
):
    """
    Configures logger to push on standard output.

    :param logger: Logging channel
    :param level: Logging level (10: INFO to 50: CRITICAL)
    :param handler: Logging handler (StreamHandler sending to stdout by default)
    """
    logger.setLevel(level)
    for hdl in logger.handlers:
        logger.removeHandler(hdl)

    if handler is None:
        handler = StreamHandler(stdout)

    logger.addHandler(handler)
