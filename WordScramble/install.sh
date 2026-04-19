#!/bin/bash
# Install dependencies
pkg install -y python-tkinter
pip install customtkinter

# Create app directory and move files
mkdir -p ~/WordScramble
cp app.py ~/WordScramble/app.py
cp icon.png ~/WordScramble/

# Create launch wrapper
cat <<EOF > /data/data/com.termux/files/usr/bin/WordScramble-launch
#!/bin/bash
python ~/WordScramble/app.py
EOF
chmod +x /data/data/com.termux/files/usr/bin/WordScramble-launch

# Install desktop entry
mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/WordScramble.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/

echo "WordScramble installed successfully!"
