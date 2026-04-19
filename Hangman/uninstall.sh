#!/bin/bash
# uninstall.sh for Hangman

echo "Uninstalling Hangman..."

# 1. Remove application folder
rm -rf ~/Hangman

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/Hangman-launch
rm -f /data/data/com.termux/files/usr/bin/Hangman_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/Hangman.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "Hangman uninstalled successfully."
