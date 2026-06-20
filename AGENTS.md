# Helios 项目约定

## 源文件后缀

所有 Helios 源代码文件使用 `.helios` 后缀。

## 构建与运行

- 安装：`pip install -e .`
- 运行文件：`python -m helios run <file.helios>` 或 `helios run <file.helios>`
- 独立可执行文件：`dist/compiler.exe run <file.helios>`
- 交互式 REPL：`python -m helios repl` 或 `helios repl`
- 反汇编查看字节码：`python -m helios dis <file.helios>`
- 运行测试：`python -m unittest discover tests` 或 `python scripts/run_tests.py`

## 项目结构

- `helios/`：编译器与虚拟机源码。
- `examples/`：`.helios` 示例程序。
- `tests/`：单元测试。
- `scripts/`：辅助脚本。
- `sphinx-docs/`：Sphinx 中文文档。

## 构建文档

```bash
cd sphinx-docs
python -m sphinx -b html . _build/html
```

Read the Docs 构建配置见 `.readthedocs.yml`。

## 构建独立可执行文件

```bash
pip install nuitka
python scripts/build_exe.py
```

生成 `dist/compiler.exe`，不依赖 Python 环境即可运行。

## Windows 安装程序

PowerShell 安装（无需额外工具）：

```powershell
cd installer
powershell -ExecutionPolicy Bypass -File install.ps1
```

Inno Setup 打包：

```bash
iscc installer/setup.iss
```

安装后双击 `.helios` 文件即可执行。

## 编码风格

- Python 代码遵循 PEP 8。
- 使用类型注解。
- 保持模块化：lexer、parser、analyzer、compiler、vm 各司其职。

## 添加新特性流程

1. 更新 lexer / parser / ast_nodes 支持新语法。
2. 更新 analyzer 进行类型检查。
3. 更新 bytecode / compiler 生成对应字节码。
4. 更新 vm 执行字节码。
5. 添加示例和单元测试。

## 注意事项

- 顶层函数与类使用全局作用域，便于递归和跨函数引用。
- 方法调用统一使用 `LOAD_ATTR` + `CALL`，同时适用于类方法和内置类型方法。
- 类字段初始化会自动注入构造器开头执行。
