"""Semantic analyzer / type checker for Helios."""
from __future__ import annotations

from typing import Dict, List, Optional

from . import ast_nodes as ast
from .errors import HeliosTypeError


class Type:
    def __init__(self, name: str, params: Optional[List[Type]] = None, base: Optional[Type] = None):
        self.name = name
        self.params = params or []
        self.base = base

    def __str__(self) -> str:
        if self.params:
            return f"{self.name}<{', '.join(str(p) for p in self.params)}>"
        return self.name

    def __eq__(self, other) -> bool:
        if not isinstance(other, Type):
            return False
        return self.name == other.name and self.params == other.params

    def is_subtype_of(self, other: Type) -> bool:
        if self == other:
            return True
        if self.name == "Any" or other.name == "Any":
            return True
        if self.name == "Int" and other.name == "Float":
            return True
        if self.name == other.name and not other.params:
            return True
        if self.base is not None:
            return self.base.is_subtype_of(other)
        return False

    def is_numeric(self) -> bool:
        return self.name in ("Int", "Float")


class FunctionType(Type):
    def __init__(self, param_types: List[Type], return_type: Type):
        super().__init__("Fun")
        self.param_types = param_types
        self.return_type = return_type

    def __str__(self) -> str:
        params = ", ".join(str(p) for p in self.param_types)
        return f"({params}) -> {self.return_type}"

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, FunctionType)
            and self.param_types == other.param_types
            and self.return_type == other.return_type
        )


VOID = Type("Void")
ANY = Type("Any")
INT = Type("Int")
FLOAT = Type("Float")
BOOL = Type("Bool")
STRING = Type("String")
NULL = Type("Null")
LIST = Type("List")
DICT = Type("Dict")


BUILTIN_TYPES = {
    "Int": INT,
    "Float": FLOAT,
    "Bool": BOOL,
    "String": STRING,
    "Any": ANY,
    "Void": VOID,
    "List": LIST,
    "Dict": DICT,
}


class Symbol:
    def __init__(self, name: str, sym_type: Type, mutable: bool = True):
        self.name = name
        self.type = sym_type
        self.mutable = mutable


class Scope:
    def __init__(self, parent: Optional[Scope] = None):
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}

    def define(self, name: str, sym_type: Type, mutable: bool = True) -> None:
        self.symbols[name] = Symbol(name, sym_type, mutable)

    def resolve(self, name: str) -> Optional[Symbol]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.resolve(name)
        return None


class ClassInfo:
    def __init__(self, name: str, base: Optional[str], fields: Dict[str, Type], methods: Dict[str, FunctionType]):
        self.name = name
        self.base = base
        self.fields = fields
        self.methods = methods


class Analyzer:
    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.current_function_return: Optional[Type] = None
        self.in_loop = False
        self.classes: Dict[str, ClassInfo] = {}
        self._init_builtins()

    def _init_builtins(self) -> None:
        for name, t in BUILTIN_TYPES.items():
            self.global_scope.define(name, t)
        # Built-in functions
        self.global_scope.define("print", FunctionType([ANY], VOID))
        self.global_scope.define("println", FunctionType([ANY], VOID))
        self.global_scope.define("input", FunctionType([], STRING))
        self.global_scope.define("len", FunctionType([ANY], INT))
        self.global_scope.define("range", FunctionType([INT], LIST))
        self.global_scope.define("str", FunctionType([ANY], STRING))
        self.global_scope.define("int", FunctionType([ANY], INT))
        self.global_scope.define("float", FunctionType([ANY], FLOAT))
        self.global_scope.define("type", FunctionType([ANY], STRING))

    def error(self, message: str) -> None:
        raise HeliosTypeError(message)

    def resolve_type(self, node: ast.TypeNode) -> Type:
        name = node.name
        if name in self.classes:
            return Type(name, base=Type(self.classes[name].base) if self.classes[name].base else None)
        if name in BUILTIN_TYPES:
            t = BUILTIN_TYPES[name]
            if node.params:
                resolved_params = [self.resolve_type(p) for p in node.params]
                return Type(name, resolved_params)
            return t
        self.error(f"Unknown type '{name}'")

    def analyze(self, program: ast.Program) -> None:
        # First pass: register class skeletons and function signatures
        for stmt in program.statements:
            if isinstance(stmt, ast.ClassDef):
                self.register_class(stmt)
            elif isinstance(stmt, ast.FunctionDef):
                self.register_function(stmt)

        # Second pass: analyze bodies
        for stmt in program.statements:
            self.analyze_statement(stmt)

    def register_class(self, node: ast.ClassDef) -> None:
        fields: Dict[str, Type] = {}
        methods: Dict[str, FunctionType] = {}
        base_type: Optional[Type] = None
        if node.base:
            if node.base not in self.classes:
                self.error(f"Unknown base class '{node.base}'")
            base_info = self.classes[node.base]
            fields.update(base_info.fields)
            methods.update(base_info.methods)
            base_type = Type(node.base)

        for member in node.members:
            if isinstance(member, ast.FieldDecl):
                fields[member.name] = self.resolve_type(member.field_type)
            elif isinstance(member, ast.MethodDef):
                param_types = [self.resolve_type(p.param_type) for p in member.params]
                return_type = self.resolve_type(member.return_type) if member.return_type else VOID
                methods[member.name] = FunctionType(param_types, return_type)
            elif isinstance(member, ast.ConstructorDef):
                param_types = [self.resolve_type(p.param_type) for p in member.params]
                methods["constructor"] = FunctionType(param_types, VOID)

        self.classes[node.name] = ClassInfo(node.name, node.base, fields, methods)
        self.global_scope.define(
            node.name,
            Type(node.name, base=base_type),
        )

    def register_function(self, node: ast.FunctionDef) -> None:
        param_types = [self.resolve_type(p.param_type) for p in node.params]
        return_type = self.resolve_type(node.return_type) if node.return_type else VOID
        self.global_scope.define(node.name, FunctionType(param_types, return_type))

    def analyze_statement(self, node: ast.ASTNode) -> None:
        if isinstance(node, ast.VarDecl):
            init_type = self.analyze_expr(node.initializer)
            if node.var_type:
                declared = self.resolve_type(node.var_type)
                if not init_type.is_subtype_of(declared):
                    self.error(
                        f"Cannot assign {init_type} to variable '{node.name}' of type {declared}"
                    )
                final_type = declared
            else:
                final_type = init_type
            self.current_scope.define(node.name, final_type, mutable=not node.is_const)

        elif isinstance(node, ast.FunctionDef):
            self.analyze_function(node)

        elif isinstance(node, ast.ClassDef):
            self.analyze_class(node)

        elif isinstance(node, ast.ExprStmt):
            self.analyze_expr(node.expr)

        elif isinstance(node, ast.Block):
            self._with_scope(lambda: self._analyze_block(node))

        elif isinstance(node, ast.IfStmt):
            self.analyze_expr(node.condition)
            self.analyze_statement(node.then_block)
            for _, elif_block in node.elifs:
                self.analyze_statement(elif_block)
            if node.else_block:
                self.analyze_statement(node.else_block)

        elif isinstance(node, ast.WhileStmt):
            self.analyze_expr(node.condition)
            prev_loop = self.in_loop
            self.in_loop = True
            self.analyze_statement(node.body)
            self.in_loop = prev_loop

        elif isinstance(node, ast.ForStmt):
            iterable_type = self.analyze_expr(node.iterable)
            if iterable_type.name not in ("List", "Dict", "String", "Any"):
                self.error(f"Cannot iterate over {iterable_type}")
            prev_loop = self.in_loop
            self.in_loop = True
            self._with_scope(lambda: self._analyze_for_body(node, iterable_type))
            self.in_loop = prev_loop

        elif isinstance(node, ast.ReturnStmt):
            if self.current_function_return is None:
                self.error("Return outside of function")
            if node.value:
                value_type = self.analyze_expr(node.value)
                if not value_type.is_subtype_of(self.current_function_return):
                    self.error(
                        f"Return type {value_type} does not match expected {self.current_function_return}"
                    )
            elif self.current_function_return != VOID:
                self.error(f"Expected return value of type {self.current_function_return}")

        elif isinstance(node, ast.BreakStmt) or isinstance(node, ast.ContinueStmt):
            if not self.in_loop:
                self.error(f"{'Break' if isinstance(node, ast.BreakStmt) else 'Continue'} outside loop")

        elif isinstance(node, ast.TryStmt):
            self.analyze_statement(node.try_block)
            self._with_scope(lambda: (
                self.current_scope.define(node.catch_var, ANY),
                self.analyze_statement(node.catch_block),
            ))
            if node.finally_block:
                self.analyze_statement(node.finally_block)

        elif isinstance(node, ast.ThrowStmt):
            self.analyze_expr(node.value)

        elif isinstance(node, ast.ImportStmt):
            pass

        else:
            self.error(f"Unknown statement type: {type(node).__name__}")

    def _analyze_block(self, block: ast.Block) -> None:
        for stmt in block.statements:
            self.analyze_statement(stmt)

    def _analyze_for_body(self, node: ast.ForStmt, iterable_type: Type) -> None:
        item_type = ANY
        if iterable_type.name == "List" and iterable_type.params:
            item_type = iterable_type.params[0]
        elif iterable_type.name == "String":
            item_type = STRING
        elif iterable_type.name == "Dict" and iterable_type.params:
            item_type = iterable_type.params[0]
        if node.var_name:
            self.current_scope.define(node.var_name, item_type)
        self.analyze_statement(node.body)

    def analyze_function(self, node: ast.FunctionDef) -> None:
        param_types = [self.resolve_type(p.param_type) for p in node.params]
        return_type = self.resolve_type(node.return_type) if node.return_type else VOID
        func_type = FunctionType(param_types, return_type)
        self.global_scope.define(node.name, func_type)

        prev_return = self.current_function_return
        self.current_function_return = return_type

        def body_analysis():
            for param, ptype in zip(node.params, param_types):
                self.current_scope.define(param.name, ptype)
            self._analyze_block(node.body)

        self._with_scope(body_analysis)
        self.current_function_return = prev_return

    def analyze_class(self, node: ast.ClassDef) -> None:
        info = self.classes[node.name]
        for member in node.members:
            if isinstance(member, ast.MethodDef):
                self._analyze_method(member, info)
            elif isinstance(member, ast.ConstructorDef):
                self._analyze_constructor(member, info)

    def _analyze_method(self, node: ast.MethodDef, class_info: ClassInfo) -> None:
        param_types = [self.resolve_type(p.param_type) for p in node.params]
        return_type = self.resolve_type(node.return_type) if node.return_type else VOID
        prev_return = self.current_function_return
        self.current_function_return = return_type

        def body_analysis():
            if not node.is_static:
                this_type = Type(class_info.name)
                this_type.base = Type(class_info.base) if class_info.base else None
                self.current_scope.define("this", this_type)
            for param, ptype in zip(node.params, param_types):
                self.current_scope.define(param.name, ptype)
            self._analyze_block(node.body)

        self._with_scope(body_analysis)
        self.current_function_return = prev_return

    def _analyze_constructor(self, node: ast.ConstructorDef, class_info: ClassInfo) -> None:
        param_types = [self.resolve_type(p.param_type) for p in node.params]
        prev_return = self.current_function_return
        self.current_function_return = VOID

        def body_analysis():
            this_type = Type(class_info.name)
            this_type.base = Type(class_info.base) if class_info.base else None
            self.current_scope.define("this", this_type)
            for param, ptype in zip(node.params, param_types):
                self.current_scope.define(param.name, ptype)
            self._analyze_block(node.body)

        self._with_scope(body_analysis)
        self.current_function_return = prev_return

    def analyze_expr(self, node: ast.ASTNode) -> Type:
        if isinstance(node, ast.IntegerLiteral):
            return INT
        if isinstance(node, ast.FloatLiteral):
            return FLOAT
        if isinstance(node, ast.StringLiteral):
            return STRING
        if isinstance(node, ast.BooleanLiteral):
            return BOOL
        if isinstance(node, ast.NullLiteral):
            return NULL

        if isinstance(node, ast.Identifier):
            sym = self.current_scope.resolve(node.name)
            if sym is None:
                self.error(f"Undefined variable '{node.name}'")
            return sym.type

        if isinstance(node, ast.ThisExpr):
            sym = self.current_scope.resolve("this")
            if sym is None:
                self.error("'this' outside class method")
            return sym.type

        if isinstance(node, ast.BinaryOp):
            left = self.analyze_expr(node.left)
            right = self.analyze_expr(node.right)
            if node.op in ("+", "-", "*", "/", "%"):
                if left.is_numeric() and right.is_numeric():
                    if left == FLOAT or right == FLOAT:
                        return FLOAT
                    return INT
                if node.op == "+" and (left == STRING or right == STRING):
                    return STRING
                self.error(f"Operator '{node.op}' not supported for {left} and {right}")
            if node.op in ("==", "!="):
                return BOOL
            if node.op in ("<", ">", "<=", ">="):
                if left.is_numeric() and right.is_numeric():
                    return BOOL
                if left == STRING and right == STRING:
                    return BOOL
                if left.name == "Any" or right.name == "Any":
                    return BOOL
                self.error(f"Comparison not supported for {left} and {right}")
            if node.op in ("and", "or"):
                if left == BOOL and right == BOOL:
                    return BOOL
                self.error(f"Logical operator '{node.op}' requires Bool operands")

        if isinstance(node, ast.UnaryOp):
            operand = self.analyze_expr(node.operand)
            if node.op == "-":
                if operand.is_numeric():
                    return operand
                self.error(f"Cannot negate {operand}")
            if node.op == "not":
                if operand == BOOL:
                    return BOOL
                self.error(f"Cannot apply 'not' to {operand}")

        if isinstance(node, ast.Assignment):
            target_type = self.analyze_expr(node.target)
            value_type = self.analyze_expr(node.value)
            if isinstance(node.target, ast.Identifier):
                sym = self.current_scope.resolve(node.target.name)
                if sym and not sym.mutable:
                    self.error(f"Cannot assign to constant '{node.target.name}'")
            if not value_type.is_subtype_of(target_type):
                self.error(f"Cannot assign {value_type} to {target_type}")
            return target_type

        if isinstance(node, ast.CallExpr):
            callee_type = self.analyze_expr(node.callee)
            if isinstance(callee_type, FunctionType):
                expected = callee_type.param_types
                if len(node.args) != len(expected):
                    self.error(
                        f"Expected {len(expected)} arguments, got {len(node.args)}"
                    )
                for arg, expected_type in zip(node.args, expected):
                    arg_type = self.analyze_expr(arg)
                    if not arg_type.is_subtype_of(expected_type):
                        self.error(f"Argument type {arg_type} does not match {expected_type}")
                return callee_type.return_type
            if callee_type == ANY:
                for arg in node.args:
                    self.analyze_expr(arg)
                return ANY
            self.error(f"Cannot call {callee_type}")

        if isinstance(node, ast.MemberExpr):
            obj_type = self.analyze_expr(node.obj)
            if obj_type.name in self.classes:
                info = self.classes[obj_type.name]
                if node.member in info.fields:
                    return info.fields[node.member]
                if node.member in info.methods:
                    return info.methods[node.member]
                self.error(f"Class {obj_type.name} has no member '{node.member}'")
            if obj_type == STRING:
                if node.member in ("length", "split", "contains", "upper", "lower"):
                    return ANY
            if obj_type.name == "List":
                if node.member in ("length", "append", "pop", "contains"):
                    return ANY
            if obj_type.name == "Dict":
                if node.member == "length":
                    return ANY
            if obj_type == ANY:
                return ANY
            self.error(f"Cannot access member '{node.member}' on {obj_type}")

        if isinstance(node, ast.IndexExpr):
            obj_type = self.analyze_expr(node.obj)
            index_type = self.analyze_expr(node.index)
            if obj_type.name == "List":
                if not index_type.is_subtype_of(INT):
                    self.error("List index must be Int")
                if obj_type.params:
                    return obj_type.params[0]
                return ANY
            if obj_type.name == "Dict":
                return obj_type.params[1] if len(obj_type.params) > 1 else ANY
            if obj_type == STRING:
                if not index_type.is_subtype_of(INT):
                    self.error("String index must be Int")
                return STRING
            self.error(f"Cannot index {obj_type}")

        if isinstance(node, ast.ListLiteral):
            elem_type = ANY
            for elem in node.elements:
                t = self.analyze_expr(elem)
                if elem_type == ANY:
                    elem_type = t
                elif t != elem_type and t != ANY:
                    elem_type = ANY
            return Type("List", [elem_type])

        if isinstance(node, ast.DictLiteral):
            key_type = ANY
            value_type = ANY
            for k, v in node.entries:
                kt = self.analyze_expr(k)
                vt = self.analyze_expr(v)
                if key_type == ANY:
                    key_type = kt
                if value_type == ANY:
                    value_type = vt
            return Type("Dict", [key_type, value_type])

        if isinstance(node, ast.LambdaExpr):
            param_types = [self.resolve_type(p.param_type) for p in node.params]
            return_type = self.resolve_type(node.return_type) if node.return_type else ANY
            return FunctionType(param_types, return_type)

        if isinstance(node, ast.NewExpr):
            if node.class_name not in self.classes:
                self.error(f"Unknown class '{node.class_name}'")
            info = self.classes[node.class_name]
            ctor = info.methods.get("constructor")
            if ctor:
                if len(node.args) != len(ctor.param_types):
                    self.error(
                        f"Constructor expects {len(ctor.param_types)} arguments, got {len(node.args)}"
                    )
                for arg, expected_type in zip(node.args, ctor.param_types):
                    arg_type = self.analyze_expr(arg)
                    if not arg_type.is_subtype_of(expected_type):
                        self.error(f"Constructor argument type {arg_type} does not match {expected_type}")
            elif node.args:
                self.error("Class has no constructor but arguments were provided")
            return Type(node.class_name)

        self.error(f"Unknown expression type: {type(node).__name__}")

    def _with_scope(self, func) -> None:
        old_scope = self.current_scope
        self.current_scope = Scope(old_scope)
        try:
            func()
        finally:
            self.current_scope = old_scope


def analyze(program: ast.Program) -> None:
    Analyzer().analyze(program)
