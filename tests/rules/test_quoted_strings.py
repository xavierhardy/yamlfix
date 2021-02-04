import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class QuotedStringsRuleTest(LoggingTester):
    """quoted-strings"""

    def test_no_config(self):
        expected = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_enabled(self):
        config_content = '{extends: default, rules: {quoted-strings: "enable"}}'

        expected = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: "somevalue"
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_single_quote_required(self):
        config_content = "{extends: default, rules: {quoted-strings: {quote-type: single, required: true}}}"

        expected = """---
test42: {something469: 'value'}
test43:
    hey879: 'someothervalue'
    hey880: 'somevalue'
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_double_quote_required(self):
        config_content = "{extends: default, rules: {quoted-strings: {quote-type: double, required: true}}}"

        expected = """---
test42: {something469: "value"}
test43:
    hey879: "someothervalue"
    hey880: "somevalue"
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_single_quote_optional(self):
        config_content = "{extends: default, rules: {quoted-strings: {quote-type: single, required: false}}}"

        expected = """---
test42: {something469: 'value'}
test43:
    hey879: 'someothervalue'
    hey880: somevalue
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_double_quote_optional(self):
        config_content = "{extends: default, rules: {quoted-strings: {quote-type: double, required: false}}}"

        expected = """---
test42: {something469: "value"}
test43:
    hey879: "someothervalue"
    hey880: somevalue
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_single_quote_if_needed(self):
        config_content = (
            "{extends: default,"
            " rules: {quoted-strings: {quote-type: single, required: only-when-needed}}}"
        )

        expected = """---
test42: {something469: value}
test43:
    hey879: someothervalue
    hey880: somevalue
    required: '{this: needsquotes}'
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
    required: '{this: needsquotes}'
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_double_quote_if_needed(self):
        config_content = (
            "{extends: default,"
            " rules: {quoted-strings: {quote-type: double, required: only-when-needed}}}"
        )

        expected = """---
test42: {something469: value}
test43:
    hey879: someothervalue
    hey880: somevalue
    required: "{this: needsquotes}"
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
    required: "{this: needsquotes}"
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_any_quote_if_needed(self):
        config_content = "{extends: default, rules: {quoted-strings: {quote-type: any, required: only-when-needed}}}"

        expected = """---
test42: {something469: value}
test43:
    hey879: someothervalue
    hey880: somevalue
    required: "{this: needsquotes}"
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
    required: "{this: needsquotes}"
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_single_quote_if_needed_extra_required(self):
        config_content = (
            "{extends: default,"
            " rules: {"
            "  quoted-strings: {"
            "   quote-type: single, required: only-when-needed, extra-required: [some]"
            "  }"
            "}}"
        )

        expected = """---
test42: {something469: value}
test43:
    hey879: 'someothervalue'
    hey880: 'somevalue'
    required: '{this: needsquotes}'
"""

        content = """---
test42: {something469: value}
test43:
    hey879: "someothervalue"
    hey880: somevalue
    required: '{this: needsquotes}'
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_double_quote_if_needed_extra_required(self):
        config_content = (
            "{extends: default,"
            " rules: {"
            "  quoted-strings: {"
            "   quote-type: double, required: only-when-needed, extra-required: [some]"
            "  }"
            "}}"
        )

        expected = """---
test42: {something469: value}
test43:
    hey879: "someothervalue"
    hey880: "somevalue"
    required: "{this: needsquotes}"
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
    required: "{this: needsquotes}"
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_any_quote_if_needed_extra_required(self):
        config_content = (
            "{extends: default,"
            " rules: {"
            "  quoted-strings: {quote-type: any, required: only-when-needed, extra-required: [some]}"
            "}}"
        )

        expected = """---
test42: {something469: value}
test43:
    hey879: "someothervalue"
    hey880: "somevalue"
    required: "{this: needsquotes}"
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
    required: "{this: needsquotes}"
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_single_quote_extra_required(self):
        config_content = (
            "{extends: default,"
            " rules: {quoted-strings: {quote-type: single, required: false, extra-required: [some]}}}"
        )

        expected = """---
test42: {something469: value}
test43:
    hey879: 'someothervalue'
    hey880: 'somevalue'
    required: '{this: needsquotes}'
"""

        content = """---
test42: {something469: value}
test43:
    hey879: "someothervalue"
    hey880: somevalue
    required: '{this: needsquotes}'
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_double_quote_extra_required(self):
        config_content = (
            "{extends: default,"
            " rules: {quoted-strings: {quote-type: double, required: false, extra-required: [some]}}}"
        )

        expected = """---
test42: {something469: "value"}
test43:
    hey879: "someothervalue"
    hey880: "somevalue"
    required: "{this: needsquotes}"
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
    required: "{this: needsquotes}"
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_any_quote_extra_required(self):
        config_content = (
            "{extends: default,"
            " rules: {quoted-strings: {quote-type: any, required: false, extra-required: [some]}}}"
        )

        expected = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: "somevalue"
    required: "{this: needsquotes}"
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
    required: "{this: needsquotes}"
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_single_quote_if_needed_extra_allowed(self):
        config_content = (
            "{extends: default,"
            " rules: {"
            "  quoted-strings: {quote-type: single, required: only-when-needed, extra-allowed: [some]}"
            "}}"
        )

        expected = """---
test42: {something469: value}
test43:
    hey879: 'someothervalue'
    hey880: somevalue
    required: '{this: needsquotes}'
"""

        content = """---
test42: {something469: value}
test43:
    hey879: "someothervalue"
    hey880: somevalue
    required: '{this: needsquotes}'
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_double_quote_if_needed_extra_allowed(self):
        config_content = (
            "{extends: default,"
            " rules: {"
            "  quoted-strings: {quote-type: double, required: only-when-needed, extra-allowed: [some]}"
            "}}"
        )

        expected = """---
test42: {something469: value}
test43:
    hey879: "someothervalue"
    hey880: somevalue
    required: "{this: needsquotes}"
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
    required: "{this: needsquotes}"
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_any_quote_if_needed_extra_allowed(self):
        config_content = (
            "{extends: default,"
            " rules: {"
            "  quoted-strings: {quote-type: any, required: only-when-needed, extra-allowed: [some]}"
            "}}"
        )

        expected = """---
test42: {something469: value}
test43:
    hey879: "someothervalue"
    hey880: somevalue
    required: "{this: needsquotes}"
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
    required: "{this: needsquotes}"
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled(self):
        config_content = '{extends: default, rules: {quoted-strings: "disable"}}'

        expected = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
"""

        content = """---
test42: {something469: 'value'}
test43:
    hey879: "someothervalue"
    hey880: somevalue
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
