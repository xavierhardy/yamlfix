#!/usr/bin/env python
"""
YAML format fixing methods.
"""

import re
from typing import Any, Union, Tuple, List, Optional

from ruamel.yaml import load, dump, RoundTripLoader, RoundTripDumper
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.tokens import CommentToken

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


def read_and_format_text(text: str) -> str:
    data = load(text, Loader)
    format_comments(data)
    return dump(data, Dumper=RoundTripDumper, explicit_start=True, block_seq_indent=2)
