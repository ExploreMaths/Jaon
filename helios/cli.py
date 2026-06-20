"""Command-line interface for the Helios language."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .lexer import tokenize, LexerError
from .parser import parse, ParseError
from .analyzer import analyze, HeliosTypeError
from .compiler import compile_program
from .vm import execute


def run_file(path: str) -> None:
    source = Path(path).read_text(encoding="utf-8")
    tokens = tokenize(source)
    program = parse(tokens)
    analyze(program)
    compiler = compile_program(program)
    execute(compiler.module_code)


def run_repl() -> None:
    print(f"Helios {__version__} REPL")
    print("Type 'exit' or press Ctrl+C to quit.\n")

    while True:
        try:
            line = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        stripped = line.strip()
        if stripped == "exit":
            print("Goodbye.")
            break
        if not stripped:
            continue

        # Allow multiline input if braces are unbalanced
        source = line
        while source.count("{") > source.count("}"):
            try:
                extra = input("... ")
            except (EOFError, KeyboardInterrupt):
                break
            source += "\n" + extra

        try:
            tokens = tokenize(source)
            program = parse(tokens)
            analyze(program)
            compiler = compile_program(program)
            result = execute(compiler.module_code)
            if result is not None:
                print(result)
        except (LexerError, ParseError, HeliosTypeError) as e:
            print(f"Error: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Runtime error: {e}", file=sys.stderr)


def disassemble_file(path: str) -> None:
    source = Path(path).read_text(encoding="utf-8")
    tokens = tokenize(source)
    program = parse(tokens)
    compiler = compile_program(program)

    def show_code(code, indent=0):
        prefix = "  " * indent
        print(f"{prefix}Code: {code.name} (params={code.param_count}, locals={code.locals})")
        for i, instr in enumerate(code.instructions):
            print(f"{prefix}  {i:04d}: {instr}")
        for const in code.constants:
            if hasattr(const, "instructions"):
                show_code(const, indent + 1)
            elif hasattr(const, "methods"):
                print(f"{prefix}  Class {const.name} methods: {list(const.methods.keys())}")

    show_code(compiler.module_code)


def main(argv: list = None) -> int:
    parser = argparse.ArgumentParser(prog="helios", description="Helios programming language")
    parser.add_argument("--version", action="version", version=f"Helios {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a Helios source file")
    run_parser.add_argument("file", help="Path to .helios file")

    subparsers.add_parser("repl", help="Start interactive REPL")

    dis_parser = subparsers.add_parser("dis", help="Disassemble a Helios source file")
    dis_parser.add_argument("file", help="Path to .helios file")

    args = parser.parse_args(argv)

    if args.command == "run":
        try:
            run_file(args.file)
        except (LexerError, ParseError, HeliosTypeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Runtime error: {e}", file=sys.stderr)
            return 1
        return 0

    if args.command == "repl":
        run_repl()
        return 0

    if args.command == "dis":
        try:
            disassemble_file(args.file)
        except (LexerError, ParseError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
