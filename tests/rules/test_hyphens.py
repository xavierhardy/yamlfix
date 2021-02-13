import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class HyphensRuleTest(LoggingTester):
    """hyphens"""

    def test_no_config(self):
        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        - something_else
        - hey
        - 'yo'
        - 42
        - "56"
        - -sometextwithhyphen
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        -  something_else
        -    hey
        - 'yo'
        - 42
        -  "56"
        -   -sometextwithhyphen
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_enabled(self):
        config_content = '{extends: default, rules: {hyphens: "enable"}}'

        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        - something_else
        - hey
        - 'yo'
        - 42
        - "56"
        - -sometextwithhyphen
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        -  something_else
        -    hey
        - 'yo'
        - 42
        -  "56"
        -   -sometextwithhyphen
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_is_2(self):
        config_content = "{extends: default, rules: {hyphens: {max-spaces-after: 2}}}"

        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        -  something_else
        -  hey
        - 'yo'
        - 42
        -  "56"
        -  -sometextwithhyphen
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        -  something_else
        -    hey
        - 'yo'
        - 42
        -  "56"
        -   -sometextwithhyphen
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_is_3(self):
        config_content = "{extends: default, rules: {hyphens: {max-spaces-after: 3}}}"

        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        -  something_else
        -   hey
        - 'yo'
        - 42
        -  "56"
        -   -sometextwithhyphen
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        -  something_else
        -    hey
        - 'yo'
        - 42
        -  "56"
        -   -sometextwithhyphen
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_is_large(self):
        config_content = "{extends: default, rules: {hyphens: {max-spaces-after: 10}}}"

        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        -  something_else
        -    hey
        - 'yo'
        - 42
        -  "56"
        -   -sometextwithhyphen
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        -  something_else
        -    hey
        - 'yo'
        - 42
        -  "56"
        -   -sometextwithhyphen
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled_unix_newline(self):
        config_content = (
            "{extends: default, rules: {hyphens: disable, new-lines: {type: unix}}}"
        )

        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        -  something_else
        -    hey
        - 'yo'
        - 42
        -  "56"
        -   -sometextwithhyphen
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        -  something_else
        -    hey
        - 'yo'
        - 42
        -  "56"
        -   -sometextwithhyphen
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled_dos_newline(self):
        config_content = (
            "{extends: default, rules: {hyphens: disable, new-lines: {type: dos}}}"
        )

        expected = """---\r
test42: {something469: true}\r
test43:\r
    noquote: TRuE\r
    hey879: 'TRuE'\r
    "off": "FALSE"\r
    lst:\r
        - somelist\r
        -  something_else\r
        -    hey\r
        - 'yo'\r
        - 42\r
        -  "56"\r
        -   -sometextwithhyphen\r
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        -  something_else
        -    hey
        - 'yo'
        - 42
        -  "56"
        -   -sometextwithhyphen
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled(self):
        config_content = "{extends: default, rules: {hyphens: disable}}"

        expected = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        -  something_else
        -    hey
        - 'yo'
        - 42
        -  "56"
        -   -sometextwithhyphen
"""

        content = """---
test42: {something469: true}
test43:
    noquote: TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        -  something_else
        -    hey
        - 'yo'
        - 42
        -  "56"
        -   -sometextwithhyphen
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
