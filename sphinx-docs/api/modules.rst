模块说明
========

``jaon.lexer``
----------------

词法分析模块，提供 ``tokenize`` 函数。

``jaon.parser``
-----------------

语法分析模块，提供 ``parse`` 函数。

``jaon.analyzer``
-------------------

语义分析模块，提供 ``analyze`` 函数及类型相关错误。

``jaon.compiler``
-------------------

字节码编译模块，提供 ``compile_program`` 函数。

``jaon.vm``
-------------

虚拟机执行模块，提供 ``execute`` 函数。

``jaon.builtins``
-------------------

内建函数实现，如 ``print``、``println``、``len``、``range`` 等。

``jaon.cli``
--------------

命令行接口，提供 ``main`` 入口函数。
