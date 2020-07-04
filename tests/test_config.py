import unittest
from io import StringIO
from logging import StreamHandler, getLogger, DEBUG, WARNING

from yamlfix.config import configure_app, Config
from tests.utils import (
    LoggingTester,
    DEBUG_MSG,
    INFO_MSG,
    WARNING_MSG,
    ERROR_MSG,
    CRITICAL_MSG,
)


class ConfigTest(LoggingTester):
    def test_default_config(self):
        with StringIO() as stream:
            config = Config({})
            logger = getLogger("ConfigTest.test_default_config")
            configure_app(config, logger, handler=StreamHandler(stream))
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

    def test_non_verbose_config(self):
        with StringIO() as stream:
            config = Config({"verbose": False})
            logger = getLogger("ConfigTest.test_non_verbose_config")
            configure_app(config, logger, handler=StreamHandler(stream))
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

    def test_verbose_config(self):
        with StringIO() as stream:
            config = Config({"verbose": True})
            logger = getLogger("ConfigTest.test_verbose_config")
            configure_app(config, logger, handler=StreamHandler(stream))
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

    def test_debug_config(self):
        with StringIO() as stream:
            config = Config({"log_level": DEBUG // 10})
            logger = getLogger("ConfigTest.test_debug_config")
            configure_app(config, logger, handler=StreamHandler(stream))
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

    def test_warning_config(self):
        with StringIO() as stream:
            config = Config({"log_level": WARNING // 10})
            logger = getLogger("ConfigTest.test_warning_config")
            configure_app(config, logger, handler=StreamHandler(stream))
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
