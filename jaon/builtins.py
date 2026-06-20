"""Built-in functions and values for the Jaon VM."""
from __future__ import annotations

import math
from typing import Any, List

from .errors import JaonRuntimeError, JaonTypeError


def jaon_print(*args):
    print(*args, end="")


def jaon_println(*args):
    print(*args)


def jaon_input(prompt: str = "") -> str:
    return input(prompt)


def jaon_len(obj: Any) -> int:
    if hasattr(obj, "__len__"):
        return len(obj)
    raise JaonTypeError(f"Object of type {type(obj).__name__} has no length")


def jaon_range(*args) -> List[int]:
    if len(args) == 1:
        return list(range(args[0]))
    if len(args) == 2:
        return list(range(args[0], args[1]))
    if len(args) == 3:
        return list(range(args[0], args[1], args[2]))
    raise JaonRuntimeError("range expects 1-3 arguments")


def jaon_str(obj: Any) -> str:
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, float):
        if obj.is_integer():
            return str(int(obj))
    return str(obj)


def jaon_int(obj: Any) -> int:
    if isinstance(obj, int):
        return obj
    if isinstance(obj, float):
        return int(obj)
    if isinstance(obj, str):
        return int(obj)
    raise JaonTypeError(f"Cannot convert {type(obj).__name__} to Int")


def jaon_float(obj: Any) -> float:
    if isinstance(obj, (int, float)):
        return float(obj)
    if isinstance(obj, str):
        return float(obj)
    raise JaonTypeError(f"Cannot convert {type(obj).__name__} to Float")


def jaon_type(obj: Any) -> str:
    from .vm import JaonInstance, JaonFunction, JaonMethod, JaonClass
    if obj is None:
        return "Null"
    if isinstance(obj, bool):
        return "Bool"
    if isinstance(obj, int):
        return "Int"
    if isinstance(obj, float):
        return "Float"
    if isinstance(obj, str):
        return "String"
    if isinstance(obj, list):
        return "List"
    if isinstance(obj, dict):
        return "Dict"
    if isinstance(obj, JaonInstance):
        return obj.cls.name
    if isinstance(obj, JaonClass):
        return "Class"
    if isinstance(obj, (JaonFunction, JaonMethod)):
        return "Function"
    return type(obj).__name__


BUILTINS = {
    "print": jaon_print,
    "println": jaon_println,
    "input": jaon_input,
    "len": jaon_len,
    "range": jaon_range,
    "str": jaon_str,
    "int": jaon_int,
    "float": jaon_float,
    "type": jaon_type,
    "math": {
        "pi": math.pi,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "floor": math.floor,
        "ceil": math.ceil,
    },
}
