"""Stack-based virtual machine for the Helios language."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .bytecode import OpCode, CodeObject, ClassObject
from .builtins import BUILTINS
from .errors import HeliosRuntimeError, HeliosTypeError, HeliosIndexError, HeliosAttributeError, HeliosNameError


class HeliosFunction:
    def __init__(self, code: CodeObject, name: str = "", param_count: int = 0):
        self.code = code
        self.name = name or code.name
        self.param_count = param_count

    def __repr__(self) -> str:
        return f"<function {self.name}>"


class HeliosMethod:
    def __init__(self, instance: "HeliosInstance", func: HeliosFunction):
        self.instance = instance
        self.func = func

    def __repr__(self) -> str:
        return f"<method {self.func.name} of {self.instance}>"


class HeliosClass:
    def __init__(self, class_obj: ClassObject, methods: Dict[str, HeliosFunction]):
        self.name = class_obj.name
        self.base_name = class_obj.base
        self.base_class: Optional[HeliosClass] = None
        self.methods = methods
        self.fields = class_obj.fields

    def find_method(self, name: str) -> Optional[HeliosFunction]:
        if name in self.methods:
            return self.methods[name]
        if self.base_class:
            return self.base_class.find_method(name)
        return None

    def __repr__(self) -> str:
        return f"<class {self.name}>"


class HeliosInstance:
    def __init__(self, cls: HeliosClass):
        self.cls = cls
        self.fields: Dict[str, Any] = {}

    def get(self, name: str) -> Any:
        if name in self.fields:
            return self.fields[name]
        method = self.cls.find_method(name)
        if method:
            return HeliosMethod(self, method)
        raise HeliosAttributeError(f"'{self.cls.name}' object has no attribute '{name}'")

    def set(self, name: str, value: Any) -> None:
        self.fields[name] = value

    def __repr__(self) -> str:
        return f"<{self.cls.name} instance>"


class CallFrame:
    def __init__(self, code: CodeObject, locals: List[Any], return_addr: int = -1):
        self.code = code
        self.locals = locals
        self.ip = 0
        self.return_addr = return_addr
        self.try_blocks: List[tuple] = []  # (catch_offset, finally_offset, stack_depth)
        self.loop_blocks: List[tuple] = []  # (break_offset, continue_offset, stack_depth)


class VM:
    def __init__(self):
        self.stack: List[Any] = []
        self.frames: List[CallFrame] = []
        self.globals: Dict[str, Any] = dict(BUILTINS)
        self.classes: Dict[str, HeliosClass] = {}

    def reset(self) -> None:
        self.stack.clear()
        self.frames.clear()
        self.globals = dict(BUILTINS)
        self.classes.clear()

    def run(self, module_code: CodeObject) -> Any:
        self.reset()
        self._install_module(module_code)
        frame = CallFrame(module_code, [None] * len(module_code.locals))
        self.frames.append(frame)
        return self._execute()

    def _install_module(self, module_code: CodeObject) -> None:
        # Build classes first so methods can reference each other.
        for const in module_code.constants:
            if isinstance(const, ClassObject):
                self._build_class(const, module_code)

    def _build_class(self, class_obj: ClassObject, module_code: CodeObject) -> None:
        methods: Dict[str, HeliosFunction] = {}
        for name, code in class_obj.methods.items():
            methods[name] = HeliosFunction(code, code.name, code.param_count)
        cls = HeliosClass(class_obj, methods)
        self.classes[class_obj.name] = cls

    def _execute(self) -> Any:
        while self.frames:
            frame = self.frames[-1]
            code = frame.code

            while frame.ip < len(code.instructions):
                instr = code.instructions[frame.ip]
                frame.ip += 1
                op = instr.opcode
                arg = instr.arg

                if op == OpCode.LOAD_CONST:
                    self.stack.append(code.constants[arg])

                elif op == OpCode.LOAD_NAME:
                    name = arg
                    if name in self.globals:
                        self.stack.append(self.globals[name])
                    elif name in self.classes:
                        self.stack.append(self.classes[name])
                    else:
                        raise HeliosNameError(f"Name '{name}' is not defined")

                elif op == OpCode.STORE_NAME:
                    name = arg
                    value = self.stack.pop()
                    self.globals[name] = value

                elif op == OpCode.LOAD_GLOBAL:
                    name = arg
                    if name not in self.globals:
                        raise HeliosNameError(f"Global '{name}' is not defined")
                    self.stack.append(self.globals[name])

                elif op == OpCode.STORE_GLOBAL:
                    name = arg
                    self.globals[name] = self.stack.pop()

                elif op == OpCode.LOAD_FAST:
                    self.stack.append(frame.locals[arg])

                elif op == OpCode.STORE_FAST:
                    frame.locals[arg] = self.stack.pop()

                elif op == OpCode.POP:
                    self.stack.pop()

                elif op == OpCode.DUP:
                    self.stack.append(self.stack[-1])

                elif op == OpCode.ROT_TWO:
                    a, b = self.stack.pop(), self.stack.pop()
                    self.stack.append(a)
                    self.stack.append(b)

                elif op == OpCode.LOAD_ATTR:
                    obj = self.stack.pop()
                    name = arg
                    if isinstance(obj, HeliosInstance):
                        self.stack.append(obj.get(name))
                    elif isinstance(obj, dict):
                        if name not in obj:
                            raise HeliosAttributeError(f"Dict has no key '{name}'")
                        self.stack.append(obj[name])
                    elif isinstance(obj, str):
                        self.stack.append(self._string_method(obj, name))
                    elif isinstance(obj, list):
                        self.stack.append(self._list_method(obj, name))
                    else:
                        raise HeliosTypeError(f"Cannot access attribute '{name}' on {type(obj).__name__}")

                elif op == OpCode.STORE_ATTR:
                    value = self.stack.pop()
                    obj = self.stack.pop()
                    name = arg
                    if isinstance(obj, HeliosInstance):
                        obj.set(name, value)
                    elif isinstance(obj, dict):
                        obj[name] = value
                    else:
                        raise HeliosTypeError(f"Cannot set attribute '{name}' on {type(obj).__name__}")
                    self.stack.append(value)

                elif op == OpCode.LOAD_INDEX:
                    index = self.stack.pop()
                    obj = self.stack.pop()
                    if isinstance(obj, list):
                        if not isinstance(index, int):
                            raise HeliosTypeError("List index must be integer")
                        if index < 0 or index >= len(obj):
                            raise HeliosIndexError("List index out of range")
                        self.stack.append(obj[index])
                    elif isinstance(obj, dict):
                        if index not in obj:
                            raise HeliosIndexError(f"Key {index} not found")
                        self.stack.append(obj[index])
                    elif isinstance(obj, str):
                        if not isinstance(index, int):
                            raise HeliosTypeError("String index must be integer")
                        if index < 0 or index >= len(obj):
                            raise HeliosIndexError("String index out of range")
                        self.stack.append(obj[index])
                    else:
                        raise HeliosTypeError(f"Cannot index {type(obj).__name__}")

                elif op == OpCode.STORE_INDEX:
                    value = self.stack.pop()
                    index = self.stack.pop()
                    obj = self.stack.pop()
                    if isinstance(obj, list):
                        if not isinstance(index, int):
                            raise HeliosTypeError("List index must be integer")
                        if index < 0 or index >= len(obj):
                            raise HeliosIndexError("List index out of range")
                        obj[index] = value
                    elif isinstance(obj, dict):
                        obj[index] = value
                    else:
                        raise HeliosTypeError(f"Cannot index {type(obj).__name__}")
                    self.stack.append(value)

                elif op == OpCode.BUILD_LIST:
                    items = []
                    for _ in range(arg):
                        items.append(self.stack.pop())
                    items.reverse()
                    self.stack.append(items)

                elif op == OpCode.BUILD_DICT:
                    d = {}
                    for _ in range(arg):
                        value = self.stack.pop()
                        key = self.stack.pop()
                        d[key] = value
                    self.stack.append(d)

                elif op == OpCode.GET_ITER:
                    obj = self.stack.pop()
                    self.stack.append(iter(obj))

                elif op == OpCode.FOR_ITER:
                    iterator = self.stack[-1]
                    try:
                        value = next(iterator)
                        self.stack.append(value)
                    except StopIteration:
                        self.stack.pop()
                        frame.ip += arg - 1

                elif op == OpCode.BINARY_OP:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(self._binary_op(arg, left, right))

                elif op == OpCode.UNARY_OP:
                    operand = self.stack.pop()
                    self.stack.append(self._unary_op(arg, operand))

                elif op == OpCode.COMPARE_OP:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(self._compare_op(arg, left, right))

                elif op == OpCode.JUMP:
                    frame.ip += arg - 1

                elif op == OpCode.JUMP_IF_FALSE:
                    value = self.stack.pop()
                    if not self._truthy(value):
                        frame.ip += arg - 1

                elif op == OpCode.JUMP_IF_TRUE:
                    value = self.stack.pop()
                    if self._truthy(value):
                        frame.ip += arg - 1

                elif op == OpCode.CALL:
                    arg_count = arg
                    args = []
                    for _ in range(arg_count):
                        args.append(self.stack.pop())
                    args.reverse()
                    callee = self.stack.pop()
                    self._call(callee, args)
                    break  # Let the new frame execute

                elif op == OpCode.CALL_METHOD:
                    arg_count = arg
                    args = []
                    for _ in range(arg_count):
                        args.append(self.stack.pop())
                    args.reverse()
                    method = self.stack.pop()
                    self.stack.pop()  # pop receiver (bound into method)
                    self._call(method, args)
                    break

                elif op == OpCode.MAKE_FUNCTION:
                    _, name, param_count = arg
                    code_obj = code.constants[arg[0]]
                    func = HeliosFunction(code_obj, name, param_count)
                    self.stack.append(func)

                elif op == OpCode.RETURN:
                    self.frames.pop()
                    if not self.frames:
                        return None
                    # Continue in caller
                    break

                elif op == OpCode.RETURN_VALUE:
                    value = self.stack.pop()
                    self.frames.pop()
                    if not self.frames:
                        return value
                    self.stack.append(value)
                    break

                elif op == OpCode.LOAD_THIS:
                    self.stack.append(frame.locals[0])

                elif op == OpCode.STORE_THIS:
                    frame.locals[0] = self.stack.pop()

                elif op == OpCode.NEW_OBJECT:
                    class_name = arg
                    cls = self.classes.get(class_name)
                    if cls is None:
                        raise HeliosRuntimeError(f"Unknown class '{class_name}'")
                    ctor_method = cls.find_method("constructor")
                    expected_args = ctor_method.param_count - 1 if ctor_method else 0
                    # Stack order is [class, arg1, arg2, ...]
                    args = []
                    for _ in range(expected_args):
                        args.append(self.stack.pop())
                    args.reverse()
                    self.stack.pop()  # pop class
                    instance = HeliosInstance(cls)
                    # Initialize fields to null
                    for name in cls.fields:
                        instance.fields[name] = None
                    if ctor_method:
                        self._call(HeliosMethod(instance, ctor_method), args)
                        break
                    else:
                        self.stack.append(instance)

                elif op == OpCode.BUILD_CLASS:
                    name, base_name, _ = arg
                    cls_obj = self.stack.pop()
                    methods = {}
                    for mname, mcode in cls_obj.methods.items():
                        methods[mname] = HeliosFunction(mcode, mcode.name, mcode.param_count)
                    cls = HeliosClass(cls_obj, methods)
                    if base_name and base_name in self.classes:
                        cls.base_class = self.classes[base_name]
                    self.classes[name] = cls
                    self.stack.append(cls)

                elif op == OpCode.LOAD_METHOD:
                    name = arg
                    obj = self.stack[-1]
                    if isinstance(obj, HeliosInstance):
                        method = obj.cls.find_method(name)
                        if method is None:
                            raise HeliosAttributeError(f"'{obj.cls.name}' has no method '{name}'")
                        self.stack.append(HeliosMethod(obj, method))
                    else:
                        raise HeliosTypeError(f"Cannot load method '{name}' on {type(obj).__name__}")

                elif op == OpCode.TRY_BEGIN:
                    catch_offset, finally_offset = arg
                    frame.try_blocks.append((
                        frame.ip + catch_offset - 1,
                        frame.ip + finally_offset - 1,
                        len(self.stack),
                    ))

                elif op == OpCode.TRY_END:
                    if frame.try_blocks:
                        frame.try_blocks.pop()

                elif op == OpCode.THROW:
                    value = self.stack.pop()
                    self._handle_exception(frame, value)
                    break

                elif op == OpCode.SETUP_LOOP:
                    break_offset, continue_offset = arg
                    frame.loop_blocks.append((
                        frame.ip + break_offset - 1,
                        frame.ip + continue_offset - 1,
                        len(self.stack),
                    ))

                elif op == OpCode.POP_BLOCK:
                    if frame.loop_blocks:
                        frame.loop_blocks.pop()

                elif op == OpCode.BREAK_LOOP:
                    if not frame.loop_blocks:
                        raise HeliosRuntimeError("break outside loop")
                    target, _, depth = frame.loop_blocks[-1]
                    while len(self.stack) > depth:
                        self.stack.pop()
                    frame.ip = target

                elif op == OpCode.CONTINUE_LOOP:
                    if not frame.loop_blocks:
                        raise HeliosRuntimeError("continue outside loop")
                    _, target, depth = frame.loop_blocks[-1]
                    while len(self.stack) > depth:
                        self.stack.pop()
                    frame.ip = target

                else:
                    raise HeliosRuntimeError(f"Unknown opcode {op}")

            else:
                # Frame finished naturally
                self.frames.pop()
                if not self.frames:
                    return None

        return None

    def _call(self, callee: Any, args: List[Any]) -> None:
        if isinstance(callee, HeliosFunction):
            if len(args) != callee.param_count:
                raise HeliosTypeError(
                    f"{callee.name} expects {callee.param_count} arguments, got {len(args)}"
                )
            locals_list = [None] * len(callee.code.locals)
            for i, arg in enumerate(args):
                locals_list[i] = arg
            self.frames.append(CallFrame(callee.code, locals_list))
        elif isinstance(callee, HeliosMethod):
            func = callee.func
            if len(args) + 1 != func.param_count:
                raise HeliosTypeError(
                    f"{func.name} expects {func.param_count} arguments, got {len(args) + 1}"
                )
            locals_list = [None] * len(func.code.locals)
            locals_list[0] = callee.instance
            for i, arg in enumerate(args):
                locals_list[i + 1] = arg
            self.frames.append(CallFrame(func.code, locals_list))
        elif callable(callee):
            result = callee(*args)
            self.stack.append(result)
        else:
            raise HeliosTypeError(f"Cannot call {type(callee).__name__}")

    def _handle_exception(self, frame: CallFrame, value: Any) -> None:
        while self.frames:
            frame = self.frames[-1]
            while frame.try_blocks:
                catch_ip, finally_ip, depth = frame.try_blocks.pop()
                while len(self.stack) > depth:
                    self.stack.pop()
                self.stack.append(value)
                frame.ip = catch_ip
                return
            self.frames.pop()
        raise HeliosRuntimeError(f"Uncaught exception: {value}")

    def _binary_op(self, op: str, left: Any, right: Any) -> Any:
        if op == "+":
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            return left / right
        if op == "%":
            return left % right
        raise HeliosRuntimeError(f"Unknown binary operator {op}")

    def _unary_op(self, op: str, operand: Any) -> Any:
        if op == "-":
            return -operand
        if op == "not":
            return not self._truthy(operand)
        raise HeliosRuntimeError(f"Unknown unary operator {op}")

    def _compare_op(self, op: str, left: Any, right: Any) -> bool:
        if op == "==":
            return left == right
        if op == "!=":
            return left != right
        if op == "<":
            return left < right
        if op == ">":
            return left > right
        if op == "<=":
            return left <= right
        if op == ">=":
            return left >= right
        raise HeliosRuntimeError(f"Unknown comparison operator {op}")

    def _truthy(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, (str, list, dict)):
            return len(value) > 0
        return True

    def _string_method(self, s: str, name: str) -> Any:
        methods = {
            "length": lambda: len(s),
            "split": lambda: s.split(),
            "contains": lambda substr: substr in s,
            "upper": lambda: s.upper(),
            "lower": lambda: s.lower(),
        }
        if name in methods:
            return methods[name]
        raise HeliosAttributeError(f"String has no method '{name}'")

    def _list_method(self, lst: list, name: str) -> Any:
        methods = {
            "length": lambda: len(lst),
            "append": lambda x: lst.append(x),
            "pop": lambda: lst.pop(),
            "contains": lambda x: x in lst,
        }
        if name in methods:
            return methods[name]
        raise HeliosAttributeError(f"List has no method '{name}'")


def execute(module_code: CodeObject) -> Any:
    return VM().run(module_code)
