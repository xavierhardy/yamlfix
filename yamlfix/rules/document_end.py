"""
document-end
"""

from typing import Any

from yamllint.rules.document_end import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule


def apply_before_load(text: str, rule: FormattingRule) -> FormattingResult:
    explicit_end = DEFAULT.get("present")
    if rule is not None:
        if not rule:
            explicit_end = None
        else:
            explicit_end = rule.get("present", explicit_end)

        # rule is disabled, leave current state
        if explicit_end is None:
            explicit_end = text.strip().endswith("...")

    return FormattingResult(text=text, dumping_config={"explicit_end": explicit_end})


def apply_before_dump(data: Any, rule: FormattingRule, text: str, rules: dict) -> Any:
    return data


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    return result
