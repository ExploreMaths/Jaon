"""Recursive-descent parser for the Helios programming language."""
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

    # ------------------------------------------------------------------
    # Program
    # ------------------------------------------------------------------

    def parse(self) -> ast.Program:
        imports: List[ast.ImportStmt] = []
        statements: List[ast.ASTNode] = []
        while not self.is_at_end():
            if self.peek().type == TokenType.IMPORT:
                imports.append(self.import_stmt())
            else:
                statements.append(self.declaration())
        return ast.Program(imports=imports, statements=statements)

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
        self.advance()  # fun
        name = self.expect(TokenType.IDENT, "Expected function name").value
        params = self.parameters()
        return_type: Optional[ast.TypeNode] = None
        if self.match(TokenType.COLON):
            return_type = self.type_annotation()
        body = self.block()
        return ast.FunctionDef(name=name, params=params, return_type=return_type, body=body)

    def class_declaration(self) -> ast.ClassDef:
        self.advance()  # class
        name = self.expect(TokenType.IDENT, "Expected class name").value
        base: Optional[str] = None
        if self.match(TokenType.EXTENDS):
            base = self.expect(TokenType.IDENT, "Expected base class name").value
        self.expect(TokenType.LBRACE, "Expected '{' before class body")
        members: List[ast.ASTNode] = []
        while self.peek().type != TokenType.RBRACE and not self.is_at_end():
            members.append(self.class_member())
        self.expect(TokenType.RBRACE, "Expected '}' after class body")
        return ast.ClassDef(name=name, base=base, members=members)

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
            return ast.FieldDecl(
                access=access,
                name=decl.name,
                field_type=decl.var_type or ast.TypeNode("Any"),
                initializer=decl.initializer,
            )

        if self.peek().type == TokenType.FUN:
            self.advance()
            name = self.expect(TokenType.IDENT, "Expected method name").value
            params = self.parameters()
            return_type: Optional[ast.TypeNode] = None
            if self.match(TokenType.COLON):
                return_type = self.type_annotation()
            body = self.block()
            return ast.MethodDef(
                access=access,
                name=name,
                params=params,
                return_type=return_type,
                body=body,
                is_static=is_static,
            )

        self.error("Expected class member")

    def constructor_definition(self) -> ast.ConstructorDef:
        self.advance()  # constructor
        params = self.parameters()
        body = self.block()
        return ast.ConstructorDef(params=params, body=body)

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
        name = self.expect(TokenType.IDENT, "Expected parameter name").value
        self.expect(TokenType.COLON, "Expected ':' after parameter name")
        param_type = self.type_annotation()
        return ast.Parameter(name=name, param_type=param_type)

    def var_declaration(self) -> ast.VarDecl:
        is_const = self.peek().type == TokenType.VAL
        self.advance()  # var / val
        name = self.expect(TokenType.IDENT, "Expected variable name").value
        var_type: Optional[ast.TypeNode] = None
        if self.match(TokenType.COLON):
            var_type = self.type_annotation()
        self.expect(TokenType.ASSIGN, "Expected '=' after variable name")
        initializer = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return ast.VarDecl(name=name, var_type=var_type, initializer=initializer, is_const=is_const)

    def type_annotation(self) -> ast.TypeNode:
        name = self.expect(TokenType.IDENT, "Expected type name").value
        params: List[ast.TypeNode] = []
        if self.match(TokenType.LT):
            params.append(self.type_annotation())
            while self.match(TokenType.COMMA):
                params.append(self.type_annotation())
            self.expect(TokenType.GT, "Expected '>' after type parameters")
        return ast.TypeNode(name=name, params=params)

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
            self.advance()
            self.expect(TokenType.SEMICOLON, "Expected ';' after break")
            return ast.BreakStmt()
        if self.peek().type == TokenType.CONTINUE:
            self.advance()
            self.expect(TokenType.SEMICOLON, "Expected ';' after continue")
            return ast.ContinueStmt()
        if self.peek().type == TokenType.TRY:
            return self.try_statement()
        if self.peek().type == TokenType.THROW:
            return self.throw_statement()
        return self.expr_statement()

    def import_stmt(self) -> ast.ImportStmt:
        self.advance()  # import
        path = [self.expect(TokenType.IDENT, "Expected import name").value]
        while self.match(TokenType.DOT):
            path.append(self.expect(TokenType.IDENT, "Expected import name").value)
        self.expect(TokenType.SEMICOLON, "Expected ';' after import")
        return ast.ImportStmt(path=path)

    def block(self) -> ast.Block:
        self.expect(TokenType.LBRACE, "Expected '{'")
        statements: List[ast.ASTNode] = []
        while self.peek().type != TokenType.RBRACE and not self.is_at_end():
            statements.append(self.declaration())
        self.expect(TokenType.RBRACE, "Expected '}'")
        return ast.Block(statements=statements)

    def if_statement(self) -> ast.IfStmt:
        self.advance()  # if
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
        return ast.IfStmt(
            condition=condition,
            then_block=then_block,
            elifs=elifs,
            else_block=else_block,
        )

    def while_statement(self) -> ast.WhileStmt:
        self.advance()  # while
        condition = self.expression()
        body = self.block()
        return ast.WhileStmt(condition=condition, body=body)

    def for_statement(self) -> ast.ForStmt:
        self.advance()  # for
        self.expect(TokenType.LPAREN, "Expected '(' after 'for'")
        var_name: Optional[str] = None
        if self.peek().type == TokenType.IDENT:
            var_name = self.advance().value
            self.expect(TokenType.IN, "Expected 'in' after loop variable")
        iterable = self.expression()
        self.expect(TokenType.RPAREN, "Expected ')' after for iterable")
        body = self.block()
        return ast.ForStmt(var_name=var_name, iterable=iterable, body=body)

    def return_statement(self) -> ast.ReturnStmt:
        self.advance()  # return
        value: Optional[ast.ASTNode] = None
        if self.peek().type != TokenType.SEMICOLON:
            value = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after return")
        return ast.ReturnStmt(value=value)

    def try_statement(self) -> ast.TryStmt:
        self.advance()  # try
        try_block = self.block()
        self.expect(TokenType.CATCH, "Expected 'catch'")
        self.expect(TokenType.LPAREN, "Expected '(' after 'catch'")
        catch_var = self.expect(TokenType.IDENT, "Expected catch variable").value
        self.expect(TokenType.RPAREN, "Expected ')' after catch variable")
        catch_block = self.block()
        finally_block: Optional[ast.Block] = None
        if self.match(TokenType.FINALLY):
            finally_block = self.block()
        return ast.TryStmt(
            try_block=try_block,
            catch_var=catch_var,
            catch_block=catch_block,
            finally_block=finally_block,
        )

    def throw_statement(self) -> ast.ThrowStmt:
        self.advance()  # throw
        value = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after throw")
        return ast.ThrowStmt(value=value)

    def expr_statement(self) -> ast.ExprStmt:
        expr = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after expression")
        return ast.ExprStmt(expr=expr)

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
                return ast.Assignment(target=expr, value=value)
            self.error("Invalid assignment target")
        return expr

    def or_expr(self) -> ast.ASTNode:
        left = self.and_expr()
        while self.match(TokenType.OR):
            right = self.and_expr()
            left = ast.BinaryOp(op="or", left=left, right=right)
        return left

    def and_expr(self) -> ast.ASTNode:
        left = self.equality()
        while self.match(TokenType.AND):
            right = self.equality()
            left = ast.BinaryOp(op="and", left=left, right=right)
        return left

    def equality(self) -> ast.ASTNode:
        left = self.comparison()
        while True:
            if self.match(TokenType.EQ):
                right = self.comparison()
                left = ast.BinaryOp(op="==", left=left, right=right)
            elif self.match(TokenType.NEQ):
                right = self.comparison()
                left = ast.BinaryOp(op="!=", left=left, right=right)
            else:
                break
        return left

    def comparison(self) -> ast.ASTNode:
        left = self.term()
        while True:
            if self.match(TokenType.LT):
                right = self.term()
                left = ast.BinaryOp(op="<", left=left, right=right)
            elif self.match(TokenType.GT):
                right = self.term()
                left = ast.BinaryOp(op=">", left=left, right=right)
            elif self.match(TokenType.LE):
                right = self.term()
                left = ast.BinaryOp(op="<=", left=left, right=right)
            elif self.match(TokenType.GE):
                right = self.term()
                left = ast.BinaryOp(op=">=", left=left, right=right)
            else:
                break
        return left

    def term(self) -> ast.ASTNode:
        left = self.factor()
        while True:
            if self.match(TokenType.PLUS):
                right = self.factor()
                left = ast.BinaryOp(op="+", left=left, right=right)
            elif self.match(TokenType.MINUS):
                right = self.factor()
                left = ast.BinaryOp(op="-", left=left, right=right)
            else:
                break
        return left

    def factor(self) -> ast.ASTNode:
        left = self.unary()
        while True:
            if self.match(TokenType.STAR):
                right = self.unary()
                left = ast.BinaryOp(op="*", left=left, right=right)
            elif self.match(TokenType.SLASH):
                right = self.unary()
                left = ast.BinaryOp(op="/", left=left, right=right)
            elif self.match(TokenType.PERCENT):
                right = self.unary()
                left = ast.BinaryOp(op="%", left=left, right=right)
            else:
                break
        return left

    def unary(self) -> ast.ASTNode:
        if self.match(TokenType.MINUS):
            return ast.UnaryOp(op="-", operand=self.unary())
        if self.match(TokenType.NOT):
            return ast.UnaryOp(op="not", operand=self.unary())
        return self.postfix()

    def postfix(self) -> ast.ASTNode:
        expr = self.primary()
        while True:
            if self.match(TokenType.LPAREN):
                args: List[ast.ASTNode] = []
                if self.peek().type != TokenType.RPAREN:
                    args.append(self.expression())
                    while self.match(TokenType.COMMA):
                        args.append(self.expression())
                self.expect(TokenType.RPAREN, "Expected ')' after arguments")
                expr = ast.CallExpr(callee=expr, args=args)
            elif self.match(TokenType.DOT):
                member = self.expect(TokenType.IDENT, "Expected member name").value
                expr = ast.MemberExpr(obj=expr, member=member)
            elif self.match(TokenType.LBRACKET):
                index = self.expression()
                self.expect(TokenType.RBRACKET, "Expected ']' after index")
                expr = ast.IndexExpr(obj=expr, index=index)
            else:
                break
        return expr

    def primary(self) -> ast.ASTNode:
        if self.match(TokenType.INT):
            return ast.IntegerLiteral(value=self.previous().value)
        if self.match(TokenType.FLOAT):
            return ast.FloatLiteral(value=self.previous().value)
        if self.match(TokenType.STRING):
            return ast.StringLiteral(value=self.previous().value)
        if self.match(TokenType.BOOL):
            return ast.BooleanLiteral(value=self.previous().value)
        if self.match(TokenType.NULL):
            return ast.NullLiteral()

        if self.match(TokenType.IDENT):
            return ast.Identifier(name=self.previous().value)

        if self.match(TokenType.THIS):
            return ast.ThisExpr()

        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.expect(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        if self.match(TokenType.LBRACKET):
            elements: List[ast.ASTNode] = []
            if self.peek().type != TokenType.RBRACKET:
                elements.append(self.expression())
                while self.match(TokenType.COMMA):
                    elements.append(self.expression())
            self.expect(TokenType.RBRACKET, "Expected ']' after list elements")
            return ast.ListLiteral(elements=elements)

        if self.match(TokenType.LBRACE):
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
            return ast.DictLiteral(entries=entries)

        if self.match(TokenType.FUN):
            params = self.parameters()
            return_type: Optional[ast.TypeNode] = None
            if self.match(TokenType.COLON):
                return_type = self.type_annotation()
            body = self.block()
            return ast.LambdaExpr(params=params, return_type=return_type, body=body)

        if self.match(TokenType.NEW):
            class_name = self.expect(TokenType.IDENT, "Expected class name after 'new'").value
            self.expect(TokenType.LPAREN, "Expected '(' after class name")
            args: List[ast.ASTNode] = []
            if self.peek().type != TokenType.RPAREN:
                args.append(self.expression())
                while self.match(TokenType.COMMA):
                    args.append(self.expression())
            self.expect(TokenType.RPAREN, "Expected ')' after arguments")
            return ast.NewExpr(class_name=class_name, args=args)

        self.error(f"Unexpected token {self.peek().type.name}")

    def previous(self) -> Token:
        return self.tokens[self.pos - 1]


def parse(tokens: List[Token]) -> ast.Program:
    return Parser(tokens).parse()
