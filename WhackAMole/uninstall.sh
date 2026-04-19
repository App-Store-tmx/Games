#!/bin/bash
# uninstall.sh for WhackAMole

echo "Uninstalling WhackAMole..."

# 1. Remove application folder
rm -rf ~/WhackAMole

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/WhackAMole-launch
rm -f /data/data/com.termux/files/usr/bin/WhackAMole_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/WhackAMole.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "WhackAMole uninstalled successfully."
