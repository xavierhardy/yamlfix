"""
trailing-spaces
"""

from typing import Any

from yamlfix.rules import new_lines
from yamllint.rules.trailing_spaces import ID  # noqa: F401

from yamlfix.rules.new_lines import get_line_break
from yamlfix.rules.types import FormattingResult, FormattingRule


def count_trailing_spaces(text: str) -> int:
    count = 0
    for char in reversed(text):
        if char == " ":
            count += 1
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
    if rule:
        return result

    changes = False
    trailing_space_map = {}
    for line in original.replace("\r\n", "\n").split("\n"):
        content = line.strip()
        trailing_space_map.setdefault(content, [])
        count = count_trailing_spaces(line)
        trailing_space_map[content].append(count)
        changes = changes or count > 0

    if not changes:
        return result

    fixed_lines = []
    line_break = get_line_break(original, rules.get(new_lines.ID))
    for line in result.replace("\r\n", "\n").split("\n"):
        content = line.strip()
        counts = trailing_space_map.get(content, [])
        if counts and counts[0] > 0:
            fixed_lines.append(line + (counts.pop(0) * " "))
        else:
            fixed_lines.append(line)

    return line_break.join(fixed_lines)
