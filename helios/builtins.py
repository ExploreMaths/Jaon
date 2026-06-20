"""Built-in functions and values for the Helios VM."""
from __future__ import annotations

import math
from typing import Any, List

from .errors import HeliosRuntimeError, HeliosTypeError


def helios_print(*args):
    print(*args, end="")


def helios_println(*args):
    print(*args)


def helios_input(prompt: str = "") -> str:
    return input(prompt)


def helios_len(obj: Any) -> int:
    if hasattr(obj, "__len__"):
        return len(obj)
    raise HeliosTypeError(f"Object of type {type(obj).__name__} has no length")


def helios_range(*args) -> List[int]:
    if len(args) == 1:
        return list(range(args[0]))
    if len(args) == 2:
        return list(range(args[0], args[1]))
    if len(args) == 3:
        return list(range(args[0], args[1], args[2]))
    raise HeliosRuntimeError("range expects 1-3 arguments")


def helios_str(obj: Any) -> str:
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, float):
        if obj.is_integer():
            return str(int(obj))
    return str(obj)


def helios_int(obj: Any) -> int:
    if isinstance(obj, int):
        return obj
    if isinstance(obj, float):
        return int(obj)
    if isinstance(obj, str):
        return int(obj)
    raise HeliosTypeError(f"Cannot convert {type(obj).__name__} to Int")


def helios_float(obj: Any) -> float:
    if isinstance(obj, (int, float)):
        return float(obj)
    if isinstance(obj, str):
        return float(obj)
    raise HeliosTypeError(f"Cannot convert {type(obj).__name__} to Float")


def helios_type(obj: Any) -> str:
    from .vm import HeliosInstance, HeliosFunction, HeliosMethod, HeliosClass
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
    if isinstance(obj, HeliosInstance):
        return obj.cls.name
    if isinstance(obj, HeliosClass):
        return "Class"
    if isinstance(obj, (HeliosFunction, HeliosMethod)):
        return "Function"
    return type(obj).__name__


BUILTINS = {
    "print": helios_print,
    "println": helios_println,
    "input": helios_input,
    "len": helios_len,
    "range": helios_range,
    "str": helios_str,
    "int": helios_int,
    "float": helios_float,
    "type": helios_type,
    "math": {
        "pi": math.pi,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "floor": math.floor,
        "ceil": math.ceil,
    },
}
