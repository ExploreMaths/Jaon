# Helios Installer for Windows
# Run as Administrator: Right-click PowerShell -> Run as Administrator
# Then execute: .\install.ps1

param(
    [string]$InstallDir = "$env:LOCALAPPDATA\Helios"
)

$ErrorActionPreference = "Stop"

# Check admin rights
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Please run this installer as Administrator." -ForegroundColor Red
    exit 1
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$rootDir = Split-Path -Parent $scriptDir
$compilerSource = Join-Path $rootDir "dist\compiler.exe"
$iconSource = Join-Path $scriptDir "helios-file.ico"

if (-not (Test-Path $compilerSource)) {
    Write-Host "compiler.exe not found at $compilerSource" -ForegroundColor Red
    Write-Host "Please build it first: python scripts/build_exe.py" -ForegroundColor Yellow
    exit 1
}

Write-Host "Installing Helios to $InstallDir ..." -ForegroundColor Cyan

# Create directories
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
$binDir = Join-Path $InstallDir "bin"
New-Item -ItemType Directory -Force -Path $binDir | Out-Null

# Copy files
Copy-Item -Path $compilerSource -Destination (Join-Path $binDir "compiler.exe") -Force
Copy-Item -Path $iconSource -Destination (Join-Path $InstallDir "helios-file.ico") -Force

$compilerPath = Join-Path $binDir "compiler.exe"

# Add to user PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$binDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$binDir", "User")
    Write-Host "Added Helios to user PATH." -ForegroundColor Green
}

# Register .helios file extension
$regPath = "HKCU:\Software\Classes\.helios"
if (-not (Test-Path $regPath)) {
    New-Item -Path $regPath -Force | Out-Null
}
Set-ItemProperty -Path $regPath -Name "(Default)" -Value "HeliosSourceFile"

$progIdPath = "HKCU:\Software\Classes\HeliosSourceFile"
if (-not (Test-Path $progIdPath)) {
    New-Item -Path $progIdPath -Force | Out-Null
}
Set-ItemProperty -Path $progIdPath -Name "(Default)" -Value "Helios Source File"

$iconPath = Join-Path $InstallDir "helios-file.ico"
$iconRegPath = "$progIdPath\DefaultIcon"
if (-not (Test-Path $iconRegPath)) {
    New-Item -Path $iconRegPath -Force | Out-Null
}
Set-ItemProperty -Path $iconRegPath -Name "(Default)" -Value $iconPath

$shellPath = "$progIdPath\shell\open\command"
if (-not (Test-Path $shellPath)) {
    New-Item -Path $shellPath -Force | Out-Null
}
Set-ItemProperty -Path $shellPath -Name "(Default)" -Value '"' + $compilerPath + '" run "%1"'

# Add a "Run with Helios" context menu item
$runPath = "$progIdPath\shell\RunWithHelios\command"
if (-not (Test-Path $runPath)) {
    New-Item -Path $runPath -Force | Out-Null
}
Set-ItemProperty -Path $runPath -Name "(Default)" -Value '"' + $compilerPath + '" run "%1"'
$runLabelPath = "$progIdPath\shell\RunWithHelios"
Set-ItemProperty -Path $runLabelPath -Name "(Default)" -Value "Run with Helios"
Set-ItemProperty -Path $runLabelPath -Name "Icon" -Value $compilerPath

# Uninstall registry info
$uninstallPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\Helios"
if (-not (Test-Path $uninstallPath)) {
    New-Item -Path $uninstallPath -Force | Out-Null
}
Set-ItemProperty -Path $uninstallPath -Name "DisplayName" -Value "Helios Programming Language"
Set-ItemProperty -Path $uninstallPath -Name "UninstallString" -Value "powershell.exe -ExecutionPolicy Bypass -File `"$scriptDir\uninstall.ps1`""
Set-ItemProperty -Path $uninstallPath -Name "InstallLocation" -Value $InstallDir
Set-ItemProperty -Path $uninstallPath -Name "DisplayIcon" -Value $iconPath
Set-ItemProperty -Path $uninstallPath -Name "Publisher" -Value "Helios Project"
Set-ItemProperty -Path $uninstallPath -Name "Version" -Value "0.1.0"

# Refresh icon cache
Write-Host "Refreshing icon cache..." -ForegroundColor Cyan
ie4uinit.exe -show | Out-Null

Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "You can now double-click any .helios file to run it." -ForegroundColor Green
Write-Host "Restart File Explorer or log out/in if icons don't update immediately." -ForegroundColor Yellow
