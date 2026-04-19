#!/bin/bash
# Install dependencies
pkg install -y python-tkinter
pip install customtkinter

# Create app directory and move files
mkdir -p ~/MathQuiz
cp app.py ~/MathQuiz/app.py
cp icon.png ~/MathQuiz/

# Create launch wrapper
cat <<EOF > /data/data/com.termux/files/usr/bin/MathQuiz-launch
#!/bin/bash
python ~/MathQuiz/app.py
EOF
chmod +x /data/data/com.termux/files/usr/bin/MathQuiz-launch

# Install desktop entry
mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/MathQuiz.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/

echo "MathQuiz installed successfully!"
