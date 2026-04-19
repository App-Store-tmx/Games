import customtkinter as ctk
import random
import time
from tkinter import messagebox

class MemoryMatch(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Memory Match")
        self.geometry("500x600")
        ctk.set_appearance_mode("dark")

        self.symbols = ["🍎", "🍌", "🍇", "🍉", "🍓", "🍒", "🍍", "🥝"] * 2
        random.shuffle(self.symbols)

        self.buttons = []
        self.first_guess = None
        self.second_guess = None
        self.matches = 0
        self.can_click = True

        self.label = ctk.CTkLabel(self, text="Memory Match", font=("Arial", 24))
        self.label.pack(pady=20)

        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(padx=20, pady=10)

        for i in range(16):
            btn = ctk.CTkButton(self.grid_frame, text="?", width=100, height=100, 
                                font=("Arial", 32), command=lambda i=i: self.click(i))
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
            self.buttons.append(btn)

        self.reset_btn = ctk.CTkButton(self, text="Reset Game", command=self.reset_game)
        self.reset_btn.pack(pady=20)

    def click(self, i):
        if not self.can_click or self.buttons[i].cget("text") != "?":
            return

        self.buttons[i].configure(text=self.symbols[i])

        if self.first_guess is None:
            self.first_guess = i
        else:
            self.second_guess = i
            self.can_click = False
            self.after(700, self.check_match)

    def check_match(self):
        if self.symbols[self.first_guess] == self.symbols[self.second_guess]:
            self.matches += 1
            if self.matches == 8:
                messagebox.showinfo("Game Over", "Congratulations! You found all matches!")
        else:
            self.buttons[self.first_guess].configure(text="?")
            self.buttons[self.second_guess].configure(text="?")

        self.first_guess = None
        self.second_guess = None
        self.can_click = True

    def reset_game(self):
        random.shuffle(self.symbols)
        for btn in self.buttons:
            btn.configure(text="?")
        self.matches = 0
        self.first_guess = None
        self.second_guess = None
        self.can_click = True

if __name__ == "__main__":
    app = MemoryMatch()
    app.mainloop()
