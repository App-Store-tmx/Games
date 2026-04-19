#!/bin/bash
# uninstall.sh for Sudoku

echo "Uninstalling Sudoku..."

# 1. Remove application folder
rm -rf ~/Sudoku

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/Sudoku-launch
rm -f /data/data/com.termux/files/usr/bin/Sudoku_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/Sudoku.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "Sudoku uninstalled successfully."
