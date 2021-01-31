import unittest

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.formatting import read_and_format_text


class EmptyLinesRuleTest(LoggingTester):
    """empty-lines"""

    def test_no_config(self):
        expected = """---
test:
   key: value
   lst:
      - item1
   obj:
      something: else
"""

        content = """


---
test:
   key: value
   lst:
      - item1
   obj:
      something: else


"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_enabled(self):
        config_content = '{"extends": "default", "rules": {"empty-lines": "enable"}}'

        expected = """---
test:
  key: value
  lst:
    - item1
"""

        content = """

---
test:
  key: value
  lst:
    - item1

"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_disabled(self):
        config_content = '{"extends": "default", "rules": {"empty-lines": "disable"}}'

        expected = """---
test:
  key: value
  lst:
    - item1
"""

        content = """---
test:
  key: value
  lst:
    - item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_disabled_present(self):
        config_content = '{"extends": "default", "rules": {"empty-lines": "disable"}}'

        expected = """

---
test:
  key: value
  lst:
    - item1

"""

        content = """

---
test:
  key: value
  lst:
    - item1

"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_dos_disabled(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"empty-lines": "disable", "new-lines": {"type": "dos"}}}'
        )

        expected = """---\r
test:\r
  key: value\r
  lst:\r
    - item1\r
"""

        content = """---\r
test:\r
  key: value\r
  lst:\r
    - item1\r
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_dos_disabled_present(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"empty-lines": "disable", "new-lines": {"type": "dos"}}}'
        )

        expected = """\r
---\r
test:\r
  key: value\r
  lst:\r
    - item1\r
\r
\r
\r
"""

        content = """\r
---\r
test:\r
  key: value\r
  lst:\r
    - item1\r
\r
\r
\r
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_dos_enabled(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"empty-lines": "enable", "new-lines": {"type": "dos"}}}'
        )

        expected = """---\r
test:\r
  key: value\r
  lst:\r
    - item1\r
"""

        content = """\r
---\r
test:\r
  key: value\r
  lst:\r
    - item1\r
\r
\r
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_unix_disabled(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"empty-lines": "disable", "new-lines": {"type": "unix"}}}'
        )

        expected = """---
test:
  key: value
  lst:
    - item1
"""

        content = """---
test:
  key: value
  lst:
    - item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_unix_disabled_present(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"empty-lines": "disable", "new-lines": {"type": "unix"}}}'
        )

        expected = """


---
test:
  key: value
  lst:
    - item1

"""

        content = """


---
test:
  key: value
  lst:
    - item1

"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_unix_enabled(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"empty-lines": "enable", "new-lines": {"type": "unix"}}}'
        )

        expected = """---
test:
  key: value
  lst:
    - item1
"""

        content = """

---
test:
  key: value
  lst:
    - item1

"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_unix_max_start_end(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"empty-lines": {"max-start": 2, "max-end": 1}, "new-lines": {"type": "unix"}}}'
        )

        expected = """

---
test:
  key: value
  lst:
    - item1

"""

        content = """



---
test:
  key: value
  lst:
    - item1





"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_unix_lines_in_the_middle(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"empty-lines": {"max": 5}, "new-lines": {"type": "unix"}}}'
        )

        expected = """---
test:
  key: value





  lst:
    - item1
"""

        content = """---
test:
  key: value






  lst:
    - item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_dos_lines_in_the_middle(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"empty-lines": {"max": 5}, "new-lines": {"type": "dos"}}}'
        )

        expected = """---\r
test:\r
  key: value\r
\r
\r
\r
\r
\r
  lst:\r
    - item1\r
"""

        content = """---\r
test:\r
  key: value\r
\r
\r
\r
\r
\r
\r
  lst:\r
    - item1\r
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_dos_max_start_end(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"empty-lines": {"max-start": 2, "max-end": 1}, "new-lines": {"type": "dos"}}}'
        )

        expected = """\r
\r
---\r
test:\r
  key: value\r
  lst:\r
    - item1\r
\r
"""

        content = """\r
\r
\r
\r
---\r
test:\r
  key: value\r
  lst:\r
    - item1\r
\r
\r
\r
\r
\r
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_unix_lines_in_the_middle_with_comments(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"empty-lines": {"max": 5}, "new-lines": {"type": "unix"}}}'
        )

        expected = """---
test:
  key: value





# some test

# some test

  lst:
    - item1
"""

        content = """---
test:
  key: value








# some test

# some test

  lst:
    - item1
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)

    def test_dos_lines_in_the_middle_with_comments(self):
        config_content = (
            '{"extends": "default", '
            '"rules": {"empty-lines": {"max": 5}, "new-lines": {"type": "dos"}}}'
        )

        expected = """---\r
test:\r
  key: value\r
\r
\r
# some test\r
\r
# some test\r
\r
  lst:\r
    - item1\r
"""

        content = """---\r
test:\r
  key: value\r
\r
\r
# some test\r
\r
# some test\r
\r
  lst:\r
    - item1\r
"""
        output = read_and_format_text(content, YamlLintConfig(content=config_content))
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
