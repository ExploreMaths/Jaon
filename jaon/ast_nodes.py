"""Abstract syntax tree nodes for the Jaon programming language."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


class ASTNode:
    pass


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

@dataclass
class TypeNode(ASTNode):
    name: str
    params: List[TypeNode] = field(default_factory=list)

    def __str__(self) -> str:
        if self.params:
            params = ", ".join(str(p) for p in self.params)
            return f"{self.name}<{params}>"
        return self.name


# ---------------------------------------------------------------------------
# Literals / Primary
# ---------------------------------------------------------------------------

@dataclass
class IntegerLiteral(ASTNode):
    value: int


@dataclass
class FloatLiteral(ASTNode):
    value: float


@dataclass
class StringLiteral(ASTNode):
    value: str


@dataclass
class BooleanLiteral(ASTNode):
    value: bool


@dataclass
class NullLiteral(ASTNode):
    pass


@dataclass
class Identifier(ASTNode):
    name: str


@dataclass
class ThisExpr(ASTNode):
    pass


# ---------------------------------------------------------------------------
# Expressions
# ---------------------------------------------------------------------------

@dataclass
class BinaryOp(ASTNode):
    op: str
    left: ASTNode
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    op: str
    operand: ASTNode


@dataclass
class Assignment(ASTNode):
    target: ASTNode
    value: ASTNode


@dataclass
class CallExpr(ASTNode):
    callee: ASTNode
    args: List[ASTNode]


@dataclass
class IndexExpr(ASTNode):
    obj: ASTNode
    index: ASTNode


@dataclass
class MemberExpr(ASTNode):
    obj: ASTNode
    member: str


@dataclass
class ListLiteral(ASTNode):
    elements: List[ASTNode]


@dataclass
class DictLiteral(ASTNode):
    entries: List[tuple]


@dataclass
class LambdaExpr(ASTNode):
    params: List[Parameter]
    return_type: Optional[TypeNode]
    body: Block


@dataclass
class NewExpr(ASTNode):
    class_name: str
    args: List[ASTNode]


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

@dataclass
class Parameter(ASTNode):
    name: str
    param_type: TypeNode


# ---------------------------------------------------------------------------
# Statements
# ---------------------------------------------------------------------------

@dataclass
class Block(ASTNode):
    statements: List[ASTNode]


@dataclass
class VarDecl(ASTNode):
    name: str
    var_type: Optional[TypeNode]
    initializer: ASTNode
    is_const: bool = False


@dataclass
class ExprStmt(ASTNode):
    expr: ASTNode


@dataclass
class ReturnStmt(ASTNode):
    value: Optional[ASTNode]


@dataclass
class IfStmt(ASTNode):
    condition: ASTNode
    then_block: Block
    elifs: List[tuple] = field(default_factory=list)
    else_block: Optional[Block] = None


@dataclass
class WhileStmt(ASTNode):
    condition: ASTNode
    body: Block


@dataclass
class ForStmt(ASTNode):
    var_name: Optional[str]
    iterable: ASTNode
    body: Block


@dataclass
class BreakStmt(ASTNode):
    pass


@dataclass
class ContinueStmt(ASTNode):
    pass


@dataclass
class TryStmt(ASTNode):
    try_block: Block
    catch_var: str
    catch_block: Block
    finally_block: Optional[Block]


@dataclass
class ThrowStmt(ASTNode):
    value: ASTNode


@dataclass
class ImportStmt(ASTNode):
    path: List[str]


# ---------------------------------------------------------------------------
# Functions and Classes
# ---------------------------------------------------------------------------

@dataclass
class FunctionDef(ASTNode):
    name: str
    params: List[Parameter]
    return_type: Optional[TypeNode]
    body: Block


@dataclass
class FieldDecl(ASTNode):
    access: str
    name: str
    field_type: TypeNode
    initializer: Optional[ASTNode]


@dataclass
class ConstructorDef(ASTNode):
    params: List[Parameter]
    body: Block


@dataclass
class MethodDef(ASTNode):
    access: str
    name: str
    params: List[Parameter]
    return_type: Optional[TypeNode]
    body: Block
    is_static: bool = False


@dataclass
class ClassDef(ASTNode):
    name: str
    base: Optional[str]
    members: List[ASTNode]


# ---------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------

@dataclass
class Program(ASTNode):
    imports: List[ImportStmt]
    statements: List[ASTNode]
