from typing import Any, Sequence

from rrtarget import Api, serialize_arbitrary_to_str



def snake_case_to_lower_camel_case(key: str) -> str:
    split = key.split("_")
    if len(split) > 1:
        key = split[0] + "".join(
            [val.title() for val in split[1:]]
        )
    return key


def pi_default_formatter(key: str, val: Any) -> str:
    return (
        f"{snake_case_to_lower_camel_case(key)}={serialize_arbitrary_to_str(val)}"
    )


def multi_inst_formatter(key: str, val: Sequence[str]) -> str:
    ret = ""
    for i, val in enumerate(val):
        if i > 0:
            ret += "&"
        ret += f"{snake_case_to_lower_camel_case(key)}={val}"
    return ret


def semi_col_formatter(key: str, val: Sequence[str]) -> str:
    return (
        f"{snake_case_to_lower_camel_case(key)}={';'.join(val)}"
    )


api = Api('/piwebapi', default_formatter=pi_default_formatter)