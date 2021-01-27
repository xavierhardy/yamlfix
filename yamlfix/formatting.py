#!/usr/bin/env python
"""
YAML format fixing methods.
"""

import re
from typing import Any, Union, Tuple, List, Optional

from ruamel.yaml import load, dump, RoundTripLoader, RoundTripDumper
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.scalarint import OctalInt, ScalarInt
from ruamel.yaml.tokens import CommentToken

from yamllint.config import YamlLintConfig
from yamllint.rules import (
    comments,
    document_start,
    document_end,
    new_lines,
    octal_values,
    indentation,
)

StreamType = Any

StreamTextType = StreamType
VersionType = Union[List[int], str, Tuple[int, int]]

COMMENT_START_REGEX = re.compile(r"^(\n?) *(#+)([^ #\n].*\n)")


def fix_comment_start(comment: CommentToken):
    comment.value = COMMENT_START_REGEX.sub(r"\1\2 \3", comment.value)


def format_comments(data: Any):
    if isinstance(data, (CommentedMap, CommentedSeq)):
        comment = data.ca.comment
        for comment_token in comment or []:
            if isinstance(comment_token, CommentToken):
                fix_comment_start(comment_token)
            elif isinstance(comment_token, list):
                for tkn in comment_token:
                    if isinstance(tkn, CommentToken):
                        fix_comment_start(tkn)

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


def format_octals(data: Any, forbid_implicit_octal: bool, forbid_explicit_octal: bool):
    if isinstance(data, dict):
        for key, value in dict(data).items():
            data[key] = format_octals(
                value, forbid_implicit_octal, forbid_explicit_octal
            )
    elif isinstance(data, list):
        for index, item in enumerate(list(data)):
            data[index] = format_octals(
                item, forbid_implicit_octal, forbid_explicit_octal
            )
    elif isinstance(data, OctalInt):
        if forbid_explicit_octal:
            return int(data)
    elif isinstance(data, ScalarInt):
        if forbid_implicit_octal:
            return int(data)

    return data


class Loader(RoundTripLoader):
    def __init__(
        self,
        stream: StreamTextType,
        version: Optional[VersionType] = None,
        preserve_quotes: Optional[bool] = None,
        allow_duplicate_keys: bool = True,
    ):
        super().__init__(stream, version=version, preserve_quotes=preserve_quotes)
        self.allow_duplicate_keys = allow_duplicate_keys


def find_first_indent(text):
    for line in text.splitlines():
        if not line.startswith(" "):
            continue

        indent = 0
        for c in line:
            if c == "#":
                break

            if c != " ":
                return indent

            indent += 1


def read_and_format_text(
    text: str, config: Optional[YamlLintConfig] = YamlLintConfig("extends: default")
) -> str:
    stripped_text = text.strip()

    explicit_start = document_start.DEFAULT.get("present")
    explicit_end = document_end.DEFAULT.get("present")
    indent = indentation.DEFAULT.get("spaces")
    block_seq_indent = indentation.DEFAULT.get("indent-sequences")
    # TODO: check-multi-line-strings
    comment_starting_space = comments.DEFAULT.get("require-starting-space")
    # TODO: min-spaces-from-content, ignore-shebangs
    new_line_type = new_lines.DEFAULT.get("type")
    forbid_explicit_octal = octal_values.DEFAULT.get("forbid-explicit-octal")
    forbid_implicit_octal = octal_values.DEFAULT.get("forbid-implicit-octal")
    if config and config.rules:
        rules = config.rules

        if "document-start" in rules:
            document_start_rule = rules["document-start"]
            if not document_start_rule:
                explicit_start = None
            else:
                explicit_start = document_start_rule.get("present", explicit_start)

        # rule is disabled, leave current state
        if explicit_start is None:
            explicit_start = stripped_text.startswith("---")

        if "document-end" in rules:
            document_end_rule = rules["document-end"]
            if not document_end_rule:
                explicit_end = None
            else:
                explicit_end = document_end_rule.get("present", explicit_end)

        # rule is disabled, leave current state
        if explicit_end is None:
            explicit_end = stripped_text.endswith("...")

        if "indentation" in rules:
            indentation_rule = rules["indentation"]
            if not indentation_rule:
                indent = "consistent"
                block_seq_indent = True
            else:
                indent = indentation_rule.get("spaces", indent)
                block_seq_indent = indentation_rule.get(
                    "indent-sequences", block_seq_indent
                )

        if "comments" in rules:
            comment_rule = rules["comments"]
            comment_starting_space = comment_rule and comment_rule.get(
                "require-starting-space", comment_starting_space
            )

        if "new-lines" in rules:
            new_line_rule = rules["new-lines"]
            new_line_type = (
                new_line_rule.get("type", new_line_type) if new_line_rule else None
            )

        if "octal-values" in rules:
            octal_value_rule = rules["octal-values"]
            forbid_explicit_octal = octal_value_rule and octal_value_rule.get(
                "forbid-explicit-octal", forbid_explicit_octal
            )
            forbid_implicit_octal = octal_value_rule and octal_value_rule.get(
                "forbid-implicit-octal", forbid_implicit_octal
            )

    if indent == "consistent":
        indent = find_first_indent(text) or 2

    if block_seq_indent:
        if indent:
            block_seq_indent = indent
        else:
            block_seq_indent = 2
    else:
        block_seq_indent = None

    if new_line_type == "unix":
        line_break = "\n"
    elif new_line_type == "dos" or "\r\n" in text:
        line_break = "\r\n"
    else:
        line_break = "\n"

    data = load(text, Loader)
    if comment_starting_space:
        format_comments(data)
    if forbid_explicit_octal or forbid_implicit_octal:
        data = format_octals(data, forbid_implicit_octal, forbid_explicit_octal)

    return dump(
        data,
        Dumper=RoundTripDumper,
        explicit_start=explicit_start,
        explicit_end=explicit_end,
        block_seq_indent=block_seq_indent,
        indent=indent,
        line_break=line_break,
    )
