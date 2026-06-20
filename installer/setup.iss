; Jaon Installer Script for Inno Setup
; Build with: iscc installer/setup.iss

#define MyAppName "Jaon"
#define MyAppVersion "0.0.1"
#define MyAppPublisher "Jaon Project"
#define MyAppURL "https://github.com/ExploreMaths/Jaon"

[Setup]
AppId={{JAON-LANG-0F3A-4B8C-9D2E-1A7B5C4D8E2F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={autopf}\Jaon
DisableProgramGroupPage=yes
LicenseFile=..\LICENSE
OutputDir=..\dist
OutputBaseFilename=Jaon-Setup
SetupIconFile=jaon-file.ico
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
Name: "installvscodeext"; Description: "Install VS Code extension for .jaon files"; GroupDescription: "Editor integration:"

[Files]
Source: "..\dist\compiler.exe"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "jaon-file.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\examples\*"; DestDir: "{app}\examples"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\editors\vscode\jaon-lang-*.vsix"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\bin\compiler.exe"; Parameters: "repl"; IconFilename: "{app}\jaon-file.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\bin\compiler.exe"; Parameters: "repl"; IconFilename: "{app}\jaon-file.ico"; Tasks: desktopicon

[Registry]
; Register .jaon file extension
Root: HKLM; Subkey: "Software\\Classes\\.jaon"; ValueType: string; ValueName: ""; ValueData: "JaonSourceFile"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\\Classes\\JaonSourceFile"; ValueType: string; ValueName: ""; ValueData: "Jaon Source File"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\\Classes\\JaonSourceFile\\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\\jaon-file.ico"
Root: HKLM; Subkey: "Software\\Classes\\JaonSourceFile\\shell\\open\\command"; ValueType: string; ValueName: ""; ValueData: """{app}\\bin\\compiler.exe"" run ""%1"""
Root: HKLM; Subkey: "Software\\Classes\\JaonSourceFile\\shell\\RunWithJaon"; ValueType: string; ValueName: ""; ValueData: "Run with Jaon"
Root: HKLM; Subkey: "Software\\Classes\\JaonSourceFile\\shell\\RunWithJaon"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\\bin\\compiler.exe"
Root: HKLM; Subkey: "Software\\Classes\\JaonSourceFile\\shell\\RunWithJaon\\command"; ValueType: string; ValueName: ""; ValueData: """{app}\\bin\\compiler.exe"" run ""%1"""

[Run]
Filename: "{app}\\bin\\compiler.exe"; Parameters: "run ""{app}\\examples\\hello.jaon"""; Description: "Test Jaon installation"; Flags: nowait postinstall skipifsilent
Filename: "cmd.exe"; Parameters: "/c code --install-extension ""{app}\\jaon-lang-{#MyAppVersion}.vsix"""; Description: "Install VS Code extension"; Flags: postinstall skipifsilent; Tasks: installvscodeext

[UninstallRun]
Filename: "cmd.exe"; Parameters: "/c code --uninstall-extension exploremaths.jaon-lang"; RunOnceId: "UninstallJaonVSCodeExt"

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
