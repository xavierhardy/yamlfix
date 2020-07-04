from io import StringIO
from unittest import TestCase

DEBUG_MSG = "debug"
INFO_MSG = "info"
WARNING_MSG = "warning"
ERROR_MSG = "error"
CRITICAL_MSG = "critical"


class LoggingTester(TestCase):
    def assert_log(self, expected: str, stream: StringIO):
        actual_log_lines = stream.getvalue().strip().split()
        self.assertEqual(expected, actual_log_lines[-1])

    def assert_empty_log(self, stream: StringIO):
        self.assertEqual("", stream.getvalue().strip())
