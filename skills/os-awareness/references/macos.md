# macOS Tool Reference

**Shell:** zsh (default macOS 10.15+), bash (older)  
**Package Manager:** Homebrew (`brew`), MacPorts  
**Path separator:** `/`  
**Line endings:** LF (`\n`)  
**Env vars:** `$VAR` or `${VAR}`  
**Home dir:** `$HOME` or `~` (typically `/Users/username`)  
**Script shebang:** `#!/bin/zsh` or `#!/usr/bin/env bash`

## Key Differences from Linux (BSD vs GNU)

macOS ships with **BSD versions** of core tools — they differ from GNU Linux versions:

| Tool             | macOS (BSD)                                | Linux (GNU)            | Fix                                     |
| ---------------- | ------------------------------------------ | ---------------------- | --------------------------------------- |
| `sed -i`         | Requires backup: `sed -i '' 's/a/b/' file` | `sed -i 's/a/b/' file` | Add `''` on mac                         |
| `grep -P`        | Not supported (no Perl regex)              | Supported              | Use `grep -E` or install GNU grep       |
| `find -maxdepth` | Supported                                  | Supported              | Same                                    |
| `date`           | `date -v+1d` for date math                 | `date -d '+1 day'`     | Different flags                         |
| `ls --color`     | Not supported                              | Supported              | Use `ls -G` on mac                      |
| `readlink -f`    | Not supported                              | Supported              | Use `greadlink -f` (brew gnu-coreutils) |
| `xargs -d`       | Not supported                              | Supported              | Use `tr` workaround                     |

## Common Idioms

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install packages
brew install package-name

# Install GNU tools to replace BSD versions
brew install gnu-sed grep findutils coreutils
# Then use: gsed, ggrep, gfind, gls, greadlink

# Find files
find /path -name "*.txt" -type f

# In-place sed (macOS style)
sed -i '' 's/old/new/g' file.txt

# Check listening ports
lsof -i :8080

# Show processes
ps aux | grep process-name

# Open file with default app
open file.pdf
open -a "Visual Studio Code" file.txt

# Copy to clipboard
cat file.txt | pbcopy

# Paste from clipboard
pbpaste > file.txt
```

## Notes

- Use `sw_vers` to get macOS version info.
- Apple Silicon (M1/M2/M3) Macs use ARM64 — some software needs Rosetta 2 or ARM builds.
- Homebrew on Apple Silicon installs to `/opt/homebrew/`, on Intel to `/usr/local/`.
- `open` is a macOS-only command (no Linux equivalent without a DE).
