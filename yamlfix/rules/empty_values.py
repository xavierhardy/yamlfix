"""
empty-values
"""

from typing import Any

from ruamel.yaml import add_representer, RoundTripDumper
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from yamllint.rules.empty_values import DEFAULT, ID  # noqa: F401

from yamlfix.rules.types import FormattingResult, FormattingRule

NULL_TAG = "tag:yaml.org,2002:null"
NULL_TXT = "null"


class Null:
    pass


class EmptyNull:
    pass


def represent_null(self, data: Any) -> Any:
    return self.represent_scalar(NULL_TAG, NULL_TXT)


def represent_empty_null(self, data: Any) -> Any:
    if len(self.represented_objects) == 0 and not self.serializer.use_explicit_start:
        # this will be open ended (although it is not yet)
        return self.represent_scalar(NULL_TAG, NULL_TXT)
    return self.represent_scalar(NULL_TAG, "")


def replace_empty_values(
    data: Any, forbid_block_map: bool, forbid_flow_map: bool
) -> Any:
    if isinstance(data, (CommentedMap, CommentedSeq)):
        # it won't work with items() or iterating through it like list
        if isinstance(data, CommentedMap):
            for key in data.keys():
                is_null = data[key] is None
                is_flow = data.fa.flow_style()
                if is_null:
                    if (is_flow and forbid_flow_map) or (
                        not is_flow and forbid_block_map
                    ):
                        data[key] = Null()
                    elif (is_flow and not forbid_flow_map) or (
                        not is_flow and not forbid_block_map
                    ):
                        data[key] = EmptyNull()
                else:
                    replace_empty_values(data[key], forbid_block_map, forbid_flow_map)
        else:
            for indx in range(len(data)):
                replace_empty_values(data[indx], forbid_block_map, forbid_flow_map)
    return data


def apply_before_load(text: str, rule: FormattingRule) -> FormattingResult:
    return FormattingResult(text=text, dumping_config={}, loading_config={})


# TODO: support not modifying existing format if rule is disabled
def apply_before_dump(data: Any, rule: FormattingRule, text: str, rules: dict) -> Any:
    forbid_in_block_mappings = DEFAULT.get("forbid-in-block-mappings")
    forbid_in_flow_mappings = DEFAULT.get("forbid-in-flow-mappings")
    if rule is not None:
        forbid_in_block_mappings = rule and rule.get(
            "forbid-in-block-mappings", forbid_in_block_mappings
        )
        forbid_in_flow_mappings = rule and rule.get(
            "forbid-in-flow-mappings", forbid_in_flow_mappings
        )

    if (rule is None or rule) and (
        forbid_in_block_mappings and forbid_in_flow_mappings
    ):
        # no need to go through all of them
        # just represent them as `null`
        add_representer(type(None), represent_null, Dumper=RoundTripDumper)

        return data
    elif (rule is not None and not rule) or (
        not forbid_in_flow_mappings and not forbid_in_block_mappings
    ):
        # no need to go through all of them
        # just represent them as ``
        add_representer(type(None), represent_empty_null, Dumper=RoundTripDumper)

        return data

    add_representer(Null, represent_null, Dumper=RoundTripDumper)
    add_representer(EmptyNull, represent_empty_null, Dumper=RoundTripDumper)

    return replace_empty_values(data, forbid_in_block_mappings, forbid_in_flow_mappings)


def apply_on_result(result: str, original: str, rule: FormattingRule) -> str:
    return result.replace("!!null ''", "")
