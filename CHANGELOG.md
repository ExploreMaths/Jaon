# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- 初始实现 Jaon 编程语言
- 自定义文件后缀 `.jaon`
- 完整编译器链：Lexer、Parser、Analyzer、Bytecode Compiler、Stack VM
- 静态类型系统 + 局部类型推断
- 类、继承、构造器、访问控制
- 函数、递归、匿名函数
- 控制流：if/elif/else、while、for...in、break/continue/return
- 异常处理：try/catch/finally/throw
- 内建类型：Int、Float、Bool、String、List、Dict
- 内建函数：print、println、input、len、range、str、int、float、type
- REPL 交互式解释器
- 命令行工具：run、repl、dis
- 23 个单元测试
- Sphinx 中文文档（Furo 主题 + 华文中宋字体）
- Read the Docs 配置文件
- Nuitka 构建独立 `compiler.exe`
- GitHub Actions CI/CD 工作流

## [0.0.1] - 2026-06-20

- 项目初始发布（pre-release）
