#!/usr/bin/env python
"""
YAML format fixing methods.
"""

import re
from typing import Any, Union, Tuple, List, Optional

from ruamel.yaml import load, dump, RoundTripLoader, RoundTripDumper
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.tokens import CommentToken

from yamllint.config import YamlLintConfig
from yamllint.rules.document_start import DEFAULT as DOCUMENT_START_DEFAULT
from yamllint.rules.document_end import DEFAULT as DOCUMENT_END_DEFAULT

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


# def read_and_format_text(text: str, config: Optional[YamlLintConfig] = None) -> str: #YamlLintConfig("extends: default")) -> str:
def read_and_format_text(text: str, config: Optional[YamlLintConfig] = YamlLintConfig("extends: default")) -> str:
    stripped_text = text.strip()

    explicit_start = DOCUMENT_START_DEFAULT.get("present")
    if config and config.rules:
        rules = config.rules

        if "document-start" in rules:
            document_start_rule = rules["document-start"]
            if not document_start_rule:
                explicit_start = None
            else:
                explicit_start = document_start_rule.get("present", DOCUMENT_START_DEFAULT.get("present"))

        # rule is disabled, leave current state
        if explicit_start is None:
            explicit_start = stripped_text.startswith("---")

    explicit_end = DOCUMENT_END_DEFAULT.get("present")
    if config and config.rules:
        rules = config.rules

        if "document-end" in rules:
            document_end_rule = rules["document-end"]
            if not document_end_rule:
                explicit_end = None
            else:
                explicit_end = document_end_rule.get("present", DOCUMENT_END_DEFAULT.get("present"))

        # rule is disabled, leave current state
        if explicit_end is None:
            explicit_end = stripped_text.endswith("...")

    data = load(text, Loader)
    format_comments(data)
    return dump(data, Dumper=RoundTripDumper, explicit_start=explicit_start, explicit_end=explicit_end, block_seq_indent=2)
