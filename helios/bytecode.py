"""Bytecode definitions for the Helios VM."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, List


class OpCode(Enum):
    # Stack manipulation
    LOAD_CONST = auto()      # arg: constant index
    LOAD_NAME = auto()       # arg: variable name
    STORE_NAME = auto()      # arg: variable name
    LOAD_GLOBAL = auto()     # arg: global name
    STORE_GLOBAL = auto()    # arg: global name
    LOAD_FAST = auto()       # arg: local index
    STORE_FAST = auto()      # arg: local index
    LOAD_UPVALUE = auto()    # arg: upvalue index
    STORE_UPVALUE = auto()   # arg: upvalue index
    CLOSE_UPVALUE = auto()   # arg: local index
    POP = auto()
    DUP = auto()
    ROT_TWO = auto()

    # Attributes / indexing
    LOAD_ATTR = auto()       # arg: attribute name
    STORE_ATTR = auto()      # arg: attribute name
    LOAD_INDEX = auto()
    STORE_INDEX = auto()

    # Collections
    BUILD_LIST = auto()      # arg: element count
    BUILD_DICT = auto()      # arg: entry count
    GET_ITER = auto()
    FOR_ITER = auto()        # arg: jump offset

    # Arithmetic / logic
    BINARY_OP = auto()       # arg: operator string
    UNARY_OP = auto()        # arg: operator string
    COMPARE_OP = auto()      # arg: operator string

    # Control flow
    JUMP = auto()            # arg: jump offset
    JUMP_IF_FALSE = auto()   # arg: jump offset
    JUMP_IF_TRUE = auto()    # arg: jump offset

    # Functions
    CALL = auto()            # arg: argument count
    RETURN = auto()
    RETURN_VALUE = auto()
    MAKE_FUNCTION = auto()   # arg: (code_idx, name, param_count)
    MAKE_CLOSURE = auto()    # arg: (code_idx, name, param_count, upvalue_count)

    # Classes / objects
    LOAD_THIS = auto()
    STORE_THIS = auto()
    NEW_OBJECT = auto()      # arg: class name
    BUILD_CLASS = auto()     # arg: (name, base_name, method_count)
    LOAD_METHOD = auto()     # arg: method name
    CALL_METHOD = auto()     # arg: argument count

    # Exceptions
    TRY_BEGIN = auto()       # arg: (catch_offset, finally_offset)
    TRY_END = auto()
    THROW = auto()

    # Loops
    SETUP_LOOP = auto()      # arg: (break_offset, continue_offset)
    POP_BLOCK = auto()
    BREAK_LOOP = auto()
    CONTINUE_LOOP = auto()


@dataclass
class Instruction:
    opcode: OpCode
    arg: Any = None
    line: int = 0

    def __repr__(self) -> str:
        arg_str = f" {self.arg}" if self.arg is not None else ""
        return f"{self.opcode.name}{arg_str}"


@dataclass
class CodeObject:
    name: str
    param_count: int
    instructions: List[Instruction] = field(default_factory=list)
    constants: List[Any] = field(default_factory=list)
    locals: List[str] = field(default_factory=list)
    upvalues: List[tuple] = field(default_factory=list)

    def add_const(self, value: Any) -> int:
        if value in self.constants:
            return self.constants.index(value)
        self.constants.append(value)
        return len(self.constants) - 1

    def emit(self, opcode: OpCode, arg: Any = None, line: int = 0) -> None:
        self.instructions.append(Instruction(opcode, arg, line))


@dataclass
class ClassObject:
    name: str
    base: str
    methods: dict
    fields: dict
