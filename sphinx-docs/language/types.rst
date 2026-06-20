类型系统
========

Jaon 采用静态类型系统，同时支持局部类型推断，兼顾 Java 的严谨与 Python 的简洁。

基本类型
--------

===============  ===================
类型             说明
===============  ===================
``Int``          整数
``Float``        浮点数
``Bool``         布尔值
``String``       字符串
``Null``         空值
``Any``          动态任意类型
``Void``         无返回值
===============  ===================


类型推断
--------

使用 ``var`` 声明变量时，类型可由右侧表达式推断::

    var x = 10;        // Int
    var y = 3.14;      // Float
    var s = "hello";   // String

使用 ``val`` 声明常量，同样支持推断::

    val pi = 3.14159;  // Float


显式类型标注
------------

函数参数和返回值必须显式标注类型::

    fun add(a: Int, b: Int): Int {
        return a + b;
    }

局部变量也可以显式标注::

    var count: Int = 0;
    var ratio: Float = 0.5;


集合类型
--------

列表::

    var nums: List<Int> = [1, 2, 3];

字典::

    var scores: Dict<String, Int> = {"Alice": 90, "Bob": 85};

也可以省略泛型参数，由编译器推断::

    var nums = [1, 2, 3];                    // List<Int>
    var scores = {"Alice": 90, "Bob": 85};   // Dict<String, Int>


类型兼容性
----------

- ``Int`` 可隐式提升为 ``Float``。
- ``Any`` 与所有类型兼容。
- 子类实例可赋值给父类类型变量。
- 带泛型参数的集合可赋值给对应裸类型（如 ``List<Int>`` 到 ``List``）。
