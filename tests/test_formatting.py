import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class FormattingTest(LoggingTester):
    def test_default_document_start_enabled(self):
        """document-start"""
        config_content = '{"rules": {"document-start": "enable"}}'

        expected = """---
test: 79
"""

        content = """test: 79
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_document_start_not_present(self):
        """document-start"""
        config_content = '{"rules": {"document-start": {"present": false}}}'

        expected = """test: 12
"""

        content = """---
test: 12
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_document_start_present(self):
        """document-start"""
        config_content = '{"rules": {"document-start": {"present": true}}}'

        expected = """---
test: 88
"""

        content = """test: 88
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_document_start_disable(self):
        """document-start"""
        config_content = '{"rules": {"document-start": "disable"}}'

        expected = """---
test: 77
"""

        content = """---
test: 77
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_document_start_disable_missing(self):
        """document-start"""
        config_content = '{"rules": {"document-start": "disable"}}'

        expected = """test: 4452
"""

        content = """test: 4452
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
