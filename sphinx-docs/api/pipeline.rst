完整流程
========

将 Jaon 源码编译并执行的完整流程如下：

.. code-block:: python

    from jaon.lexer import tokenize
    from jaon.parser import parse
    from jaon.analyzer import analyze
    from jaon.compiler import compile_program
    from jaon.vm import execute

    source = 'println("Hello, Jaon!");'

    tokens = tokenize(source)
    program = parse(tokens)
    analyze(program)
    compiler = compile_program(program)
    execute(compiler.module_code)

各模块职责
----------

- ``jaon.lexer.tokenize``：源码 → Token 列表
- ``jaon.parser.parse``：Token 列表 → AST
- ``jaon.analyzer.analyze``：AST 类型检查
- ``jaon.compiler.compile_program``：AST → 编译器对象（含 Bytecode）
- ``jaon.vm.execute``：Bytecode → 执行结果
