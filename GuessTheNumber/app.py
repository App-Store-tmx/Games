import customtkinter as ctk
import random
from tkinter import messagebox
import tkinter as tk
import os
VERSION = "1.0.0"

class GuessTheNumber(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Guess The Number - Pro")
        self.geometry("600x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Icon logic
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "icon.png")
            self.icon_img = tk.PhotoImage(file=icon_path)
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass

        self.range_max = 100
        self.target_number = random.randint(1, self.range_max)
        self.attempts = 0
        self.history = []

        self.setup_ui()

    def setup_ui(self):
        # Layout: 2 columns
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Frame: Main Game
        self.game_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.game_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self.game_frame, text="GUESS THE NUMBER", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=(0, 20))

        # Difficulty Selection
        self.diff_label = ctk.CTkLabel(self.game_frame, text="Difficulty Level:", font=("Helvetica", 14))
        self.diff_label.pack()
        
        self.diff_switch = ctk.CTkSegmentedButton(
            self.game_frame, 
            values=["1-100", "1-1000"],
            command=self.change_difficulty
        )
        self.diff_switch.set("1-100")
        self.diff_switch.pack(pady=(0, 20))

        # Thermometer / Gauge
        self.gauge_label = ctk.CTkLabel(self.game_frame, text="Hot / Cold Meter", font=("Helvetica", 12))
        self.gauge_label.pack()
        
        self.gauge = ctk.CTkProgressBar(self.game_frame, width=300, height=20)
        self.gauge.set(0)
        self.gauge.configure(progress_color="blue")
        self.gauge.pack(pady=(0, 20))

        self.hint_label = ctk.CTkLabel(self.game_frame, text=f"Guess a number between 1 and {self.range_max}", font=("Helvetica", 16))
        self.hint_label.pack(pady=10)

        self.entry = ctk.CTkEntry(self.game_frame, placeholder_text="Enter your guess", width=200, font=("Helvetica", 16))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda e: self.check_guess())

        self.guess_btn = ctk.CTkButton(self.game_frame, text="GUESS", command=self.check_guess, font=("Helvetica", 16, "bold"))
        self.guess_btn.pack(pady=10)

        self.result_label = ctk.CTkLabel(self.game_frame, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=10)

        # Right Frame: History
        self.history_frame = ctk.CTkFrame(self)
        self.history_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)

        self.hist_title = ctk.CTkLabel(self.history_frame, text="History", font=("Helvetica", 16, "bold"))
        self.hist_title.pack(pady=10)

        self.history_list = ctk.CTkTextbox(self.history_frame, width=150, font=("Helvetica", 12))
        self.history_list.pack(padx=10, pady=10, fill="both", expand=True)
        self.history_list.configure(state="disabled")

    def change_difficulty(self, value):
        if value == "1-100":
            self.range_max = 100
        else:
            self.range_max = 1000
        self.reset_game()

    def check_guess(self):
        try:
            guess_str = self.entry.get()
            if not guess_str: return
            
            guess = int(guess_str)
            self.attempts += 1
            self.entry.delete(0, 'end')

            distance = abs(self.target_number - guess)
            proximity = max(0, 1 - (distance / self.range_max))
            
            # Update Gauge
            self.gauge.set(proximity)
            if proximity > 0.9:
                self.gauge.configure(progress_color="#FF4500") # Red-Orange (Hot)
                self.result_label.configure(text="Sizzling Hot!", text_color="#FF4500")
            elif proximity > 0.7:
                self.gauge.configure(progress_color="#FFA500") # Orange (Warm)
                self.result_label.configure(text="Getting Warm...", text_color="#FFA500")
            elif proximity > 0.4:
                self.gauge.configure(progress_color="#FFD700") # Gold (Lukewarm)
                self.result_label.configure(text="Lukewarm", text_color="#FFD700")
            else:
                self.gauge.configure(progress_color="#1E90FF") # DodgerBlue (Cold)
                self.result_label.configure(text="Ice Cold...", text_color="#1E90FF")

            # Update History
            arrow = "↑" if guess < self.target_number else "↓"
            if guess == self.target_number: arrow = "★"
            
            self.history.insert(0, f"#{self.attempts}: {guess} {arrow}")
            self.update_history_ui()

            if guess == self.target_number:
                messagebox.showinfo("Victory!", f"Bullseye! {guess} was correct.\nTotal attempts: {self.attempts}")
                self.reset_game()
            elif guess < self.target_number:
                self.result_label.configure(text=f"Too Low! {self.result_label.cget('text')}")
            else:
                self.result_label.configure(text=f"Too High! {self.result_label.cget('text')}")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer.")

    def update_history_ui(self):
        self.history_list.configure(state="normal")
        self.history_list.delete("1.0", "end")
        self.history_list.insert("1.0", "\n".join(self.history))
        self.history_list.configure(state="disabled")

    def reset_game(self):
        self.target_number = random.randint(1, self.range_max)
        self.attempts = 0
        self.history = []
        self.update_history_ui()
        self.entry.delete(0, 'end')
        self.result_label.configure(text="")
        self.gauge.set(0)
        self.gauge.configure(progress_color="#1E90FF")
        self.hint_label.configure(text=f"Guess a number between 1 and {self.range_max}")

if __name__ == "__main__":
    app = GuessTheNumber()
    app.mainloop()
