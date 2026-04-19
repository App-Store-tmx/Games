#!/bin/bash
# uninstall.sh for Snake

echo "Uninstalling Snake..."

# 1. Remove application folder
rm -rf ~/Snake

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/Snake-launch
rm -f /data/data/com.termux/files/usr/bin/Snake_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/Snake.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "Snake uninstalled successfully."
