#!/bin/bash
# install.sh for TicTacToe

echo "Installing TicTacToe..."

# Install system dependencies
pkg install python-tkinter -y

# Install python dependencies
pip install customtkinter

# Create application directory
mkdir -p ~/TicTacToe

# Copy application files
cp app.py ~/TicTacToe/

# Install launch script to /usr/bin/
cp launch.sh /data/data/com.termux/files/usr/bin/TicTacToe-launch
chmod +x /data/data/com.termux/files/usr/bin/TicTacToe-launch

# Install desktop entry
mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/TicTacToe.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/

echo "Installation complete! You can find TicTacToe in your applications menu."
