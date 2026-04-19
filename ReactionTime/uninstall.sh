#!/bin/bash
# uninstall.sh for ReactionTime

echo "Uninstalling ReactionTime..."

# 1. Remove application folder
rm -rf ~/ReactionTime

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/ReactionTime-launch
rm -f /data/data/com.termux/files/usr/bin/ReactionTime_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/ReactionTime.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "ReactionTime uninstalled successfully."
