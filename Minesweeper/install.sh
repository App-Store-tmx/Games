#!/bin/bash
# install.sh for Minesweeper

echo "Installing Minesweeper..."

pkg install python-tkinter -y
pip install customtkinter

mkdir -p ~/Minesweeper
cp app.py ~/Minesweeper/
cp icon.png ~/Minesweeper/

cp launch.sh /data/data/com.termux/files/usr/bin/Minesweeper-launch
chmod +x /data/data/com.termux/files/usr/bin/Minesweeper-launch

mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/Minesweeper.desktop
update-desktop-database ~/.local/share/applications/

echo "Installation complete!"
