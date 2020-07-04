#!/usr/bin/env python
"""
Small skeleton Python-3 application trying to follow good practices such as automatic code formatting, unit testing,
separations of concerns, linting and typing.
"""

import re
from concurrent.futures import ProcessPoolExecutor
from glob import iglob
from logging import getLogger, Logger, Handler, INFO, WARN, ERROR
from os import cpu_count
from os.path import isfile
from sys import argv
from typing import Sequence, Any, Collection, Pattern

from ruamel.yaml import load, dump, RoundTripLoader, RoundTripDumper
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.tokens import CommentToken

from yamlfix.config import configure_app
from yamlfix.config_parser import parse_arguments

LOGGER = getLogger(__name__)

COMMENT_START_REGEX = re.compile(r"^(\n?) *(#+)([^ #\n].*\n)")
DEFAULT_INCLUDE = (re.compile(r".*\.ya?ml", re.IGNORECASE),)


def fix_comment_start(comment: CommentToken):
    comment.value = COMMENT_START_REGEX.sub(r"\1\2 \3", comment.value)


def format_comments(data: Any):
    if isinstance(data, (CommentedMap, CommentedSeq)):
        comment = data.ca.comment
        for comment_token in comment or []:
            if isinstance(comment_token, CommentToken):
                fix_comment_start(comment_token)

        for token_list in data.ca.items.values():
            for token in token_list:
                if isinstance(token, CommentToken):
                    fix_comment_start(token)

        # it won't work with items() or iterating through it like list
        if isinstance(data, CommentedMap):
            for key in data.keys():
                format_comments(data[key])
        else:
            for indx in range(len(data)):
                format_comments(data[indx])


def read_and_format_text(text: str) -> str:
    data = load(text, RoundTripLoader)
    format_comments(data)
    return dump(data, Dumper=RoundTripDumper)


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


def log_result(total: int, changed: int, errors: int):
    result_texts = ["%(untouched)d files without changes"]
    log_level = INFO
    if changed > 0:
        result_texts.insert(0, "%(changed) files with changes")
        log_level = WARN

    if errors > 0:
        result_texts.insert(0, "%(errors) errors")
        log_level = ERROR

    LOGGER.log(
        log_level,
        ", ".join(result_texts),
        dict(changed=changed, errors=errors, untouched=total - changed),
    )


def main(args: Sequence[str] = None, logger: Logger = None, handler: Handler = None):
    if args is None:
        args = argv[1:]

    if logger is None:
        logger = LOGGER

    config = parse_arguments(*args)
    configure_app(config, logger, handler=handler)
    paths = set()
    for path in config.get("paths", []):
        paths.update(find_files(path))

    check_only = config.get("check")
    fail_text = "FAIL" if check_only else "reformatted"
    changed_file_count = 0
    error_count = 0
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        # executor.map would trigger if one of the underlying function calls
        # raised an exception on iterating
        futures = map(
            lambda pth: executor.submit(format_file, pth, dry_run=check_only), paths
        )

        # list makes sure the futures are all submitted before waiting on the first results
        for pth, future in list(zip(paths, futures)):
            try:
                if future.result():
                    changed_file_count += 1
                    LOGGER.warning("%s: %s", pth, fail_text)
                else:
                    LOGGER.debug("%s: OK", pth)
            except Exception as e:
                error_count += 1
                LOGGER.error("%s: ERROR", pth)
                LOGGER.error(e)

    log_result(len(paths), changed_file_count, error_count)
    return error_count > 0 and (not check_only or changed_file_count == 0)


if __name__ == "__main__":
    exit_code = 0 if main(argv, LOGGER) else 1
    exit(exit_code)
