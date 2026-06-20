类与对象
========

类定义
------

使用 ``class`` 关键字定义类::

    class Point {
        public var x: Int = 0;
        public var y: Int = 0;

        constructor(x: Int, y: Int) {
            this.x = x;
            this.y = y;
        }

        public fun distance(): Float {
            return 0.0;
        }
    }


构造器
------

构造器使用 ``constructor`` 关键字声明::

    constructor(x: Int, y: Int) {
        this.x = x;
        this.y = y;
    }

字段初始化表达式会自动注入到构造器开头执行，因此即使不手动赋值，
字段也会获得初始值。


访问控制
--------

成员可使用 ``public`` 或 ``private`` 修饰，默认为 ``private``::

    class Counter {
        private var value: Int = 0;

        public fun increment(): Int {
            this.value = this.value + 1;
            return this.value;
        }
    }


创建对象
--------

使用 ``new`` 关键字创建实例::

    var p = new Point(3, 4);
    println(p.x);


继承
----

使用 ``extends`` 声明继承关系::

    class Animal {
        public var name: String = "";

        constructor(n: String) {
            this.name = n;
        }

        public fun speak(): String {
            return "Some sound";
        }
    }

    class Dog extends Animal {
        constructor(n: String) {
            this.name = n;
        }

        public fun speak(): String {
            return "Woof!";
        }
    }

    var dog = new Dog("Buddy");
    println(dog.speak());  // Woof!


静态方法
--------

使用 ``static`` 修饰静态方法。静态方法不接收 ``this``::

    class MathUtil {
        public static fun add(a: Int, b: Int): Int {
            return a + b;
        }
    }
