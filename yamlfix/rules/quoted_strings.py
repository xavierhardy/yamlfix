"""
quoted-strings
"""

from re import compile, Pattern
from typing import Any, NamedTuple, List

from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.scalarstring import (
    PlainScalarString,
    SingleQuotedScalarString,
    DoubleQuotedScalarString,
)
from yamllint.rules.quoted_strings import DEFAULT, ID, _quotes_are_needed  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule

QuotedStringOptions = NamedTuple(
    "QuotedStringOptions",
    (
        ("quote_type", int),
        ("required", int),
        ("extra_required", List[Pattern]),
        ("extra_allowed", List[Pattern]),
    ),
)


ANY = 0
SINGLE = 1
DOUBLE = 2

QUOTE_TYPES = {
    "any": ANY,
    "single": SINGLE,
    "double": DOUBLE,
}

FALSE = 0
TRUE = 1
ONLY_WHEN_NEEDED = 2

REQUIRED_MAP = {
    "": FALSE,
    "false": FALSE,
    "f": FALSE,
    "no": FALSE,
    "n": FALSE,
    False: FALSE,
    0: FALSE,
    None: FALSE,
    "true": TRUE,
    "t": TRUE,
    "yes": TRUE,
    "y": TRUE,
    1: TRUE,
    True: TRUE,
    "only-when-needed": ONLY_WHEN_NEEDED,
}


def replace_quoted_strings(data: Any, options: QuotedStringOptions) -> Any:
    quote_cast = (
        SingleQuotedScalarString
        if options.quote_type == SINGLE
        else DoubleQuotedScalarString
    )
    patterns = options.extra_required + options.extra_allowed
    # it won't work with items() or iterating through it like list
    if isinstance(data, CommentedMap):
        for key in data.keys():
            data[key] = replace_quoted_strings(data[key], options)
    elif isinstance(data, CommentedSeq):
        for indx in range(len(data)):
            data[indx] = replace_quoted_strings(data[indx], options)
    elif isinstance(data, str):
        if (
            options.required == ONLY_WHEN_NEEDED
            and isinstance(data, (SingleQuotedScalarString, DoubleQuotedScalarString))
            and not _quotes_are_needed(data)
            and all(pattern.search(data) is None for pattern in patterns)
        ):
            return PlainScalarString(data)
        elif (
            options.required == TRUE
            or _quotes_are_needed(data)
            or any(
                pattern.search(data) is not None for pattern in options.extra_required
            )
        ) and not isinstance(
            data, (SingleQuotedScalarString, DoubleQuotedScalarString)
        ):
            return quote_cast(data)
        elif options.quote_type == SINGLE and isinstance(
            data, DoubleQuotedScalarString
        ):
            return SingleQuotedScalarString(data)
        elif options.quote_type == DOUBLE and isinstance(
            data, SingleQuotedScalarString
        ):
            return DoubleQuotedScalarString(data)
    return data


def get_options(rule: FormattingRule) -> QuotedStringOptions:
    return QuotedStringOptions(
        quote_type=QUOTE_TYPES.get(
            rule.get("quote-type", DEFAULT.get("quote-type", "any")), ANY
        ),
        required=REQUIRED_MAP.get(rule.get("required", DEFAULT.get("required")), FALSE),
        extra_required=[
            compile(value)
            for value in rule.get("extra-required", DEFAULT.get("extra-required", []))
        ],
        extra_allowed=[
            compile(value)
            for value in rule.get("extra-allowed", DEFAULT.get("extra-allowed", []))
        ],
    )


def apply_before_load(text: str, rule: FormattingRule, rules: dict) -> FormattingResult:
    return FormattingResult(
        text=text, dumping_config={}, loading_config={"preserve_quotes": False},
    )


def apply_before_dump(data: Any, rule: FormattingRule, text: str, rules: dict) -> Any:
    if not rule:
        return data

    options = get_options(rule)
    return replace_quoted_strings(data, options)


def apply_on_result(
    result: str, original: str, rule: FormattingRule, rules: dict
) -> str:
    return result
