#!/bin/bash
# uninstall.sh for SimonSays

echo "Uninstalling SimonSays..."

# 1. Remove application folder
rm -rf ~/SimonSays

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/SimonSays-launch
rm -f /data/data/com.termux/files/usr/bin/SimonSays_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/SimonSays.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "SimonSays uninstalled successfully."
