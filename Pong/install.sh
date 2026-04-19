#!/bin/bash
# install.sh for Pong

echo "Installing Pong..."

pkg install python-tkinter -y
pip install customtkinter

mkdir -p ~/Pong
cp app.py ~/Pong/
cp icon.png ~/Pong/

cp launch.sh /data/data/com.termux/files/usr/bin/Pong-launch
chmod +x /data/data/com.termux/files/usr/bin/Pong-launch

mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/Pong.desktop
update-desktop-database ~/.local/share/applications/

echo "Installation complete!"
