# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2026-06-21

- VS Code 扩展新增定义跳转（Go to Definition）
- VS Code 扩展新增静态检查诊断，使用 `jaon check` 在编辑器中显示红色/黄色波浪线
- VS Code 扩展新增语义高亮，函数与类引用使用对应颜色
- VS Code 扩展改进内建函数悬停文档格式，包含函数签名与示例代码块
- 修复 `fun` 定义的函数名语法高亮

## [0.1.1] - 2026-06-20

- VS Code 扩展新增 Jaon 语言自动补全（关键字、类型、内建函数、常用方法、代码片段）
- VS Code 扩展新增鼠标悬停提示（Hover），显示关键字、类型与内建函数说明

## [0.1.0] - 2026-06-20

### Added

- 新增项目官网目录 `docs/`，包含响应式单页网站、特性介绍、安装指南与示例
- 安装脚本 `installer/install.ps1` 自动识别并安装最新版 VS Code 扩展 `.vsix`

### Changed

- 首个正式版本，版本号从 `0.0.x` 进入 `0.1.0`
- README 和 Sphinx 文档顶部改用 `jaon-social.png`（带文字标语的社交预览图），不再只放图标
- Banner 与 Social 图片字体改为优先使用 Inter / Roboto / Segoe UI，避免使用黑体

## [0.0.12] - 2026-06-20

- 重新设计 Logo：保留 Java 图标三条 S 形线，改用 Python 蓝黄配色，去掉外圈圆盘，并放大至接近画布边缘
- 同步更新所有 Logo 资源、VS Code 文件图标（改用 PNG）、`dist/compiler.exe` 嵌入图标及文档说明

## [0.0.11] - 2026-06-20

- 重新设计 Logo：保留 Java 图标三条 S 形线，改用 Python 蓝黄配色，去掉外圈圆盘
- 同步更新所有 Logo 资源、VS Code 文件图标、`dist/compiler.exe` 嵌入图标及文档说明

## [0.0.10] - 2026-06-20

- VS Code 扩展语法高亮为普通变量标识符添加颜色（`variable.other.readwrite.jaon`）

## [0.0.9] - 2026-06-20

- 安装包在 `bin` 目录中新增 `jaon.cmd` 命令包装器，安装后可直接使用 `jaon run <file.jaon>`

## [0.0.8] - 2026-06-20

- 修复 Inno Setup 脚本中 `Duplicate identifier 'Result'` 编译错误
- 安装包打包时严格匹配当前版本的 VS Code 扩展文件

## [0.0.7] - 2026-06-20

- 修复 Inno Setup 脚本中 HWND_BROADCAST 常量重复定义问题

## [0.0.6] - 2026-06-20

- Inno Setup 安装后广播环境变量变更通知，新终端无需重启即可识别 jaon
- PowerShell 安装脚本安装后立即刷新当前进程 PATH
- VS Code 扩展运行时若 PATH 中找不到 jaon，自动回退到默认安装路径

## [0.0.5] - 2026-06-20

- Inno Setup 和 PowerShell 安装前自动卸载/删除旧版本

## [0.0.4] - 2026-06-20

- 修复 Inno Setup 脚本中 PATH 清理函数的兼容性问题

## [0.0.3] - 2026-06-20

- Inno Setup 安装包安装时自动添加 Jaon 到用户 PATH
- 卸载时自动从用户 PATH 移除 Jaon

## [0.0.2] - 2026-06-20

- 修复 VS Code 扩展运行按钮在 PowerShell 终端下的命令引号问题

## [0.0.1] - 2026-06-20

- 项目初始发布（pre-release）
