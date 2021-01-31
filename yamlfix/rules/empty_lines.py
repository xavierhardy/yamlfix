"""
empty-lines
"""

from typing import Any, Iterator

from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.tokens import CommentToken
from yamllint.rules.empty_lines import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule
from yamlfix.rules import new_lines


def extract_prefix(text: str) -> str:
    index = count_newline_chars(iter(text))
    if index:
        return text[:index]
    return ""


def extract_suffix(text: str) -> str:
    index = count_newline_chars(reversed(text))
    if index:
        return text[-index : len(text)]  # noqa: E203
    return ""


def count_newline_chars(text: Iterator[str]) -> int:
    index = 0
    for index, chrc in enumerate(text):
        if chrc not in ("\n", "\r"):
            return index

    return index


def fix_empty_line_group(comment: CommentToken, max_length: int, line_break: str):
    # once parsed, only UNIX line breaks are kept
    count = 0
    result = []
    for line in comment.value.split("\n"):
        if not line:
            if count <= max_length + 1:
                result.append(line)
            count += 1
        else:
            result.append(line)
            count = 0

    text = line_break.join(result)

    # the dumper replaces the last line break, with `line_break`
    if line_break != "\n" and text.endswith(line_break):
        comment.value = text[: -len(line_break)] + "\n"
    else:
        comment.value = text


def fix_empty_lines(data: Any, max_length: int, line_break: str) -> Any:
    if isinstance(data, (CommentedMap, CommentedSeq)):
        comment = data.ca.comment
        for comment_token in comment or []:
            if isinstance(comment_token, CommentToken):
                fix_empty_line_group(comment_token, max_length, line_break)
            elif isinstance(comment_token, list):
                for tkn in comment_token:
                    if isinstance(tkn, CommentToken):
                        fix_empty_line_group(tkn, max_length, line_break)

        for token_list in data.ca.items.values():
            for token in token_list:
                if isinstance(token, CommentToken):
                    fix_empty_line_group(token, max_length, line_break)

        # it won't work with items() or iterating through it like list
        if isinstance(data, CommentedMap):
            for key in data.keys():
                fix_empty_lines(data[key], max_length, line_break)
        else:
            for indx in range(len(data)):
                fix_empty_lines(data[indx], max_length, line_break)

    return data


def apply_before_load(text: str, rule: FormattingRule) -> FormattingResult:
    return FormattingResult(text=text, dumping_config={})


def apply_before_dump(data: Any, rule: FormattingRule, text: str, rules: dict) -> Any:
    if rule is not None and not rule:
        return data

    max_length = DEFAULT.get("max")
    if rule is not None:
        max_length = rule and rule.get("max", max_length)

    if max_length is not None:
        return fix_empty_lines(
            data, max_length, new_lines.get_line_break(text, rules.get(new_lines.ID))
        )
    return data


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    original_line_break = "\r\n" if "\r\n" in original else "\n"
    line_break = "\r\n" if "\r\n" in result else "\n"
    original_prefix = extract_prefix(original).replace(original_line_break, line_break)
    original_suffix = extract_suffix(original).replace(original_line_break, line_break)

    if rule is not None and not rule:
        if original_prefix or original_suffix:
            length_end = count_newline_chars(reversed(result))
            if length_end:
                return original_prefix + result[:-length_end] + original_suffix

            return original_prefix + result + original_suffix

        return result

    max_start = DEFAULT.get("max-start")
    max_end = DEFAULT.get("max-end")
    max_all = DEFAULT.get("max")
    if rule is not None:
        max_start = rule.get("max-start", max_start)
        max_end = rule.get("max-end", max_end)
        max_all = rule.get("max")

    if max_start is None:
        max_start = max_all

    if max_end is None:
        max_end = max_all

    if original_prefix or original_suffix:
        length_end = count_newline_chars(reversed(result))
        return (
            original_prefix[: max_start * len(line_break)]
            + result[:-length_end]
            + original_suffix[: (max_end + 1) * len(line_break)]
        )
    return result
