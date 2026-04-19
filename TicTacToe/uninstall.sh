#!/bin/bash
# uninstall.sh for TicTacToe

echo "Uninstalling TicTacToe..."

# 1. Remove application folder
rm -rf ~/TicTacToe

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/TicTacToe-launch
rm -f /data/data/com.termux/files/usr/bin/TicTacToe_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/TicTacToe.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "TicTacToe uninstalled successfully."
