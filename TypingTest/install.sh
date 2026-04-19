#!/bin/bash
# Install dependencies
pkg install -y python-tkinter
pip install customtkinter

# Create app directory and move files
mkdir -p ~/TypingTest
cp app.py ~/TypingTest/app.py

# Create launch wrapper
cat <<EOF > /data/data/com.termux/files/usr/bin/TypingTest-launch
#!/bin/bash
python ~/TypingTest/app.py
EOF
chmod +x /data/data/com.termux/files/usr/bin/TypingTest-launch

# Install desktop entry
mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/TypingTest.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/

echo "TypingTest installed successfully!"
