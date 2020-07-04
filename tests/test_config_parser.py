import unittest
from logging import INFO
from unittest import TestCase

from yamlfix.config_parser import parse_arguments


class ConfigTest(TestCase):
    def test_parsing_default_config(self):
        config = parse_arguments()
        self.assertEqual(INFO // 10, config.get("log_level"))
        self.assertFalse(config.get("verbose"))

    def test_parsing_verbose_config(self):
        config = parse_arguments("--verbose")
        self.assertEqual(INFO // 10, config.get("log_level"))
        self.assertTrue(config.get("verbose"))

    def test_parsing_verbose_short_config(self):
        config = parse_arguments("-v")
        self.assertEqual(INFO // 10, config.get("log_level"))
        self.assertTrue(config.get("verbose"))

    def test_parsing_log_level_config(self):
        config = parse_arguments("-l", "3")
        self.assertEqual(3, config.get("log_level"))
        self.assertFalse(config.get("verbose"))

    def test_parsing_invalid_config(self):
        self.assertRaises(SystemExit, parse_arguments, "-l", "3", "-v")


if __name__ == "__main__":
    unittest.main()
