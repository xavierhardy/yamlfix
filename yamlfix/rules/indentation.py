"""
indentation
"""

from typing import Any

from yamllint.rules.indentation import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule


def find_first_indent(text):
    for line in text.splitlines():
        if not line.startswith(" "):
            continue

        indent = 0
        for c in line:
            if c == "#":
                break

            if c != " ":
                return indent

            indent += 1


def apply_before_load(text: str, rule: FormattingRule) -> FormattingResult:
    indent = DEFAULT.get("spaces")
    block_seq_indent = DEFAULT.get("indent-sequences")
    if rule is not None:
        if not rule:
            indent = "consistent"
            block_seq_indent = True
        else:
            indent = rule.get("spaces", indent)
            block_seq_indent = rule.get("indent-sequences", block_seq_indent)

    if indent == "consistent":
        indent = find_first_indent(text) or 2

    if block_seq_indent:
        if indent:
            block_seq_indent = indent
        else:
            block_seq_indent = 2
    else:
        block_seq_indent = None

    return FormattingResult(
        text=text,
        dumping_config={"block_seq_indent": block_seq_indent, "indent": indent},
    )


def apply_before_dump(data: Any, rule: FormattingRule, text: str, rules: dict) -> Any:
    return data


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    return result
