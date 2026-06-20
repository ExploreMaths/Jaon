import unittest

from jaon.lexer import tokenize
from jaon.parser import parse
from jaon.analyzer import analyze, JaonTypeError


class AnalyzerTest(unittest.TestCase):
    def check(self, source: str):
        tokens = tokenize(source)
        program = parse(tokens)
        analyze(program)

    def test_valid_program(self):
        self.check("var x: Int = 10; var y = x + 5;")

    def test_function_return(self):
        self.check("fun add(a: Int, b: Int): Int { return a + b; }")

    def test_class(self):
        self.check("class Point { var x: Int = 0; constructor() {} public fun getX(): Int { return this.x; } }")

    def test_type_error(self):
        with self.assertRaises(JaonTypeError):
            self.check("var x: Int = \"hello\";")

    def test_undefined_variable(self):
        with self.assertRaises(JaonTypeError):
            self.check("println(z);")


if __name__ == "__main__":
    unittest.main()
