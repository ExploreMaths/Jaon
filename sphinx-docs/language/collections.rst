集合类型
========

列表
----

列表使用方括号 ``[]`` 定义::

    var nums = [1, 2, 3];
    var empty = [];

访问与修改元素::

    println(nums[0]);    // 1
    nums[1] = 99;
    println(nums);       // [1, 99, 3]

列表方法::

    nums.append(4);      // 追加元素
    nums.pop();          // 弹出末尾元素
    var ok = nums.contains(2);  // 是否包含
    var n = nums.length();      // 元素个数


字典
----

字典使用花括号 ``{}`` 定义，键值对以 ``:`` 分隔::

    var scores = {"Alice": 90, "Bob": 85};

访问与修改::

    println(scores["Alice"]);  // 90
    scores["Carol"] = 95;

字典方法::

    var n = scores.length();   // 键值对数量


字符串
------

字符串支持索引访问和常用方法::

    var s = "hello";
    println(s[0]);             // h
    println(s.length());       // 5
    println(s.upper());        // HELLO
    println(s.lower());        // hello
    println(s.contains("ell")); // true

字符串拼接::

    var greeting = "Hello, " + name + "!";
