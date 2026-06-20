模块与导入
==========

Helios 支持 ``import`` 语法声明模块依赖::

    import stdio;

当前实现中，``import`` 主要用于表达依赖关系，标准库函数（如 ``print``、
``println`` 等）已通过全局作用域直接可用。

未来计划支持按文件导入用户模块::

    import utils.math;
