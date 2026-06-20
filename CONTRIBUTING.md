# Contributing to Helios

感谢你对 Helios 的兴趣！以下是参与贡献的指南。

## 开发环境

```bash
git clone https://github.com/yourusername/helios.git
cd helios
pip install -e .[dev,docs]
```

## 代码规范

- 遵循 PEP 8
- 最大行长度 120 字符
- 使用类型注解
- 保持模块化设计

## 提交前检查

```bash
# 运行测试
python -m unittest discover tests

# 运行示例
python -m helios run examples/hello.helios

# 代码风格检查
flake8 helios tests scripts --max-line-length=120 --extend-ignore=E203,W503

# 构建文档
cd sphinx-docs
python -m sphinx -b html . _build/html
```

## 提交 Issue

- Bug 报告请使用 [Bug report](.github/ISSUE_TEMPLATE/bug_report.md) 模板
- 功能建议请使用 [Feature request](.github/ISSUE_TEMPLATE/feature_request.md) 模板

## 提交 Pull Request

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 创建 Pull Request

PR 模板已提供，请按要求填写。
