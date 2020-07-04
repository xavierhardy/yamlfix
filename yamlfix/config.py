"""
Utility module for configuration
"""

from logging import Logger, Handler, INFO
from typing import NewType

from yamlfix.log import configure_logger, DEBUG_LVL, LogLevel

Config = NewType("Config", dict)


def configure_app(config: Config, logger: Logger, handler: Handler = None):
    """
    Configure the application.

    :param config: Parsed arguments directly from the CLI
    :param logger: Logging channel
    :param handler: Logging handler
    """
    log_level = (
        DEBUG_LVL
        if config.get("verbose")
        else LogLevel(10 * config.get("log_level", INFO // 10))
    )
    configure_logger(logger, level=log_level, handler=handler)
