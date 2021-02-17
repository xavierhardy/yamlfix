"""
commas
"""

from re import compile, sub
from typing import Any, NamedTuple

from yamllint.rules.commas import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule

SpaceCounts = NamedTuple("SpaceCounts", (("before", int), ("after", int)))

COMMA_REGEX = compile(
    r"('(?:\\'|[^'\r\n])*?'|\"(?:\\\"|[^\"\r\n])*?\"|[^\"\'\r\n,:{}[\] ]+)( *),( *)"
)


def apply_before_load(text: str, rule: FormattingRule, rules: dict) -> FormattingResult:
    return FormattingResult(text=text, dumping_config={}, loading_config={},)


def apply_before_dump(data: Any, rule: FormattingRule, text: str, rules: dict) -> Any:
    return data


def apply_on_result(
    result: str, original: str, rule: FormattingRule, rules: dict
) -> str:
    min_spaces_after = DEFAULT.get("min-spaces-after")
    max_spaces_before = DEFAULT.get("max-spaces-before")
    max_spaces_after = DEFAULT.get("max-spaces-after")
    if rule:
        min_spaces_after = rule.get("min-spaces-after", min_spaces_after)
        max_spaces_before = rule.get("max-spaces-before", max_spaces_before)
        max_spaces_after = rule.get("max-spaces-after", max_spaces_after)
    elif rule is not None:
        min_spaces_after = None
        max_spaces_before = None
        max_spaces_after = None

    if max_spaces_before == 0 and min_spaces_after == 1 and max_spaces_after == 1:
        return result

    changes = False
    comma_map = {}
    for key, spaces_before, spaces_after in COMMA_REGEX.findall(original):
        comma_map.setdefault(key, [])
        if max_spaces_before is None and max_spaces_after is None:
            count = SpaceCounts(len(spaces_before), len(spaces_after))
        else:
            count = SpaceCounts(
                min(max_spaces_before, len(spaces_before)),
                max(min_spaces_after, min(max_spaces_after, len(spaces_after))),
            )

        comma_map[key].append(count)
        changes = changes or count != (0, 1)

    if not changes:
        return result

    for key, space_counts in comma_map.items():
        for count_spaces_before, count_spaces_after in space_counts:
            result = sub(
                r"(\"%s\"|'%s'|%s), " % (key, key, key),
                r"\g<1>%s,%s" % (" " * count_spaces_before, " " * count_spaces_after),
                result,
                1,
            )

    return result
