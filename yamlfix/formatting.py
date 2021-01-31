"""
YAML format fixing methods.
"""

from typing import Any, Union, Tuple, List, Optional

from ruamel.yaml import load, dump, RoundTripLoader, RoundTripDumper
from yamllint.config import YamlLintConfig

from yamlfix.rules import RULES

StreamType = Any

StreamTextType = StreamType
VersionType = Union[List[int], str, Tuple[int, int]]


class Loader(RoundTripLoader):
    def __init__(
        self,
        stream: StreamTextType,
        version: Optional[VersionType] = None,
        preserve_quotes: Optional[bool] = None,
        allow_duplicate_keys: bool = True,
    ):
        super().__init__(stream, version=version, preserve_quotes=preserve_quotes)
        self.allow_duplicate_keys = allow_duplicate_keys


def read_and_format_text(
    text: str, config: Optional[YamlLintConfig] = YamlLintConfig("extends: default")
) -> str:
    dumping_config = {}
    rules = config.rules if config else {}
    for rule_id, rule in RULES.items():
        result = rule.apply_before_load(text, rules.get(rule_id))

        text = result.text
        dumping_config.update(result.dumping_config)

    data = load(text, Loader)

    for rule_id, rule in RULES.items():
        data = rule.apply_before_dump(data, rules.get(rule_id), text, rules)

    result = dump(data, Dumper=RoundTripDumper, **dumping_config)

    for rule_id, rule in RULES.items():
        result = rule.apply_on_result(result, text, rules.get(rule_id))

    return result
