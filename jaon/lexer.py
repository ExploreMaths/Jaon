"""Lexer for the Jaon programming language."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class TokenType(Enum):
    # Literals
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOL = auto()
    NULL = auto()

    # Identifiers
    IDENT = auto()

    # Keywords
    VAR = auto()
    VAL = auto()
    FUN = auto()
    CLASS = auto()
    EXTENDS = auto()
    CONSTRUCTOR = auto()
    PUBLIC = auto()
    PRIVATE = auto()
    STATIC = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    TRY = auto()
    CATCH = auto()
    FINALLY = auto()
    THROW = auto()
    IMPORT = auto()
    NEW = auto()
    THIS = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    TRUE = auto()
    FALSE = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    ASSIGN = auto()
    ARROW = auto()

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    SEMICOLON = auto()
    COLON = auto()
    COMMA = auto()
    DOT = auto()

    EOF = auto()


KEYWORDS = {
    "var": TokenType.VAR,
    "val": TokenType.VAL,
    "fun": TokenType.FUN,
    "class": TokenType.CLASS,
    "extends": TokenType.EXTENDS,
    "constructor": TokenType.CONSTRUCTOR,
    "public": TokenType.PUBLIC,
    "private": TokenType.PRIVATE,
    "static": TokenType.STATIC,
    "if": TokenType.IF,
    "elif": TokenType.ELIF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "in": TokenType.IN,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "return": TokenType.RETURN,
    "try": TokenType.TRY,
    "catch": TokenType.CATCH,
    "finally": TokenType.FINALLY,
    "throw": TokenType.THROW,
    "import": TokenType.IMPORT,
    "new": TokenType.NEW,
    "this": TokenType.THIS,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "null": TokenType.NULL,
}


@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def error(self, message: str) -> None:
        raise LexerError(f"{message} at line {self.line}, column {self.column}")

    def peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx >= len(self.source):
            return "\0"
        return self.source[idx]

    def advance(self) -> str:
        ch = self.peek()
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def match(self, expected: str) -> bool:
        if self.peek() == expected:
            self.advance()
            return True
        return False

    def skip_whitespace(self) -> None:
        while self.peek() in " \t\r\n":
            self.advance()

    def skip_comment(self) -> None:
        if self.peek() == "/" and self.peek(1) == "/":
            while self.peek() not in "\n\0":
                self.advance()
        elif self.peek() == "/" and self.peek(1) == "*":
            self.advance()
            self.advance()
            while not (self.peek() == "*" and self.peek(1) == "/"):
                if self.peek() == "\0":
                    self.error("Unterminated block comment")
                self.advance()
            self.advance()
            self.advance()

    def read_string(self) -> str:
        quote = self.advance()
        value = ""
        while self.peek() != quote:
            if self.peek() == "\0":
                self.error("Unterminated string")
            if self.peek() == "\\":
                self.advance()
                esc = self.advance()
                mapping = {
                    "n": "\n",
                    "t": "\t",
                    "r": "\r",
                    "\\": "\\",
                    '"': '"',
                    "'": "'",
                }
                value += mapping.get(esc, esc)
            else:
                value += self.advance()
        self.advance()
        return value

    def read_number(self) -> Token:
        start_line, start_col = self.line, self.column
        value = ""
        while self.peek().isdigit():
            value += self.advance()
        if self.peek() == "." and self.peek(1).isdigit():
            value += self.advance()
            while self.peek().isdigit():
                value += self.advance()
            return Token(TokenType.FLOAT, float(value), start_line, start_col)
        return Token(TokenType.INT, int(value), start_line, start_col)

    def read_identifier(self) -> Token:
        start_line, start_col = self.line, self.column
        value = ""
        while self.peek().isalnum() or self.peek() == "_":
            value += self.advance()
        token_type = KEYWORDS.get(value, TokenType.IDENT)
        if token_type in (TokenType.TRUE, TokenType.FALSE):
            return Token(TokenType.BOOL, value == "true", start_line, start_col)
        if token_type == TokenType.NULL:
            return Token(TokenType.NULL, None, start_line, start_col)
        return Token(token_type, value, start_line, start_col)

    def add_token(self, token_type: TokenType, value: any = None) -> None:
        self.tokens.append(Token(token_type, value, self.line, self.column))

    def scan_token(self) -> bool:
        self.skip_whitespace()
        while self.peek() == "/" and self.peek(1) in "/*":
            self.skip_comment()
            self.skip_whitespace()

        start_line, start_col = self.line, self.column
        ch = self.peek()

        if ch == "\0":
            self.tokens.append(Token(TokenType.EOF, None, start_line, start_col))
            return False

        # Single-character tokens
        single_tokens = {
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
            "%": TokenType.PERCENT,
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            "{": TokenType.LBRACE,
            "}": TokenType.RBRACE,
            "[": TokenType.LBRACKET,
            "]": TokenType.RBRACKET,
            ";": TokenType.SEMICOLON,
            ":": TokenType.COLON,
            ",": TokenType.COMMA,
            ".": TokenType.DOT,
        }

        if ch in single_tokens:
            self.advance()
            # Check arrow ->
            if ch == "-" and self.peek() == ">":
                self.advance()
                self.tokens.append(Token(TokenType.ARROW, "->", start_line, start_col))
            else:
                self.tokens.append(Token(single_tokens[ch], ch, start_line, start_col))
            return True

        if ch == "/":
            self.advance()
            self.tokens.append(Token(TokenType.SLASH, "/", start_line, start_col))
            return True

        if ch == "=":
            self.advance()
            if self.match("="):
                self.tokens.append(Token(TokenType.EQ, "==", start_line, start_col))
            else:
                self.tokens.append(Token(TokenType.ASSIGN, "=", start_line, start_col))
            return True

        if ch == "!":
            self.advance()
            if self.match("="):
                self.tokens.append(Token(TokenType.NEQ, "!=", start_line, start_col))
            else:
                self.error("Unexpected '!'")
            return True

        if ch == "<":
            self.advance()
            if self.match("="):
                self.tokens.append(Token(TokenType.LE, "<=", start_line, start_col))
            else:
                self.tokens.append(Token(TokenType.LT, "<", start_line, start_col))
            return True

        if ch == ">":
            self.advance()
            if self.match("="):
                self.tokens.append(Token(TokenType.GE, ">=", start_line, start_col))
            else:
                self.tokens.append(Token(TokenType.GT, ">", start_line, start_col))
            return True

        if ch in ('"', "'"):
            value = self.read_string()
            self.tokens.append(Token(TokenType.STRING, value, start_line, start_col))
            return True

        if ch.isdigit():
            self.tokens.append(self.read_number())
            return True

        if ch.isalpha() or ch == "_":
            self.tokens.append(self.read_identifier())
            return True

        self.error(f"Unexpected character '{ch}'")
        return False

    def tokenize(self) -> List[Token]:
        while self.scan_token():
            pass
        return self.tokens


def tokenize(source: str) -> List[Token]:
    return Lexer(source).tokenize()
