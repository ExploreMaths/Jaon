贡献指南
========

开发流程
--------

1. 在 ``jaon/`` 中修改源码。
2. 在 ``tests/`` 中添加或更新单元测试。
3. 在 ``examples/`` 中添加示例程序。
4. 更新 ``sphinx-docs/`` 中的文档。
5. 运行测试确保全部通过::

       python -m unittest discover tests

新增语法特性
------------

新增语法通常需要修改以下文件：

1. ``jaon/lexer.py``：添加 Token 类型
2. ``jaon/ast_nodes.py``：添加 AST 节点
3. ``jaon/parser.py``：添加解析规则
4. ``jaon/analyzer.py``：添加类型检查
5. ``jaon/compiler.py``：添加字节码生成
6. ``jaon/vm.py``：添加字节码执行
7. ``tests/``：添加测试
8. ``sphinx-docs/``：更新文档

构建文档
--------

在 ``sphinx-docs/`` 目录下执行::

    make html

生成的 HTML 位于 ``sphinx-docs/_build/html/``。
