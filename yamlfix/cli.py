#!/usr/bin/env python
"""
A tool to fix yamllint issues.
"""

from concurrent.futures import ProcessPoolExecutor
from logging import getLogger, Logger, Handler, INFO, WARN
from os import cpu_count
from os.path import abspath
from sys import argv
from typing import Sequence

from yamllint.config import YamlLintConfig

from yamlfix.config import configure_app
from yamlfix.config_parser import parse_arguments
from yamlfix.files import find_files, format_file

LOGGER = getLogger(__name__)


def log_result(total: int, changed: int, errors: int, check_only: bool = False):
    untouched = total - changed - errors
    verb = " would be" if check_only else ""
    error_verb = "would fail" if check_only else "failed"
    result_texts = []
    if untouched > 0:
        result_texts.append(
            "1 file%(verb)s left unchanged"
            if untouched == 1
            else "%(untouched)d files%(verb)s left unchanged"
        )

    log_level = INFO
    if changed > 0:
        result_texts.insert(
            0,
            "1 file%(verb)s reformatted"
            if changed == 1
            else "%(changed)d%(verb)s reformatted",
        )
        log_level = WARN

    if errors > 0:
        result_texts.append(
            "1 file %(error_verb)s to reformat"
            if errors == 1
            else "%(errors)d %(error_verb)s to reformat",
        )
        log_level = WARN
        message = "Oh no!"
    else:
        message = "All done!"

    LOGGER.log(
        log_level,
        "%s\n%s." % (message, ", ".join(result_texts)),
        dict(
            changed=changed,
            errors=errors,
            untouched=untouched,
            verb=verb,
            error_verb=error_verb,
        ),
    )


def main(args: Sequence[str] = None, logger: Logger = None, handler: Handler = None):
    if args is None:
        args = argv[1:]

    if logger is None:
        logger = LOGGER

    config = parse_arguments(*args)
    configure_app(config, logger, handler=handler)

    try:
        yaml_config = YamlLintConfig(file=".yamllint")
    except IOError:
        yaml_config = None

    paths = set()
    for path in config.get("paths", []):
        paths.update(find_files(path, yaml_config=yaml_config))

    check_only = config.get("check")
    fail_text = "would reformat" if check_only else "reformatted"
    changed_file_count = 0
    error_count = 0
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        # executor.map would trigger if one of the underlying function calls
        # raised an exception on iterating
        futures = map(
            lambda pth: executor.submit(
                format_file, pth, dry_run=check_only, yaml_config=yaml_config
            ),
            paths,
        )

        # list makes sure the futures are all submitted before waiting on the first results
        for pth, future in list(zip(paths, futures)):
            full_path = abspath(pth)
            try:
                if future.result():
                    changed_file_count += 1
                    LOGGER.warning("%s %s", fail_text, full_path)
                else:
                    LOGGER.debug("%s already well formatted, good job.", full_path)
            except Exception as e:
                error_count += 1
                LOGGER.error("error: cannot format %s: %s", full_path, e)

    log_result(len(paths), changed_file_count, error_count, check_only=check_only)
    return error_count > 0 and (not check_only or changed_file_count == 0)


if __name__ == "__main__":
    exit_code = 0 if main(argv, LOGGER) else 1
    exit(exit_code)
