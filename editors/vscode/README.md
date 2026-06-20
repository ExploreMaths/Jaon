# Jaon for VS Code

Visual Studio Code extension for the [Jaon](https://github.com/ExploreMaths/Jaon) programming language.

## Features

- **Syntax highlighting** for `.jaon` files.
- **Run button** in the editor title bar (play icon) to execute the current file.
- **Command palette** support: `Jaon: Run Jaon File`.
-Configurable executable path.

## Requirements

You need the Jaon compiler installed:

```bash
pip install -e .
```

Or use the standalone `compiler.exe` on Windows.

## Extension Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `jaon.executablePath` | `jaon` | Path to the Jaon executable. Use `jaon` if it is on PATH, or an absolute path such as `C:\Program Files\Jaon\bin\compiler.exe`. |

## Usage

1. Open any `.jaon` file.
2. Click the **▶ Run Jaon File** button in the top-right corner of the editor.
3. The output appears in the integrated terminal named **Jaon**.

You can also run the command from the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) by typing `Jaon: Run Jaon File`.
