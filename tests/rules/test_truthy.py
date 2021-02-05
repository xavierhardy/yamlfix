import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class TruthyRuleTest(LoggingTester):
    """truthy"""

    def test_no_config(self):
        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    off: FALSE
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_enabled(self):
        config_content = '{extends: default, rules: {truthy: "enable"}}'

        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    off: FALSE
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_single_quote(self):
        config_content = (
            "{extends: default,"
            " rules: {truthy: enable, quoted-strings: {quote-type: single, required: false}}}"
        )

        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    'off': 'FALSE'
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    off: FALSE
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_double_quote(self):
        config_content = (
            "{extends: default,"
            " rules: {truthy: enable, quoted-strings: {quote-type: double, required: false}}}"
        )

        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: "TRuE"
    "off": "FALSE"
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    off: FALSE
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_any_quote(self):
        config_content = (
            "{extends: default,"
            " rules: {truthy: enable, quoted-strings: {quote-type: any, required: false}}}"
        )

        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    'off': "FALSE"
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    'off': FALSE
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_allowed_values(self):
        config_content = "{extends: default, rules: {truthy: {allowed-values: ['no']}}}"

        expected = """---
test42: {something469: "true"}
test43:
    noquote: no
    hey879: 'TRuE'
    "off": "FALSE"
"""

        content = """---
test42: {something469: true}
test43:
    noquote: no
    hey879: 'TRuE'
    off: FALSE
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_check_keys(self):
        config_content = "{extends: default, rules: {truthy: {check-keys: false}}}"

        expected = """---
test42: {something469: true}
test43:
    noquote: "no"
    hey879: 'TRuE'
    off: "FALSE"
"""

        content = """---
test42: {something469: true}
test43:
    noquote: no
    hey879: 'TRuE'
    off: FALSE
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled(self):
        config_content = "{extends: default, rules: {truthy: disable}}"

        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    off: FALSE
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    off: FALSE
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
