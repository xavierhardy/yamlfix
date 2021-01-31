"""
empty-lines
"""

from typing import Any, Iterator, List

from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.tokens import CommentToken
from yamllint.rules.empty_lines import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule
from yamlfix.rules import new_lines


def extract_newlines(text: Iterator[str]) -> Iterator[str]:
    for chrc in text:
        if chrc in ("\n", "\r"):
            yield chrc
        else:
            break


def extract_prefix(text: str) -> str:
    return "".join(extract_newlines(iter(text)))


def extract_suffix(text: str) -> str:
    result = []
    for chrc in text:
        if chrc in ("\n", "\r"):
            result.append(chrc)
        else:
            result = []
    return "".join(result)


def count_newline_chars(text: Iterator[str]) -> int:
    index = 0
    for index, chrc in enumerate(text):
        if chrc not in ("\n", "\r"):
            break

    return index


def skip_extra_new_lines(lines: List[str], max_length: int) -> Iterator[str]:
    count = 0
    line = ""
    for line in lines:
        if not line:
            if count <= max_length:
                yield line
                count += 1
        else:
            yield line
            count = 0
    if not line and count == max_length + 1:
        yield line


def fix_empty_line_group(text: str, max_length: int, line_break: str):
    line_break = "\n"
    # once parsed, only UNIX line breaks are kept
    lines = text.replace("\r\n", "\n").split("\n")
    result = line_break.join(skip_extra_new_lines(lines, max_length))

    # the dumper replaces the last line break, with `line_break`
    if line_break != "\n" and result.endswith(line_break):
        return result[: -len(line_break)] + "\n"

    return result


def fix_empty_lines(data: Any, max_length: int, line_break: str) -> Any:
    if isinstance(data, CommentToken):
        data.value = fix_empty_line_group(data.value, max_length, line_break)
    elif isinstance(data, (CommentedMap, CommentedSeq)):
        comment = data.ca.comment
        for comment_token in comment or []:
            fix_empty_lines(comment_token, max_length, line_break)

        for token_list in data.ca.items.values():
            fix_empty_lines(token_list, max_length, line_break)

        # it won't work with items() or iterating through it like list
        if isinstance(data, CommentedMap):
            for key in data.keys():
                fix_empty_lines(data[key], max_length, line_break)
        else:
            for indx in range(len(data)):
                fix_empty_lines(data[indx], max_length, line_break)
    elif isinstance(data, list):
        for token in data:
            fix_empty_lines(token, max_length, line_break)

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


def replace_linebreaks(text: str, line_break: str) -> str:
    if line_break == "\n":
        return text

    return text.replace("\r\n", "\n").replace("\n", "\r\n")


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    original_line_break = "\r\n" if "\r\n" in original else "\n"
    line_break = "\r\n" if "\r\n" in result else "\n"
    original_prefix = extract_prefix(original).replace(original_line_break, line_break)
    original_suffix = extract_suffix(original).replace(original_line_break, line_break)

    if rule is not None and not rule:
        if original_prefix or original_suffix:
            length_end = count_newline_chars(reversed(result))
            if length_end:
                return replace_linebreaks(
                    original_prefix + result[:-length_end] + original_suffix, line_break
                )

            return replace_linebreaks(
                original_prefix + result + original_suffix, line_break
            )

        return replace_linebreaks(result, line_break)

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
        return replace_linebreaks(
            original_prefix[: max_start * len(line_break)]
            + result[:-length_end]
            + original_suffix[: (max_end + 1) * len(line_break)],
            line_break,
        )
    return replace_linebreaks(result, line_break)
