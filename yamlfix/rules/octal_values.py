"""
octal-values
"""

from typing import Any

from ruamel.yaml.scalarint import OctalInt, ScalarInt
from yamllint.rules.octal_values import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule


def format_octals(data: Any, forbid_implicit_octal: bool, forbid_explicit_octal: bool):
    if isinstance(data, dict):
        for key, value in dict(data).items():
            data[key] = format_octals(
                value, forbid_implicit_octal, forbid_explicit_octal
            )
    elif isinstance(data, list):
        for index, item in enumerate(list(data)):
            data[index] = format_octals(
                item, forbid_implicit_octal, forbid_explicit_octal
            )
    elif isinstance(data, OctalInt):
        if forbid_explicit_octal:
            return int(data)
    elif isinstance(data, ScalarInt) and forbid_implicit_octal:
        return int(data)

    return data


def apply_before_load(text: str, rule: FormattingRule) -> FormattingResult:
    return FormattingResult(text=text, dumping_config={})


def apply_before_dump(data: Any, rule: FormattingRule) -> Any:
    forbid_explicit_octal = DEFAULT.get("forbid-explicit-octal")
    forbid_implicit_octal = DEFAULT.get("forbid-implicit-octal")
    if rule is not None:
        forbid_explicit_octal = rule and rule.get(
            "forbid-explicit-octal", forbid_explicit_octal
        )
        forbid_implicit_octal = rule and rule.get(
            "forbid-implicit-octal", forbid_implicit_octal
        )

    if forbid_explicit_octal or forbid_implicit_octal:
        return format_octals(data, forbid_implicit_octal, forbid_explicit_octal)
    return data


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    return result
