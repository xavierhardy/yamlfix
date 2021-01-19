#!/usr/bin/env python
"""
File-related functions.
"""

import re
from glob import iglob
from os.path import isfile
from typing import Collection, Pattern

from yamlfix.formatting import read_and_format_text

DEFAULT_INCLUDE = (re.compile(r".*\.ya?ml", re.IGNORECASE),)


def format_file(path: str, dry_run: bool) -> bool:
    with open(path) as file_reader:
        original_content = file_reader.read()

    new_content = read_and_format_text(original_content)

    if original_content != new_content:
        if not dry_run:
            with open(path, "w") as file_writer:
                file_writer.write(new_content)
        return True

    return False


def find_files(
    path: str,
    include: Collection[Pattern] = DEFAULT_INCLUDE,
    exclude: Collection[Pattern] = (),
):
    for filename in iglob(path, recursive=True):
        if (
            not isfile(filename)
            or any(rgx.match(filename) for rgx in exclude)
            or not all(rgx.match(filename) for rgx in include)
        ):
            continue

        yield path
