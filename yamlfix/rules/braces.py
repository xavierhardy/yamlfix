"""
braces
"""

from typing import Any, NamedTuple

from ruamel.yaml.comments import CommentedMap, CommentedSeq
from yamllint.rules.braces import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule

BracesOptions = NamedTuple("BracesOptions", (("forbid", int),))

FALSE = 0
TRUE = 1
NON_EMPTY = 2


FORBID_MAP = {
    False: FALSE,
    0: FALSE,
    "f": FALSE,
    "FALSE": FALSE,
    "false": FALSE,
    True: TRUE,
    1: TRUE,
    "t": TRUE,
    "TRUE": TRUE,
    "true": TRUE,
    "non-empty": NON_EMPTY,
}


def set_block_style(data: Any) -> Any:
    # it won't work with items() or iterating through it like list
    if isinstance(data, CommentedMap):
        data.fa.set_block_style()

        for key in data.keys():
            set_block_style(data[key])
    elif isinstance(data, CommentedSeq):
        for indx in range(len(data)):
            set_block_style(data[indx])
    return data


def get_options(rule: FormattingRule, rules: dict) -> BracesOptions:
    return BracesOptions(
        forbid=FORBID_MAP.get(rule.get("forbid", DEFAULT.get("forbid")), FALSE),
    )


def apply_before_load(text: str, rule: FormattingRule, rules: dict) -> FormattingResult:
    return FormattingResult(text=text, dumping_config={}, loading_config={},)


def apply_before_dump(data: Any, rule: FormattingRule, text: str, rules: dict) -> Any:
    if not rule:
        return data

    if get_options(rule, rules).forbid != FALSE:
        return set_block_style(data)
    return data


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    return result
