import unittest

from yamlfix.formatting import read_and_format_text

from tests.utils import LoggingTester


class FormattingTest(LoggingTester):
    def test_key_duplicates(self):
        """key-duplicates"""
        expected = """---
test: 456
"""

        content = """---
test: 456
test: 42
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_document_start(self):
        """document-start"""
        expected = """---
test: 42
"""

        content = """test: 42
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_new_line_at_end_of_file(self):
        """new-line-at-end-of-file"""
        expected = """---
test: 42
"""

        content = """---
test: 42"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_object_indentation(self):
        """indentation"""
        expected = """---
things:
  stuff:
    something: 312
"""

        content = """---
things:
    stuff:
     something: 312
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_array_indentation(self):
        expected = """---
somearray:
  - item1
  - item2
"""

        content = """---
somearray:
- item1
- item2
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_comments_start(self):
        """comments"""
        expected = """---
key: value  # comments should start with a space
"""

        content = """---
key: value  #comments should start with a space
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_newlines(self):
        """newlines"""
        expected = """---
key: value
"""

        content = """---\r
key: value\r
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_trailing_spaces(self):
        """trailing-spaces"""
        expected = """---
key: value
"""

        content = """---
key: value   
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_hyphens(self):
        """hyphens"""
        expected = """---
somelist:
  - item1
  - item2
  - item3
"""

        content = """---
somelist:
  -  item1
  -   item2
  - item3
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_no_empty_lines_at_start(self):
        """empty-lines"""
        expected = """---
something1: 45
"""

        content = """
---
something1: 45
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_space_before_commas(self):
        """commas"""
        expected = """---
array: [45, 789]
"""

        content = """---
array: [45 , 789]
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_space_after_commas(self):
        """commas"""
        expected = """---
array: [qwe, rty]
"""

        content = """---
array: [qwe,  rty]
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_min_space_after_commas(self):
        """commas"""
        expected = """---
array: [asd, fgh]
"""

        content = """---
array: [asd,fgh]
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_min_space_after_colons(self):
        """colons"""
        expected = """---
somekey: stuff
"""

        content = """---
somekey:  stuff
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)

    def test_min_space_before_colons(self):
        """colons"""
        expected = """---
somekey1: stuff
"""

        content = """---
somekey1 : stuff
"""
        output = read_and_format_text(content)
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
