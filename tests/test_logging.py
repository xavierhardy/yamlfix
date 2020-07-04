import unittest
from io import StringIO
from logging import StreamHandler, getLogger

from yamlfix.log import configure_logger, DEBUG_LVL, WARNING_LVL
from tests.utils import (
    LoggingTester,
    DEBUG_MSG,
    INFO_MSG,
    WARNING_MSG,
    ERROR_MSG,
    CRITICAL_MSG,
)


class LoggingTest(LoggingTester):
    def test_default_logging(self):
        with StringIO() as stream:
            logger = getLogger("LoggingTest.test_default_logging")
            configure_logger(logger, handler=StreamHandler(stream))
            self.assert_empty_log(stream)

            logger.debug(DEBUG_MSG)
            self.assert_empty_log(stream)

            logger.info(INFO_MSG)
            self.assert_log(INFO_MSG, stream)

            logger.warning(WARNING_MSG)
            self.assert_log(WARNING_MSG, stream)

            logger.error(ERROR_MSG)
            self.assert_log(ERROR_MSG, stream)

            logger.critical(CRITICAL_MSG)
            self.assert_log(CRITICAL_MSG, stream)

    def test_debug_logging(self):
        with StringIO() as stream:
            logger = getLogger("LoggingTest.test_debug_logging")
            configure_logger(logger, level=DEBUG_LVL, handler=StreamHandler(stream))
            self.assert_empty_log(stream)

            logger.debug(DEBUG_MSG)
            self.assert_log(DEBUG_MSG, stream)

            logger.info(INFO_MSG)
            self.assert_log(INFO_MSG, stream)

            logger.warning(WARNING_MSG)
            self.assert_log(WARNING_MSG, stream)

            logger.error(ERROR_MSG)
            self.assert_log(ERROR_MSG, stream)

            logger.critical(CRITICAL_MSG)
            self.assert_log(CRITICAL_MSG, stream)

    def test_warning_logging(self):
        with StringIO() as stream:
            logger = getLogger("LoggingTest.test_warning_logging")
            configure_logger(logger, level=WARNING_LVL, handler=StreamHandler(stream))
            self.assert_empty_log(stream)

            logger.debug(DEBUG_MSG)
            self.assert_empty_log(stream)

            logger.info(INFO_MSG)
            self.assert_empty_log(stream)

            logger.warning(WARNING_MSG)
            self.assert_log(WARNING_MSG, stream)

            logger.error(ERROR_MSG)
            self.assert_log(ERROR_MSG, stream)

            logger.critical(CRITICAL_MSG)
            self.assert_log(CRITICAL_MSG, stream)


if __name__ == "__main__":
    unittest.main()
