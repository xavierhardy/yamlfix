import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class IndentationRuleTest(LoggingTester):
    """indentation"""

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
    something: else
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_default_enabled(self):
        config_content = '{"extends": "default", "rules": {"indentation": "enable"}}'

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
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_default_disabled(self):
        config_content = '{"extends": "default", "rules": {"indentation": "disable"}}'

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

    def test_defined_indent(self):
        config_content = (
            '{"extends": "default", "rules": {"indentation": {"spaces": 6}}}'
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

    def test_no_sequence_indentation(self):
        config_content = '{"extends": "default", "rules": {"indentation": {"indent-sequences": false}}}'

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

    def test_sequence_indentation(self):
        config_content = '{"extends": "default", "rules": {"indentation": {"indent-sequences": true}}}'

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


if __name__ == "__main__":
    unittest.main()
