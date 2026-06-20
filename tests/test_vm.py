import io
import sys
import unittest

from jaon.lexer import tokenize
from jaon.parser import parse
from jaon.analyzer import analyze
from jaon.compiler import compile_program
from jaon.vm import execute


class VMTest(unittest.TestCase):
    def run_source(self, source: str) -> str:
        tokens = tokenize(source)
        program = parse(tokens)
        analyze(program)
        compiler = compile_program(program)

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            execute(compiler.module_code)
            return sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

    def test_arithmetic(self):
        out = self.run_source("println(2 + 3 * 4);")
        self.assertEqual(out.strip(), "14")

    def test_function(self):
        out = self.run_source("fun double(x: Int): Int { return x * 2; } println(double(5));")
        self.assertEqual(out.strip(), "10")

    def test_recursion(self):
        out = self.run_source(
            "fun fact(n: Int): Int { "
            "if (n <= 1) { return 1; } "
            "return n * fact(n - 1); "
            "} println(fact(5));"
        )
        self.assertEqual(out.strip(), "120")

    def test_list(self):
        out = self.run_source(
            "var xs = [1, 2, 3]; "
            "println(xs[1]); xs[1] = 99; println(xs[1]);"
        )
        self.assertEqual(out.strip(), "2\n99")

    def test_class(self):
        out = self.run_source(
            "class Box { var v: Int = 0; "
            "public fun set(x: Int): Int { this.v = x; return this.v; } } "
            "var b = new Box(); println(b.set(42));"
        )
        self.assertEqual(out.strip(), "42")

    def test_for_loop(self):
        out = self.run_source("var s = 0; for (i in [1, 2, 3, 4]) { s = s + i; } println(s);")
        self.assertEqual(out.strip(), "10")


if __name__ == "__main__":
    unittest.main()
