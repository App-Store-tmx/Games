#!/bin/bash
# uninstall.sh for Breakout

echo "Uninstalling Breakout..."

# 1. Remove application folder
rm -rf ~/Breakout

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/Breakout-launch
rm -f /data/data/com.termux/files/usr/bin/Breakout_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/Breakout.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "Breakout uninstalled successfully."
