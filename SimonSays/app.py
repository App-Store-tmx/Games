import customtkinter as ctk
import random
from tkinter import messagebox

class SimonSays(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simon Says")
        self.geometry("400x500")
        ctk.set_appearance_mode("dark")

        self.colors = ["red", "green", "blue", "yellow"]
        self.sequence = []
        self.user_sequence = []
        self.can_click = False

        self.label = ctk.CTkLabel(self, text="Simon Says", font=("Arial", 24))
        self.label.pack(pady=20)

        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(padx=20, pady=10)

        self.buttons = {}
        for color in self.colors:
            btn = ctk.CTkButton(self.grid_frame, text="", width=150, height=150, 
                                fg_color=color, hover_color=color,
                                command=lambda c=color: self.user_click(c))
            self.buttons[color] = btn
            
        self.buttons["green"].grid(row=0, column=0, padx=5, pady=5)
        self.buttons["red"].grid(row=0, column=1, padx=5, pady=5)
        self.buttons["yellow"].grid(row=1, column=0, padx=5, pady=5)
        self.buttons["blue"].grid(row=1, column=1, padx=5, pady=5)

        self.start_btn = ctk.CTkButton(self, text="Start Game", command=self.start_game)
        self.start_btn.pack(pady=20)

    def start_game(self):
        self.sequence = []
        self.next_round()

    def next_round(self):
        self.user_sequence = []
        self.sequence.append(random.choice(self.colors))
        self.can_click = False
        self.label.configure(text=f"Round {len(self.sequence)}")
        self.after(1000, self.play_sequence)

    def play_sequence(self):
        for i, color in enumerate(self.sequence):
            self.after(i * 600, lambda c=color: self.flash_button(c))
        self.after(len(self.sequence) * 600, self.enable_clicks)

    def flash_button(self, color):
        original_color = self.buttons[color].cget("fg_color")
        self.buttons[color].configure(fg_color="white")
        self.after(300, lambda: self.buttons[color].configure(fg_color=original_color))

    def enable_clicks(self):
        self.can_click = True

    def user_click(self, color):
        if not self.can_click:
            return

        self.flash_button(color)
        self.user_sequence.append(color)

        if self.user_sequence[len(self.user_sequence)-1] != self.sequence[len(self.user_sequence)-1]:
            messagebox.showinfo("Game Over", f"Wrong! Your score: {len(self.sequence)-1}")
            self.can_click = False
            self.label.configure(text="Simon Says")
            return

        if len(self.user_sequence) == len(self.sequence):
            self.can_click = False
            self.after(1000, self.next_round)

if __name__ == "__main__":
    app = SimonSays()
    app.mainloop()
