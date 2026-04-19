#!/bin/bash
# uninstall.sh for 15Puzzle

echo "Uninstalling 15Puzzle..."

# 1. Remove application folder
rm -rf ~/15Puzzle

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/15Puzzle-launch
rm -f /data/data/com.termux/files/usr/bin/15Puzzle_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/15Puzzle.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "15Puzzle uninstalled successfully."
