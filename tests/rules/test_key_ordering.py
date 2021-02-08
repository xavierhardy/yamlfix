import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class KeyOrderingRuleTest(LoggingTester):
    """key-ordering"""

    def test_no_config(self):
        expected = """---
key 2: v
key 1: val
lst:
    - {first_name: something, age: 42, last_name: else}
    - {age: 41, first_name: already, last_name: in_order}
"""

        content = """---
key 2: v
key 1: val
lst:
    - {first_name: something, age: 42, last_name: else}
    - {age: 41, first_name: already, last_name: in_order}
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_enabled(self):
        config_content = '{"extends": "default", "rules": {"key-ordering": "enable"}}'

        expected = """---
key 1: val
key 2: v
key 3:
    else: 45
    something: 456
lst:
    - {age: 42, first_name: something, last_name: else}
    - {age: 41, first_name: already, last_name: in_order}
"""

        content = """---
key 3:
    something: 456
    else: 45
key 2: v
key 1: val
lst:
    - {first_name: something, age: 42, last_name: else}
    - {age: 41, first_name: already, last_name: in_order}
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled(self):
        config_content = '{"extends": "default", "rules": {"key-ordering": "disable"}}'

        expected = """---
key 1: val
key 2: v
key 3:
    else: 45
    something: 456
lst:
    - {first_name: something, age: 42, last_name: else}
    - {age: 41, first_name: already, last_name: in_order}
"""

        content = """---
key 1: val
key 2: v
key 3:
    else: 45
    something: 456
lst:
    - {first_name: something, age: 42, last_name: else}
    - {age: 41, first_name: already, last_name: in_order}
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled_with_changes(self):
        config_content = '{"extends": "default", "rules": {"key-ordering": "disable"}}'

        expected = """---
key 3:
    something: 456
    else: 45
key 2: v
key 1: val
lst:
    - {first_name: something, age: 42, last_name: else}
    - {age: 41, first_name: already, last_name: in_order}
"""

        content = """---
key 3:
    something: 456
    else: 45
key 2: v
key 1: val
lst:
    - {first_name: something, age: 42, last_name: else}
    - {age: 41, first_name: already, last_name: in_order}
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
