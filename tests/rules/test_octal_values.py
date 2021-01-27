import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class OctalValuesRuleTest(LoggingTester):
    """octal-values"""

    def test_no_config(self):
        expected = """---
test:
   key: 010
   lst:
      - 0o10
      - 42
   obj:
      something: else
"""

        content = """---
test:
   key: 010
   lst:
      - 0o10
      - 42
   obj:
      something: else
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_disabled(self):
        config_content = '{"extends": "default", "rules": {"octal-values": "disable"}}'
        expected = """---
test:
   key: 010
   lst:
      - 0o10
      - 42
   obj:
      something: else
"""

        content = """---
test:
   key: 010
   lst:
      - 0o10
      - 42
   obj:
      something: else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_default_enabled(self):
        config_content = '{"extends": "default", "rules": {"octal-values": "enable"}}'

        # TODO: 010 is supposed to be Octal as well though implicit
        expected = """---
test:
  key: 8
  lst:
    - 10
"""

        content = """---
test:
  key: 0o10
  lst:
    - 010
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_implicit_octal_forbidden(self):
        config_content = '{"extends": "default", "rules": {"octal-values": {"forbid-explicit-octal": false}}}'

        # TODO: 010 is supposed to be Octal as well though implicit
        expected = """---
test:
  key: 0o10
  lst:
    - 10
"""

        content = """---
test:
  key: 0o10
  lst:
    - 010
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_exlicit_octal_forbidden(self):
        config_content = '{"extends": "default", "rules": {"octal-values": {"forbid-implicit-octal": false}}}'

        expected = """---
test:
  key: 8
  lst:
    - 010
"""

        content = """---
test:
  key: 0o10
  lst:
    - 010
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_forbid_both(self):
        config_content = '{"rules": {"octal-values": {"forbid-implicit-octal": true, "forbid-explicit-octal": true}}}'

        expected = """---
test:
  key: 8
  lst:
    - 10
...
"""

        content = """---
test:
  key: 0o10
  lst:
    - 010
...
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
