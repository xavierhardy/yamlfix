"""
new-line-at-end-of-file
"""

from typing import Any

from yamllint.rules.new_line_at_end_of_file import ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule


def apply_before_load(text: str, rule: FormattingRule) -> FormattingResult:
    return FormattingResult(text=text, dumping_config={})


def apply_before_dump(data: Any, rule: FormattingRule) -> Any:
    return data


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    line_break = "\r\n" if "\r\n" in original else "\n"
    has_new_line_at_end_of_file = original.endswith(line_break)

    if not rule and not has_new_line_at_end_of_file and result.endswith(line_break):
        return result[: -len(line_break)]
    return result
