"""
empty-lines
"""

from typing import Any, Iterator

from yamllint.rules.empty_lines import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule


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
    for index, chrc in enumerate(text):
        if chrc not in ("\n", "\r"):
            return index

    return 0


def apply_before_load(text: str, rule: FormattingRule) -> FormattingResult:
    return FormattingResult(text=text, dumping_config={})


def apply_before_dump(data: Any, rule: FormattingRule) -> Any:
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
