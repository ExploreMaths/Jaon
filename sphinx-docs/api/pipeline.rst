完整流程
========

将 Helios 源码编译并执行的完整流程如下：

.. code-block:: python

    from helios.lexer import tokenize
    from helios.parser import parse
    from helios.analyzer import analyze
    from helios.compiler import compile_program
    from helios.vm import execute

    source = 'println("Hello, Helios!");'

    tokens = tokenize(source)
    program = parse(tokens)
    analyze(program)
    compiler = compile_program(program)
    execute(compiler.module_code)

各模块职责
----------

- ``helios.lexer.tokenize``：源码 → Token 列表
- ``helios.parser.parse``：Token 列表 → AST
- ``helios.analyzer.analyze``：AST 类型检查
- ``helios.compiler.compile_program``：AST → 编译器对象（含 Bytecode）
- ``helios.vm.execute``：Bytecode → 执行结果
