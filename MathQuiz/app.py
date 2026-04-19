import customtkinter as ctk
import random
import tkinter as tk
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MathQuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Math Quiz - Blitz")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass
        self.geometry("500x550")

        self.score = 0
        self.streak = 0
        self.current_answer = 0
        self.time_left = 100
        self.difficulty = "Addition"
        self.game_active = False

        self.setup_ui()

    def setup_ui(self):
        self.label_title = ctk.CTkLabel(self, text="Math Blitz", font=("Arial", 32, "bold"))
        self.label_title.pack(pady=20)

        self.mode_frame = ctk.CTkFrame(self)
        self.mode_frame.pack(pady=10, fill="x", padx=20)
        
        self.diff_var = tk.StringVar(value="Addition")
        modes = ["Addition", "Subtraction", "Multiplication", "Mix"]
        for mode in modes:
            rb = ctk.CTkRadioButton(self.mode_frame, text=mode, variable=self.diff_var, value=mode, command=self.reset_game)
            rb.pack(side="left", expand=True, padx=5)

        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(pady=10, fill="x", padx=20)
        
        self.label_score = ctk.CTkLabel(self.stats_frame, text="Score: 0", font=("Arial", 18))
        self.label_score.pack(side="left", expand=True)
        
        self.label_streak = ctk.CTkLabel(self.stats_frame, text="Streak: 0", font=("Arial", 18), text_color="orange")
        self.label_streak.pack(side="left", expand=True)

        # Timer Bar
        self.timer_bar = ctk.CTkProgressBar(self, width=400)
        self.timer_bar.pack(pady=20)
        self.timer_bar.set(1.0)

        self.label_question = ctk.CTkLabel(self, text="Ready?", font=("Arial", 48, "bold"))
        self.label_question.pack(pady=20)

        self.entry_answer = ctk.CTkEntry(self, width=200, font=("Arial", 24), justify="center")
        self.entry_answer.pack(pady=10)
        self.entry_answer.bind("<Return>", lambda e: self.check_answer())
        self.entry_answer.configure(state="disabled")

        self.button_start = ctk.CTkButton(self, text="START GAME", command=self.start_game, font=("Arial", 20, "bold"), fg_color="green", hover_color="#006400")
        self.button_start.pack(pady=20)

        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 16))
        self.label_feedback.pack(pady=10)

    def reset_game(self):
        self.game_active = False
        self.score = 0
        self.streak = 0
        self.label_score.configure(text="Score: 0")
        self.label_streak.configure(text="Streak: 0")
        self.label_question.configure(text="Ready?")
        self.timer_bar.set(1.0)
        self.button_start.configure(state="normal", text="START GAME")
        self.entry_answer.delete(0, 'end')
        self.entry_answer.configure(state="disabled")

    def start_game(self):
        self.game_active = True
        self.score = 0
        self.streak = 0
        self.difficulty = self.diff_var.get()
        self.button_start.configure(state="disabled")
        self.entry_answer.configure(state="normal")
        self.entry_answer.focus()
        self.next_question()
        self.update_timer()

    def update_timer(self):
        if not self.game_active: return
        
        # Decrease timer based on difficulty and streak
        decrement = 0.01 + (self.streak * 0.002)
        current_val = self.timer_bar.get()
        new_val = current_val - decrement
        
        if new_val <= 0:
            self.timer_bar.set(0)
            self.game_over()
        else:
            self.timer_bar.set(new_val)
            self.after(100, self.update_timer)

    def next_question(self):
        mode = self.difficulty
        if mode == "Mix":
            mode = random.choice(["Addition", "Subtraction", "Multiplication"])
        
        if mode == "Addition":
            n1 = random.randint(1, 50 + self.score)
            n2 = random.randint(1, 50 + self.score)
            self.current_answer = n1 + n2
            op = "+"
        elif mode == "Subtraction":
            n1 = random.randint(10, 100 + self.score)
            n2 = random.randint(1, n1)
            self.current_answer = n1 - n2
            op = "-"
        else: # Multiplication
            n1 = random.randint(2, 12 + (self.score // 5))
            n2 = random.randint(2, 12 + (self.score // 5))
            self.current_answer = n1 * n2
            op = "×"

        self.label_question.configure(text=f"{n1} {op} {n2}")
        self.entry_answer.delete(0, 'end')
        self.timer_bar.set(1.0) # Reset timer for each question

    def check_answer(self):
        if not self.game_active: return
        
        try:
            user_ans = int(self.entry_answer.get())
            if user_ans == self.current_answer:
                # Correct
                points = 10 + self.streak
                self.score += points
                self.streak += 1
                self.label_feedback.configure(text=f"Correct! +{points}", text_color="green")
                self.next_question()
            else:
                # Wrong
                self.streak = 0
                self.label_feedback.configure(text=f"Wrong! It was {self.current_answer}", text_color="red")
                self.timer_bar.set(self.timer_bar.get() - 0.2) # Penalty
                self.next_question()
            
            self.label_score.configure(text=f"Score: {self.score}")
            self.label_streak.configure(text=f"Streak: {self.streak}")
        except ValueError:
            pass

    def game_over(self):
        self.game_active = False
        self.entry_answer.configure(state="disabled")
        self.button_start.configure(state="normal", text="RETRY")
        tk.messagebox.showinfo("Time's Up!", f"Game Over!\nFinal Score: {self.score}\nBest Streak: {self.streak}")

if __name__ == "__main__":
    app = MathQuizApp()
    app.mainloop()
