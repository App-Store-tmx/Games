#!/bin/bash
# install.sh for GuessTheNumber

echo "Installing GuessTheNumber..."

pkg install python-tkinter -y
pip install customtkinter

mkdir -p ~/GuessTheNumber
cp app.py ~/GuessTheNumber/
cp icon.png ~/GuessTheNumber/

cp launch.sh /data/data/com.termux/files/usr/bin/GuessTheNumber-launch
chmod +x /data/data/com.termux/files/usr/bin/GuessTheNumber-launch

mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/GuessTheNumber.desktop

update-desktop-database ~/.local/share/applications/

echo "Installation complete!"
