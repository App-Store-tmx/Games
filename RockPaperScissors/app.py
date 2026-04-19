import customtkinter as ctk
import random
from tkinter import messagebox

class RockPaperScissors(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Rock Paper Scissors")
        self.geometry("400x400")
        ctk.set_appearance_mode("dark")

        self.user_score = 0
        self.comp_score = 0

        self.label = ctk.CTkLabel(self, text="Choose your weapon!", font=("Arial", 20))
        self.label.pack(pady=20)

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10)

        self.rock_btn = ctk.CTkButton(self.btn_frame, text="Rock", command=lambda: self.play("Rock"))
        self.rock_btn.grid(row=0, column=0, padx=5, pady=5)

        self.paper_btn = ctk.CTkButton(self.btn_frame, text="Paper", command=lambda: self.play("Paper"))
        self.paper_btn.grid(row=0, column=1, padx=5, pady=5)

        self.scissors_btn = ctk.CTkButton(self.btn_frame, text="Scissors", command=lambda: self.play("Scissors"))
        self.scissors_btn.grid(row=0, column=2, padx=5, pady=5)

        self.result_label = ctk.CTkLabel(self, text="", font=("Arial", 16))
        self.result_label.pack(pady=20)

        self.score_label = ctk.CTkLabel(self, text="Score - You: 0 | Comp: 0", font=("Arial", 14))
        self.score_label.pack(pady=10)

    def play(self, user_choice):
        choices = ["Rock", "Paper", "Scissors"]
        comp_choice = random.choice(choices)

        if user_choice == comp_choice:
            result = "It's a tie!"
        elif (user_choice == "Rock" and comp_choice == "Scissors") or \
             (user_choice == "Paper" and comp_choice == "Rock") or \
             (user_choice == "Scissors" and comp_choice == "Paper"):
            result = "You win!"
            self.user_score += 1
        else:
            result = "Computer wins!"
            self.comp_score += 1

        self.result_label.configure(text=f"You: {user_choice}\nComp: {comp_choice}\n{result}")
        self.score_label.configure(text=f"Score - You: {self.user_score} | Comp: {self.comp_score}")

if __name__ == "__main__":
    app = RockPaperScissors()
    app.mainloop()
