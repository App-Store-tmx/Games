import customtkinter as ctk
import random
from tkinter import messagebox
import tkinter as tk

class Hangman(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hangman")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            # Fallback if icon.png is missing or loading fails
            pass
        self.geometry("500x500")
        ctk.set_appearance_mode("dark")

        self.words = ["PYTHON", "TERMUX", "LINUX", "GAME", "DESKTOP", "CODING", "TKINTER", "MOBILE"]
        self.reset_game()

        self.word_label = ctk.CTkLabel(self, text=self.display_word(), font=("Courier", 30))
        self.word_label.pack(pady=40)

        self.info_label = ctk.CTkLabel(self, text=f"Attempts left: {self.attempts_left}", font=("Arial", 16))
        self.info_label.pack(pady=10)

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter a letter", width=150)
        self.entry.pack(pady=10)

        self.guess_btn = ctk.CTkButton(self, text="Guess", command=self.make_guess)
        self.guess_btn.pack(pady=10)

        self.used_label = ctk.CTkLabel(self, text="Used: ", font=("Arial", 14))
        self.used_label.pack(pady=10)

        self.reset_btn = ctk.CTkButton(self, text="New Game", command=self.reset_game_ui)
        self.reset_btn.pack(pady=20)

    def reset_game(self):
        self.target_word = random.choice(self.words)
        self.guessed_letters = set()
        self.attempts_left = 6

    def reset_game_ui(self):
        self.reset_game()
        self.word_label.configure(text=self.display_word())
        self.info_label.configure(text=f"Attempts left: {self.attempts_left}")
        self.used_label.configure(text="Used: ")
        self.entry.delete(0, 'end')

    def display_word(self):
        return " ".join([c if c in self.guessed_letters else "_" for c in self.target_word])

    def make_guess(self):
        guess = self.entry.get().upper()
        self.entry.delete(0, 'end')

        if not guess or len(guess) != 1 or not guess.isalpha():
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Info", "You already guessed that letter.")
            return

        self.guessed_letters.add(guess)
        self.used_label.configure(text=f"Used: {', '.join(sorted(self.guessed_letters))}")

        if guess not in self.target_word:
            self.attempts_left -= 1
            self.info_label.configure(text=f"Attempts left: {self.attempts_left}")

        self.word_label.configure(text=self.display_word())

        if "_" not in self.display_word():
            messagebox.showinfo("Winner!", f"You got it! The word was {self.target_word}")
            self.reset_game_ui()
        elif self.attempts_left <= 0:
            messagebox.showinfo("Game Over", f"Out of attempts! The word was {self.target_word}")
            self.reset_game_ui()

if __name__ == "__main__":
    app = Hangman()
    app.mainloop()
