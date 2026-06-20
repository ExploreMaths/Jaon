; Helios Installer Script for Inno Setup
; Build with: iscc installer/setup.iss

#define MyAppName "Helios"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Helios Project"
#define MyAppURL "https://github.com/ExploreMaths/Helios"

[Setup]
AppId={{HELIOS-LANG-0F3A-4B8C-9D2E-1A7B5C4D8E2F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={autopf}\Helios
DisableProgramGroupPage=yes
LicenseFile=..\LICENSE
OutputDir=..\dist
OutputBaseFilename=Helios-Setup
SetupIconFile=helios-file.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

; Use ISPP to include Chinese only when the language file is present (e.g. local builds).
; CI runners usually only have the Default English language installed.
#define ChineseIslPath "C:\\Program Files (x86)\\Inno Setup 6\\Languages\\ChineseSimplified.isl"

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
#if FileExists(ChineseIslPath)
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\\ChineseSimplified.isl"
#endif

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "installvscodeext"; Description: "Install VS Code extension for .helios files"; GroupDescription: "Editor integration:"; Flags: checked

[Files]
Source: "..\dist\compiler.exe"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "helios-file.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\examples\*"; DestDir: "{app}\examples"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\editors\vscode\helios-lang-*.vsix"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\bin\compiler.exe"; Parameters: "repl"; IconFilename: "{app}\helios-file.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\bin\compiler.exe"; Parameters: "repl"; IconFilename: "{app}\helios-file.ico"; Tasks: desktopicon

[Registry]
; Register .helios file extension
Root: HKLM; Subkey: "Software\\Classes\\.helios"; ValueType: string; ValueName: ""; ValueData: "HeliosSourceFile"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\\Classes\\HeliosSourceFile"; ValueType: string; ValueName: ""; ValueData: "Helios Source File"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\\Classes\\HeliosSourceFile\\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\\helios-file.ico"
Root: HKLM; Subkey: "Software\\Classes\\HeliosSourceFile\\shell\\open\\command"; ValueType: string; ValueName: ""; ValueData: """{app}\\bin\\compiler.exe"" run ""%1"""
Root: HKLM; Subkey: "Software\\Classes\\HeliosSourceFile\\shell\\RunWithHelios"; ValueType: string; ValueName: ""; ValueData: "Run with Helios"
Root: HKLM; Subkey: "Software\\Classes\\HeliosSourceFile\\shell\\RunWithHelios"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\\bin\\compiler.exe"
Root: HKLM; Subkey: "Software\\Classes\\HeliosSourceFile\\shell\\RunWithHelios\\command"; ValueType: string; ValueName: ""; ValueData: """{app}\\bin\\compiler.exe"" run ""%1"""

[Run]
Filename: "{app}\\bin\\compiler.exe"; Parameters: "run ""{app}\\examples\\hello.helios"""; Description: "Test Helios installation"; Flags: nowait postinstall skipifsilent
Filename: "cmd.exe"; Parameters: "/c code --install-extension ""{app}\\helios-lang-{#MyAppVersion}.vsix"""; Description: "Install VS Code extension"; Flags: postinstall skipifsilent; Tasks: installvscodeext

[UninstallRun]
Filename: "cmd.exe"; Parameters: "/c code --uninstall-extension exploremaths.helios-lang"; RunOnceId: "UninstallHeliosVSCodeExt"

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    // Refresh icon cache
    Exec('ie4uinit.exe', '-show', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  end;
end;
