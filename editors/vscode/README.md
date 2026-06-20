# Helios for VS Code

Visual Studio Code extension for the [Helios](https://github.com/ExploreMaths/Helios) programming language.

## Features

- **Syntax highlighting** for `.helios` files.
- **Run button** in the editor title bar (play icon) to execute the current file.
- **Command palette** support: `Helios: Run Helios File`.
-Configurable executable path.

## Requirements

You need the Helios compiler installed:

```bash
pip install -e .
```

Or use the standalone `compiler.exe` on Windows.

## Extension Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `helios.executablePath` | `helios` | Path to the Helios executable. Use `helios` if it is on PATH, or an absolute path such as `C:\Program Files\Helios\bin\compiler.exe`. |

## Usage

1. Open any `.helios` file.
2. Click the **▶ Run Helios File** button in the top-right corner of the editor.
3. The output appears in the integrated terminal named **Helios**.

You can also run the command from the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) by typing `Helios: Run Helios File`.
