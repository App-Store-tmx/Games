import customtkinter as ctk
import random
import time
import tkinter as tk
from tkinter import messagebox

class MemoryMatch(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Memory Match Pro")
        self.geometry("600x750")
        ctk.set_appearance_mode("dark")
        
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass

        self.symbols = [
            ("🍎", "#FF5252"), ("🍌", "#FFEB3B"), ("🍇", "#9C27B0"), ("🍉", "#4CAF50"),
            ("🍓", "#E91E63"), ("🍒", "#F44336"), ("🍍", "#FFC107"), ("🥝", "#8BC34A")
        ] * 2
        
        self.reset_game_state()

        # UI Layout
        self.title_label = ctk.CTkLabel(self, text="Memory Match", font=("Arial", 28, "bold"))
        self.title_label.pack(pady=20)

        # Stats Frame
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(pady=10)

        self.timer_label = ctk.CTkLabel(self.stats_frame, text="Time: 0s", font=("Arial", 18))
        self.timer_label.grid(row=0, column=0, padx=20)

        self.flips_label = ctk.CTkLabel(self.stats_frame, text="Flips: 0", font=("Arial", 18))
        self.flips_label.grid(row=0, column=1, padx=20)

        # Grid Frame
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(padx=20, pady=10)

        self.buttons = []
        for i in range(16):
            btn = ctk.CTkButton(self.grid_frame, text="?", width=120, height=120, 
                                font=("Arial", 40), corner_radius=10,
                                fg_color="#333333", hover_color="#444444",
                                command=lambda i=i: self.on_click(i))
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
            self.buttons.append(btn)

        self.reset_btn = ctk.CTkButton(self, text="Reset Game", font=("Arial", 16),
                                      command=self.new_game)
        self.reset_btn.pack(pady=30)

        self.new_game()

    def reset_game_state(self):
        random.shuffle(self.symbols)
        self.first_guess = None
        self.second_guess = None
        self.matches = 0
        self.flips = 0
        self.start_time = None
        self.game_running = False
        self.can_click = True

    def new_game(self):
        self.reset_game_state()
        for btn in self.buttons:
            btn.configure(text="?", fg_color="#333333", state="normal")
        self.timer_label.configure(text="Time: 0s")
        self.flips_label.configure(text="Flips: 0")

    def update_timer(self):
        if self.game_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.configure(text=f"Time: {elapsed}s")
            self.after(1000, self.update_timer)

    def on_click(self, i):
        if not self.can_click or self.buttons[i].cget("text") != "?":
            return

        if not self.game_running:
            self.game_running = True
            self.start_time = time.time()
            self.update_timer()

        symbol, color = self.symbols[i]
        self.buttons[i].configure(text=symbol, fg_color=color)
        
        if self.first_guess is None:
            self.first_guess = i
        else:
            self.second_guess = i
            self.flips += 1
            self.flips_label.configure(text=f"Flips: {self.flips}")
            self.can_click = False
            self.after(800, self.check_match)

    def check_match(self):
        s1, c1 = self.symbols[self.first_guess]
        s2, c2 = self.symbols[self.second_guess]

        if s1 == s2:
            self.matches += 1
            self.buttons[self.first_guess].configure(state="disabled")
            self.buttons[self.second_guess].configure(state="disabled")
            if self.matches == 8:
                self.game_running = False
                elapsed = int(time.time() - self.start_time)
                messagebox.showinfo("Perfect Match!", f"Finished in {elapsed}s with {self.flips} flips!")
        else:
            # Flip back animation
            self.buttons[self.first_guess].configure(text="?", fg_color="#333333")
            self.buttons[self.second_guess].configure(text="?", fg_color="#333333")

        self.first_guess = None
        self.second_guess = None
        self.can_click = True

if __name__ == "__main__":
    app = MemoryMatch()
    app.mainloop()
