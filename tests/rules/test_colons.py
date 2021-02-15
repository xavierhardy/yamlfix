import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class ColonsRuleTest(LoggingTester):
    """colons"""

    def test_no_config(self):
        expected = """---
test42: {something469: true}
test43:
    'with_colon:': TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        - something_else
"""

        content = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_enabled(self):
        config_content = '{extends: default, rules: {colons: "enable"}}'

        expected = """---
test42: {something469: true}
test43:
    'with_colon:': TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        - something_else
"""

        content = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_after_is_2(self):
        config_content = "{extends: default, rules: {colons: {max-spaces-after: 2}}}"

        expected = """---
test42:  {something469:  true}
test43:
    'with_colon:':  TRuE
    hey879: 'TRuE'
    "off":  "FALSE"
    lst:
        - somelist
        - something_else
"""

        content = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_after_is_3(self):
        config_content = "{extends: default, rules: {colons: {max-spaces-after: 3}}}"

        expected = """---
test42:   {something469:   true}
test43:
    'with_colon:':  TRuE
    hey879: 'TRuE'
    "off":  "FALSE"
    lst:
        - somelist
        - something_else
"""

        content = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_after_is_large(self):
        config_content = "{extends: default, rules: {colons: {max-spaces-after: 10}}}"

        expected = """---
test42:   {something469:    true}
test43:
    'with_colon:':  TRuE
    hey879: 'TRuE'
    "off":  "FALSE"
    lst:
        - somelist
        - something_else
"""

        content = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_before_is_2(self):
        config_content = "{extends: default, rules: {colons: {max-spaces-before: 2}}}"

        expected = """---
test42  : {something469 : true}
test43 :
    'with_colon:' : TRuE
    hey879 : 'TRuE'
    "off" : "FALSE"
    lst:
        - somelist
        - something_else
"""

        content = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_before_is_3(self):
        config_content = "{extends: default, rules: {colons: {max-spaces-before: 3}}}"

        expected = """---
test42   : {something469 : true}
test43 :
    'with_colon:' : TRuE
    hey879 : 'TRuE'
    "off" : "FALSE"
    lst:
        - somelist
        - something_else
"""

        content = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_before_is_large(self):
        config_content = "{extends: default, rules: {colons: {max-spaces-before: 10}}}"

        expected = """---
test42     : {something469 : true}
test43 :
    'with_colon:' : TRuE
    hey879 : 'TRuE'
    "off" : "FALSE"
    lst:
        - somelist
        - something_else
"""

        content = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_is_2(self):
        config_content = "{extends: default, rules: {colons: {max-spaces-after: 2, max-spaces-before: 2}}}"

        expected = """---
test42  :  {something469 :  true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""

        content = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_is_3(self):
        config_content = "{extends: default, rules: {colons: {max-spaces-after: 3, max-spaces-before: 3}}}"

        expected = """---
test42   :   {something469 :   true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""

        content = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_is_large(self):
        config_content = "{extends: default, rules: {colons: {max-spaces-after: 10, max-spaces-before: 10}}}"

        expected = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""

        content = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_no_change(self):
        config_content = "{extends: default, rules: {colons: {max-spaces-after: 10, max-spaces-before: 10}}}"

        expected = """---
test42: {something469: true}
test43:
    'with_colon:': TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        - something_else
"""

        content = """---
test42: {something469: true}
test43:
    'with_colon:': TRuE
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - somelist
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled_unix_newline(self):
        config_content = (
            "{extends: default, rules: {colons: disable, new-lines: {type: unix}}}"
        )

        expected = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""

        content = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled_dos_newline(self):
        config_content = (
            "{extends: default, rules: {colons: disable, new-lines: {type: dos}}}"
        )

        expected = """---\r
test42     :   {something469 :    true}\r
test43 :\r
    'with_colon:' :  TRuE\r
    hey879 : 'TRuE'\r
    "off" :  "FALSE"\r
    lst:\r
        - somelist\r
        - something_else\r
"""

        content = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled(self):
        config_content = "{extends: default, rules: {colons: disable}}"

        expected = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""

        content = """---
test42     :   {something469 :    true}
test43 :
    'with_colon:' :  TRuE
    hey879 : 'TRuE'
    "off" :  "FALSE"
    lst:
        - somelist
        - something_else
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
