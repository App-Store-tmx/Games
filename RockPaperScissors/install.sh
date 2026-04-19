#!/bin/bash
# install.sh for RockPaperScissors

echo "Installing RockPaperScissors..."

pkg install python-tkinter -y
pip install customtkinter

mkdir -p ~/RockPaperScissors
cp app.py ~/RockPaperScissors/
cp icon.png ~/RockPaperScissors/

cp launch.sh /data/data/com.termux/files/usr/bin/RockPaperScissors-launch
chmod +x /data/data/com.termux/files/usr/bin/RockPaperScissors-launch

mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/RockPaperScissors.desktop

update-desktop-database ~/.local/share/applications/

echo "Installation complete!"
