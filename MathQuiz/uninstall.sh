#!/bin/bash
# uninstall.sh for MathQuiz

echo "Uninstalling MathQuiz..."

# 1. Remove application folder
rm -rf ~/MathQuiz

# 2. Remove launch scripts from /usr/bin/
rm -f /data/data/com.termux/files/usr/bin/MathQuiz-launch
rm -f /data/data/com.termux/files/usr/bin/MathQuiz_launch

# 3. Remove desktop entry
rm -f ~/.local/share/applications/MathQuiz.desktop

# 4. Update desktop database
update-desktop-database ~/.local/share/applications/

echo "MathQuiz uninstalled successfully."
