import customtkinter as ctk
import random
import tkinter as tk
from collections import deque

class RockPaperScissors(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Rock Paper Scissors Deluxe")
        self.geometry("600x550")
        ctk.set_appearance_mode("dark")
        
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass

        # Game State
        self.stats = {"Wins": 0, "Losses": 0, "Draws": 0}
        self.history = deque(maxlen=5)
        self.choices = ["Rock", "Paper", "Scissors"]
        self.emojis = {"Rock": "🪨", "Paper": "📄", "Scissors": "✂️"}

        # UI Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Rock Paper Scissors", font=("Arial", 28, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Main Game Frame
        self.game_frame = ctk.CTkFrame(self)
        self.game_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.instruction_label = ctk.CTkLabel(self.game_frame, text="Choose your weapon!", font=("Arial", 18))
        self.instruction_label.pack(pady=15)

        self.btn_frame = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        self.rock_btn = ctk.CTkButton(self.btn_frame, text="🪨 Rock", command=lambda: self.play("Rock"), width=120)
        self.rock_btn.grid(row=0, column=0, padx=5, pady=5)

        self.paper_btn = ctk.CTkButton(self.btn_frame, text="📄 Paper", command=lambda: self.play("Paper"), width=120)
        self.paper_btn.grid(row=0, column=1, padx=5, pady=5)

        self.scissors_btn = ctk.CTkButton(self.btn_frame, text="✂️ Scissors", command=lambda: self.play("Scissors"), width=120)
        self.scissors_btn.grid(row=0, column=2, padx=5, pady=5)

        self.result_label = ctk.CTkLabel(self.game_frame, text="Waiting for first move...", font=("Arial", 16), height=100)
        self.result_label.pack(pady=20)

        # Sidebar / Stats Frame
        self.side_frame = ctk.CTkFrame(self)
        self.side_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        self.stats_title = ctk.CTkLabel(self.side_frame, text="Statistics", font=("Arial", 18, "bold"))
        self.stats_title.pack(pady=10)

        self.wins_label = ctk.CTkLabel(self.side_frame, text="Wins: 0", font=("Arial", 14), text_color="#4CAF50")
        self.wins_label.pack()
        self.losses_label = ctk.CTkLabel(self.side_frame, text="Losses: 0", font=("Arial", 14), text_color="#F44336")
        self.losses_label.pack()
        self.draws_label = ctk.CTkLabel(self.side_frame, text="Draws: 0", font=("Arial", 14), text_color="#FFC107")
        self.draws_label.pack()

        self.history_title = ctk.CTkLabel(self.side_frame, text="Last 5 Rounds", font=("Arial", 18, "bold"))
        self.history_title.pack(pady=(20, 10))

        self.history_label = ctk.CTkLabel(self.side_frame, text="", font=("Arial", 12), justify="left")
        self.history_label.pack(padx=10)

    def play(self, user_choice):
        comp_choice = random.choice(self.choices)
        
        if user_choice == comp_choice:
            result_text = "IT'S A DRAW!"
            color = "#FFC107"
            self.stats["Draws"] += 1
            history_icon = "➖"
        elif (user_choice == "Rock" and comp_choice == "Scissors") or \
             (user_choice == "Paper" and comp_choice == "Rock") or \
             (user_choice == "Scissors" and comp_choice == "Paper"):
            result_text = "YOU WIN!"
            color = "#4CAF50"
            self.stats["Wins"] += 1
            history_icon = "✅"
        else:
            result_text = "COMPUTER WINS!"
            color = "#F44336"
            self.stats["Losses"] += 1
            history_icon = "❌"

        # Update Result with "Animation" (Color flash)
        self.result_label.configure(
            text=f"You: {self.emojis[user_choice]} {user_choice}\n"
                 f"Comp: {self.emojis[comp_choice]} {comp_choice}\n\n"
                 f"{result_text}",
            text_color=color
        )
        
        # Update Stats
        self.wins_label.configure(text=f"Wins: {self.stats['Wins']}")
        self.losses_label.configure(text=f"Losses: {self.stats['Losses']}")
        self.draws_label.configure(text=f"Draws: {self.stats['Draws']}")

        # Update History
        round_summary = f"{history_icon} {user_choice} vs {comp_choice}"
        self.history.appendleft(round_summary)
        self.history_label.configure(text="\n".join(self.history))

        # Brief animation effect
        self.animate_result(color)

    def animate_result(self, target_color):
        original_color = self.result_label.cget("text_color")
        def flash(count):
            if count > 0:
                current = self.result_label.cget("text_color")
                new_color = "white" if current != "white" else target_color
                self.result_label.configure(text_color=new_color)
                self.after(100, lambda: flash(count - 1))
            else:
                self.result_label.configure(text_color=target_color)
        flash(4)

if __name__ == "__main__":
    app = RockPaperScissors()
    app.mainloop()
