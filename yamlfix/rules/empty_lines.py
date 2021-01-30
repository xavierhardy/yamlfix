"""
empty-lines
"""

from typing import Any, Iterator, Tuple

from yamllint.rules.empty_lines import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule


def remove_prefix(text: str, max_size: int = 0) -> str:
    start, index = count_newline_chars(iter(text), max_size)
    if index:
        return text[index - start :]  # noqa: E203
    return text


def remove_suffix(text: str, max_size: int = 0) -> str:
    start, index = count_newline_chars(reversed(text), max_size)
    if index:
        return text[: -index + start]
    return text


def extract_prefix(text: str, max_size: int = 0) -> str:
    start, index = count_newline_chars(iter(text), max_size)
    if index:
        return text[start:index]
    return ""


def extract_suffix(text: str, max_size: int = 0) -> str:
    start, index = count_newline_chars(reversed(text), max_size)
    if index:
        return text[-index : len(text) - start]  # noqa: E203
    return ""


def count_newline_chars(text: Iterator[str], max_size: int = 0) -> Tuple[int, int]:
    start = 0
    for index, chrc in enumerate(text):
        if chrc not in ("\n", "\r"):
            return start, index
        elif chrc == "\n" and max_size > 0:
            max_size -= 1
            start = index
    return start, 0


def apply_before_load(text: str, rule: FormattingRule) -> FormattingResult:
    return FormattingResult(text=text, dumping_config={})


def apply_before_dump(data: Any, rule: FormattingRule) -> Any:
    return data


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    if rule is not None and not rule:
        original_prefix = extract_prefix(original)
        original_suffix = extract_suffix(original)
        if original_prefix or original_suffix:
            _, length_end = count_newline_chars(reversed(result))
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

    result = remove_prefix(result, max_start)
    return remove_suffix(result, max_end)
