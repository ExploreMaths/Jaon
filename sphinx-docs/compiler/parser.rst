语法分析器
==========

``helios/parser.py`` 使用递归下降算法将 Token 流解析为抽象语法树（AST）。

支持的语法结构
--------------

- 变量声明与赋值
- 函数定义与调用
- 类、继承、构造器、方法
- 条件语句与循环
- 异常处理
- 列表、字典字面量
- 成员访问与索引访问

使用示例
--------

.. code-block:: python

    from helios.lexer import tokenize
    from helios.parser import parse

    tokens = tokenize('fun add(a: Int, b: Int): Int { return a + b; }')
    program = parse(tokens)

AST 节点定义位于 ``helios/ast_nodes.py``。
