#!/bin/bash
# uninstall.sh for 2048

echo "Uninstalling 2048..."

# 1. Remove application folder
rm -rf ~/2048

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/2048-launch
rm -f /data/data/com.termux/files/usr/bin/2048_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/2048.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "2048 uninstalled successfully."
