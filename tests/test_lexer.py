import unittest

from jaon.lexer import tokenize, TokenType


class LexerTest(unittest.TestCase):
    def test_empty(self):
        tokens = tokenize("")
        self.assertEqual(tokens[-1].type, TokenType.EOF)

    def test_numbers(self):
        tokens = tokenize("42 3.14")
        self.assertEqual(tokens[0].type, TokenType.INT)
        self.assertEqual(tokens[0].value, 42)
        self.assertEqual(tokens[1].type, TokenType.FLOAT)
        self.assertEqual(tokens[1].value, 3.14)

    def test_string(self):
        tokens = tokenize('"hello world"')
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, "hello world")

    def test_keywords(self):
        tokens = tokenize("fun var if else while return true false null")
        types = [t.type for t in tokens[:-1]]
        self.assertEqual(
            types,
            [
                TokenType.FUN,
                TokenType.VAR,
                TokenType.IF,
                TokenType.ELSE,
                TokenType.WHILE,
                TokenType.RETURN,
                TokenType.BOOL,
                TokenType.BOOL,
                TokenType.NULL,
            ],
        )

    def test_operators(self):
        tokens = tokenize("+ - * / == != <= >= < > =")
        types = [t.type for t in tokens[:-1]]
        self.assertEqual(
            types,
            [
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.STAR,
                TokenType.SLASH,
                TokenType.EQ,
                TokenType.NEQ,
                TokenType.LE,
                TokenType.GE,
                TokenType.LT,
                TokenType.GT,
                TokenType.ASSIGN,
            ],
        )

    def test_comments(self):
        tokens = tokenize("// line comment\n42 /* block */ 43")
        self.assertEqual(tokens[0].type, TokenType.INT)
        self.assertEqual(tokens[0].value, 42)
        self.assertEqual(tokens[1].type, TokenType.INT)
        self.assertEqual(tokens[1].value, 43)


if __name__ == "__main__":
    unittest.main()
