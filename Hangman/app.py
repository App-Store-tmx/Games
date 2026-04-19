import customtkinter as ctk
import random
import tkinter as tk
from tkinter import messagebox

class Hangman(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hangman Deluxe")
        self.geometry("700x600")
        ctk.set_appearance_mode("dark")
        
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass

        self.categories = {
            "Animals": ["LION", "TIGER", "ELEPHANT", "GIRAFFE", "ZEBRA", "MONKEY", "PANDA", "KANGAROO"],
            "Fruits": ["APPLE", "BANANA", "ORANGE", "STRAWBERRY", "PINEAPPLE", "MANGO", "GRAPES", "WATERMELON"],
            "Programming": ["PYTHON", "JAVASCRIPT", "TYPESCRIPT", "KOTLIN", "FLUTTER", "TKINTER", "REACT", "ANDROID"]
        }

        self.reset_game_state()

        # UI Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Left Side: Canvas
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="nsew")
        
        self.canvas = tk.Canvas(self.canvas_frame, width=300, height=400, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.draw_gallows()

        # Right Side: Game Controls
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.cat_label = ctk.CTkLabel(self.control_frame, text="Select Category:", font=("Arial", 16, "bold"))
        self.cat_label.pack(pady=(20, 5))

        self.cat_var = ctk.StringVar(value="Animals")
        self.cat_menu = ctk.CTkOptionMenu(self.control_frame, values=list(self.categories.keys()), 
                                          variable=self.cat_var, command=self.change_category)
        self.cat_menu.pack(pady=5)

        self.word_display = ctk.CTkLabel(self.control_frame, text="", font=("Courier", 32, "bold"))
        self.word_display.pack(pady=30)

        self.info_label = ctk.CTkLabel(self.control_frame, text="Attempts: 6", font=("Arial", 16))
        self.info_label.pack(pady=5)

        self.used_label = ctk.CTkLabel(self.control_frame, text="Used: ", font=("Arial", 14), wraplength=250)
        self.used_label.pack(pady=5)

        self.entry_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.entry_frame.pack(pady=20)

        self.entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Letter", width=60, font=("Arial", 18))
        self.entry.grid(row=0, column=0, padx=5)
        self.entry.bind("<Return>", lambda e: self.make_guess())

        self.guess_btn = ctk.CTkButton(self.entry_frame, text="Guess", width=80, command=self.make_guess)
        self.guess_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = ctk.CTkButton(self.control_frame, text="New Game", fg_color="#d32f2f", hover_color="#b71c1c",
                                      command=self.new_game)
        self.reset_btn.pack(pady=20)

        self.new_game()

    def reset_game_state(self):
        self.target_word = ""
        self.guessed_letters = set()
        self.attempts_left = 6

    def change_category(self, choice):
        self.new_game()

    def new_game(self):
        self.reset_game_state()
        self.target_word = random.choice(self.categories[self.cat_var.get()])
        self.canvas.delete("all")
        self.draw_gallows()
        self.update_ui()

    def update_ui(self):
        display = " ".join([c if c in self.guessed_letters else "_" for c in self.target_word])
        self.word_display.configure(text=display)
        self.info_label.configure(text=f"Attempts: {self.attempts_left}")
        self.used_label.configure(text=f"Used: {', '.join(sorted(self.guessed_letters))}")
        self.entry.delete(0, 'end')

    def draw_gallows(self):
        # Base
        self.canvas.create_line(50, 380, 250, 380, fill="white", width=4)
        # Vertical pole
        self.canvas.create_line(100, 380, 100, 50, fill="white", width=4)
        # Horizontal pole
        self.canvas.create_line(100, 50, 200, 50, fill="white", width=4)
        # Rope
        self.canvas.create_line(200, 50, 200, 100, fill="white", width=4)

    def draw_part(self):
        parts = [
            lambda: self.canvas.create_oval(175, 100, 225, 150, outline="white", width=4), # Head
            lambda: self.canvas.create_line(200, 150, 200, 250, fill="white", width=4),    # Body
            lambda: self.canvas.create_line(200, 170, 160, 210, fill="white", width=4),    # Left Arm
            lambda: self.canvas.create_line(200, 170, 240, 210, fill="white", width=4),    # Right Arm
            lambda: self.canvas.create_line(200, 250, 160, 310, fill="white", width=4),    # Left Leg
            lambda: self.canvas.create_line(200, 250, 240, 310, fill="white", width=4),    # Right Leg
        ]
        # Calculate which part to draw based on attempts left (6 total)
        part_idx = 6 - self.attempts_left - 1
        if 0 <= part_idx < len(parts):
            parts[part_idx]()

    def make_guess(self):
        guess = self.entry.get().upper()
        self.entry.delete(0, 'end')

        if not guess or len(guess) != 1 or not guess.isalpha():
            return

        if guess in self.guessed_letters:
            return

        self.guessed_letters.add(guess)

        if guess not in self.target_word:
            self.attempts_left -= 1
            self.draw_part()

        self.update_ui()

        if "_" not in self.word_display.cget("text"):
            messagebox.showinfo("Winner!", f"Congratulations! The word was {self.target_word}")
            self.new_game()
        elif self.attempts_left <= 0:
            messagebox.showinfo("Game Over", f"You ran out of attempts! The word was {self.target_word}")
            self.new_game()

if __name__ == "__main__":
    app = Hangman()
    app.mainloop()
