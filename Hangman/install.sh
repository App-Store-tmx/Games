#!/bin/bash
# install.sh for Hangman

echo "Installing Hangman..."

# Install system dependencies
pkg install python-tkinter -y

# Install python dependencies
pip install customtkinter

# Create application directory
mkdir -p ~/Hangman

# Copy application files
cp app.py ~/Hangman/

# Install launch script to /usr/bin/
cp launch.sh /data/data/com.termux/files/usr/bin/Hangman-launch
chmod +x /data/data/com.termux/files/usr/bin/Hangman-launch

# Install desktop entry
mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/Hangman.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/

echo "Installation complete! You can find Hangman in your applications menu."
