import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class EmptyValuesRuleTest(LoggingTester):
    """empty-values"""

    def test_no_config(self):
        expected = """---
test42: {something469: }
test43:
    hey879:
    hey880:
"""

        content = """---
test42: {something469: }
test43:
    hey879:
    hey880: null
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_default_enabled(self):
        config_content = '{"extends": "default", "rules": {"empty-values": "enable"}}'

        expected = """---
test42: {something469: null}
test43:
    hey879: null
    hey880: null
"""

        content = """---
test42: {something469: }
test43:
    hey879:
    hey880: null
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_forbidden(self):
        config_content = (
            '{"extends": "default",'
            '"rules": {"empty-values": {"forbid-in-block-mappings": true, "forbid-in-flow-mappings": true}}}'
        )

        expected = """---
test42: {something469: null}
test43:
    hey879: null
    hey880: null
"""

        content = """---
test42: {something469: }
test43:
    hey879:
    hey880: null
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_allowed(self):
        config_content = (
            '{"extends": "default",'
            '"rules": {"empty-values": {"forbid-in-block-mappings": false, "forbid-in-flow-mappings": false}}}'
        )

        expected = """---
test42: {something469: }
test43:
    hey879:
    hey880:
"""

        content = """---
test42: {something469: }
test43:
    hey879:
    hey880: null
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_forbid_in_block(self):
        config_content = (
            '{"extends": "default",'
            '"rules": {"empty-values": {"forbid-in-block-mappings": true, "forbid-in-flow-mappings": false}}}'
        )

        expected = """---
test42: {something469: }
test43:
    hey879: null
    hey880: null
"""

        content = """---
test42: {something469: }
test43:
    hey879:
    hey880: null
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_forbid_in_flow(self):
        config_content = (
            '{"extends": "default",'
            '"rules": {"empty-values": {"forbid-in-block-mappings": false, "forbid-in-flow-mappings": true}}}'
        )

        expected = """---
test42: {something469: null}
test43:
    hey879:
    hey880:
"""

        content = """---
test42: {something469: }
test43:
    hey879:
    hey880: null
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disable(self):
        config_content = '{"extends": "default", "rules": {"empty-values": "disable"}}'

        expected = """---
test42: {something469: }
test43:
    hey879:
    hey880:
"""

        content = """---
test42: {something469: }
test43:
    hey879:
    hey880: null
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disable_missing(self):
        config_content = '{"extends": "default", "rules": {"empty-values": "disable"}}'

        expected = """---
test42: {something469: }
test43:
    hey879:
    hey880:
"""

        content = """---
test42: {something469: }
test43:
    hey879:
    hey880:
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
