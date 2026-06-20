示例程序
========

``examples/`` 目录包含多个可运行的 Jaon 示例程序。

hello.jaon
------------

最基础的 Hello World 程序::

    println("Hello, Jaon!");

运行::

    python -m jaon run examples/hello.jaon


control_flow.jaon
-------------------

展示函数、递归、条件判断与循环::

    fun factorial(n: Int): Int {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }

    println(factorial(5));


classes.jaon
--------------

展示类、继承、构造器与方法::

    class Dog extends Animal {
        constructor(n: String) {
            this.name = n;
        }

        public fun speak(): String {
            return "Woof!";
        }
    }

    var dog = new Dog("Buddy");
    println(dog.speak());


fibonacci.jaon
----------------

递归与迭代实现斐波那契数列::

    fun fib(n: Int): Int {
        if (n <= 1) {
            return n;
        }
        return fib(n - 1) + fib(n - 2);
    }


sorting.jaon
--------------

冒泡排序与列表操作::

    fun bubble_sort(arr: List): List {
        // ...
    }


exceptions.jaon
-----------------

异常抛出与捕获::

    try {
        divide(10, 0);
    } catch (e) {
        println("Error: " + e);
    }


advanced.jaon
---------------

匿名函数、字符串/列表方法、字典、类型查询等综合示例。
