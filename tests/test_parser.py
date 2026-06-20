import unittest

from jaon.lexer import tokenize
from jaon.parser import parse
from jaon import ast_nodes as ast


class ParserTest(unittest.TestCase):
    def parse(self, source: str):
        return parse(tokenize(source))

    def test_hello(self):
        program = self.parse('println("Hello");')
        self.assertEqual(len(program.statements), 1)
        self.assertIsInstance(program.statements[0], ast.ExprStmt)

    def test_var_decl(self):
        program = self.parse("var x: Int = 10;")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.VarDecl)
        self.assertEqual(stmt.name, "x")
        self.assertEqual(stmt.var_type.name, "Int")

    def test_function(self):
        program = self.parse("fun add(a: Int, b: Int): Int { return a + b; }")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.FunctionDef)
        self.assertEqual(stmt.name, "add")
        self.assertEqual(len(stmt.params), 2)
        self.assertEqual(stmt.return_type.name, "Int")

    def test_class(self):
        program = self.parse("class Point { var x: Int = 0; constructor() {} }")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.ClassDef)
        self.assertEqual(stmt.name, "Point")

    def test_if(self):
        program = self.parse("if (x) { y = 1; } elif (z) { y = 2; } else { y = 3; }")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.IfStmt)
        self.assertEqual(len(stmt.elifs), 1)
        self.assertIsNotNone(stmt.else_block)

    def test_for(self):
        program = self.parse("for (i in [1, 2, 3]) { println(i); }")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ast.ForStmt)
        self.assertEqual(stmt.var_name, "i")


if __name__ == "__main__":
    unittest.main()
