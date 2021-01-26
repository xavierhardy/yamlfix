import unittest

from yamllint.config import YamlLintConfig

from yamlfix.files import is_matching_path

from tests.utils import LoggingTester


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


if __name__ == "__main__":
    unittest.main()
