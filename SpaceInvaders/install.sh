#!/bin/bash
# Install dependencies
pkg install -y python-tkinter
pip install customtkinter

# Create app directory and move files
mkdir -p ~/SpaceInvaders
cp app.py ~/SpaceInvaders/app.py
cp icon.png ~/SpaceInvaders/

# Create launch wrapper
cat <<EOF > /data/data/com.termux/files/usr/bin/SpaceInvaders-launch
#!/bin/bash
python ~/SpaceInvaders/app.py
EOF
chmod +x /data/data/com.termux/files/usr/bin/SpaceInvaders-launch

# Install desktop entry
mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/SpaceInvaders.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/

echo "SpaceInvaders installed successfully!"
