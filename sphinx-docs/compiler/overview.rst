架构概览
========

Jaon 编译器从源代码到执行结果经历以下阶段：

.. code-block:: text

    .jaon 源码
       │
       ▼
    Lexer（词法分析）
       │ Token 流
       ▼
    Parser（语法分析）
       │ AST
       ▼
    Analyzer（语义分析）
       │ 类型检查后的 AST
       ▼
    Compiler（字节码编译）
       │ Bytecode
       ▼
    VM（虚拟机执行）
       │ 运行结果
       ▼
    输出

各阶段说明
----------

1. **Lexer** 将字符流转换为 Token 流，同时处理注释、字符串转义等。
2. **Parser** 使用递归下降法构建抽象语法树（AST）。
3. **Analyzer** 进行类型检查、作用域解析和类成员解析。
4. **Compiler** 将 AST 编译为自定义 Bytecode，生成 ``CodeObject``。
5. **VM** 作为栈式虚拟机解释执行 Bytecode。

这种设计便于独立测试和扩展：例如新增语法只需修改 Parser 和 Analyzer，
新增执行语义只需修改 Compiler 和 VM。
