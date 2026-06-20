"""AST-to-bytecode compiler for the Helios language."""
from __future__ import annotations

from typing import Any, List

from . import ast_nodes as ast
from .bytecode import OpCode, CodeObject, ClassObject


class CompileError(Exception):
    pass


class LoopContext:
    def __init__(self):
        self.break_patches: List[int] = []
        self.continue_patches: List[int] = []


class Compiler:
    def __init__(self):
        self.module_code = CodeObject(name="<module>", param_count=0)
        self.code = self.module_code
        self.functions: List[CodeObject] = []
        self.classes: List[ClassObject] = []
        self.locals_stack: List[List[str]] = [[]]
        self.loop_stack: List[LoopContext] = []
        self.try_stack: List[tuple] = []
        self.line = 0

    def error(self, message: str) -> None:
        raise CompileError(message)

    def is_module_level(self) -> bool:
        return self.code is self.module_code

    # ------------------------------------------------------------------
    # Scope helpers
    # ------------------------------------------------------------------

    def enter_scope(self) -> None:
        self.locals_stack.append([])

    def exit_scope(self) -> None:
        self.locals_stack.pop()

    def declare_local(self, name: str) -> int:
        self.locals_stack[-1].append(name)
        self.code.locals.append(name)
        return self.resolve_local(name)

    def resolve_local(self, name: str) -> int:
        # Locals are indexed across all scopes in the current function.
        idx = 0
        for scope in self.locals_stack:
            for local in scope:
                if local == name:
                    return idx
                idx += 1
        return -1

    def emit(self, opcode: OpCode, arg: Any = None) -> None:
        self.code.emit(opcode, arg, self.line)

    def emit_placeholder(self, opcode: OpCode = OpCode.JUMP) -> int:
        idx = len(self.code.instructions)
        self.emit(opcode, 0)
        return idx

    def patch_jump(self, idx: int) -> None:
        offset = len(self.code.instructions) - idx
        self.code.instructions[idx].arg = offset

    # ------------------------------------------------------------------
    # Compile program
    # ------------------------------------------------------------------

    def compile(self, program: ast.Program) -> CodeObject:
        for imp in program.imports:
            self.compile_import(imp)
        for stmt in program.statements:
            self.compile_statement(stmt)
        self.emit(OpCode.RETURN)
        return self.module_code

    def compile_import(self, node: ast.ImportStmt) -> None:
        # Imports are resolved at runtime via globals; nothing to emit for now.
        pass

    # ------------------------------------------------------------------
    # Statements
    # ------------------------------------------------------------------

    def compile_statement(self, node: ast.ASTNode) -> None:
        if isinstance(node, ast.VarDecl):
            self.compile_var_decl(node)
        elif isinstance(node, ast.FunctionDef):
            self.compile_function_def(node)
        elif isinstance(node, ast.ClassDef):
            self.compile_class_def(node)
        elif isinstance(node, ast.ExprStmt):
            self.compile_expr(node.expr)
            self.emit(OpCode.POP)
        elif isinstance(node, ast.Block):
            self.compile_block(node)
        elif isinstance(node, ast.IfStmt):
            self.compile_if(node)
        elif isinstance(node, ast.WhileStmt):
            self.compile_while(node)
        elif isinstance(node, ast.ForStmt):
            self.compile_for(node)
        elif isinstance(node, ast.ReturnStmt):
            self.compile_return(node)
        elif isinstance(node, ast.BreakStmt):
            self.compile_break()
        elif isinstance(node, ast.ContinueStmt):
            self.compile_continue()
        elif isinstance(node, ast.TryStmt):
            self.compile_try(node)
        elif isinstance(node, ast.ThrowStmt):
            self.compile_expr(node.value)
            self.emit(OpCode.THROW)
        else:
            self.error(f"Cannot compile statement {type(node).__name__}")

    def compile_var_decl(self, node: ast.VarDecl) -> None:
        self.compile_expr(node.initializer)
        if self.is_module_level():
            self.emit(OpCode.STORE_GLOBAL, node.name)
        else:
            idx = self.resolve_local(node.name)
            if idx >= 0:
                self.emit(OpCode.STORE_FAST, idx)
            else:
                self.declare_local(node.name)
                idx = self.resolve_local(node.name)
                self.emit(OpCode.STORE_FAST, idx)

    def compile_function_def(self, node: ast.FunctionDef) -> None:
        old_code = self.code
        func_code = CodeObject(name=node.name, param_count=len(node.params))
        self.code = func_code
        self.locals_stack.append([])

        # Parameters become locals
        for param in node.params:
            self.declare_local(param.name)

        for stmt in node.body.statements:
            self.compile_statement(stmt)

        # Implicit return
        self.emit(OpCode.LOAD_CONST, func_code.add_const(None))
        self.emit(OpCode.RETURN_VALUE)

        self.locals_stack.pop()
        self.code = old_code
        self.functions.append(func_code)

        # Emit make function
        func_idx = self.code.add_const(func_code)
        self.emit(OpCode.LOAD_CONST, func_idx)
        self.emit(OpCode.MAKE_FUNCTION, (func_idx, node.name, len(node.params)))
        if self.is_module_level():
            self.emit(OpCode.STORE_GLOBAL, node.name)
        else:
            idx = self.declare_local(node.name)
            self.emit(OpCode.STORE_FAST, idx)

    def compile_class_def(self, node: ast.ClassDef) -> None:
        methods: dict = {}
        fields: dict = {}
        ctor_node: ast.ConstructorDef = ast.ConstructorDef(params=[], body=ast.Block(statements=[]))

        for member in node.members:
            if isinstance(member, ast.FieldDecl):
                fields[member.name] = member.initializer
            elif isinstance(member, ast.MethodDef):
                methods[member.name] = self.compile_method(member, node.name)
            elif isinstance(member, ast.ConstructorDef):
                ctor_node = member

        # Inject field initializers at the start of the constructor body.
        init_statements: List[ast.ASTNode] = []
        for fname, finit in fields.items():
            if finit is not None:
                init_statements.append(
                    ast.ExprStmt(
                        expr=ast.Assignment(
                            target=ast.MemberExpr(obj=ast.ThisExpr(), member=fname),
                            value=finit,
                        )
                    )
                )
        ctor_node.body.statements = init_statements + ctor_node.body.statements
        methods["constructor"] = self.compile_constructor(ctor_node, node.name)

        cls = ClassObject(
            name=node.name,
            base=node.base or "",
            methods=methods,
            fields=fields,
        )
        self.classes.append(cls)

        cls_idx = self.code.add_const(cls)
        self.emit(OpCode.LOAD_CONST, cls_idx)
        self.emit(OpCode.BUILD_CLASS, (node.name, node.base or "", len(methods)))
        if self.is_module_level():
            self.emit(OpCode.STORE_GLOBAL, node.name)
        else:
            idx = self.declare_local(node.name)
            self.emit(OpCode.STORE_FAST, idx)

    def compile_method(self, node: ast.MethodDef, class_name: str) -> CodeObject:
        old_code = self.code
        method_code = CodeObject(
            name=f"{class_name}.{node.name}",
            param_count=len(node.params) + (0 if node.is_static else 1),
        )
        self.code = method_code
        self.locals_stack.append([])

        if not node.is_static:
            self.declare_local("this")
        for param in node.params:
            self.declare_local(param.name)

        for stmt in node.body.statements:
            self.compile_statement(stmt)

        self.emit(OpCode.LOAD_CONST, method_code.add_const(None))
        self.emit(OpCode.RETURN_VALUE)

        self.locals_stack.pop()
        self.code = old_code
        self.functions.append(method_code)
        return method_code

    def compile_constructor(self, node: ast.ConstructorDef, class_name: str) -> CodeObject:
        old_code = self.code
        ctor_code = CodeObject(name=f"{class_name}.constructor", param_count=len(node.params) + 1)
        self.code = ctor_code
        self.locals_stack.append([])

        self.declare_local("this")
        for param in node.params:
            self.declare_local(param.name)

        for stmt in node.body.statements:
            self.compile_statement(stmt)

        self.emit(OpCode.LOAD_FAST, 0)  # return this
        self.emit(OpCode.RETURN_VALUE)

        self.locals_stack.pop()
        self.code = old_code
        self.functions.append(ctor_code)
        return ctor_code

    def compile_block(self, node: ast.Block) -> None:
        self.enter_scope()
        for stmt in node.statements:
            self.compile_statement(stmt)
        self.exit_scope()

    def compile_if(self, node: ast.IfStmt) -> None:
        self.compile_expr(node.condition)
        jump_false_idx = self.emit_placeholder(OpCode.JUMP_IF_FALSE)
        self.compile_statement(node.then_block)

        end_jumps: List[int] = []
        if node.elifs or node.else_block:
            end_jumps.append(self.emit_placeholder())

        self.patch_jump(jump_false_idx)

        for condition, block in node.elifs:
            self.compile_expr(condition)
            elif_jump_false = self.emit_placeholder(OpCode.JUMP_IF_FALSE)
            self.compile_statement(block)
            end_jumps.append(self.emit_placeholder())
            self.patch_jump(elif_jump_false)

        if node.else_block:
            self.compile_statement(node.else_block)

        for end_idx in end_jumps:
            self.patch_jump(end_idx)

    def compile_while(self, node: ast.WhileStmt) -> None:
        loop_start = len(self.code.instructions)
        self.compile_expr(node.condition)
        exit_jump = self.emit_placeholder(OpCode.JUMP_IF_FALSE)

        loop_ctx = LoopContext()
        self.loop_stack.append(loop_ctx)

        self.compile_statement(node.body)

        # Continue patches point here
        offset = len(self.code.instructions) - loop_start
        self.emit(OpCode.JUMP, -offset)

        self.loop_stack.pop()

        exit_idx = len(self.code.instructions)
        self.patch_jump(exit_jump)

        # Patch break jumps
        for patch_idx in loop_ctx.break_patches:
            self.code.instructions[patch_idx].arg = exit_idx - patch_idx

        # Patch continue jumps to loop_start
        for patch_idx in loop_ctx.continue_patches:
            self.code.instructions[patch_idx].arg = loop_start - patch_idx

    def compile_for(self, node: ast.ForStmt) -> None:
        self.enter_scope()

        # Push iterator
        self.compile_expr(node.iterable)
        self.emit(OpCode.GET_ITER)

        loop_start = len(self.code.instructions)

        # FOR_ITER pops iterator, pushes next value or jumps
        exit_jump = self.emit_placeholder()  # placeholder for FOR_ITER jump offset

        if node.var_name:
            idx = self.declare_local(node.var_name)
            self.emit(OpCode.STORE_FAST, idx)

        loop_ctx = LoopContext()
        self.loop_stack.append(loop_ctx)

        self.compile_statement(node.body)

        # Jump back
        offset = len(self.code.instructions) - loop_start
        self.emit(OpCode.JUMP, -offset)

        self.loop_stack.pop()

        exit_idx = len(self.code.instructions)
        self.code.instructions[exit_jump].arg = exit_idx - exit_jump
        self.code.instructions[exit_jump].opcode = OpCode.FOR_ITER

        # Patch breaks and continues
        for patch_idx in loop_ctx.break_patches:
            self.code.instructions[patch_idx].arg = exit_idx - patch_idx
        for patch_idx in loop_ctx.continue_patches:
            self.code.instructions[patch_idx].arg = loop_start - patch_idx

        self.exit_scope()

    def compile_return(self, node: ast.ReturnStmt) -> None:
        if node.value:
            self.compile_expr(node.value)
            self.emit(OpCode.RETURN_VALUE)
        else:
            self.emit(OpCode.RETURN)

    def compile_break(self) -> None:
        if not self.loop_stack:
            self.error("break outside loop")
        patch = self.emit_placeholder()
        self.loop_stack[-1].break_patches.append(patch)

    def compile_continue(self) -> None:
        if not self.loop_stack:
            self.error("continue outside loop")
        patch = self.emit_placeholder()
        self.loop_stack[-1].continue_patches.append(patch)

    def compile_try(self, node: ast.TryStmt) -> None:
        try_begin_idx = len(self.code.instructions)
        self.emit(OpCode.TRY_BEGIN, (0, 0))
        self.try_stack.append((try_begin_idx, node))

        self.compile_statement(node.try_block)

        self.emit(OpCode.TRY_END)
        end_jump = self.emit_placeholder()

        catch_start = len(self.code.instructions)
        self.enter_scope()
        idx = self.declare_local(node.catch_var)
        self.emit(OpCode.STORE_FAST, idx)
        self.compile_statement(node.catch_block)
        self.exit_scope()

        finally_start = len(self.code.instructions)
        if node.finally_block:
            self.compile_statement(node.finally_block)

        self.patch_jump(end_jump)

        # Patch try begin
        self.code.instructions[try_begin_idx].arg = (catch_start - try_begin_idx, finally_start - try_begin_idx)
        self.try_stack.pop()

    # ------------------------------------------------------------------
    # Expressions
    # ------------------------------------------------------------------

    def compile_expr(self, node: ast.ASTNode) -> None:
        if isinstance(node, ast.IntegerLiteral):
            self.emit(OpCode.LOAD_CONST, self.code.add_const(node.value))
        elif isinstance(node, ast.FloatLiteral):
            self.emit(OpCode.LOAD_CONST, self.code.add_const(node.value))
        elif isinstance(node, ast.StringLiteral):
            self.emit(OpCode.LOAD_CONST, self.code.add_const(node.value))
        elif isinstance(node, ast.BooleanLiteral):
            self.emit(OpCode.LOAD_CONST, self.code.add_const(node.value))
        elif isinstance(node, ast.NullLiteral):
            self.emit(OpCode.LOAD_CONST, self.code.add_const(None))
        elif isinstance(node, ast.Identifier):
            self.compile_identifier(node)
        elif isinstance(node, ast.ThisExpr):
            self.emit(OpCode.LOAD_THIS)
        elif isinstance(node, ast.BinaryOp):
            self.compile_binary(node)
        elif isinstance(node, ast.UnaryOp):
            self.compile_unary(node)
        elif isinstance(node, ast.Assignment):
            self.compile_assignment(node)
        elif isinstance(node, ast.CallExpr):
            self.compile_call(node)
        elif isinstance(node, ast.MemberExpr):
            self.compile_member(node)
        elif isinstance(node, ast.IndexExpr):
            self.compile_index(node)
        elif isinstance(node, ast.ListLiteral):
            self.compile_list(node)
        elif isinstance(node, ast.DictLiteral):
            self.compile_dict(node)
        elif isinstance(node, ast.LambdaExpr):
            self.compile_lambda(node)
        elif isinstance(node, ast.NewExpr):
            self.compile_new(node)
        else:
            self.error(f"Cannot compile expression {type(node).__name__}")

    def compile_identifier(self, node: ast.Identifier) -> None:
        idx = self.resolve_local(node.name)
        if idx >= 0:
            self.emit(OpCode.LOAD_FAST, idx)
        else:
            self.emit(OpCode.LOAD_NAME, node.name)

    def compile_binary(self, node: ast.BinaryOp) -> None:
        self.compile_expr(node.left)
        self.compile_expr(node.right)
        if node.op in ("==", "!=", "<", ">", "<=", ">="):
            self.emit(OpCode.COMPARE_OP, node.op)
        else:
            self.emit(OpCode.BINARY_OP, node.op)

    def compile_unary(self, node: ast.UnaryOp) -> None:
        self.compile_expr(node.operand)
        self.emit(OpCode.UNARY_OP, node.op)

    def compile_assignment(self, node: ast.Assignment) -> None:
        if isinstance(node.target, ast.Identifier):
            self.compile_expr(node.value)
            idx = self.resolve_local(node.target.name)
            if idx >= 0:
                self.emit(OpCode.STORE_FAST, idx)
                self.emit(OpCode.LOAD_FAST, idx)
            else:
                if self.is_module_level():
                    self.emit(OpCode.STORE_GLOBAL, node.target.name)
                    self.emit(OpCode.LOAD_GLOBAL, node.target.name)
                else:
                    self.emit(OpCode.STORE_NAME, node.target.name)
                    self.emit(OpCode.LOAD_NAME, node.target.name)
        elif isinstance(node.target, ast.MemberExpr):
            self.compile_expr(node.target.obj)
            self.compile_expr(node.value)
            self.emit(OpCode.STORE_ATTR, node.target.member)
        elif isinstance(node.target, ast.IndexExpr):
            self.compile_expr(node.target.obj)
            self.compile_expr(node.target.index)
            self.compile_expr(node.value)
            self.emit(OpCode.STORE_INDEX)
        else:
            self.error("Invalid assignment target")

    def compile_call(self, node: ast.CallExpr) -> None:
        # Method call syntax sugar: obj.method(args)
        if isinstance(node.callee, ast.MemberExpr):
            self.compile_expr(node.callee.obj)
            self.emit(OpCode.LOAD_ATTR, node.callee.member)
            for arg in node.args:
                self.compile_expr(arg)
            self.emit(OpCode.CALL, len(node.args))
        else:
            self.compile_expr(node.callee)
            for arg in node.args:
                self.compile_expr(arg)
            self.emit(OpCode.CALL, len(node.args))

    def compile_member(self, node: ast.MemberExpr) -> None:
        self.compile_expr(node.obj)
        self.emit(OpCode.LOAD_ATTR, node.member)

    def compile_index(self, node: ast.IndexExpr) -> None:
        self.compile_expr(node.obj)
        self.compile_expr(node.index)
        self.emit(OpCode.LOAD_INDEX)

    def compile_list(self, node: ast.ListLiteral) -> None:
        for elem in node.elements:
            self.compile_expr(elem)
        self.emit(OpCode.BUILD_LIST, len(node.elements))

    def compile_dict(self, node: ast.DictLiteral) -> None:
        for k, v in node.entries:
            self.compile_expr(k)
            self.compile_expr(v)
        self.emit(OpCode.BUILD_DICT, len(node.entries))

    def compile_lambda(self, node: ast.LambdaExpr) -> None:
        old_code = self.code
        lambda_code = CodeObject(name="<lambda>", param_count=len(node.params))
        self.code = lambda_code
        self.locals_stack.append([])

        for param in node.params:
            self.declare_local(param.name)

        for stmt in node.body.statements:
            self.compile_statement(stmt)

        self.emit(OpCode.LOAD_CONST, lambda_code.add_const(None))
        self.emit(OpCode.RETURN_VALUE)

        self.locals_stack.pop()
        self.code = old_code
        self.functions.append(lambda_code)

        lambda_idx = self.code.add_const(lambda_code)
        self.emit(OpCode.LOAD_CONST, lambda_idx)
        self.emit(OpCode.MAKE_FUNCTION, (lambda_idx, "<lambda>", len(node.params)))

    def compile_new(self, node: ast.NewExpr) -> None:
        self.emit(OpCode.LOAD_NAME, node.class_name)
        for arg in node.args:
            self.compile_expr(arg)
        self.emit(OpCode.NEW_OBJECT, node.class_name)


def compile_program(program: ast.Program) -> Compiler:
    compiler = Compiler()
    compiler.compile(program)
    return compiler
