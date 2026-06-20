语义分析器
==========

``helios/analyzer.py`` 对 AST 进行类型检查和作用域解析。

主要职责
--------

- 变量、函数、类的作用域管理
- 类型推断与类型兼容性检查
- 函数参数与返回值类型校验
- 类字段和方法访问校验
- 控制流语句（如 ``break`` 是否在循环内）检查

类型系统
--------

分析器内置以下类型：

- 原始类型：``Int``、``Float``、``Bool``、``String``、``Null``、``Any``、``Void``
- 集合类型：``List<T>``、``Dict<K, V>``
- 类类型
- 函数类型

使用示例
--------

.. code-block:: python

    from helios.lexer import tokenize
    from helios.parser import parse
    from helios.analyzer import analyze

    tokens = tokenize('var x: Int = "hello";')
    program = parse(tokens)
    analyze(program)  # 抛出类型错误
