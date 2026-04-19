#!/bin/bash
# Install dependencies
pkg install -y python-tkinter
pip install customtkinter

# Create app directory and move files
mkdir -p ~/WhackAMole
cp app.py ~/WhackAMole/app.py

# Create launch wrapper
cat <<EOF > /data/data/com.termux/files/usr/bin/WhackAMole-launch
#!/bin/bash
python ~/WhackAMole/app.py
EOF
chmod +x /data/data/com.termux/files/usr/bin/WhackAMole-launch

# Install desktop entry
mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/WhackAMole.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/

echo "WhackAMole installed successfully!"
