<p align="center">
  <img src="assets/logo/jaon-logo-256x256.png" alt="Jaon Logo" width="160">
</p>

<h1 align="center">Jaon 编程语言</h1>

<p align="center">
  <a href="https://github.com/ExploreMaths/Jaon/actions/workflows/ci.yml">
    <img src="https://github.com/ExploreMaths/Jaon/actions/workflows/ci.yml/badge.svg" alt="CI">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
  <a href="https://jaon.readthedocs.io/zh_CN/latest/?badge=latest">
    <img src="https://readthedocs.org/projects/jaon/badge/?version=latest" alt="Documentation Status">
  </a>
</p>

Jaon 是一门融合了 **Python 的简洁** 与 **Java 的严谨** 的实验性编程语言。

- **自定义源文件后缀**：`.jaon`
- **自定义编译器**：完整的前端（Lexer / Parser / 语义分析）+ 后端（Bytecode 编译器 / 栈式虚拟机）
- **类型系统**：静态类型 + 局部类型推断
- **语法风格**：Python 式关键字 + Java 式 `{}` 块结构
- **面向对象**：类、继承、构造器、访问控制

---

## 安装

### 从源码安装

```bash
git clone https://github.com/ExploreMaths/Jaon.git
cd jaon
pip install -e .
```

### 安装开发依赖

```bash
pip install -e .[dev,docs]
```

## 快速开始

### 运行示例

```bash
python -m jaon run examples/hello.jaon
```

项目根目录也提供了独立的 Windows 可执行文件（无需 Python）：

```bash
dist/compiler.exe run examples/hello.jaon
```

### 进入 REPL

```bash
python -m jaon repl
```

### 运行测试

```bash
python scripts/run_tests.py
# 或
python -m unittest discover tests
```

### 构建文档

```bash
cd sphinx-docs
python -m sphinx -b html . _build/html
```

文档也可在 Read the Docs 上自动构建（配置见 `.readthedocs.yml`）。

### 构建独立可执行文件

需要安装 Nuitka 和 Visual C++ 编译器（通常已随 Visual Studio 或 Build Tools 安装）：

```bash
pip install nuitka
python scripts/build_exe.py
```

生成的 ``dist/compiler.exe`` 可直接运行，不依赖 Python 环境。

### Windows 安装程序（双击运行 .jaon）

PowerShell 安装（无需额外工具）：

```powershell
cd installer
powershell -ExecutionPolicy Bypass -File install.ps1
```

或使用 Inno Setup 生成安装包：

```bash
iscc installer/setup.iss
```

安装后，双击任意 `.jaon` 文件即可自动使用 Jaon 编译器执行。

---

## 项目结构

```
jaon/
├── __init__.py
├── __main__.py       # python -m jaon 入口
├── ast_nodes.py      # AST 节点定义
├── lexer.py          # 词法分析器
├── parser.py         # 递归下降语法分析器
├── analyzer.py       # 语义分析 / 类型检查
├── bytecode.py       # 字节码与 CodeObject
├── compiler.py       # AST -> Bytecode 编译器
├── vm.py             # 栈式虚拟机
├── builtins.py       # 内建函数
├── cli.py            # 命令行接口
└── errors.py         # 错误类型

examples/             # 示例程序 (*.jaon)
tests/                # 单元测试
scripts/              # 辅助脚本
```

---

## 语言特性

### 变量与类型

```jaon
var x = 10;          // 类型推断为 Int
var y: Float = 3.14; // 显式类型
val pi = 3.14159;    // 常量
```

支持类型：`Int`、`Float`、`Bool`、`String`、`List<T>`、`Dict<K,V>`、类类型、`Any`。

### 函数

```jaon
fun add(a: Int, b: Int): Int {
    return a + b;
}
```

### 控制流

```jaon
if (x > 0) {
    println("positive");
} elif (x < 0) {
    println("negative");
} else {
    println("zero");
}

while (i < 10) {
    i = i + 1;
}

for (n in [1, 2, 3]) {
    println(n);
}
```

### 类与继承

```jaon
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
println(dog.speak());
```

### 异常处理

```jaon
fun divide(a: Int, b: Int): Int {
    if (b == 0) {
        throw "Division by zero";
    }
    return a / b;
}

try {
    divide(10, 0);
} catch (e) {
    println("Error: " + e);
}
```

### 集合

```jaon
var nums = [1, 2, 3];
nums[1] = 99;
println(nums[1]);

var scores = {"Alice": 90, "Bob": 85};
println(scores["Alice"]);
```

### 内建函数

- `print(x)` / `println(x)`
- `input()`
- `len(x)`
- `range(n)`
- `str(x)` / `int(x)` / `float(x)`
- `type(x)`

---

## 编译器架构

Jaon 编译器采用经典分层设计：

1. **Lexer**：将 `.jaon` 源码切分为 Token 流。
2. **Parser**：递归下降解析生成 AST。
3. **Analyzer**：类型检查、作用域解析、类成员解析。
4. **Compiler**：AST 编译为自定义 Bytecode。
5. **VM**：基于栈的虚拟机执行 Bytecode。

---

## 命令行

```bash
python -m jaon --help
python -m jaon run file.jaon
python -m jaon repl
python -m jaon dis file.jaon
```

---

## 贡献

欢迎提交 Issue 和 Pull Request！

提交前请确保：

```bash
python -m unittest discover tests
flake8 jaon tests scripts --max-line-length=120 --extend-ignore=E203,W503
```

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 发布

推送标签即可触发 GitHub Actions 自动构建 Windows 可执行文件并发布 Release：

```bash
git tag v0.0.12
git push origin v0.0.12
```

## 许可证

MIT License
