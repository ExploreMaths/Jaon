虚拟机
======

``jaon/vm.py`` 实现了一个栈式虚拟机，负责解释执行 Bytecode。

核心组件
--------

- **操作数栈**：存放运算过程中的中间值
- **调用帧（CallFrame）**：每个函数调用对应一个帧，包含局部变量、指令指针等
- **全局环境**：存放顶层变量、类、内建函数
- **类与实例模型**：``JaonClass``、``JaonInstance``、``JaonMethod``

对象模型
--------

- ``JaonFunction``：用户定义函数
- ``JaonMethod``：绑定到实例的方法
- ``JaonClass``：类定义，包含方法与字段
- ``JaonInstance``：类的实例

执行流程
--------

1. 从模块 ``CodeObject`` 创建初始调用帧
2. 循环取出指令并执行
3. 函数调用时压入新帧
4. 返回时弹出帧并将结果压入调用者栈
5. 遇到 ``THROW`` 或运行时错误时沿调用栈传播异常

使用示例
--------

.. code-block:: python

    from jaon.lexer import tokenize
    from jaon.parser import parse
    from jaon.analyzer import analyze
    from jaon.compiler import compile_program
    from jaon.vm import execute

    tokens = tokenize('println("Hello");')
    program = parse(tokens)
    analyze(program)
    compiler = compile_program(program)
    execute(compiler.module_code)
