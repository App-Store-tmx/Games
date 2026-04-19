#!/bin/bash
# install.sh for ColorPickerGame

echo "Installing ColorPickerGame..."
pkg install python-tkinter -y
pip install customtkinter

mkdir -p ~/ColorPickerGame
cp app.py ~/ColorPickerGame/

cp launch.sh /data/data/com.termux/files/usr/bin/ColorPickerGame-launch
chmod +x /data/data/com.termux/files/usr/bin/ColorPickerGame-launch

mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/ColorPickerGame.desktop
update-desktop-database ~/.local/share/applications/

echo "Done!"
