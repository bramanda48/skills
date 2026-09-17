# Windows cmd.exe Reference

**Shell:** cmd.exe (legacy Command Prompt)  
**Path separator:** `\`  
**Line endings:** CRLF (`\r\n`)  
**Env vars:** `%VAR%`  
**Home dir:** `%USERPROFILE%`  
**Script extension:** `.bat` or `.cmd`

> ⚠️ **Recommendation:** Switch to PowerShell when possible — it is far more capable. Use cmd.exe only when required (legacy batch scripts, CI locked to cmd, etc.).

---

## Built-in & Native Commands (Verified)

```cmd
REM --- FILE OPERATIONS ---
type file.txt                        :: like cat
copy source.txt dest.txt             :: like cp
xcopy src\ dst\ /E /I                :: recursive copy (use robocopy instead on Vista+)
robocopy src\ dst\ /E                :: preferred recursive copy
move source.txt dest.txt             :: like mv
del file.txt                         :: like rm
rd /s /q directory\                  :: like rm -rf (rd = rmdir, same command)
mkdir a\b\c                          :: like mkdir -p (auto-creates nested on cmd)
dir                                  :: like ls
dir /a                               :: show hidden files
dir /s /b *.txt                      :: like find . -name "*.txt"
tree                                 :: show directory tree
attrib +r file.txt                   :: set read-only (limited vs chmod)

REM --- TEXT PROCESSING ---
findstr "pattern" file.txt           :: like grep
findstr /s /i "pattern" *.txt        :: recursive, case-insensitive
findstr /r "regex" file.txt          :: basic regex support
find /c /v "" file.txt               :: count lines (like wc -l)
find "string" file.txt               :: find exact string (NOTE: different from Unix find!)
fc file1 file2                       :: compare files (like diff, but less powerful)
sort file.txt                        :: sort lines
more file.txt                        :: page output (like less, but basic)
type file.txt | more                 :: pipe through pager

REM --- ENVIRONMENT ---
set                                  :: list all env vars (like env/printenv)
set MYVAR                            :: print one variable (like echo $MYVAR)
echo %PATH%                          :: print specific var
set MYVAR=value                      :: set for session (like export VAR=val)
setx MYVAR "value"                   :: set persistently (user scope)
set Path=%Path%;C:\new\dir           :: append to PATH
where python                         :: like which (find command location)
doskey /history                      :: print command history (like history)
cls                                  :: clear screen (like clear)
title My Terminal                    :: set terminal title
ver                                  :: print Windows version (brief, like uname)
systeminfo                           :: full system info (like uname -a + more)
cd                                   :: print current directory (like pwd)
cd path                              :: change directory

REM --- PROCESSES ---
tasklist                             :: list processes (like ps aux)
taskkill /PID 1234 /F                :: kill by PID (like kill PID)
taskkill /IM notepad.exe /F          :: kill by name (like pkill name)
start notepad.exe                    :: launch process (like cmd &)

REM --- NETWORKING ---
ipconfig /all                        :: show all interfaces + MAC (like ip addr / ifconfig -a)
ping host                            :: ping
nslookup host                        :: DNS lookup
tracert host                         :: traceroute (cmd name is tracert, NOT traceroute)
arp -a                               :: show ARP table
netstat -ano                         :: show connections + ports
netstat -ano | findstr :8080         :: filter by port
hostname                             :: print hostname
ftp host                             :: FTP client (deprecated but present)
curl -o file.zip https://url         :: download (Win10 build 1803+)

REM --- SYSTEM & ADMIN ---
chkdsk C: /f                         :: check disk (needs admin, needs reboot for C:)
shutdown -s                          :: shutdown
shutdown -r                          :: reboot
shutdown -a                          :: abort pending shutdown
net session                          :: show logged-in users (needs admin)
net statistics workstation           :: show uptime info (like uptime)
regedit                              :: open registry editor (GUI)
help                                 :: list built-in commands (like man with no args)
command /?                           :: help for specific command (like man command)
assoc .txt                           :: show file extension association (like file command)
schtasks                             :: schedule tasks (modern replacement for at)
at                                   :: schedule tasks (DEPRECATED since Win8, use schtasks)
mklink link target                   :: create symbolic link (needs admin)
mklink /H link target                :: create hard link (needs admin)
explorer .                           :: open file browser here
print file.txt                       :: send file to printer (like lpr, basic)
```

---

## Commands That Do NOT Exist in Modern Windows

| Command    | Status                       | Alternative                                             |
| ---------- | ---------------------------- | ------------------------------------------------------- |
| `assign`   | ❌ Removed in Vista+         | Use `mklink` or `subst`                                 |
| `edit`     | ❌ Removed (was 16-bit only) | Use `notepad file.txt`                                  |
| `mem`      | ❌ Removed in 64-bit Windows | Use `tasklist` or Task Manager                          |
| `datetime` | ❌ Not a real command        | Use `date` and `time` as separate commands              |
| `grep`     | ❌ Not available natively    | Use `findstr`, or install Git Bash / WSL                |
| `ls`       | ❌ Not available             | Use `dir`                                               |
| `cat`      | ❌ Not available             | Use `type`                                              |
| `rm`       | ❌ Not available             | Use `del` or `rd`                                       |
| `wget`     | ❌ Not available natively    | Use `curl` (Win10+) or PowerShell's `Invoke-WebRequest` |
| `touch`    | ❌ Not available             | Use `type nul > file.txt`                               |

---

## Important Gotchas

- **`find` vs `findstr`**: In cmd, `find` searches for a literal string in files (like a basic `grep`). It does NOT locate files by name like Unix `find`. Use `dir /s /b` to search for files by name.
- **`sort /unique`**: The `/unique` flag exists but reliability varies by Windows version — prefer PowerShell's `Sort-Object -Unique`.
- **`xcopy` vs `robocopy`**: `xcopy` still works but `robocopy` is the preferred tool for recursive copies since Vista.
- **`at` scheduler**: Deprecated since Windows 8. Use `schtasks` instead.
- **`curl`**: Available natively since Windows 10 build 1803. Not available on older systems.
- **Long paths**: Paths over 260 characters may fail unless Long Path support is enabled (Group Policy or registry).
- **Script directory**: Use `%~dp0` to get the directory of the running batch file: `cd /d %~dp0`

---

## Batch Script Basics

```bat
@echo off
REM This is a comment
setlocal enabledelayedexpansion

REM Variables
set NAME=World
echo Hello, %NAME%!

REM If/else — check file existence
if exist file.txt (
    echo File exists
) else (
    echo File not found
)

REM String comparison
if "%VAR%"=="expected" (
    echo Match
)

REM For loop over files
for %%f in (*.txt) do (
    echo Processing %%f
)

REM For loop with counter
for /l %%i in (1,1,10) do (
    echo %%i
)

REM Capture command output
for /f "tokens=*" %%i in ('date /t') do set TODAY=%%i

REM Call another script
call other-script.bat

REM Exit with code
exit /b 0
```
