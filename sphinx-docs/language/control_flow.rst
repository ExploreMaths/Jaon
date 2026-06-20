控制流
======

条件语句
--------

``if`` 语句支持 ``elif`` 和 ``else``::

    if (x > 0) {
        println("positive");
    } elif (x < 0) {
        println("negative");
    } else {
        println("zero");
    }

条件表达式可以使用任意类型，运行时按 Python 风格判断真假：

- ``null``、``false``、空字符串、空列表、空字典、数字 ``0`` 为假
- 其余值为真


循环
----

``while`` 循环::

    var i = 0;
    while (i < 10) {
        println(i);
        i = i + 1;
    }

``for ... in`` 循环用于遍历列表、字符串或字典::

    for (n in [1, 2, 3]) {
        println(n);
    }

    for (ch in "abc") {
        println(ch);
    }


跳转语句
--------

``break`` 和 ``continue`` 用于循环控制::

    for (n in [1, 2, 3, 4, 5]) {
        if (n == 3) {
            break;
        }
        println(n);
    }

    for (n in [1, 2, 3, 4, 5]) {
        if (n == 3) {
            continue;
        }
        println(n);
    }


返回语句
--------

``return`` 用于从函数返回结果::

    fun square(x: Int): Int {
        return x * x;
    }
