#!/bin/bash
# Install dependencies
pkg install -y python-tkinter
pip install customtkinter

# Create app directory and move files
mkdir -p ~/15Puzzle
cp app.py ~/15Puzzle/app.py
cp icon.png ~/15Puzzle/

# Create launch wrapper
cat <<EOF > /data/data/com.termux/files/usr/bin/15Puzzle-launch
#!/bin/bash
python ~/15Puzzle/app.py
EOF
chmod +x /data/data/com.termux/files/usr/bin/15Puzzle-launch

# Install desktop entry
mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/15Puzzle.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/

echo "15Puzzle installed successfully!"
