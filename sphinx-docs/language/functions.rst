函数
====

函数定义
--------

使用 ``fun`` 关键字定义函数::

    fun greet(name: String): String {
        return "Hello, " + name;
    }

无返回值函数可省略返回类型::

    fun sayHi(): {
        println("Hi!");
    }


参数与返回值
------------

参数必须声明类型，返回值类型在参数列表后以 ``:`` 标注::

    fun max(a: Int, b: Int): Int {
        if (a > b) {
            return a;
        }
        return b;
    }


递归
----

函数支持递归调用::

    fun factorial(n: Int): Int {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }


匿名函数
--------

Jaon 支持匿名函数表达式，可赋值给变量或作为参数传递::

    var double = fun(x: Int): Int { return x * 2; };
    println(double(5));  // 10

作为高阶函数参数::

    fun apply(f: Any, x: Int): Int {
        return f(x);
    }

    println(apply(double, 7));  // 14


作用域
------

函数参数和函数体内声明的变量为局部变量。顶层函数与类存储在全局作用域，
因此支持递归和跨函数引用。
