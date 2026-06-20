词法分析器
==========

``jaon/lexer.py`` 负责将 ``.jaon`` 源码转换为 Token 流。

主要 Token 类型
---------------

- 字面量：``INT``、``FLOAT``、``STRING``、``BOOL``、``NULL``
- 标识符：``IDENT``
- 关键字：``var``、``fun``、``class``、``if``、``while``、``for``、``return`` 等
- 运算符：``+``、``-``、``*``、``/``、``==``、``!=``、``<=``、``>=``、``<``、``>``、``=``
- 分隔符：``()``、``{}``、``[]``、``;``、``:``、``,``、``.``

使用示例
--------

.. code-block:: python

    from jaon.lexer import tokenize

    tokens = tokenize('var x = 10;')
    for token in tokens:
        print(token)
