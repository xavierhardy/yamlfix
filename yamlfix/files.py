#!/usr/bin/env python
"""
File-related functions.
"""

from glob import iglob
from os.path import isfile
from typing import Collection, Pattern, Optional

from yamllint.config import YamlLintConfig

from yamlfix.formatting import read_and_format_text

DEFAULT_CONFIG = YamlLintConfig("extends: default")


def format_file(
    path: str, dry_run: bool, yaml_config: Optional[YamlLintConfig] = None
) -> bool:
    with open(path) as file_reader:
        original_content = file_reader.read()

    new_content = read_and_format_text(original_content, config=yaml_config)

    if original_content != new_content:
        if not dry_run:
            with open(path, "w") as file_writer:
                file_writer.write(new_content)
        return True

    return False


def is_matching_path(
    filename: str,
    include: Collection[Pattern] = (),
    exclude: Collection[Pattern] = (),
    yaml_config: Optional[YamlLintConfig] = DEFAULT_CONFIG,
) -> bool:
    return (
        all(rgx.match(filename) is None for rgx in exclude)
        and (yaml_config is None or not yaml_config.is_file_ignored(filename))
        and (
            any(rgx.match(filename) for rgx in include)
            or yaml_config is None
            or yaml_config.is_yaml_file(filename)
        )
    )


def find_files(
    path: str,
    include: Collection[Pattern] = (),
    exclude: Collection[Pattern] = (),
    yaml_config: Optional[YamlLintConfig] = DEFAULT_CONFIG,
):
    for filename in iglob(path, recursive=True):
        if not isfile(filename) or not is_matching_path(
            filename, include=include, exclude=exclude, yaml_config=yaml_config
        ):
            continue

        yield path
