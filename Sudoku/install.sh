#!/bin/bash
# Install dependencies
pkg install -y python-tkinter
pip install customtkinter

# Create app directory and move files
mkdir -p ~/Sudoku
cp app.py ~/Sudoku/app.py
cp icon.png ~/Sudoku/

# Create launch wrapper
cat <<EOF > /data/data/com.termux/files/usr/bin/Sudoku-launch
#!/bin/bash
python ~/Sudoku/app.py
EOF
chmod +x /data/data/com.termux/files/usr/bin/Sudoku-launch

# Install desktop entry
mkdir -p ~/.local/share/applications/
cp app.desktop ~/.local/share/applications/Sudoku.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/

echo "Sudoku installed successfully!"
