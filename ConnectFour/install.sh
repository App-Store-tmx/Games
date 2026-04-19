#!/bin/bash
# Install dependencies
pkg install -y python-tkinter
pip install customtkinter

# Create app directory and move files
mkdir -p ~/ConnectFour
cp app.py ~/ConnectFour/app.py
cp icon.png ~/ConnectFour/

# Create launch wrapper
cat <<EOF > /data/data/com.termux/files/usr/bin/ConnectFour-launch
#!/bin/bash
python ~/ConnectFour/app.py
EOF
chmod +x /data/data/com.termux/files/usr/bin/ConnectFour-launch

# Install desktop entry
mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/ConnectFour.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/

echo "ConnectFour installed successfully!"
