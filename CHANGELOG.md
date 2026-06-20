# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
