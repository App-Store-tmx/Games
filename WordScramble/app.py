import customtkinter as ctk
import random
import tkinter as tk
import time
VERSION = "1.0.0"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class WordScrambleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Word Scramble - Challenge")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass
        self.geometry("550x650")

        self.word_data = [
            {"word": "PYTHON", "clue": "A popular high-level programming language."},
            {"word": "ALGORITHM", "clue": "A process or set of rules to be followed in calculations."},
            {"word": "DATABASE", "clue": "A structured set of data held in a computer."},
            {"word": "NETWORK", "clue": "A group of two or more computer systems linked together."},
            {"word": "VARIABLE", "clue": "A value that can change depending on conditions."},
            {"word": "FUNCTION", "clue": "A block of code which only runs when it is called."},
            {"word": "INTERFACE", "clue": "A point where two systems, subjects, organizations, etc. meet."},
            {"word": "SOFTWARE", "clue": "The programs and other operating information used by a computer."},
            {"word": "HARDWARE", "clue": "The physical parts of a computer system."},
            {"word": "ENCRYPTION", "clue": "The process of converting information into a code."}
        ]

        self.current_word = ""
        self.scrambled_word = ""
        self.score = 0
        self.hints_revealed = []
        self.game_mode = "Classic"
        self.time_left = 60
        self.game_active = False

        self.setup_ui()

    def setup_ui(self):
        self.label_title = ctk.CTkLabel(self, text="Word Scramble", font=("Arial", 32, "bold"))
        self.label_title.pack(pady=20)

        self.mode_frame = ctk.CTkFrame(self)
        self.mode_frame.pack(pady=10, fill="x", padx=20)
        
        self.mode_var = tk.StringVar(value="Classic")
        for m in ["Classic", "Time Attack"]:
            rb = ctk.CTkRadioButton(self.mode_frame, text=m, variable=self.mode_var, value=m, command=self.reset_game)
            rb.pack(side="left", expand=True, padx=5)

        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(pady=10, fill="x", padx=20)
        
        self.label_score = ctk.CTkLabel(self.stats_frame, text="Score: 0", font=("Arial", 18))
        self.label_score.pack(side="left", expand=True)
        
        self.label_timer = ctk.CTkLabel(self.stats_frame, text="Time: --", font=("Arial", 18), text_color="cyan")
        self.label_timer.pack(side="left", expand=True)

        self.word_card = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=15)
        self.word_card.pack(pady=20, padx=20, fill="both")

        self.label_word = ctk.CTkLabel(self.word_card, text="SCRAMBLED", font=("Courier", 40, "bold"), text_color="orange")
        self.label_word.pack(pady=30)

        self.label_clue = ctk.CTkLabel(self.word_card, text="Clue will appear here", font=("Arial", 14, "italic"), wraplength=450)
        self.label_clue.pack(pady=10)

        self.entry_guess = ctk.CTkEntry(self, width=300, font=("Arial", 24), justify="center", placeholder_text="Your Guess")
        self.entry_guess.pack(pady=10)
        self.entry_guess.bind("<Return>", lambda e: self.check_guess())
        self.entry_guess.configure(state="disabled")

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.btn_start = ctk.CTkButton(self.btn_frame, text="START", command=self.start_game, font=("Arial", 18, "bold"), fg_color="green")
        self.btn_start.pack(side="left", padx=10)

        self.btn_hint = ctk.CTkButton(self.btn_frame, text="HINT (-5 pts)", command=self.give_hint, font=("Arial", 16), fg_color="#555555")
        self.btn_hint.pack(side="left", padx=10)

        self.label_hint_display = ctk.CTkLabel(self, text="", font=("Courier", 18), text_color="gray")
        self.label_hint_display.pack(pady=5)

        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 16))
        self.label_feedback.pack(pady=10)

    def reset_game(self):
        self.game_active = False
        self.score = 0
        self.label_score.configure(text="Score: 0")
        self.label_timer.configure(text="Time: --")
        self.btn_start.configure(state="normal", text="START")
        self.entry_guess.configure(state="disabled")
        self.label_word.configure(text="SCRAMBLED")
        self.label_clue.configure(text="Clue will appear here")
        self.label_hint_display.configure(text="")

    def start_game(self):
        self.game_active = True
        self.score = 0
        self.game_mode = self.mode_var.get()
        self.btn_start.configure(state="disabled")
        self.entry_guess.configure(state="normal")
        self.entry_guess.focus()
        
        if self.game_mode == "Time Attack":
            self.time_left = 60
            self.update_timer()
        
        self.next_word()

    def update_timer(self):
        if not self.game_active or self.game_mode != "Time Attack": return
        self.time_left -= 1
        self.label_timer.configure(text=f"Time: {self.time_left}s")
        if self.time_left <= 0:
            self.game_over()
        else:
            self.after(1000, self.update_timer)

    def next_word(self):
        data = random.choice(self.word_data)
        self.current_word = data["word"]
        word_list = list(self.current_word)
        random.shuffle(word_list)
        self.scrambled_word = "".join(word_list)
        
        if self.scrambled_word == self.current_word:
            self.next_word()
            return

        self.label_word.configure(text=self.scrambled_word)
        self.label_clue.configure(text=f"Clue: {data['clue']}")
        self.entry_guess.delete(0, 'end')
        self.hints_revealed = ["_"] * len(self.current_word)
        self.label_hint_display.configure(text=" ".join(self.hints_revealed))
        self.label_feedback.configure(text="")

    def give_hint(self):
        if not self.game_active: return
        
        # Find unrevealed indices
        unrevealed = [i for i, char in enumerate(self.hints_revealed) if char == "_"]
        if unrevealed:
            idx = random.choice(unrevealed)
            self.hints_revealed[idx] = self.current_word[idx]
            self.label_hint_display.configure(text=" ".join(self.hints_revealed))
            self.score -= 5
            self.label_score.configure(text=f"Score: {self.score}")

    def check_guess(self):
        if not self.game_active: return
        
        guess = self.entry_guess.get().strip().upper()
        if guess == self.current_word:
            reward = 10 + len(self.current_word)
            self.score += reward
            self.label_score.configure(text=f"Score: {self.score}")
            self.label_feedback.configure(text=f"CORRECT! +{reward}", text_color="green")
            
            if self.game_mode == "Time Attack":
                self.time_left += 5 # Bonus time
            
            self.after(1000, self.next_word)
        else:
            self.label_feedback.configure(text="Incorrect! Try again.", text_color="red")

    def game_over(self):
        self.game_active = False
        self.entry_guess.configure(state="disabled")
        self.btn_start.configure(state="normal", text="RETRY")
        tk.messagebox.showinfo("Time's Up!", f"Game Over!\nFinal Score: {self.score}")

if __name__ == "__main__":
    app = WordScrambleApp()
    app.mainloop()
