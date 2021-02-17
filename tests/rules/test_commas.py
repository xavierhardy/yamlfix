import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class CommasRuleTest(LoggingTester):
    """commas"""

    def test_no_config(self):
        expected = """---
three_comma_club: {something469: true, somethingelse: 42, yetanother: test, some: 78}
test43:
    'with_colon:': [TRuE, test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist, "withcommas,", 78, 'withother,']
        - something_else
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_enabled(self):
        config_content = '{extends: default, rules: {commas: "enable"}}'

        expected = """---
three_comma_club: {something469: true, somethingelse: 42, yetanother: test, some: 78}
test43:
    'with_colon:': [TRuE, test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist, "withcommas,", 78, 'withother,']
        - something_else
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_after_is_2(self):
        config_content = "{extends: default, rules: {commas: {max-spaces-after: 2}}}"

        expected = """---
three_comma_club: {something469: true, somethingelse: 42,  yetanother: test,  some: 78}
test43:
    'with_colon:': [TRuE,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas,", 78,  'withother,']
        - something_else
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_after_is_3(self):
        config_content = "{extends: default, rules: {commas: {max-spaces-after: 3}}}"

        expected = """---
three_comma_club: {something469: true, somethingelse: 42,   yetanother: test,  some: 78}
test43:
    'with_colon:': [TRuE,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas,", 78,  'withother,']
        - something_else
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_after_is_large(self):
        config_content = "{extends: default, rules: {commas: {max-spaces-after: 10}}}"

        expected = """---
three_comma_club: {something469: true, somethingelse: 42,     yetanother: test,  some: 78}
test43:
    'with_colon:': [TRuE,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas,", 78,  'withother,']
        - something_else
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_before_is_2(self):
        config_content = "{extends: default, rules: {commas: {max-spaces-before: 2}}}"

        expected = """---
three_comma_club: {something469: true, somethingelse: 42  , yetanother: test  , some: 78}
test43:
    'with_colon:': [TRuE , test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist, "withcommas," , 78 , 'withother,']
        - something_else
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_before_is_3(self):
        config_content = "{extends: default, rules: {commas: {max-spaces-before: 3}}}"

        expected = """---
three_comma_club: {something469: true, somethingelse: 42   , yetanother: test  , some: 78}
test43:
    'with_colon:': [TRuE , test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist, "withcommas," , 78 , 'withother,']
        - something_else
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_before_is_large(self):
        config_content = "{extends: default, rules: {commas: {max-spaces-before: 10}}}"

        expected = """---
three_comma_club: {something469: true, somethingelse: 42   , yetanother: test  , some: 78}
test43:
    'with_colon:': [TRuE , test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist, "withcommas," , 78 , 'withother,']
        - something_else
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_is_2(self):
        config_content = "{extends: default, rules: {commas: {max-spaces-after: 2, max-spaces-before: 2}}}"

        expected = """---
three_comma_club: {something469: true, somethingelse: 42  ,  yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_is_3(self):
        config_content = "{extends: default, rules: {commas: {max-spaces-after: 3, max-spaces-before: 3}}}"

        expected = """---
three_comma_club: {something469: true, somethingelse: 42   ,   yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_max_space_is_large(self):
        config_content = "{extends: default, rules: {commas: {max-spaces-after: 10, max-spaces-before: 10}}}"

        expected = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_no_change(self):
        config_content = "{extends: default, rules: {commas: {max-spaces-after: 10, max-spaces-before: 10}}}"

        expected = """---
three_comma_club: {something469: true, somethingelse: 42, yetanother: test, some: 78}
test43:
    'with_colon:': [TRuE, test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist, "withcommas,", 78, 'withother,']
        - something_else
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42, yetanother: test, some: 78}
test43:
    'with_colon:': [TRuE, test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist, "withcommas,", 78, 'withother,']
        - something_else
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled_unix_newline(self):
        config_content = (
            "{extends: default, rules: {commas: disable, new-lines: {type: unix}}}"
        )

        expected = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled_dos_newline(self):
        config_content = (
            "{extends: default, rules: {commas: disable, new-lines: {type: dos}}}"
        )

        expected = """---\r
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}\r
test43:\r
    'with_colon:': [TRuE ,  test]\r
    hey879: 'TRuE'\r
    "off": "FALSE"\r
    lst:\r
        - [somelist,  "withcommas," , 78 ,  'withother,']\r
        - something_else\r
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled(self):
        config_content = "{extends: default, rules: {commas: disable}}"

        expected = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""

        content = """---
three_comma_club: {something469: true, somethingelse: 42   ,     yetanother: test  ,  some: 78}
test43:
    'with_colon:': [TRuE ,  test]
    hey879: 'TRuE'
    "off": "FALSE"
    lst:
        - [somelist,  "withcommas," , 78 ,  'withother,']
        - something_else
"""

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
