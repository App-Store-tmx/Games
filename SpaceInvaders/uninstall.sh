#!/bin/bash
# uninstall.sh for SpaceInvaders

echo "Uninstalling SpaceInvaders..."

# 1. Remove application folder
rm -rf ~/SpaceInvaders

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/SpaceInvaders-launch
rm -f /data/data/com.termux/files/usr/bin/SpaceInvaders_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/SpaceInvaders.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "SpaceInvaders uninstalled successfully."
