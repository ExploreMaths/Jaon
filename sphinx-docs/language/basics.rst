基础语法
========

注释
----

Jaon 支持两种注释形式。

单行注释以 ``//`` 开头::

    // 这是一行注释
    var x = 10;  // 行尾注释

块注释使用 ``/* */`` 包裹::

    /*
       这是多行注释
       可以跨越多行
    */
    var y = 20;


语句与分号
----------

Jaon 是语句式语言，每条语句以分号 ``;`` 结尾。块由花括号 ``{}`` 界定，
不依赖缩进::

    if (x > 0) {
        println("positive");
    }


标识符
------

标识符以字母或下划线开头，后可接字母、数字或下划线::

    var name = "Jaon";
    var _private = 1;
    var camelCase = true;


关键字
------

保留关键字包括：

``var``、``val``、``fun``、``class``、``extends``、``constructor``、
``public``、``private``、``static``、
``if``、``elif``、``else``、``while``、``for``、``in``、
``break``、``continue``、``return``、
``try``、``catch``、``finally``、``throw``、
``import``、``new``、``this``、
``and``、``or``、``not``、``true``、``false``、``null``。


字面量
------

整数::

    var n = 42;

浮点数::

    var pi = 3.14;

字符串::

    var s = "hello";

布尔值::

    var ok = true;
    var no = false;

空值::

    var empty = null;
