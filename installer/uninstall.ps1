# Helios Uninstaller for Windows
# Run as Administrator

$ErrorActionPreference = "Stop"

$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Please run this uninstaller as Administrator." -ForegroundColor Red
    exit 1
}

$installDir = "$env:LOCALAPPDATA\Helios"
$binDir = Join-Path $installDir "bin"

Write-Host "Uninstalling Helios..." -ForegroundColor Cyan

# Remove file association
if (Test-Path "HKCU:\Software\Classes\.helios") {
    Remove-Item -Path "HKCU:\Software\Classes\.helios" -Recurse -Force
}
if (Test-Path "HKCU:\Software\Classes\HeliosSourceFile") {
    Remove-Item -Path "HKCU:\Software\Classes\HeliosSourceFile" -Recurse -Force
}

# Remove PATH entry
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -like "*$binDir*") {
    $newPath = ($userPath -split ';' | Where-Object { $_ -ne $binDir }) -join ';'
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "Removed Helios from user PATH." -ForegroundColor Green
}

# Remove uninstall registry entry
if (Test-Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\Helios") {
    Remove-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\Helios" -Recurse -Force
}

# Remove installation directory
if (Test-Path $installDir) {
    Remove-Item -Path $installDir -Recurse -Force
    Write-Host "Removed $installDir" -ForegroundColor Green
}

# Uninstall VS Code extension if VS Code is present
if (Get-Command code -ErrorAction SilentlyContinue) {
    Write-Host "Uninstalling VS Code extension..." -ForegroundColor Cyan
    code --uninstall-extension exploremaths.helios-lang | Out-Null
    Write-Host "VS Code extension uninstalled." -ForegroundColor Green
}

# Refresh icon cache
ie4uinit.exe -show | Out-Null

Write-Host "Uninstallation complete." -ForegroundColor Green
