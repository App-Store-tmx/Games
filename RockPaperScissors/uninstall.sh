#!/bin/bash
# uninstall.sh for RockPaperScissors

echo "Uninstalling RockPaperScissors..."

# 1. Remove application folder
rm -rf ~/RockPaperScissors

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/RockPaperScissors-launch
rm -f /data/data/com.termux/files/usr/bin/RockPaperScissors_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/RockPaperScissors.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "RockPaperScissors uninstalled successfully."
