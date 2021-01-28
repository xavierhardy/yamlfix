import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class NewLineAtEndOfFileRuleTest(LoggingTester):
    """new-line-at-end-of-file"""

    def test_no_config(self):
        expected = """---
test:
   key: value
   lst:
      - item1
   obj:
      something: else
"""

        content = """---
test:
   key: value
   lst:
      - item1
   obj:
      something: else"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_enabled(self):
        config_content = (
            '{"extends": "default", "rules": {"new-line-at-end-of-file": "enable"}}'
        )

        expected = """---
test:
  key: value
  lst:
    - item1
"""

        content = """---
test:
  key: value
  lst:
    - item1"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_disabled(self):
        config_content = (
            '{"extends": "default", "rules": {"new-line-at-end-of-file": "disable"}}'
        )

        expected = """---
test:
  key: value
  lst:
    - item1"""

        content = """---
test:
  key: value
  lst:
    - item1"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled_present(self):
        config_content = (
            '{"extends": "default", "rules": {"new-line-at-end-of-file": "disable"}}'
        )

        expected = """---
test:
  key: value
  lst:
    - item1
"""

        content = """---
test:
  key: value
  lst:
    - item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_dos_disabled(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"new-line-at-end-of-file": "disable", "new-lines": {"type": "dos"}}}'
        )

        expected = """---\r
test:\r
  key: value\r
  lst:\r
    - item1"""

        content = """---\r
test:\r
  key: value\r
  lst:\r
    - item1"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_dos_disabled_present(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"new-line-at-end-of-file": "disable", "new-lines": {"type": "dos"}}}'
        )

        expected = """---\r
test:\r
  key: value\r
  lst:\r
    - item1\r
"""

        content = """---\r
test:\r
  key: value\r
  lst:\r
    - item1\r
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_dos_enabled(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"new-line-at-end-of-file": "enable", "new-lines": {"type": "dos"}}}'
        )

        expected = """---\r
test:\r
  key: value\r
  lst:\r
    - item1\r
"""

        content = """---\r
test:\r
  key: value\r
  lst:\r
    - item1"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_unix_disabled(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"new-line-at-end-of-file": "disable", "new-lines": {"type": "unix"}}}'
        )

        expected = """---
test:
  key: value
  lst:
    - item1"""

        content = """---
test:
  key: value
  lst:
    - item1"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_unix_disabled_present(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"new-line-at-end-of-file": "disable", "new-lines": {"type": "unix"}}}'
        )

        expected = """---
test:
  key: value
  lst:
    - item1
"""

        content = """---
test:
  key: value
  lst:
    - item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_unix_enabled(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"new-line-at-end-of-file": "enable", "new-lines": {"type": "unix"}}}'
        )

        expected = """---
test:
  key: value
  lst:
    - item1
"""

        content = """---
test:
  key: value
  lst:
    - item1"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
