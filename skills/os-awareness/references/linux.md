# Linux Tool Reference

**Shell:** bash or zsh  
**Package Manager:** apt (Debian/Ubuntu), dnf/yum (Fedora/RHEL), pacman (Arch), zypper (openSUSE)  
**Path separator:** `/`  
**Line endings:** LF (`\n`)  
**Env vars:** `$VAR` or `${VAR}`  
**Home dir:** `$HOME` or `~`  
**Script shebang:** `#!/bin/bash` or `#!/usr/bin/env bash`

## Common Idioms

```bash
# Find files
find /path -name "*.txt" -type f

# Search in files
grep -r "pattern" /path

# Edit in-place
sed -i 's/old/new/g' file.txt

# Process columns
awk '{print $2}' file.txt

# Count lines
wc -l file.txt

# Show first/last lines
head -n 20 file.txt
tail -n 20 file.txt

# Recursive delete
rm -rf directory/

# Make executable
chmod +x script.sh

# Run as root
sudo command

# Install packages (Debian/Ubuntu)
sudo apt update && sudo apt install package-name

# Check running processes
ps aux | grep process-name

# Port listening check
ss -tlnp | grep :8080
# or
netstat -tlnp | grep :8080
```

## Networking Notes

```bash
# ifconfig is DEPRECATED on Linux — use ip instead:
ip addr show               # like ifconfig -a
ip addr show eth0          # specific interface
ip route show              # routing table

# traceroute may need installation:
sudo apt install traceroute   # Debian/Ubuntu
sudo dnf install traceroute   # Fedora/RHEL
# Alternative always available:
tracepath host             # like traceroute, no root needed

# nslookup works, but dig is preferred on Linux:
dig example.com
dig example.com A          # specific record type
```

## General Notes

- `grep` on Linux is GNU grep — supports `-P` for Perl regex, `-E` for extended regex.
- `sed` on Linux is GNU sed — `sed -i 's/old/new/' file` works without a backup suffix (unlike macOS).
- `find` on Linux is GNU find — many extra options vs BSD find on macOS.
- `ifconfig` still works if `net-tools` is installed, but `ip` is the modern replacement.
- Use `lsb_release -a` or `cat /etc/os-release` to identify the specific distro.
- `at` (one-time scheduling) may need `sudo apt install at`; `cron` is usually pre-installed.
