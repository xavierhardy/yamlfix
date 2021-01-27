"""
Utility module for parsing command-line arguments
"""

from argparse import ArgumentParser
from logging import INFO

from yamlfix.config import Config


def parse_arguments(*args: str) -> Config:
    """
    Parse arguments and configures what needs to be.
    """
    argument_parser = ArgumentParser("yamlfix", description="Format YAML files")
    argument_parser.add_argument(
        "paths",
        metavar="path",
        type=str,
        nargs="*",
        help="Path to file or folder to format",
    )
    argument_parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        default=False,
        help="Do not reformat files, only check need for reformatting. "
        "Returns an error code if a file needs to be reformatted.",
    )
    logging_arg_group = argument_parser.add_mutually_exclusive_group()
    logging_arg_group.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug logging"
    )
    logging_arg_group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Don't emit non-error messages to stderr. Errors are still emitted; silence those with 2>/dev/null.",
    )
    logging_arg_group.add_argument(
        "-l",
        "--log_level",
        type=int,
        default=INFO // 10,
        help="Enable a specific level of logging (1: DEBUG, 5: CRITICAL, default: INFO)",
    )

    return Config(argument_parser.parse_args(args).__dict__)
