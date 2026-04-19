#!/bin/bash
# uninstall.sh for GuessTheNumber

echo "Uninstalling GuessTheNumber..."

# 1. Remove application folder
rm -rf ~/GuessTheNumber

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/GuessTheNumber-launch
rm -f /data/data/com.termux/files/usr/bin/GuessTheNumber_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/GuessTheNumber.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "GuessTheNumber uninstalled successfully."
