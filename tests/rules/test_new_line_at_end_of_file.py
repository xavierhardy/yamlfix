import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class NewLinesRuleTest(LoggingTester):
    """new-lines"""

    def test_no_config(self):
        expected = """---
test:
   key: value
   lst:
      - item1
   obj:
      something: else
"""

        content = """---\r
test:\r
   key: value\r
   lst:\r
      - item1\r
   obj:\r
      something: else\r
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_default_enabled(self):
        config_content = '{"extends": "default", "rules": {"new-lines": "enable"}}'

        expected = """---
test:
  key: value
  lst:
    - item1
"""

        content = """---\r
test:\r
  key: value\r
  lst:\r
    - item1\r
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_default_disabled_unix(self):
        config_content = '{"extends": "default", "rules": {"new-lines": "disable"}}'

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

    def test_default_disabled_dos(self):
        config_content = '{"extends": "default", "rules": {"new-lines": "disable"}}'

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

    def test_unix_type(self):
        config_content = (
            '{"extends": "default", "rules": {"new-lines": {"type": "unix"}}}'
        )

        expected = """---
test:
  key: value
  lst:
    - item1
"""

        content = """---\r
test:\r
  key: value\r
  lst:\r
    - item1\r
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_dos_type(self):
        config_content = (
            '{"extends": "default", "rules": {"new-lines": {"type": "dos"}}}'
        )

        expected = """---\r
test:\r
  key: value\r
  lst:\r
    - item1\r
"""

        content = """---
test:
  key: value
  lst:
    - item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_already_unix_type(self):
        config_content = (
            '{"extends": "default", "rules": {"new-lines": {"type": "unix"}}}'
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

    def test_already_dos_type(self):
        config_content = (
            '{"extends": "default", "rules": {"new-lines": {"type": "dos"}}}'
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


if __name__ == "__main__":
    unittest.main()
