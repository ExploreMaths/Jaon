# Jaon Windows Installer

本目录包含 Windows 平台下的安装程序相关文件。

## 文件说明

- `setup.iss` — Inno Setup 安装脚本，可打包成 `Jaon-Setup.exe`
- `install.ps1` — PowerShell 安装脚本，无需额外工具即可运行
- `uninstall.ps1` — PowerShell 卸载脚本
- `create_icon.py` — 生成 `.jaon` 文件图标
- `jaon-file.ico` — `.jaon` 文件图标

## 安装效果

安装完成后：

1. `compiler.exe` 被复制到 `%LOCALAPPDATA%\Jaon\bin\compiler.exe`（PowerShell）
   或 `{ProgramFiles}\Jaon\bin\compiler.exe`（Inno Setup）
2. `.jaon` 文件与 Jaon 关联，双击即可自动执行
3. 右键菜单增加 "Run with Jaon"
4. 将 Jaon 添加到用户 PATH，可在命令行直接运行 `compiler.exe` 或 `jaon`

## 使用方法

### 方法一：PowerShell 安装（推荐，无需额外工具）

1. 确保已生成 `dist/compiler.exe`：

   ```bash
   python scripts/build_exe.py
   ```

2. 以管理员身份运行 PowerShell，执行：

   ```powershell
   cd installer
   powershell -ExecutionPolicy Bypass -File install.ps1
   ```

3. 现在可以双击任意 `.jaon` 文件运行。

### 方法二：Inno Setup 安装程序

1. 安装 [Inno Setup](https://jrsoftware.org/isinfo.php)
2. 生成 `dist/compiler.exe`
3. 编译安装包：

   ```bash
   iscc installer/setup.iss
   ```

4. 生成的 `dist/Jaon-Setup.exe` 即为安装程序，双击运行即可。

## 卸载

### PowerShell 安装版

以管理员身份运行：

```powershell
cd installer
powershell -ExecutionPolicy Bypass -File uninstall.ps1
```

### Inno Setup 安装版

通过 "控制面板" -> "程序和功能" 卸载，或运行安装目录下的 `unins000.exe`。
