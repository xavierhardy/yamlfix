import unittest
from logging import INFO, WARN

from tests.utils import LoggingTester
from yamlfix.cli import format_result


class CliTest(LoggingTester):
    def test_format_result_check_all(self):
        expected = """Oh no!
2 files would be reformatted, 5 files would be left unchanged, 3 files would fail to reformat."""
        log_message = format_result(10, 2, 3, True)
        self.assertEqual(expected, log_message.message % log_message.kwargs)
        self.assertEqual(WARN, log_message.level)

    def test_format_result_check_all_singular(self):
        expected = """Oh no!
1 file would be reformatted, 1 file would be left unchanged, 1 file would fail to reformat."""
        log_message = format_result(3, 1, 1, True)
        self.assertEqual(expected, log_message.message % log_message.kwargs)
        self.assertEqual(WARN, log_message.level)

    def test_format_result_check_ok(self):
        expected = """All done!
10 files would be left unchanged."""
        log_message = format_result(10, 0, 0, True)
        self.assertEqual(expected, log_message.message % log_message.kwargs)
        self.assertEqual(INFO, log_message.level)

    def test_format_result_all(self):
        expected = """Oh no!
2 files reformatted, 5 files left unchanged, 3 files failed to reformat."""
        log_message = format_result(10, 2, 3, False)
        self.assertEqual(expected, log_message.message % log_message.kwargs)
        self.assertEqual(WARN, log_message.level)

    def test_format_result_all_singular(self):
        expected = """Oh no!
1 file reformatted, 1 file left unchanged, 1 file failed to reformat."""
        log_message = format_result(3, 1, 1, False)
        self.assertEqual(expected, log_message.message % log_message.kwargs)
        self.assertEqual(WARN, log_message.level)

    def test_format_result_ok(self):
        expected = """All done!
10 files left unchanged."""
        log_message = format_result(10, 0, 0, False)
        self.assertEqual(expected, log_message.message % log_message.kwargs)
        self.assertEqual(INFO, log_message.level)


if __name__ == "__main__":
    unittest.main()
