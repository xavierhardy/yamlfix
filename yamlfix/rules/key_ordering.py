"""
key-ordering
"""

from typing import Any, Tuple

from ruamel.yaml.comments import CommentedMap, CommentedSeq
from yamllint.rules.key_ordering import ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule


def fix_key_ordering(data: Any) -> Tuple[bool, Any]:
    has_changes = False
    if isinstance(data, CommentedMap):
        keys = list(data.keys())

        ordered_keys = sorted(keys)
        if ordered_keys == keys:
            for key in keys:
                change, new_value = fix_key_ordering(data[key])
                if change:
                    has_changes = True
                    data[key] = new_value
        else:
            new_data = CommentedMap()
            new_data.anchor.value = data.anchor.value
            new_data.anchor.always_dump = data.anchor.always_dump
            new_data.ca.items.update(data.ca.items)
            new_data.ca.end = data.ca.end
            new_data.ca.comment = data.ca.comment
            new_data.lc.col = data.lc.col
            new_data.lc.line = data.lc.line
            new_data.merge.extend(data.merge)
            new_data.tag.value = data.tag.value

            for key in ordered_keys:
                _, new_data[key] = fix_key_ordering(data[key])

            return True, new_data
    elif isinstance(data, CommentedSeq):
        # it won't work with items() or iterating through it like list
        for indx in range(len(data)):
            change, new_value = fix_key_ordering(data[indx])
            if change:
                has_changes = change
                data[indx] = new_value

    return has_changes, data


def apply_before_load(text: str, rule: FormattingRule) -> FormattingResult:
    return FormattingResult(text=text, dumping_config={})


def apply_before_dump(data: Any, rule: FormattingRule, text: str, rules: dict) -> Any:
    if not rule:
        return data

    return fix_key_ordering(data)[1]


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    return result
