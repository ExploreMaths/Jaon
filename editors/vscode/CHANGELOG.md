# Change Log

## [0.1.2]

- Add Go to Definition for variables, functions, classes, fields, and methods.
- Add diagnostics (red/yellow wavy underlines) using `jaon check`.
- Add semantic highlighting so function and class references match their definitions.
- Improve built-in function hover docs with function signature and example block.
- Fix function name coloring in `fun` definitions.

## [0.1.1]

- Add IntelliSense auto-completion for Jaon keywords, types, built-in functions, common methods, and snippets.
- Add hover provider showing details for Jaon keywords, types, and built-in functions.

## [0.1.0]

- First stable release, version bumped from `0.0.x` to `0.1.0`.
- Use `jaon-social.png` banner in README and Sphinx docs instead of the square logo icon.
- Update banner/social fonts to prefer Inter / Roboto / Segoe UI and avoid SimHei.
- `installer/install.ps1` now auto-detects the latest VS Code extension `.vsix` package.

## [0.0.12]

- Redesign logo: keep Java's three S-shaped lines, color them in Python blue/yellow, remove outer circle, enlarge to near canvas edge.
- Switch VS Code file icon from SVG to PNG generated from logo.

## [0.0.11]

- Redesign logo: keep Java's three S-shaped lines, color them in Python blue/yellow, remove outer circle.

## [0.0.10]

- Add syntax highlighting for general variable identifiers (`variable.other.readwrite.jaon`).

## [0.0.9]

- Installer now ships a `jaon.cmd` shim in `bin`, so `jaon run <file.jaon>` works after installation.

## [0.0.8]

- Fix Inno Setup `Duplicate identifier 'Result'` compile error.

## [0.0.7]

- Fix duplicate HWND_BROADCAST constant in Inno Setup script.

## [0.0.6]

- Broadcast environment variable changes after Inno Setup installation.
- Refresh current process PATH immediately after PowerShell installation.
- VS Code extension falls back to default install paths when 'jaon' is not on PATH.

## [0.0.5]

- Installers now remove any previous Jaon version before installing.

## [0.0.4]

- Fix Inno Setup PATH cleanup function compatibility.

## [0.0.3]

- Inno Setup installer now adds Jaon to the user PATH and removes it on uninstall.

## [0.0.2]

- Fix command quoting for PowerShell terminals.

## [0.0.1]

- Initial release.
- Syntax highlighting for `.jaon` files.
- Run button and command to execute Jaon files in the integrated terminal.
