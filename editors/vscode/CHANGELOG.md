# Change Log

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
