---
name: os-awareness
description: >
  Detect the user's operating system and automatically use the correct CLI tools,
  shell commands, and path conventions for that platform. Use this skill whenever
  writing shell commands, scripts, or file operations for any AI agent tool or
  assistant — especially when the task involves tools that differ across operating
  systems (e.g., grep, find, sed, ls, cp, rm, cat, curl, touch, chmod, echo,
  path separators, environment variables). Trigger this skill when the user asks
  to run code, automate tasks, manipulate files, or when any OS-specific behavior
  might arise. Also trigger when the user mentions Windows, Linux, macOS,
  PowerShell, bash, zsh, cmd, WSL, or any platform-specific tool. This skill is
  agent-agnostic and applies to Claude, Cursor, Copilot, Aider, Continue, or any
  other AI coding/automation assistant.
---

# OS Awareness Skill

Ensures the AI agent always uses the correct tools, commands, and conventions
for the user's actual operating system. Agent-agnostic — works with any AI tool.

## Step 1 — Detect the Operating System

Before generating any shell command or script, detect the OS using the best
available method for your agent:

**If the agent has a shell/bash tool:**

```bash
uname -s 2>/dev/null || echo "Windows"
```

**If no shell tool is available, infer from context:**

- `C:\` or `%APPDATA%` paths → Windows
- `/home/`, `/usr/`, `~` paths → Linux or macOS
- User mentions PowerShell, cmd.exe, `.bat`, `.ps1` → Windows
- User mentions Terminal, zsh, brew, apt → Linux/macOS
- If still unsure → **ask the user**: _"Are you on Windows, macOS, or Linux?"_

**OS Detection Table:**
| Signal | Platform | Default Shell |
|---|---|---|
| `uname` = `Linux` | Linux | bash / zsh |
| `uname` = `Darwin` | macOS | zsh (bash on older) |
| No `uname`, or `Windows_NT` env | Windows | PowerShell (preferred) / cmd |
| Linux + `/mnt/c/` paths visible | WSL on Windows | bash (WSL) |

---

## Step 2 — Load the Right Reference

Once the OS is known, read the relevant reference file before generating commands:

- **Linux** → `references/linux.md`
- **macOS** → `references/macos.md`
- **Windows (PowerShell)** → `references/windows-ps.md`
- **Windows (cmd.exe)** → `references/windows-cmd.md`
- **WSL** → Use `references/linux.md`, note Windows path interop (`/mnt/c/`)

---

## Step 3 — General Rules (All Platforms)

1. **Never assume bash** — Windows users default to PowerShell unless they say otherwise.
2. **Always prefer native tools** — don't suggest `grep` on Windows unless WSL/Git Bash is confirmed available.
3. **Explain substitutions** — when swapping a tool (e.g., `grep` → `Select-String`), briefly say why.
4. **Path separators matter** — use `\` for Windows, `/` for Linux/macOS.
5. **Env vars differ** — `$VAR` on Linux/macOS, `$env:VAR` in PowerShell, `%VAR%` in cmd.
6. **Line endings** — Windows uses CRLF (`\r\n`), Linux/macOS use LF (`\n`). Flag when relevant.
7. **Package managers differ** — `apt` / `brew` / `choco` / `winget` — use the right one.
8. **Permissions** — `chmod`/`chown` are Linux/macOS only; Windows uses `icacls` or `Set-Acl`.

---

## Step 4 — Quick-Reference: Tool Swaps (Verified)

> ⚠️ = exists but has a caveat (deprecated, needs install, needs admin, etc.)
> ❌ = does NOT exist natively on that platform

### File & Directory Operations

| Purpose                | Linux / macOS                | PowerShell                                                                 | cmd.exe                                    |
| ---------------------- | ---------------------------- | -------------------------------------------------------------------------- | ------------------------------------------ |
| List files             | `ls -la`                     | `Get-ChildItem -Force`                                                     | `dir`                                      |
| Print file             | `cat file`                   | `Get-Content file`                                                         | `type file`                                |
| Copy file              | `cp src dst`                 | `Copy-Item src dst`                                                        | `copy src dst`                             |
| Copy dir recursively   | `cp -R src dst`              | `Copy-Item -Recurse src dst`                                               | `xcopy src dst /E /I` ⚠️ prefer `robocopy` |
| Move / rename          | `mv src dst`                 | `Move-Item src dst`                                                        | `move src dst`                             |
| Delete file            | `rm file`                    | `Remove-Item file`                                                         | `del file`                                 |
| Delete dir recursively | `rm -r dir`                  | `Remove-Item -Recurse -Force dir`                                          | `rd /s /q dir`                             |
| Make directory         | `mkdir -p a/b/c`             | `New-Item -ItemType Directory -Force a\b\c`                                | `mkdir a\b\c`                              |
| Create empty file      | `touch file`                 | `New-Item file -ItemType File`                                             | `type nul > file`                          |
| Current directory      | `pwd`                        | `Get-Location`                                                             | `cd` (prints cwd)                          |
| Change directory       | `cd path`                    | `Set-Location path`                                                        | `cd path`                                  |
| Directory tree         | `find . -type d` / `ls -R`   | `Get-ChildItem -Recurse`                                                   | `tree`                                     |
| Disk usage             | `df -h`                      | `Get-PSDrive`                                                              | `wmic logicaldisk get size,freespace`      |
| Dir size               | `du -sh dir`                 | `(Get-ChildItem dir -Recurse \| Measure-Object -Property Length -Sum).Sum` | ❌ use PowerShell                          |
| File type info         | `file filename`              | ❌ no direct equiv                                                         | `assoc` (extension assoc only)             |
| Filesystem check       | `fsck /dev/sdX` ⚠️ unmounted | ❌ use chkdsk                                                              | `chkdsk C: /f` ⚠️ needs admin              |
| Symbolic link          | `ln -s target link`          | `New-Item -ItemType SymbolicLink` ⚠️ needs admin                           | `mklink link target` ⚠️ needs admin        |
| Hard link              | `ln target link`             | `New-Item -ItemType HardLink`                                              | `mklink /H link target`                    |
| File attributes        | `chown` / `chmod`            | `icacls`, `Set-Acl`                                                        | `attrib` (read-only/hidden only)           |

### Search & Text Processing

| Purpose               | Linux / macOS                                | PowerShell                                          | cmd.exe                  |
| --------------------- | -------------------------------------------- | --------------------------------------------------- | ------------------------ |
| Search text in file   | `grep pattern file`                          | `Select-String -Pattern "pattern" -Path file`       | `findstr "pattern" file` |
| Recursive text search | `grep -r pattern .`                          | `Select-String -Pattern "p" -Path .\* -Recurse`     | `findstr /s "pattern" *` |
| Find files by name    | `find . -name "*.txt"`                       | `Get-ChildItem -Recurse -Filter "*.txt"`            | `dir /s /b *.txt`        |
| In-place text replace | `sed -i 's/a/b/' file` ⚠️ macOS: `sed -i ''` | `(Get-Content f) -replace 'a','b' \| Set-Content f` | ❌ use PowerShell        |
| Print column/field    | `awk '{print $2}' file`                      | `(Get-Content f) \| % { ($_ -split '\s+')[1] }`     | ❌ use PowerShell        |
| First N lines         | `head -n 10 file`                            | `Get-Content file \| Select-Object -First 10`       | ❌ use PowerShell        |
| Last N lines          | `tail -n 10 file`                            | `Get-Content file \| Select-Object -Last 10`        | ❌ use PowerShell        |
| Count lines           | `wc -l file`                                 | `(Get-Content file).Count`                          | `find /c /v "" file`     |
| Sort lines            | `sort file`                                  | `Get-Content file \| Sort-Object`                   | `sort file`              |
| Unique lines          | `sort \| uniq`                               | `Sort-Object -Unique`                               | ❌ use PowerShell        |
| Compare files         | `diff file1 file2`                           | `Compare-Object (Get-Content f1) (Get-Content f2)`  | `fc file1 file2`         |
| Page output           | `cmd \| less`                                | `cmd \| more`                                       | `cmd \| more`            |

### Environment & Shell

| Purpose                  | Linux / macOS              | PowerShell                                          | cmd.exe                  |
| ------------------------ | -------------------------- | --------------------------------------------------- | ------------------------ |
| List all env vars        | `env` or `printenv`        | `Get-ChildItem Env:`                                | `set`                    |
| Print env var            | `echo $VAR`                | `$env:VAR`                                          | `echo %VAR%`             |
| Set env var (session)    | `export VAR=val`           | `$env:VAR = "val"`                                  | `set VAR=val`            |
| Set env var (persistent) | append to `~/.bashrc`      | `[System.Environment]::SetEnvironmentVariable(...)` | `setx VAR "val"`         |
| Add to PATH              | `export PATH="$PATH:/dir"` | `$env:PATH += ";C:\dir"`                            | `set Path=%Path%;C:\dir` |
| Find command location    | `which cmd`                | `Get-Command cmd`                                   | `where cmd`              |
| Command history          | `history`                  | `Get-History`                                       | `doskey /history`        |
| Clear screen             | `clear`                    | `Clear-Host`                                        | `cls`                    |
| OS version               | `uname -a`                 | `systeminfo` / `Get-ComputerInfo`                   | `ver` or `systeminfo`    |
| Background job           | `command &`                | `Start-Job { command }`                             | `start command`          |
| Open file browser        | _(GUI-dependent)_          | `explorer.exe .`                                    | `explorer .`             |
| Exit shell               | `exit` or Ctrl+D           | `exit`                                              | `exit`                   |
| Set terminal title       | _(varies by terminal)_     | `$Host.UI.RawUI.WindowTitle = "title"`              | `title My Title`         |

### Networking

| Purpose              | Linux / macOS                                    | PowerShell                                 | cmd.exe                      |
| -------------------- | ------------------------------------------------ | ------------------------------------------ | ---------------------------- |
| Show IP / interfaces | `ip addr` ✅ / `ifconfig` ⚠️ deprecated on Linux | `Get-NetIPAddress`                         | `ipconfig /all`              |
| Ping host            | `ping -c 4 host`                                 | `Test-Connection host -Count 4`            | `ping host`                  |
| DNS lookup           | `nslookup host` / `dig host`                     | `Resolve-DnsName host`                     | `nslookup host`              |
| Trace route          | `traceroute host` ⚠️ may need install            | `Test-NetConnection -TraceRoute host`      | `tracert host`               |
| ARP table            | `arp -n`                                         | `Get-NetNeighbor`                          | `arp -a`                     |
| Show open ports      | `ss -tlnp` ✅ / `netstat`                        | `Get-NetTCPConnection`                     | `netstat -ano`               |
| Download file        | `curl -o file URL`                               | `Invoke-WebRequest -Uri URL -OutFile file` | `curl -o file URL` ⚠️ Win10+ |
| Download file        | `wget URL`                                       | `Invoke-WebRequest -Uri URL -OutFile file` | ❌ use curl                  |
| FTP client           | `ftp host` ⚠️ may need install                   | ❌ use WinSCP/sftp                         | `ftp host` ⚠️ deprecated     |
| Send to printer      | `lpr file` ⚠️ needs CUPS                         | ❌ use GUI                                 | `print file` (basic)         |
| Hostname             | `hostname`                                       | `hostname` or `$env:COMPUTERNAME`          | `hostname`                   |

### Process Management

| Purpose             | Linux / macOS   | PowerShell                                                 | cmd.exe                      |
| ------------------- | --------------- | ---------------------------------------------------------- | ---------------------------- |
| List processes      | `ps aux`        | `Get-Process`                                              | `tasklist`                   |
| Kill by PID         | `kill PID`      | `Stop-Process -Id PID`                                     | `taskkill /PID PID /F`       |
| Kill by name        | `pkill name`    | `Stop-Process -Name name`                                  | `taskkill /IM name.exe /F`   |
| System top / status | `top` or `htop` | `Get-Process \| Sort-Object CPU -Desc`                     | ❌ use Task Manager          |
| Logged-in users     | `who` / `w`     | `query user`                                               | `net session` ⚠️ needs admin |
| System uptime       | `uptime`        | `(Get-Date) - (gcim Win32_OperatingSystem).LastBootUpTime` | `net statistics workstation` |

### Scheduling & Administration

| Purpose                 | Linux / macOS       | PowerShell                   | cmd.exe                               |
| ----------------------- | ------------------- | ---------------------------- | ------------------------------------- |
| Schedule recurring task | `crontab -e`        | `New-ScheduledTask`          | `schtasks /create ...`                |
| Schedule one-time task  | `at HH:MM command`  | `schtasks /create /sc once`  | `schtasks` / `at` ⚠️ deprecated Win8+ |
| Shutdown                | `shutdown -h now`   | `Stop-Computer`              | `shutdown -s`                         |
| Reboot                  | `shutdown -r now`   | `Restart-Computer`           | `shutdown -r`                         |
| Registry edit           | ❌ (use /etc files) | `Get-ItemProperty HKLM:\...` | `regedit` (GUI)                       |
| Help for command        | `man command`       | `Get-Help command`           | `help command` or `command /?`        |

---

## Step 5 — Script Portability

If the user needs a script that runs on multiple OSes:

- Prefer **Python** or **Node.js** — they handle cross-platform differences natively.
- If shell is required, write **two versions**: `.sh` (bash) and `.ps1` (PowerShell).
- Use Python's `pathlib`, `shutil`, `os`, `subprocess` — they abstract path and OS differences.
- Never hardcode paths; use env vars or config files.

---

## Notes

- **macOS `sed`/`grep`/`find`** are BSD versions — they differ from GNU Linux. Key diff: `sed -i ''` (macOS) vs `sed -i` (Linux). Flag this whenever GNU-specific flags appear.
- **WSL** users can call Windows executables with `.exe` suffix (`notepad.exe`) and access Windows drives at `/mnt/c/`.
- **Windows `find`** searches for strings in files (like `grep`). It does NOT find files by name — use `dir /s /b` for that.
- **`ifconfig`** is deprecated on Linux — use `ip addr` instead. Still works if `net-tools` is installed.
- **`traceroute`** may not be installed on Linux by default — use `tracepath` as an always-available alternative, or `sudo apt install traceroute`.
