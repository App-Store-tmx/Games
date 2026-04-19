#!/bin/bash
# uninstall.sh for WordScramble

echo "Uninstalling WordScramble..."

# 1. Remove application folder
rm -rf ~/WordScramble

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/WordScramble-launch
rm -f /data/data/com.termux/files/usr/bin/WordScramble_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/WordScramble.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "WordScramble uninstalled successfully."
