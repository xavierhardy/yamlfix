import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class CommentsRuleTest(LoggingTester):
    """comments"""

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

    def test_default_enabled(self):
        config_content = '{"extends": "default", "rules": {"comments": "enable"}}'

        expected = """---
##############################
## Some text
# Fix me
test:  # First key
  key: value
  lst:
    - item1
"""

        content = """---
##############################
##Some text
#Fix me
test:  #First key
  key: value
  lst:
  - item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_default_disabled(self):
        config_content = '{"extends": "default", "rules": {"comments": "disable"}}'

        expected = """---
#Something
test:  #else
  key: value
  lst:
    - item1  #item1
"""

        content = """---
#Something
test:  #else
  key: value
  lst:
    - item1  #item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_not_require_starting_space(self):
        config_content = '{"extends": "default", "rules": {"comments": {"require-starting-space": false}}}'

        expected = """---
#Something
test:  #else
  key: value
  lst:
    - item1  #item1
"""

        content = """---
#Something
test:  #else
  key: value
  lst:
    - item1  #item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_require_starting_space(self):
        config_content = '{"extends": "default", "rules": {"comments": {"require-starting-space": true}}}'

        expected = """---
# Something
test:  # else
  key: value
  lst:
    - item1  # item1
"""

        content = """---
#Something
test:  #else
  key: value
  lst:
    - item1  #item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
