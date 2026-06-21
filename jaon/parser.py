"""Recursive-descent parser for the Jaon programming language."""
from __future__ import annotations

from typing import List, Optional

from .lexer import Token, TokenType
from . import ast_nodes as ast


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def error(self, message: str) -> None:
        tok = self.peek()
        raise ParseError(f"{message} at line {tok.line}, column {tok.column}")

    def peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[idx]

    def advance(self) -> Token:
        tok = self.peek()
        if self.pos < len(self.tokens):
            self.pos += 1
        return tok

    def match(self, *types: TokenType) -> Optional[Token]:
        if self.peek().type in types:
            return self.advance()
        return None

    def expect(self, token_type: TokenType, message: str) -> Token:
        if self.peek().type != token_type:
            self.error(message)
        return self.advance()

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def _node(self, node: ast.ASTNode, tok: Token) -> ast.ASTNode:
        node.line = tok.line
        node.column = tok.column
        return node

    # ------------------------------------------------------------------
    # Program
    # ------------------------------------------------------------------

    def parse(self) -> ast.Program:
        imports: List[ast.ImportStmt] = []
        statements: List[ast.ASTNode] = []
        first_tok = self.peek()
        while not self.is_at_end():
            if self.peek().type == TokenType.IMPORT:
                imports.append(self.import_stmt())
            else:
                statements.append(self.declaration())
        return self._node(ast.Program(imports=imports, statements=statements), first_tok)

    # ------------------------------------------------------------------
    # Declarations
    # ------------------------------------------------------------------

    def declaration(self) -> ast.ASTNode:
        if self.peek().type == TokenType.FUN:
            return self.function_declaration()
        if self.peek().type == TokenType.CLASS:
            return self.class_declaration()
        if self.peek().type == TokenType.VAR or self.peek().type == TokenType.VAL:
            return self.var_declaration()
        return self.statement()

    def function_declaration(self) -> ast.FunctionDef:
        tok = self.advance()  # fun
        name = self.expect(TokenType.IDENT, "Expected function name").value
        params = self.parameters()
        return_type: Optional[ast.TypeNode] = None
        if self.match(TokenType.COLON):
            return_type = self.type_annotation()
        body = self.block()
        return self._node(
            ast.FunctionDef(name=name, params=params, return_type=return_type, body=body), tok
        )

    def class_declaration(self) -> ast.ClassDef:
        tok = self.advance()  # class
        name = self.expect(TokenType.IDENT, "Expected class name").value
        base: Optional[str] = None
        if self.match(TokenType.EXTENDS):
            base = self.expect(TokenType.IDENT, "Expected base class name").value
        self.expect(TokenType.LBRACE, "Expected '{' before class body")
        members: List[ast.ASTNode] = []
        while self.peek().type != TokenType.RBRACE and not self.is_at_end():
            members.append(self.class_member())
        self.expect(TokenType.RBRACE, "Expected '}' after class body")
        return self._node(ast.ClassDef(name=name, base=base, members=members), tok)

    def class_member(self) -> ast.ASTNode:
        access = "private"
        is_static = False
        while True:
            if self.peek().type == TokenType.PUBLIC:
                access = "public"
                self.advance()
            elif self.peek().type == TokenType.PRIVATE:
                access = "private"
                self.advance()
            elif self.peek().type == TokenType.STATIC:
                is_static = True
                self.advance()
            else:
                break

        if self.peek().type == TokenType.CONSTRUCTOR:
            return self.constructor_definition()

        if self.peek().type == TokenType.VAR or self.peek().type == TokenType.VAL:
            decl = self.var_declaration()
            if not isinstance(decl, ast.VarDecl):
                self.error("Invalid field declaration")
            field = ast.FieldDecl(
                access=access,
                name=decl.name,
                field_type=decl.var_type or ast.TypeNode("Any"),
                initializer=decl.initializer,
            )
            field.line = decl.line
            field.column = decl.column
            return field

        if self.peek().type == TokenType.FUN:
            tok = self.advance()
            name = self.expect(TokenType.IDENT, "Expected method name").value
            params = self.parameters()
            return_type: Optional[ast.TypeNode] = None
            if self.match(TokenType.COLON):
                return_type = self.type_annotation()
            body = self.block()
            return self._node(
                ast.MethodDef(
                    access=access,
                    name=name,
                    params=params,
                    return_type=return_type,
                    body=body,
                    is_static=is_static,
                ),
                tok,
            )

        self.error("Expected class member")

    def constructor_definition(self) -> ast.ConstructorDef:
        tok = self.advance()  # constructor
        params = self.parameters()
        body = self.block()
        return self._node(ast.ConstructorDef(params=params, body=body), tok)

    def parameters(self) -> List[ast.Parameter]:
        self.expect(TokenType.LPAREN, "Expected '('")
        params: List[ast.Parameter] = []
        if self.peek().type != TokenType.RPAREN:
            params.append(self.parameter())
            while self.match(TokenType.COMMA):
                params.append(self.parameter())
        self.expect(TokenType.RPAREN, "Expected ')'")
        return params

    def parameter(self) -> ast.Parameter:
        tok = self.peek()
        name = self.expect(TokenType.IDENT, "Expected parameter name").value
        self.expect(TokenType.COLON, "Expected ':' after parameter name")
        param_type = self.type_annotation()
        return self._node(ast.Parameter(name=name, param_type=param_type), tok)

    def var_declaration(self) -> ast.VarDecl:
        tok = self.peek()
        is_const = tok.type == TokenType.VAL
        self.advance()  # var / val
        name = self.expect(TokenType.IDENT, "Expected variable name").value
        var_type: Optional[ast.TypeNode] = None
        if self.match(TokenType.COLON):
            var_type = self.type_annotation()
        self.expect(TokenType.ASSIGN, "Expected '=' after variable name")
        initializer = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return self._node(
            ast.VarDecl(name=name, var_type=var_type, initializer=initializer, is_const=is_const), tok
        )

    def type_annotation(self) -> ast.TypeNode:
        tok = self.peek()
        name = self.expect(TokenType.IDENT, "Expected type name").value
        params: List[ast.TypeNode] = []
        if self.match(TokenType.LT):
            params.append(self.type_annotation())
            while self.match(TokenType.COMMA):
                params.append(self.type_annotation())
            self.expect(TokenType.GT, "Expected '>' after type parameters")
        return self._node(ast.TypeNode(name=name, params=params), tok)

    # ------------------------------------------------------------------
    # Statements
    # ------------------------------------------------------------------

    def statement(self) -> ast.ASTNode:
        if self.peek().type == TokenType.LBRACE:
            return self.block()
        if self.peek().type == TokenType.IF:
            return self.if_statement()
        if self.peek().type == TokenType.WHILE:
            return self.while_statement()
        if self.peek().type == TokenType.FOR:
            return self.for_statement()
        if self.peek().type == TokenType.RETURN:
            return self.return_statement()
        if self.peek().type == TokenType.BREAK:
            tok = self.advance()
            self.expect(TokenType.SEMICOLON, "Expected ';' after break")
            return self._node(ast.BreakStmt(), tok)
        if self.peek().type == TokenType.CONTINUE:
            tok = self.advance()
            self.expect(TokenType.SEMICOLON, "Expected ';' after continue")
            return self._node(ast.ContinueStmt(), tok)
        if self.peek().type == TokenType.TRY:
            return self.try_statement()
        if self.peek().type == TokenType.THROW:
            return self.throw_statement()
        return self.expr_statement()

    def import_stmt(self) -> ast.ImportStmt:
        tok = self.advance()  # import
        path = [self.expect(TokenType.IDENT, "Expected import name").value]
        while self.match(TokenType.DOT):
            path.append(self.expect(TokenType.IDENT, "Expected import name").value)
        self.expect(TokenType.SEMICOLON, "Expected ';' after import")
        return self._node(ast.ImportStmt(path=path), tok)

    def block(self) -> ast.Block:
        tok = self.expect(TokenType.LBRACE, "Expected '{'")
        statements: List[ast.ASTNode] = []
        while self.peek().type != TokenType.RBRACE and not self.is_at_end():
            statements.append(self.declaration())
        self.expect(TokenType.RBRACE, "Expected '}'")
        return self._node(ast.Block(statements=statements), tok)

    def if_statement(self) -> ast.IfStmt:
        tok = self.advance()  # if
        condition = self.expression()
        then_block = self.block()
        elifs: List[tuple] = []
        while self.peek().type == TokenType.ELIF:
            self.advance()
            elif_condition = self.expression()
            elif_block = self.block()
            elifs.append((elif_condition, elif_block))
        else_block: Optional[ast.Block] = None
        if self.match(TokenType.ELSE):
            else_block = self.block()
        return self._node(
            ast.IfStmt(
                condition=condition,
                then_block=then_block,
                elifs=elifs,
                else_block=else_block,
            ),
            tok,
        )

    def while_statement(self) -> ast.WhileStmt:
        tok = self.advance()  # while
        condition = self.expression()
        body = self.block()
        return self._node(ast.WhileStmt(condition=condition, body=body), tok)

    def for_statement(self) -> ast.ForStmt:
        tok = self.advance()  # for
        self.expect(TokenType.LPAREN, "Expected '(' after 'for'")
        var_name: Optional[str] = None
        if self.peek().type == TokenType.IDENT:
            var_name = self.advance().value
            self.expect(TokenType.IN, "Expected 'in' after loop variable")
        iterable = self.expression()
        self.expect(TokenType.RPAREN, "Expected ')' after for iterable")
        body = self.block()
        return self._node(ast.ForStmt(var_name=var_name, iterable=iterable, body=body), tok)

    def return_statement(self) -> ast.ReturnStmt:
        tok = self.advance()  # return
        value: Optional[ast.ASTNode] = None
        if self.peek().type != TokenType.SEMICOLON:
            value = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after return")
        return self._node(ast.ReturnStmt(value=value), tok)

    def try_statement(self) -> ast.TryStmt:
        tok = self.advance()  # try
        try_block = self.block()
        self.expect(TokenType.CATCH, "Expected 'catch'")
        self.expect(TokenType.LPAREN, "Expected '(' after 'catch'")
        catch_var = self.expect(TokenType.IDENT, "Expected catch variable").value
        self.expect(TokenType.RPAREN, "Expected ')' after catch variable")
        catch_block = self.block()
        finally_block: Optional[ast.Block] = None
        if self.match(TokenType.FINALLY):
            finally_block = self.block()
        return self._node(
            ast.TryStmt(
                try_block=try_block,
                catch_var=catch_var,
                catch_block=catch_block,
                finally_block=finally_block,
            ),
            tok,
        )

    def throw_statement(self) -> ast.ThrowStmt:
        tok = self.advance()  # throw
        value = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after throw")
        return self._node(ast.ThrowStmt(value=value), tok)

    def expr_statement(self) -> ast.ExprStmt:
        expr = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after expression")
        return self._node(ast.ExprStmt(expr=expr), expr)

    # ------------------------------------------------------------------
    # Expressions
    # ------------------------------------------------------------------

    def expression(self) -> ast.ASTNode:
        return self.assignment()

    def assignment(self) -> ast.ASTNode:
        expr = self.or_expr()
        if self.match(TokenType.ASSIGN):
            value = self.assignment()
            if isinstance(expr, (ast.Identifier, ast.MemberExpr, ast.IndexExpr)):
                return self._node(ast.Assignment(target=expr, value=value), expr)
            self.error("Invalid assignment target")
        return expr

    def or_expr(self) -> ast.ASTNode:
        left = self.and_expr()
        while True:
            tok = self.match(TokenType.OR)
            if not tok:
                break
            right = self.and_expr()
            left = self._node(ast.BinaryOp(op="or", left=left, right=right), tok)
        return left

    def and_expr(self) -> ast.ASTNode:
        left = self.equality()
        while True:
            tok = self.match(TokenType.AND)
            if not tok:
                break
            right = self.equality()
            left = self._node(ast.BinaryOp(op="and", left=left, right=right), tok)
        return left

    def equality(self) -> ast.ASTNode:
        left = self.comparison()
        while True:
            tok = self.match(TokenType.EQ) or self.match(TokenType.NEQ)
            if not tok:
                break
            right = self.comparison()
            op = "==" if tok.type == TokenType.EQ else "!="
            left = self._node(ast.BinaryOp(op=op, left=left, right=right), tok)
        return left

    def comparison(self) -> ast.ASTNode:
        left = self.term()
        while True:
            tok = self.match(TokenType.LT) or self.match(TokenType.GT) or self.match(TokenType.LE) or self.match(TokenType.GE)
            if not tok:
                break
            right = self.term()
            left = self._node(ast.BinaryOp(op=tok.value, left=left, right=right), tok)
        return left

    def term(self) -> ast.ASTNode:
        left = self.factor()
        while True:
            tok = self.match(TokenType.PLUS) or self.match(TokenType.MINUS)
            if not tok:
                break
            right = self.factor()
            left = self._node(ast.BinaryOp(op=tok.value, left=left, right=right), tok)
        return left

    def factor(self) -> ast.ASTNode:
        left = self.unary()
        while True:
            tok = self.match(TokenType.STAR) or self.match(TokenType.SLASH) or self.match(TokenType.PERCENT)
            if not tok:
                break
            right = self.unary()
            left = self._node(ast.BinaryOp(op=tok.value, left=left, right=right), tok)
        return left

    def unary(self) -> ast.ASTNode:
        tok = self.match(TokenType.MINUS) or self.match(TokenType.NOT)
        if tok:
            return self._node(ast.UnaryOp(op=tok.value, operand=self.unary()), tok)
        return self.postfix()

    def postfix(self) -> ast.ASTNode:
        expr = self.primary()
        while True:
            tok = self.match(TokenType.LPAREN)
            if tok:
                args: List[ast.ASTNode] = []
                if self.peek().type != TokenType.RPAREN:
                    args.append(self.expression())
                    while self.match(TokenType.COMMA):
                        args.append(self.expression())
                self.expect(TokenType.RPAREN, "Expected ')' after arguments")
                expr = self._node(ast.CallExpr(callee=expr, args=args), tok)
                continue
            tok = self.match(TokenType.DOT)
            if tok:
                member = self.expect(TokenType.IDENT, "Expected member name").value
                expr = self._node(ast.MemberExpr(obj=expr, member=member), expr)
                continue
            tok = self.match(TokenType.LBRACKET)
            if tok:
                index = self.expression()
                self.expect(TokenType.RBRACKET, "Expected ']' after index")
                expr = self._node(ast.IndexExpr(obj=expr, index=index), tok)
                continue
            break
        return expr

    def primary(self) -> ast.ASTNode:
        tok = self.match(TokenType.INT)
        if tok:
            return self._node(ast.IntegerLiteral(value=tok.value), tok)
        tok = self.match(TokenType.FLOAT)
        if tok:
            return self._node(ast.FloatLiteral(value=tok.value), tok)
        tok = self.match(TokenType.STRING)
        if tok:
            return self._node(ast.StringLiteral(value=tok.value), tok)
        tok = self.match(TokenType.BOOL)
        if tok:
            return self._node(ast.BooleanLiteral(value=tok.value), tok)
        tok = self.match(TokenType.NULL)
        if tok:
            return self._node(ast.NullLiteral(), tok)

        tok = self.match(TokenType.IDENT)
        if tok:
            return self._node(ast.Identifier(name=tok.value), tok)

        tok = self.match(TokenType.THIS)
        if tok:
            return self._node(ast.ThisExpr(), tok)

        tok = self.match(TokenType.LPAREN)
        if tok:
            expr = self.expression()
            self.expect(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        tok = self.match(TokenType.LBRACKET)
        if tok:
            elements: List[ast.ASTNode] = []
            if self.peek().type != TokenType.RBRACKET:
                elements.append(self.expression())
                while self.match(TokenType.COMMA):
                    elements.append(self.expression())
            self.expect(TokenType.RBRACKET, "Expected ']' after list elements")
            return self._node(ast.ListLiteral(elements=elements), tok)

        tok = self.match(TokenType.LBRACE)
        if tok:
            entries: List[tuple] = []
            if self.peek().type != TokenType.RBRACE:
                key = self.expression()
                self.expect(TokenType.COLON, "Expected ':' after dict key")
                value = self.expression()
                entries.append((key, value))
                while self.match(TokenType.COMMA):
                    key = self.expression()
                    self.expect(TokenType.COLON, "Expected ':' after dict key")
                    value = self.expression()
                    entries.append((key, value))
            self.expect(TokenType.RBRACE, "Expected '}' after dict entries")
            return self._node(ast.DictLiteral(entries=entries), tok)

        tok = self.match(TokenType.FUN)
        if tok:
            params = self.parameters()
            return_type: Optional[ast.TypeNode] = None
            if self.match(TokenType.COLON):
                return_type = self.type_annotation()
            body = self.block()
            return self._node(ast.LambdaExpr(params=params, return_type=return_type, body=body), tok)

        tok = self.match(TokenType.NEW)
        if tok:
            class_name = self.expect(TokenType.IDENT, "Expected class name after 'new'").value
            self.expect(TokenType.LPAREN, "Expected '(' after class name")
            args: List[ast.ASTNode] = []
            if self.peek().type != TokenType.RPAREN:
                args.append(self.expression())
                while self.match(TokenType.COMMA):
                    args.append(self.expression())
            self.expect(TokenType.RPAREN, "Expected ')' after arguments")
            return self._node(ast.NewExpr(class_name=class_name, args=args), tok)

        self.error(f"Unexpected token {self.peek().type.name}")

    def previous(self) -> Token:
        return self.tokens[self.pos - 1]


def parse(tokens: List[Token]) -> ast.Program:
    return Parser(tokens).parse()
