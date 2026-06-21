# Jaon Installer for Windows
# Run as Administrator: Right-click PowerShell -> Run as Administrator
# Then execute: .\install.ps1

param(
    [string]$InstallDir = "$env:LOCALAPPDATA\Jaon"
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

# Remove any previous installation first
$previousInstallDir = "$env:LOCALAPPDATA\Jaon"
if (Test-Path $previousInstallDir) {
    Write-Host "Removing previous Jaon installation..." -ForegroundColor Cyan
    $previousBinDir = Join-Path $previousInstallDir "bin"

    if (Test-Path "HKCU:\Software\Classes\.jaon") {
        Remove-Item -Path "HKCU:\Software\Classes\.jaon" -Recurse -Force
    }
    if (Test-Path "HKCU:\Software\Classes\JaonSourceFile") {
        Remove-Item -Path "HKCU:\Software\Classes\JaonSourceFile" -Recurse -Force
    }

    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($userPath -like "*$previousBinDir*") {
        $newPath = ($userPath -split ';' | Where-Object { $_ -ne $previousBinDir }) -join ';'
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    }

    if (Test-Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\Jaon") {
        Remove-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\Jaon" -Recurse -Force
    }

    Remove-Item -Path $previousInstallDir -Recurse -Force
    Write-Host "Previous installation removed." -ForegroundColor Green
}

$compilerSource = Join-Path $rootDir "dist\compiler.exe"
$iconSource = Join-Path $scriptDir "jaon-file.ico"

if (-not (Test-Path $compilerSource)) {
    Write-Host "compiler.exe not found at $compilerSource" -ForegroundColor Red
    Write-Host "Please build it first: python scripts/build_exe.py" -ForegroundColor Yellow
    exit 1
}

Write-Host "Installing Jaon to $InstallDir ..." -ForegroundColor Cyan

# Create directories
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
$binDir = Join-Path $InstallDir "bin"
New-Item -ItemType Directory -Force -Path $binDir | Out-Null

# Copy files
Copy-Item -Path $compilerSource -Destination (Join-Path $binDir "compiler.exe") -Force
Copy-Item -Path $iconSource -Destination (Join-Path $InstallDir "jaon-file.ico") -Force

# Create a jaon.cmd shim so 'jaon' is available on PATH
$jaonCmdPath = Join-Path $binDir "jaon.cmd"
'@echo off' | Out-File -FilePath $jaonCmdPath -Encoding ASCII -Force
'"%~dp0\compiler.exe" %*' | Out-File -FilePath $jaonCmdPath -Encoding ASCII -Append

$compilerPath = Join-Path $binDir "compiler.exe"

# Add to user PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$binDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$binDir", "User")
    Write-Host "Added Jaon to user PATH." -ForegroundColor Green
}

# Register .jaon file extension
$regPath = "HKCU:\Software\Classes\.jaon"
if (-not (Test-Path $regPath)) {
    New-Item -Path $regPath -Force | Out-Null
}
Set-ItemProperty -Path $regPath -Name "(Default)" -Value "JaonSourceFile"

$progIdPath = "HKCU:\Software\Classes\JaonSourceFile"
if (-not (Test-Path $progIdPath)) {
    New-Item -Path $progIdPath -Force | Out-Null
}
Set-ItemProperty -Path $progIdPath -Name "(Default)" -Value "Jaon Source File"

$iconPath = Join-Path $InstallDir "jaon-file.ico"
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

# Add a "Run with Jaon" context menu item
$runPath = "$progIdPath\shell\RunWithJaon\command"
if (-not (Test-Path $runPath)) {
    New-Item -Path $runPath -Force | Out-Null
}
Set-ItemProperty -Path $runPath -Name "(Default)" -Value '"' + $compilerPath + '" run "%1"'
$runLabelPath = "$progIdPath\shell\RunWithJaon"
Set-ItemProperty -Path $runLabelPath -Name "(Default)" -Value "Run with Jaon"
Set-ItemProperty -Path $runLabelPath -Name "Icon" -Value $compilerPath

# Uninstall registry info
$uninstallPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\Jaon"
if (-not (Test-Path $uninstallPath)) {
    New-Item -Path $uninstallPath -Force | Out-Null
}
Set-ItemProperty -Path $uninstallPath -Name "DisplayName" -Value "Jaon Programming Language"
Set-ItemProperty -Path $uninstallPath -Name "UninstallString" -Value "powershell.exe -ExecutionPolicy Bypass -File `"$scriptDir\uninstall.ps1`""
Set-ItemProperty -Path $uninstallPath -Name "InstallLocation" -Value $InstallDir
Set-ItemProperty -Path $uninstallPath -Name "DisplayIcon" -Value $iconPath
Set-ItemProperty -Path $uninstallPath -Name "Publisher" -Value "Jaon Project"
Set-ItemProperty -Path $uninstallPath -Name "Version" -Value "0.1.2"

# Install VS Code extension if VS Code is present and a .vsix package exists
$vsixDir = Join-Path $rootDir "dist"
$vsixFiles = Get-ChildItem -Path $vsixDir -Filter "jaon-lang-*.vsix" -ErrorAction SilentlyContinue |
    Sort-Object { [version]($_.BaseName -replace '^jaon-lang-', '') } -Descending

if (Get-Command code -ErrorAction SilentlyContinue) {
    if ($vsixFiles) {
        $vsixPath = $vsixFiles[0].FullName
        Write-Host "Installing VS Code extension from $vsixPath ..." -ForegroundColor Cyan
        code --install-extension $vsixPath | Out-Null
        Write-Host "VS Code extension installed." -ForegroundColor Green
    } else {
        Write-Host "VS Code extension package not found in $vsixDir, skipping." -ForegroundColor Yellow
    }
} else {
    Write-Host "VS Code not detected, skipping extension installation." -ForegroundColor Yellow
}

# Refresh icon cache
Write-Host "Refreshing icon cache..." -ForegroundColor Cyan
ie4uinit.exe -show | Out-Null

# Refresh PATH in the current process so jaon is available immediately
$env:Path = [Environment]::GetEnvironmentVariable("Path", "User") + ";" + [Environment]::GetEnvironmentVariable("Path", "Machine")

Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "You can now double-click any .jaon file to run it." -ForegroundColor Green
Write-Host "Restart File Explorer or log out/in if icons don't update immediately." -ForegroundColor Yellow
