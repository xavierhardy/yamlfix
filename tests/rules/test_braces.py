import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class BracesRuleTest(LoggingTester):
    """braces"""

    def test_no_config(self):
        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst: [key: ]
    lst2:
        - key2:
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst: [key: ]
    lst2:
        - key2:
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_enabled(self):
        config_content = "{extends: default, rules: {braces: enable}}"

        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    empty: {}
    lst: [key: ]
    lst2:
        - key2:
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    empty: {}
    lst: [key: ]
    lst2:
        - key2:
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_forbid(self):
        config_content = "{extends: default, rules: {braces: {forbid: true}}}"

        expected = """---
test42:
    something469: true
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    empty: {}
    lst:
        - key:
    lst2:
        - key2:
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    empty: {}
    lst: [key: ]
    lst2:
        - key2:
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_forbid_non_empty(self):
        config_content = "{extends: default, rules: {braces: {forbid: non-empty}}}"

        expected = """---
test42:
    something469: true
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    empty: {}
    lst:
        - key:
    lst2:
        - key2:
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    empty: {}
    lst: [key: ]
    lst2:
        - key2:
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_allowed(self):
        config_content = "{extends: default, rules: {braces: {forbid: false}}}"

        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    empty: {}
    lst: [key: ]
    lst2:
        - key2:
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    empty: {}
    lst: [key: ]
    lst2:
        - key2:
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled(self):
        config_content = "{extends: default, rules: {braces: disable}}"

        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    empty: {}
    lst: [key: ]
    lst2:
        - key2:
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    empty: {}
    lst: [key: ]
    lst2:
        - key2:
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
