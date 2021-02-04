"""
comments-indentation
"""

import re
from typing import Any

from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.tokens import CommentToken
from yamllint.rules.comments_indentation import ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule
from yamlfix.rules import indentation

COMMENT_INDENTATION_REGEX = re.compile(r"^\n *(#+.*\r?\n)")


def fix_comment_indentation(text: str, indent: int) -> str:
    result = COMMENT_INDENTATION_REGEX.sub(r"\n%s\1" % (" " * indent), text)
    return result


def format_comments(
    data: Any, indent: int, block_seq_indent: int, current_indent: int = 0
) -> Any:
    if isinstance(data, CommentToken):
        data.value = fix_comment_indentation(data.value, current_indent)
    elif isinstance(data, (CommentedMap, CommentedSeq)):
        if isinstance(data, CommentedSeq) and block_seq_indent < indent:
            current_indent += block_seq_indent - indent

        comment = data.ca.comment
        for comment_token in comment or []:
            format_comments(comment_token, indent, block_seq_indent, current_indent)

        for token_list in data.ca.items.values():
            format_comments(token_list, indent, block_seq_indent, current_indent)

        # it won't work with items() or iterating through it like list
        if isinstance(data, CommentedMap):
            for key in data.keys():
                format_comments(
                    data[key], indent, block_seq_indent, current_indent + indent
                )
        else:
            for indx in range(len(data)):
                format_comments(
                    data[indx],
                    indent,
                    block_seq_indent,
                    current_indent + block_seq_indent,
                )
    elif isinstance(data, list):
        for tkn in data:
            format_comments(tkn, indent, block_seq_indent, current_indent)

    return data


def apply_before_load(text: str, rule: FormattingRule) -> FormattingResult:
    return FormattingResult(text=text, dumping_config={}, loading_config={})


def apply_before_dump(data: Any, rule: FormattingRule, text: str, rules: dict) -> Any:
    if not rule:
        return data

    indentation_config = indentation.get_config(text, rules.get("indentation"))
    indent = indentation_config["indent"]
    block_seq_indent = indentation_config["block_seq_indent"]

    return format_comments(data, indent, block_seq_indent or 0)


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    return result
