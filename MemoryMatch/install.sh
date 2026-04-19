#!/bin/bash
# install.sh for MemoryMatch

echo "Installing MemoryMatch..."

pkg install python-tkinter -y
pip install customtkinter

mkdir -p ~/MemoryMatch
cp app.py ~/MemoryMatch/
cp icon.png ~/MemoryMatch/

cp launch.sh /data/data/com.termux/files/usr/bin/MemoryMatch-launch
chmod +x /data/data/com.termux/files/usr/bin/MemoryMatch-launch

mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/MemoryMatch.desktop
update-desktop-database ~/.local/share/applications/

echo "Installation complete!"
