#!/bin/bash
# install.sh for 2048

echo "Installing 2048..."

pkg install python-tkinter -y
pip install customtkinter

mkdir -p ~/2048
cp app.py ~/2048/

cp launch.sh /data/data/com.termux/files/usr/bin/2048-launch
chmod +x /data/data/com.termux/files/usr/bin/2048-launch

mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/2048.desktop
update-desktop-database ~/.local/share/applications/

echo "Installation complete!"
