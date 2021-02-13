"""
hyphens
"""

from re import compile
from typing import Any

from yamllint.rules.hyphens import DEFAULT, ID  # noqa: F401

from yamlfix.rules import new_lines
from yamlfix.rules.new_lines import get_line_break
from yamlfix.rules.types import FormattingResult, FormattingRule

CLEAN_UP_REGEX = compile(r"^ *- +['\"]?(.*?)['\"]? *$")
REPLACEMENT_REGEX = compile(r"^( *- )")


def count_spaces_after_hyphens(text: str, max_spaces_after: int) -> int:
    count = 0
    found = False
    for char in text:
        if max_spaces_after and count == max_spaces_after:
            break

        if char == " ":
            if found:
                count += 1
        elif char == "-":
            if found:
                break

            found = True
        else:
            break

    return count


def apply_before_load(text: str, rule: FormattingRule, rules: dict) -> FormattingResult:
    return FormattingResult(text=text, dumping_config={}, loading_config={},)


def apply_before_dump(data: Any, rule: FormattingRule, text: str, rules: dict) -> Any:
    return data


def apply_on_result(
    result: str, original: str, rule: FormattingRule, rules: dict
) -> str:
    max_spaces_after = DEFAULT.get("max-spaces-after")
    if rule:
        max_spaces_after = rule.get("max-spaces-after", max_spaces_after)
        if max_spaces_after == 1:
            return result
    elif rule is not None:
        max_spaces_after = 0

    changes = False
    hyphen_map = {}
    for line in original.replace("\r\n", "\n").split("\n"):
        match = CLEAN_UP_REGEX.search(line)
        if match:
            content = match.group(1)
            hyphen_map.setdefault(content, [])
            count = count_spaces_after_hyphens(line, max_spaces_after)
            hyphen_map[content].append(count)
            changes = changes or count > 1

    if not changes:
        return result

    fixed_lines = []
    line_break = get_line_break(original, rules.get(new_lines.ID))
    for line in result.replace("\r\n", "\n").split("\n"):
        match = CLEAN_UP_REGEX.search(line)
        if match:
            content = match.group(1)
            counts = hyphen_map.get(content, [])
            if counts and counts[0] > 1:
                fixed_lines.append(
                    REPLACEMENT_REGEX.sub(r"\g<0>" + ((counts.pop(0) - 1) * " "), line)
                )
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return line_break.join(fixed_lines)
