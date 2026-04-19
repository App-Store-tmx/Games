#!/bin/bash
# uninstall.sh for ColorPickerGame

echo "Uninstalling ColorPickerGame..."

# 1. Remove application folder
rm -rf ~/ColorPickerGame

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/ColorPickerGame-launch
rm -f /data/data/com.termux/files/usr/bin/ColorPickerGame_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/ColorPickerGame.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "ColorPickerGame uninstalled successfully."
