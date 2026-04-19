#!/bin/bash
# uninstall.sh for Minesweeper

echo "Uninstalling Minesweeper..."

# 1. Remove application folder
rm -rf ~/Minesweeper

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/Minesweeper-launch
rm -f /data/data/com.termux/files/usr/bin/Minesweeper_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/Minesweeper.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "Minesweeper uninstalled successfully."
