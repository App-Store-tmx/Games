#!/bin/bash
# uninstall.sh for TypingTest

echo "Uninstalling TypingTest..."

# 1. Remove application folder
rm -rf ~/TypingTest

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/TypingTest-launch
rm -f /data/data/com.termux/files/usr/bin/TypingTest_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/TypingTest.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "TypingTest uninstalled successfully."
