快速开始
========

安装 Helios 的方法详见 :doc:`installation`，本节假设已完成安装。


运行 Helios 程序
----------------

Helios 提供两种命令行入口： ``python -m helios`` 或直接 ``helios``。

运行示例程序::

    python -m helios run examples/hello.helios

在 Windows 上若已通过安装程序关联 `.helios` 文件，直接双击示例文件即可执行。

输出::

    Hello, Helios!


进入 REPL
---------

交互式解释器支持单行与多行输入::

    python -m helios repl

示例会话::

    Helios 0.0.1 REPL
    Type 'exit' or press Ctrl+C to quit.

    >>> var x = 10;
    >>> println(x * 2);
    20
    >>> exit
    Goodbye.


查看字节码
----------

使用 ``dis`` 子命令查看编译生成的字节码::

    python -m helios dis examples/control_flow.helios


运行测试
--------

Helios 附带单元测试套件::

    python -m unittest discover tests

或::

    python scripts/run_tests.py
