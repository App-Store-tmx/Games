import customtkinter as ctk
import random
from tkinter import messagebox
import tkinter as tk

class GuessTheNumber(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Guess The Number")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            # Fallback if icon.png is missing or loading fails
            pass
        self.geometry("400x300")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.target_number = random.randint(1, 100)
        self.attempts = 0

        self.label = ctk.CTkLabel(self, text="I'm thinking of a number between 1 and 100", font=("Arial", 16))
        self.label.pack(pady=20)

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter your guess")
        self.entry.pack(pady=10)

        self.guess_btn = ctk.CTkButton(self, text="Guess", command=self.check_guess)
        self.guess_btn.pack(pady=10)

        self.result_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.reset_btn = ctk.CTkButton(self, text="Restart", command=self.reset_game)
        self.reset_btn.pack(pady=10)

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1
            if guess < self.target_number:
                self.result_label.configure(text="Too low! Try again.")
            elif guess > self.target_number:
                self.result_label.configure(text="Too high! Try again.")
            else:
                messagebox.showinfo("Congratulations!", f"Correct! It took you {self.attempts} attempts.")
                self.reset_game()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def reset_game(self):
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.entry.delete(0, 'end')
        self.result_label.configure(text="")

if __name__ == "__main__":
    app = GuessTheNumber()
    app.mainloop()
