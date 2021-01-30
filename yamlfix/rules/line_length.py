"""
line-length
"""

from sys import maxsize
from typing import Any

from yamllint.rules.line_length import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule


def apply_before_load(text: str, rule: FormattingRule) -> FormattingResult:
    width = DEFAULT.get("max", maxsize)
    if rule is not None:
        width = rule.get("max", width) if rule else maxsize

    return FormattingResult(text=text, dumping_config={"width": width},)


def apply_before_dump(data: Any, rule: FormattingRule) -> Any:
    return data


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    return result
