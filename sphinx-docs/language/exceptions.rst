异常处理
========

抛出异常
--------

使用 ``throw`` 抛出异常，异常值可以是任意类型::

    fun divide(a: Int, b: Int): Int {
        if (b == 0) {
            throw "Division by zero";
        }
        return a / b;
    }


捕获异常
--------

使用 ``try`` / ``catch`` 捕获异常，可配合 ``finally``::

    try {
        var result = divide(10, 0);
        println(result);
    } catch (e) {
        println("Error: " + e);
    } finally {
        println("cleanup");
    }

``finally`` 块无论是否发生异常都会执行。


异常传播
--------

若异常未被捕获，会沿调用栈向上传播，直到被捕获或程序终止。
