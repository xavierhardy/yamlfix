import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class LineLengthRuleTest(LoggingTester):
    """line-length"""

    def test_no_config(self):
        expected = """---
test:
  key: [value, other_value, another_thing, yet another thing, somethingelse, someothervalue,
    value, other_value, val]
  lst:
    - item1
"""

        content = """---
test:
  key: [value, other_value, another_thing, yet another thing, somethingelse, someothervalue, value, other_value, val]
  lst:
    - item1
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_default_enabled(self):
        config_content = '{"extends": "default", "rules": {"line-length": "enable"}}'

        expected = """---
test:
  key: [value, other_value, another_thing, yet another thing, somethingelse, someothervalue,
    value, other_value, val]
  lst:
    - item1
"""

        content = """---
test:
  key: [value, other_value, another_thing, yet another thing, somethingelse, someothervalue, value, other_value, val]
  lst:
    - item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_default_disabled(self):
        config_content = '{"extends": "default", "rules": {"line-length": "disable"}}'

        expected = """---
test:
  key: [value, other_value, another_thing, yet another thing, somethingelse, someothervalue, value, other_value, val]
  lst:
    - item1
"""

        content = """---
test:
  key: [value, other_value, another_thing, yet another thing, somethingelse, someothervalue,
    value, other_value, val]
  lst:
    - item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_defined_max(self):
        config_content = '{"extends": "default", "rules": {"line-length": {"max": 40}}}'

        expected = """---
test:
  key: [value, other_value, another_thing,
    yet another thing, somethingelse, someothervalue,
    value, other_value, val]
  lst:
    - item1
"""

        content = """---
test:
  key: [value, other_value, another_thing, yet another thing, somethingelse, someothervalue,
    value, other_value, val]
  lst:
    - item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
