import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class TrailingSpacesRuleTest(LoggingTester):
    """trailing-spaces"""

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
    "off": "FALSE"    
"""  # noqa: W291
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_enabled(self):
        config_content = '{extends: default, rules: {trailing-spaces: "enable"}}'

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
    "off": "FALSE"    
"""  # noqa: W291
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled_unix_newline(self):
        config_content = (
            "{extends: default,"
            " rules: {trailing-spaces: disable, new-lines: {type: unix}}}"
        )

        expected = """---
test42: {something469: true}
test43:  
    noquote: TRuE 
    hey879: 'TRuE'
    "off": "FALSE"    
"""  # noqa: W291

        content = """---
test42: {something469: true}
test43:  
    noquote: TRuE 
    hey879: 'TRuE'
    "off": "FALSE"    
"""  # noqa: W291

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled_dos_newline(self):
        config_content = (
            "{extends: default,"
            " rules: {trailing-spaces: disable, new-lines: {type: dos}}}"
        )

        expected = """---\r
test42: {something469: true}\r
test43:  \r
    noquote: TRuE \r
    hey879: 'TRuE'\r
    "off": "FALSE"    \r
"""

        content = """---
test42: {something469: true}
test43:  
    noquote: TRuE 
    hey879: 'TRuE'
    "off": "FALSE"    
"""  # noqa: W291

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled(self):
        config_content = "{extends: default, rules: {trailing-spaces: disable}}"

        expected = """---
test42: {something469: true}
test43:  
    noquote: TRuE 
    hey879: 'TRuE'
    "off": "FALSE"    
"""  # noqa: W291

        content = """---
test42: {something469: true}
test43:  
    noquote: TRuE 
    hey879: 'TRuE'
    "off": "FALSE"    
"""  # noqa: W291

        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
