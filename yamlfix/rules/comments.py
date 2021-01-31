"""
comments
"""

import re
from typing import Any

from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.tokens import CommentToken
from yamllint.rules.comments import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule

COMMENT_START_REGEX = re.compile(r"^(\r?\n?) *(#+)([^ #\r\n].*\r?\n)")


def fix_comment_start(text: str) -> str:
    return COMMENT_START_REGEX.sub(r"\1\2 \3", text)


def format_comments(data: Any) -> Any:
    if isinstance(data, CommentToken):
        data.value = fix_comment_start(data.value)
    elif isinstance(data, (CommentedMap, CommentedSeq)):
        comment = data.ca.comment
        for comment_token in comment or []:
            format_comments(comment_token)

        for token_list in data.ca.items.values():
            format_comments(token_list)

        # it won't work with items() or iterating through it like list
        if isinstance(data, CommentedMap):
            for key in data.keys():
                format_comments(data[key])
        else:
            for indx in range(len(data)):
                format_comments(data[indx])
    elif isinstance(data, list):
        for tkn in data:
            format_comments(tkn)

    return data


def apply_before_load(text: str, rule: FormattingRule) -> FormattingResult:
    return FormattingResult(text=text, dumping_config={})


def apply_before_dump(data: Any, rule: FormattingRule, text: str, rules: dict) -> Any:
    comment_starting_space = DEFAULT.get("require-starting-space")
    if rule is not None:
        comment_starting_space = rule and rule.get(
            "require-starting-space", comment_starting_space
        )

    if comment_starting_space:
        return format_comments(data)
    return data


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    return result
