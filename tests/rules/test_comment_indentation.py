import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class CommentsIndentationRuleTest(LoggingTester):
    """comments-indentation"""

    def test_no_config(self):
        expected = """---
##############################
## This is some documentation
# This sentence
# is a block comment
test: 42  # somecomment
"""

        content = """---
##############################
## This is some documentation
#This sentence
#is a block comment
test: 42  #somecomment
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_default_enabled_missing(self):
        config_content = (
            '{"extends": "default", "rules": {"comments-indentation": "enable"}}'
        )

        expected = """---
##############################
## Some text
# Fix me
test:  # First key
# thing
  key: value
  # valid
  lst:
    - item1
    # here too
"""

        content = """---
##############################
## Some text
# Fix me
test:  # First key
# thing
  key: value
# valid
  lst:
    - item1
  # here too
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_default_no_seq_indent(self):
        config_content = (
            '{"extends": "default", "rules": {'
            '"comments-indentation": "enable",'
            '"indentation": {"indent-sequences": false}'
            "}}"
        )

        expected = """---
##############################
## Some text
# Fix me
test:  # First key
# thing
  key: value
  # valid
  lst:
  - item1
  # here too
"""

        content = """---
##############################
## Some text
# Fix me
test:  # First key
# thing
  key: value
# valid
  lst:
  - item1
    # here too
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_default_enabled_present(self):
        config_content = (
            '{"extends": "default", "rules": {"comments-indentation": "enable"}}'
        )

        expected = """---
##############################
## Some text
# Fix me
test:  # First key
# thing
  key: value
  # valid
  lst:
    - item1
"""

        content = """---
##############################
## Some text
# Fix me
test:  # First key
# thing
  key: value
  # valid
  lst:
    - item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_default_disabled(self):
        config_content = (
            '{"extends": "default", "rules": {"comments-indentation": "disable"}}'
        )

        expected = """---
##############################
## Some text
# Fix me
test:  # First key
# thing
  key: value
# valid
  lst:
    - item1
 # valid
"""

        content = """---
##############################
## Some text
# Fix me
test:  # First key
# thing
  key: value
# valid
  lst:
    - item1
 # valid
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
