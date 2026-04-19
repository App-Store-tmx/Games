import customtkinter as ctk
import random
import tkinter as tk
from tkinter import messagebox

class SimonSays(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simon Says: Glow Edition")
        self.geometry("500x700")
        ctk.set_appearance_mode("dark")
        
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass

        self.color_data = {
            "green":  {"base": "#2E7D32", "glow": "#66BB6A"},
            "red":    {"base": "#C62828", "glow": "#EF5350"},
            "yellow": {"base": "#FBC02D", "glow": "#FFF176"},
            "blue":   {"base": "#1565C0", "glow": "#42A5F5"},
            "orange": {"base": "#EF6C00", "glow": "#FFB74D"},
            "purple": {"base": "#6A1B9A", "glow": "#BA68C8"}
        }

        self.sequence = []
        self.user_sequence = []
        self.can_click = False
        self.difficulty = "Easy"

        # UI Layout
        self.title_label = ctk.CTkLabel(self, text="Simon Says", font=("Arial", 28, "bold"))
        self.title_label.pack(pady=20)

        self.mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mode_frame.pack(pady=10)

        self.mode_var = ctk.StringVar(value="Easy")
        self.easy_rb = ctk.CTkRadioButton(self.mode_frame, text="Easy", variable=self.mode_var, value="Easy", command=self.change_difficulty)
        self.easy_rb.grid(row=0, column=0, padx=10)
        self.hard_rb = ctk.CTkRadioButton(self.mode_frame, text="Hard", variable=self.mode_var, value="Hard", command=self.change_difficulty)
        self.hard_rb.grid(row=0, column=1, padx=10)

        self.score_label = ctk.CTkLabel(self, text="Round: 0", font=("Arial", 18))
        self.score_label.pack(pady=10)

        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(padx=20, pady=10)

        self.buttons = {}
        self.setup_buttons()

        self.start_btn = ctk.CTkButton(self, text="Start Game", font=("Arial", 16), command=self.start_game)
        self.start_btn.pack(pady=30)

    def setup_buttons(self):
        for btn in self.buttons.values():
            btn.destroy()
        self.buttons = {}

        cols = 2
        active_colors = ["green", "red", "yellow", "blue"]
        if self.difficulty == "Hard":
            active_colors += ["orange", "purple"]
            cols = 3

        for i, color in enumerate(active_colors):
            btn = ctk.CTkButton(self.grid_frame, text="", width=120, height=120, 
                                corner_radius=15,
                                fg_color=self.color_data[color]["base"],
                                hover_color=self.color_data[color]["glow"],
                                command=lambda c=color: self.user_click(c))
            btn.grid(row=i//cols, column=i%cols, padx=10, pady=10)
            self.buttons[color] = btn

    def change_difficulty(self):
        self.difficulty = self.mode_var.get()
        self.setup_buttons()
        self.sequence = []
        self.score_label.configure(text="Round: 0")

    def start_game(self):
        self.sequence = []
        self.next_round()

    def next_round(self):
        self.user_sequence = []
        active_colors = list(self.buttons.keys())
        self.sequence.append(random.choice(active_colors))
        self.score_label.configure(text=f"Round: {len(self.sequence)}")
        self.can_click = False
        self.after(1000, self.play_sequence)

    def play_sequence(self):
        speed = 600 if self.difficulty == "Easy" else 350
        for i, color in enumerate(self.sequence):
            self.after(i * speed, lambda c=color: self.flash_button(c))
        
        self.after(len(self.sequence) * speed, self.enable_clicks)

    def flash_button(self, color):
        if color not in self.buttons: return
        btn = self.buttons[color]
        btn.configure(fg_color=self.color_data[color]["glow"])
        # Use a shorter duration for the "glow"
        duration = 300 if self.difficulty == "Easy" else 150
        self.after(duration, lambda: btn.configure(fg_color=self.color_data[color]["base"]))

    def enable_clicks(self):
        self.can_click = True

    def user_click(self, color):
        if not self.can_click:
            return

        self.flash_button(color)
        self.user_sequence.append(color)

        # Check correctness
        idx = len(self.user_sequence) - 1
        if self.user_sequence[idx] != self.sequence[idx]:
            messagebox.showinfo("Game Over", f"Wrong sequence! Your score: {len(self.sequence)-1}")
            self.can_click = False
            return

        if len(self.user_sequence) == len(self.sequence):
            self.can_click = False
            self.after(800, self.next_round)

if __name__ == "__main__":
    app = SimonSays()
    app.mainloop()
