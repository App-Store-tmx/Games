#!/bin/bash
# install.sh for Snake

echo "Installing Snake..."

pkg install python-tkinter -y
pip install customtkinter

mkdir -p ~/Snake
cp app.py ~/Snake/
cp icon.png ~/Snake/

cp launch.sh /data/data/com.termux/files/usr/bin/Snake-launch
chmod +x /data/data/com.termux/files/usr/bin/Snake-launch

mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/Snake.desktop

update-desktop-database ~/.local/share/applications/

echo "Installation complete!"
