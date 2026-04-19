#!/bin/bash
# Install dependencies
pkg install -y python-tkinter
pip install customtkinter

# Create app directory and move files
mkdir -p ~/Breakout
cp app.py ~/Breakout/app.py
cp icon.png ~/Breakout/

# Create launch wrapper
cat <<EOF > /data/data/com.termux/files/usr/bin/Breakout-launch
#!/bin/bash
python ~/Breakout/app.py
EOF
chmod +x /data/data/com.termux/files/usr/bin/Breakout-launch

# Install desktop entry
mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/Breakout.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/

echo "Breakout installed successfully!"
