#!/bin/bash
# uninstall.sh for FlappyBird

echo "Uninstalling FlappyBird..."

# 1. Remove application folder
rm -rf ~/FlappyBird

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/FlappyBird-launch
rm -f /data/data/com.termux/files/usr/bin/FlappyBird_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/FlappyBird.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "FlappyBird uninstalled successfully."
