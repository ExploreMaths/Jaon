Jaon 编程语言文档
===================

**Jaon** 是一门融合 Python 简洁性与 Java 严谨性的实验性编程语言。

本仓库从零实现了 Jaon 的完整工具链：词法分析器、语法分析器、语义分析器、
Bytecode 编译器以及栈式虚拟机。所有源代码文件使用自定义后缀 ``.jaon``。

.. toctree::
   :maxdepth: 2
   :caption: 目录

   installation
   quickstart
   language/index
   compiler/index
   examples
   api/index
   contributing


快速开始
--------

安装 Python 3 后，直接在项目根目录执行::

    python -m jaon run examples/hello.jaon

或进入交互式 REPL::

    python -m jaon repl


特性概览
--------

- **静态类型 + 类型推断**：参数与返回值需显式声明，局部变量可省略类型。
- **类与继承**：支持构造器、字段、方法、访问控制（``public`` / ``private``）。
- **简洁语法**：Python 风格的关键字配合 Java 风格的 ``{}`` 块结构。
- **内建集合**：``List``、``Dict``、``String`` 及常用方法。
- **异常处理**：``try`` / ``catch`` / ``throw``。
- **自定义编译器**：完整的前端与后端实现。


索引
----

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
