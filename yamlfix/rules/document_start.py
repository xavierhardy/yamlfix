"""
document-start
"""

from typing import Any

from yamllint.rules.document_start import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule


def apply_before_load(text: str, rule: FormattingRule) -> FormattingResult:
    explicit_start = DEFAULT.get("present")
    if rule is not None:
        if not rule:
            explicit_start = None
        else:
            explicit_start = rule.get("present", explicit_start)

        # rule is disabled, leave current state
        if explicit_start is None:
            explicit_start = text.strip().startswith("---")

    return FormattingResult(
        text=text, dumping_config={"explicit_start": explicit_start}
    )


def apply_before_dump(data: Any, rule: FormattingRule, text: str, rules: dict) -> Any:
    return data


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    return result
