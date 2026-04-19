# Hangman

Guess the hidden word letter by letter before you run out of lives.

This game is fully optimized for the **Termux XFCE4 Desktop Environment**, featuring a modern Dark Mode aesthetic powered by CustomTkinter.

## Features
- **Android/Termux Native:** Built specifically for aarch64 environments without heavy GTK/Qt dependencies.
- **XFCE Integration:** Includes an automatic `.desktop` file for your applications menu.
- **Standalone:** Independent installation and execution paths.

## Installation
To install this game individually in your Termux environment:
```bash
chmod +x install.sh
./install.sh
```
*Alternatively, use `install_all.sh` in the root directory to install all games.*

## How to Play
Once installed, you can launch the game from your **XFCE Applications Menu -> Games -> Hangman**.
Or, from the terminal:
```bash
Hangman-launch
```

## Uninstallation
To remove the game, its launcher, and desktop entry:
```bash
chmod +x uninstall.sh
./uninstall.sh
```
