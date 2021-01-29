"""
new-lines
"""

from typing import Any

from yamllint.rules.new_lines import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule


def apply_before_load(text: str, rule: FormattingRule) -> FormattingResult:
    new_line_type = DEFAULT.get("type")
    if rule is not None:
        new_line_type = rule.get("type", new_line_type) if rule else None

    if new_line_type == "unix":
        line_break = "\n"
    elif new_line_type == "dos" or "\r\n" in text:
        line_break = "\r\n"
    else:
        line_break = "\n"

    return FormattingResult(text=text, dumping_config={"line_break": line_break})


def apply_before_dump(data: Any, rule: FormattingRule) -> Any:
    return data


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    return result
