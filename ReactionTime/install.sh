#!/bin/bash
# install.sh for ReactionTime

echo "Installing ReactionTime..."
pkg install python-tkinter -y
pip install customtkinter

mkdir -p ~/ReactionTime
cp app.py ~/ReactionTime/

cp launch.sh /data/data/com.termux/files/usr/bin/ReactionTime-launch
chmod +x /data/data/com.termux/files/usr/bin/ReactionTime-launch

mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/ReactionTime.desktop
update-desktop-database ~/.local/share/applications/

echo "Done!"
