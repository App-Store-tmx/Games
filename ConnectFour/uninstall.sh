#!/bin/bash
# uninstall.sh for ConnectFour

echo "Uninstalling ConnectFour..."

# 1. Remove application folder
rm -rf ~/ConnectFour

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/ConnectFour-launch
rm -f /data/data/com.termux/files/usr/bin/ConnectFour_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/ConnectFour.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "ConnectFour uninstalled successfully."
