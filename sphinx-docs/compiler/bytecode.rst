字节码与编译器
==============

``jaon/compiler.py`` 将类型检查后的 AST 编译为自定义 Bytecode，
存储在 ``jaon/bytecode.py`` 定义的 ``CodeObject`` 中。

核心指令
--------

==================  ======================================================
指令                 说明
==================  ======================================================
``LOAD_CONST``      加载常量到栈
``LOAD_NAME``       从全局作用域加载名称
``STORE_NAME``      存储到全局作用域
``LOAD_FAST``       从局部变量加载
``STORE_FAST``      存储到局部变量
``LOAD_ATTR``       读取对象属性
``STORE_ATTR``      写入对象属性
``LOAD_INDEX``      读取索引值
``STORE_INDEX``     写入索引值
``BUILD_LIST``      构造列表
``BUILD_DICT``      构造字典
``BINARY_OP``       二元运算
``UNARY_OP``        一元运算
``COMPARE_OP``      比较运算
``JUMP``            无条件跳转
``JUMP_IF_FALSE``   条件跳转
``CALL``            函数调用
``RETURN_VALUE``    带值返回
``MAKE_FUNCTION``   构造函数对象
``BUILD_CLASS``     构造类对象
``NEW_OBJECT``      创建对象实例
``GET_ITER``        获取迭代器
``FOR_ITER``        迭代
``TRY_BEGIN``       异常处理块开始
``THROW``           抛出异常
==================  ======================================================

查看字节码
----------

.. code-block:: bash

    python -m jaon dis examples/control_flow.jaon
