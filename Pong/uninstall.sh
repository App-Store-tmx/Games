#!/bin/bash
# uninstall.sh for Pong

echo "Uninstalling Pong..."

# 1. Remove application folder
rm -rf ~/Pong

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/Pong-launch
rm -f /data/data/com.termux/files/usr/bin/Pong_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/Pong.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "Pong uninstalled successfully."
