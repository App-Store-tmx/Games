import customtkinter as ctk
import random
import time
import tkinter as tk
from tkinter import messagebox
import os
VERSION = "1.0.0"

ctk.set_appearance_mode("dark")

class Minesweeper(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Minesweeper Pro")
        self.icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
        try:
            self.icon_img = tk.PhotoImage(file=self.icon_path)
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass

        # Game Settings
        self.difficulties = {
            "Easy": {"rows": 8, "cols": 8, "mines": 10},
            "Medium": {"rows": 12, "cols": 12, "mines": 25},
            "Hard": {"rows": 16, "cols": 16, "mines": 40}
        }
        self.current_difficulty = "Easy"
        
        # State
        self.grid = []
        self.mines = set()
        self.flags = set()
        self.revealed = set()
        self.game_over = False
        self.start_time = None
        self.timer_running = False
        self.first_click = True
        self.flag_mode = False

        self.setup_ui()
        self.new_game()

    def setup_ui(self):
        # Header for Controls
        self.header = ctk.CTkFrame(self)
        self.header.pack(fill="x", padx=10, pady=5)

        # Difficulty Selector
        self.diff_var = ctk.StringVar(value=self.current_difficulty)
        self.diff_menu = ctk.CTkOptionMenu(self.header, values=list(self.difficulties.keys()),
                                           variable=self.diff_var, command=self.change_difficulty,
                                           width=100)
        self.diff_menu.pack(side="left", padx=5)

        # Flag Mode Toggle
        self.flag_btn = ctk.CTkButton(self.header, text="🚩 OFF", width=60, 
                                      fg_color="gray30", command=self.toggle_flag_mode)
        self.flag_btn.pack(side="left", padx=5)

        # Stats
        self.stats_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        self.stats_frame.pack(side="right", padx=5)

        self.mine_label = ctk.CTkLabel(self.stats_frame, text="Mines: 10", font=("Courier", 18, "bold"), text_color="orange")
        self.mine_label.pack(side="left", padx=10)

        self.timer_label = ctk.CTkLabel(self.stats_frame, text="Time: 000", font=("Courier", 18, "bold"), text_color="red")
        self.timer_label.pack(side="left", padx=10)

        # Grid container
        self.grid_container = ctk.CTkFrame(self)
        self.grid_container.pack(expand=True, fill="both", padx=10, pady=10)

    def toggle_flag_mode(self):
        self.flag_mode = not self.flag_mode
        if self.flag_mode:
            self.flag_btn.configure(text="🚩 ON", fg_color="orange")
        else:
            self.flag_btn.configure(text="🚩 OFF", fg_color="gray30")

    def change_difficulty(self, choice):
        self.current_difficulty = choice
        self.new_game()

    def new_game(self):
        self.game_over = False
        self.first_click = True
        self.timer_running = False
        self.start_time = None
        self.timer_label.configure(text="Time: 000")
        
        diff = self.difficulties[self.current_difficulty]
        self.rows = diff["rows"]
        self.cols = diff["cols"]
        self.num_mines = diff["mines"]
        
        self.mines = set()
        self.flags = set()
        self.revealed = set()
        self.update_mine_count()

        # Clear old grid
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        self.grid = []
        for r in range(self.rows):
            row_btns = []
            for c in range(self.cols):
                btn = ctk.CTkButton(self.grid_container, text="", width=30, height=30,
                                    fg_color=["#3B8ED0", "#1F6AA5"], border_width=1, corner_radius=2,
                                    command=lambda r=r, c=c: self.handle_left_click(r, c))
                btn.grid(row=r, column=c, padx=1, pady=1)
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.handle_right_click(r, c))
                row_btns.append(btn)
            self.grid.append(row_btns)

        # Adjust window size
        w = max(400, self.cols * 32 + 40)
        h = self.rows * 32 + 100
        self.geometry(f"{w}x{h}")

    def update_mine_count(self):
        remaining = self.num_mines - len(self.flags)
        self.mine_label.configure(text=f"Mines: {max(0, remaining)}")

    def start_timer(self):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running and not self.game_over:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.configure(text=f"Time: {min(999, elapsed):03}")
            self.after(1000, self.update_timer)

    def handle_left_click(self, r, c):
        if self.game_over:
            return
        
        if self.flag_mode:
            self.handle_right_click(r, c)
            return

        if (r, c) in self.flags:
            return

        if self.first_click:
            self.place_mines(r, c)
            self.first_click = False
            self.start_timer()

        if (r, c) in self.mines:
            self.loss(r, c)
        else:
            self.reveal(r, c)
            if len(self.revealed) == (self.rows * self.cols) - self.num_mines:
                self.win()

    def handle_right_click(self, r, c, event=None):
        if self.game_over or (r, c) in self.revealed:
            return
        
        if (r, c) in self.flags:
            self.flags.remove((r, c))
            self.grid[r][c].configure(text="", fg_color=["#3B8ED0", "#1F6AA5"])
        else:
            if len(self.flags) < self.num_mines:
                self.flags.add((r, c))
                self.grid[r][c].configure(text="🚩", fg_color="orange")
        
        self.update_mine_count()

    def place_mines(self, start_r, start_c):
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        all_positions.remove((start_r, start_c))
        # Remove neighbors to ensure safe start
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (start_r + dr, start_c + dc) in all_positions:
                    all_positions.remove((start_r + dr, start_c + dc))
        
        self.mines = set(random.sample(all_positions, self.num_mines))

    def reveal(self, r, c):
        if (r, c) in self.revealed or (r, c) in self.flags:
            return
        
        self.revealed.add((r, c))
        count = self.get_neighbor_mine_count(r, c)
        
        colors = {1: "#3498DB", 2: "#2ECC71", 3: "#E74C3C", 4: "#9B59B6", 
                  5: "#F1C40F", 6: "#1ABC9C", 7: "#34495E", 8: "#95A5A6"}
        text_color = colors.get(count, "white")
        
        self.grid[r][c].configure(text=str(count) if count > 0 else "",
                                  fg_color="gray25", state="disabled",
                                  text_color_disabled=text_color)
        
        if count == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.reveal(nr, nc)

    def get_neighbor_mine_count(self, r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                if (r + dr, c + dc) in self.mines:
                    count += 1
        return count

    def win(self):
        self.game_over = True
        self.timer_running = False
        for r, c in self.mines:
            self.grid[r][c].configure(text="🚩", fg_color="green")
        messagebox.showinfo("Minesweeper", "Victory! You cleared the field.")

    def loss(self, hit_r, hit_c):
        self.game_over = True
        self.timer_running = False
        for r, c in self.mines:
            if (r, c) == (hit_r, hit_c):
                self.grid[r][c].configure(text="💥", fg_color="red")
            elif (r, c) in self.flags:
                self.grid[r][c].configure(text="🚩", fg_color="green")
            else:
                self.grid[r][c].configure(text="💣", fg_color="red")
        
        for r, c in self.flags:
            if (r, c) not in self.mines:
                self.grid[r][c].configure(text="❌", fg_color="orange")
        
        messagebox.showerror("Minesweeper", "Game Over! You hit a mine.")

if __name__ == "__main__":
    app = Minesweeper()
    app.mainloop()
