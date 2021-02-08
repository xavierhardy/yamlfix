import unittest
from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile

from yamllint.config import YamlLintConfig

from tests.utils import LoggingTester
from yamlfix.files import is_matching_path, format_file


class FileTest(LoggingTester):
    def test_default(self):
        self.assertTrue(is_matching_path("something.yaml"))
        self.assertTrue(is_matching_path("folder/something.yml"))
        self.assertTrue(is_matching_path(".yamllint"))
        self.assertTrue(is_matching_path(".somefolder/test.yaml"))
        self.assertFalse(is_matching_path("ghdfshs.fadsg"))

    def test_ignore_folder(self):
        config = YamlLintConfig('{"extends": "default", "ignore": ".somefolder/"}')
        self.assertTrue(is_matching_path("something.yaml", yaml_config=config))
        self.assertTrue(is_matching_path("folder/something.yml", yaml_config=config))
        self.assertTrue(is_matching_path(".yamllint", yaml_config=config))
        self.assertFalse(is_matching_path(".somefolder/test.yaml", yaml_config=config))
        self.assertFalse(is_matching_path("ghdfshs.fadsg", yaml_config=config))

    def test_ignore_file(self):
        config = YamlLintConfig('{"extends": "default", "ignore": "something.yml"}')
        self.assertTrue(is_matching_path("something.yaml", yaml_config=config))
        self.assertFalse(is_matching_path("folder/something.yml", yaml_config=config))
        self.assertTrue(is_matching_path(".yamllint", yaml_config=config))
        self.assertTrue(is_matching_path(".somefolder/test.yaml", yaml_config=config))
        self.assertFalse(is_matching_path("ghdfshs.fadsg", yaml_config=config))

    def test_yaml_files_and_ignore(self):
        config = YamlLintConfig('{"yaml-files": ["*.yaml"], "ignore": "test.yaml"}')
        self.assertTrue(is_matching_path("something.yaml", yaml_config=config))
        self.assertFalse(is_matching_path("folder/something.yml", yaml_config=config))
        self.assertFalse(is_matching_path(".yamllint", yaml_config=config))
        self.assertFalse(is_matching_path(".somefolder/test.yaml", yaml_config=config))
        self.assertFalse(is_matching_path("ghdfshs.fadsg", yaml_config=config))

    def test_format_file_actual_run(self):
        content = """{key: 42}"""
        filename = ""
        try:
            with NamedTemporaryFile(delete=False) as f:
                filename = f.name
                f.write(content.encode("utf8"))

            has_changes = format_file(f.name, False)
            self.assertTrue(has_changes)

            with open(filename) as f:
                self.assertNotEqual(content, f.read())
        finally:
            if filename and exists(filename):
                remove(filename)

    def test_format_file_dry_run(self):
        content = """{key: 42}"""
        filename = ""
        try:
            with NamedTemporaryFile(delete=False) as f:
                filename = f.name
                f.write(content.encode("utf8"))

            has_changes = format_file(filename, True)
            self.assertTrue(has_changes)

            with open(filename) as f:
                self.assertEqual(content, f.read())
        finally:
            if filename and exists(filename):
                remove(filename)

    def test_format_unchanged_file_actual_run(self):
        content = """---
key: 42
...
"""
        filename = ""
        try:
            with NamedTemporaryFile(delete=False) as f:
                filename = f.name
                f.write(content.encode("utf8"))

            has_changes = format_file(f.name, False)
            self.assertFalse(has_changes)

            with open(filename) as f:
                self.assertEqual(content, f.read())
        finally:
            if filename and exists(filename):
                remove(filename)

    def test_format_unchanged_file_dry_run(self):
        content = """---
key: 42
...
"""
        filename = ""
        try:
            with NamedTemporaryFile(delete=False) as f:
                filename = f.name
                f.write(content.encode("utf8"))

            has_changes = format_file(filename, True)
            self.assertFalse(has_changes)

            with open(filename) as f:
                self.assertEqual(content, f.read())
        finally:
            if filename and exists(filename):
                remove(filename)


if __name__ == "__main__":
    unittest.main()
