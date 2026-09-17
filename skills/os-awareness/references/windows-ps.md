# Windows PowerShell Reference

**Shell:** PowerShell 5.1 (built-in) or PowerShell 7+ (cross-platform, recommended)  
**Package Manager:** winget (Windows 10+), Chocolatey (`choco`), Scoop  
**Path separator:** `\` (PowerShell also accepts `/` in most cases)  
**Line endings:** CRLF (`\r\n`)  
**Env vars:** `$env:VAR`  
**Home dir:** `$env:USERPROFILE` or `~`  
**Script extension:** `.ps1`

## Execution Policy

By default, scripts may be blocked. Run once to allow:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Common Idioms

```powershell
# Search in files (like grep)
Select-String -Pattern "pattern" -Path ".\*" -Recurse

# Find files (like find)
Get-ChildItem -Path . -Recurse -Filter "*.txt"
Get-ChildItem -Path . -Recurse -Include "*.txt", "*.log"

# Read a file (like cat)
Get-Content file.txt

# Write/overwrite a file
Set-Content file.txt -Value "content"

# Append to file
Add-Content file.txt -Value "more content"

# In-place replace (like sed)
(Get-Content file.txt) -replace 'old', 'new' | Set-Content file.txt

# Copy file/folder
Copy-Item source.txt destination.txt
Copy-Item -Recurse sourceDir\ destDir\

# Move file/folder
Move-Item source.txt destination.txt

# Delete file/folder
Remove-Item file.txt
Remove-Item -Recurse -Force directory\

# Create directory
New-Item -ItemType Directory -Path "a\b\c" -Force

# Create empty file (like touch)
New-Item -ItemType File -Path file.txt

# List directory
Get-ChildItem
Get-ChildItem -Force   # show hidden files

# Count lines (like wc -l)
(Get-Content file.txt).Count

# Head / tail
Get-Content file.txt | Select-Object -First 10
Get-Content file.txt | Select-Object -Last 10

# Sort
Get-Content file.txt | Sort-Object

# Unique
Get-Content file.txt | Sort-Object -Unique

# Process management
Get-Process
Stop-Process -Name "notepad"
Stop-Process -Id 1234

# Environment variables
$env:PATH
$env:MY_VAR = "value"   # set for session
[System.Environment]::SetEnvironmentVariable("MY_VAR", "value", "User")  # persistent

# Check if command exists
Get-Command grep -ErrorAction SilentlyContinue

# Download file (like wget/curl)
Invoke-WebRequest -Uri "https://example.com/file.zip" -OutFile "file.zip"

# Make HTTP request
Invoke-RestMethod -Uri "https://api.example.com/data" -Method GET

# Check listening ports
netstat -ano | findstr :8080
# or
Get-NetTCPConnection -LocalPort 8080

# Pipe output to file
Get-ChildItem | Out-File output.txt
Get-ChildItem | Select-Object -ExpandProperty Name > names.txt
```

## Install Package Managers

```powershell
# winget (built-in Windows 10 1809+)
winget install Git.Git
winget install Python.Python.3.12
winget install Microsoft.VisualStudioCode

# Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco install nodejs git python

# Scoop
irm get.scoop.sh | iex
scoop install git nodejs python
```

## Notes

- PowerShell 7+ (`pwsh`) is cross-platform and preferred for new scripts.
- Aliases exist in PowerShell: `ls`, `cat`, `cp`, `mv`, `rm` — but they map to PS cmdlets, not Unix tools. Behavior may differ.
- Use `$PSVersionTable` to check PowerShell version.
- WSL (Windows Subsystem for Linux) lets you run Linux bash inside Windows — see linux.md if user is using WSL.
