#!/bin/bash
# Install dependencies
pkg install -y python-tkinter
pip install customtkinter

# Create app directory and move files
mkdir -p ~/FlappyBird
cp app.py ~/FlappyBird/app.py
cp icon.png ~/FlappyBird/

# Create launch wrapper
cat <<EOF > /data/data/com.termux/files/usr/bin/FlappyBird-launch
#!/bin/bash
python ~/FlappyBird/app.py
EOF
chmod +x /data/data/com.termux/files/usr/bin/FlappyBird-launch

# Install desktop entry
mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/FlappyBird.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/

echo "FlappyBird installed successfully!"
