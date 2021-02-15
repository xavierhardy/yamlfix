"""
colons
"""

from re import compile, sub
from typing import Any, NamedTuple

from yamllint.rules.colons import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule

SpaceCounts = NamedTuple("SpaceCounts", (("before", int), ("after", int)))

COLON_REGEX = compile(r"(['\"].*?['\"]|[^: \n\r]+)( *):( *)(.|[\r\n])")


def apply_before_load(text: str, rule: FormattingRule, rules: dict) -> FormattingResult:
    return FormattingResult(text=text, dumping_config={}, loading_config={},)


def apply_before_dump(data: Any, rule: FormattingRule, text: str, rules: dict) -> Any:
    return data


def apply_on_result(
    result: str, original: str, rule: FormattingRule, rules: dict
) -> str:
    max_spaces_before = DEFAULT.get("max-spaces-before")
    max_spaces_after = DEFAULT.get("max-spaces-after")
    if rule:
        max_spaces_before = rule.get("max-spaces-before", max_spaces_before)
        max_spaces_after = rule.get("max-spaces-after", max_spaces_after)
    elif rule is not None:
        max_spaces_before = None
        max_spaces_after = None

    if max_spaces_before == 0 and max_spaces_after == 1:
        return result

    changes = False
    colon_map = {}

    for key, spaces_before, spaces_after, char_after in COLON_REGEX.findall(original):
        colon_map.setdefault(key, [])
        if max_spaces_before is None and max_spaces_after is None:
            count = SpaceCounts(len(spaces_before), len(spaces_after))
        else:
            count = SpaceCounts(
                min(max_spaces_before, len(spaces_before)),
                min(max_spaces_after, len(spaces_after)),
            )
        colon_map[key].append(count)
        if count[0] != 0 or count[1] > 1:
            changes = True
        else:
            has_line_break = char_after in ("\r", "\n")
            count_spaces_after = count[1]
            changes = (
                changes
                or (has_line_break and count_spaces_after != 0)
                or (not has_line_break and count_spaces_after != 1)
            )

    if not changes:
        return result

    for key, space_counts in colon_map.items():
        for count_spaces_before, count_spaces_after in space_counts:
            result = sub(
                r"(%s): ?([\r\n])?" % key,
                r"\g<1>%s:%s\g<2>"
                % (" " * count_spaces_before, " " * count_spaces_after),
                result,
                1,
            )

    return result
