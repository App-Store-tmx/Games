#!/bin/bash
# install.sh for SimonSays

echo "Installing SimonSays..."

pkg install python-tkinter -y
pip install customtkinter

mkdir -p ~/SimonSays
cp app.py ~/SimonSays/
cp icon.png ~/SimonSays/

cp launch.sh /data/data/com.termux/files/usr/bin/SimonSays-launch
chmod +x /data/data/com.termux/files/usr/bin/SimonSays-launch

mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/SimonSays.desktop
update-desktop-database ~/.local/share/applications/

echo "Installation complete!"
