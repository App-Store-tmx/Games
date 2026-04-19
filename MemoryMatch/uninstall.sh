#!/bin/bash
# uninstall.sh for MemoryMatch

echo "Uninstalling MemoryMatch..."

# 1. Remove application folder
rm -rf ~/MemoryMatch

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/MemoryMatch-launch
rm -f /data/data/com.termux/files/usr/bin/MemoryMatch_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/MemoryMatch.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "MemoryMatch uninstalled successfully."
