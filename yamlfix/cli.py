#!/usr/bin/env python
"""
A tool to fix yamllint issues.
"""

from concurrent.futures import ProcessPoolExecutor
from logging import getLogger, Logger, Handler, INFO, WARN, ERROR
from os import cpu_count
from sys import argv
from typing import Sequence

from yamllint.config import YamlLintConfig

from yamlfix.config import configure_app
from yamlfix.config_parser import parse_arguments
from yamlfix.files import find_files, format_file

LOGGER = getLogger(__name__)


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

    try:
        yaml_config = YamlLintConfig(file=".yamllint")
    except IOError:
        yaml_config = None

    check_only = config.get("check")
    fail_text = "FAIL" if check_only else "reformatted"
    changed_file_count = 0
    error_count = 0
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        # executor.map would trigger if one of the underlying function calls
        # raised an exception on iterating
        futures = map(
            lambda pth: executor.submit(format_file, pth, dry_run=check_only, config=yaml_config), paths
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
