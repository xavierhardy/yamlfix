from typing import Union, Dict, NamedTuple

FormattingRule = Union[None, Dict, bool]
FormattingResult = NamedTuple(
    "FormattingResult", [("text", str), ("dumping_config", dict)]
)
