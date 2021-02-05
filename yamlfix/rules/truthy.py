"""
truthy
"""

from typing import Any, NamedTuple, Set

from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.resolver import implicit_resolvers
from ruamel.yaml.scalarstring import (
    SingleQuotedScalarString,
    DoubleQuotedScalarString,
)
from yamllint.rules.truthy import DEFAULT, ID, TRUTHY  # noqa: F401

from yamlfix.rules import quoted_strings
from yamlfix.rules.types import FormattingResult, FormattingRule

TruthyOptions = NamedTuple(
    "TruthyOptions",
    (("allowed_values", Set[str]), ("check_keys", bool), ("quote_type", int),),
)

TRUTHY_SET = set(TRUTHY)


def replace_truthy(data: Any, options: TruthyOptions) -> Any:
    quote_cast = (
        SingleQuotedScalarString
        if options.quote_type == quoted_strings.SINGLE
        else DoubleQuotedScalarString
    )
    if isinstance(data, (CommentedMap, CommentedSeq)):
        # it won't work with items() or iterating through it like list
        if isinstance(data, CommentedMap):
            for key in data.keys():
                value = data[key]

                if (
                    isinstance(value, str)
                    and not isinstance(
                        value, (SingleQuotedScalarString, DoubleQuotedScalarString)
                    )
                    and value in TRUTHY_SET
                    and value not in options.allowed_values
                ):
                    value = quote_cast(value)

                if (
                    options.check_keys
                    and isinstance(key, str)
                    and not isinstance(
                        key, (SingleQuotedScalarString, DoubleQuotedScalarString)
                    )
                    and key in TRUTHY_SET
                    and key not in options.allowed_values
                ):
                    data.pop(key)
                    data[quote_cast(key)] = value
                else:
                    data[key] = value

                replace_truthy(data[key], options)
        else:
            for indx in range(len(data)):
                replace_truthy(data[indx], options)
    return data


def get_options(rule: FormattingRule, rules: dict) -> TruthyOptions:
    return TruthyOptions(
        allowed_values=set(
            rule.get("allowed-values", DEFAULT.get("allowed-values", ["true", "false"]))
        ),
        check_keys=rule.get("check-keys", DEFAULT.get("check-keys", True)),
        quote_type=quoted_strings.get_options(
            rules.get(quoted_strings.ID) or {}
        ).quote_type,
    )


def remove_bool_resolvers():
    i = 0
    n = len(implicit_resolvers)
    while i < n:
        if implicit_resolvers[i][1] == "tag:yaml.org,2002:bool":
            implicit_resolvers.pop(i)
            n -= 1
        else:
            i += 1


def apply_before_load(text: str, rule: FormattingRule, rules: dict) -> FormattingResult:
    remove_bool_resolvers()

    return FormattingResult(
        text=text, dumping_config={}, loading_config={"preserve_quotes": True},
    )


def apply_before_dump(data: Any, rule: FormattingRule, text: str, rules: dict) -> Any:
    if not rule:
        return data

    options = get_options(rule, rules)
    return replace_truthy(data, options)


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    return result
