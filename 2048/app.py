import customtkinter as ctk
import random
import os
import tkinter as tk
from tkinter import messagebox
VERSION = "1.0.0"

ctk.set_appearance_mode("dark")

class Game2048(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("2048 Master")
        self.icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
        try:
            self.icon_img = tk.PhotoImage(file=self.icon_path)
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass

        self.geometry("450x650")
        self.resizable(False, False)

        # Persistence
        self.best_score_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best_score.txt")
        self.best_score = self.load_best_score()

        # Game State
        self.grid_size = 4
        self.board = [[0]*4 for _ in range(4)]
        self.score = 0
        self.history = [] # For Undo

        self.setup_ui()
        self.new_game()

        self.bind("<Key>", self.handle_keypress)

    def setup_ui(self):
        # Header
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)

        # Title and Scores
        self.title_label = ctk.CTkLabel(self.header, text="2048", font=("Arial", 48, "bold"))
        self.title_label.grid(row=0, column=0, rowspan=2, sticky="nw")

        self.score_frame = ctk.CTkFrame(self.header, fg_color="#bbada0", corner_radius=5)
        self.score_frame.grid(row=0, column=1, padx=5, sticky="ne")
        ctk.CTkLabel(self.score_frame, text="SCORE", font=("Arial", 12, "bold"), text_color="#eee4da").pack(padx=10)
        self.score_label = ctk.CTkLabel(self.score_frame, text="0", font=("Arial", 20, "bold"), text_color="white")
        self.score_label.pack(padx=10, pady=(0, 5))

        self.best_frame = ctk.CTkFrame(self.header, fg_color="#bbada0", corner_radius=5)
        self.best_frame.grid(row=0, column=2, padx=5, sticky="ne")
        ctk.CTkLabel(self.best_frame, text="BEST", font=("Arial", 12, "bold"), text_color="#eee4da").pack(padx=10)
        self.best_label = ctk.CTkLabel(self.best_frame, text=str(self.best_score), font=("Arial", 20, "bold"), text_color="white")
        self.best_label.pack(padx=10, pady=(0, 5))

        # Control Buttons
        self.undo_btn = ctk.CTkButton(self.header, text="Undo", width=80, fg_color="#8f7a66", hover_color="#7f6a56", command=self.undo)
        self.undo_btn.grid(row=1, column=1, padx=5, pady=10, sticky="e")

        self.reset_btn = ctk.CTkButton(self.header, text="New Game", width=100, fg_color="#8f7a66", hover_color="#7f6a56", command=self.new_game)
        self.reset_btn.grid(row=1, column=2, padx=5, pady=10, sticky="e")

        # Grid
        self.grid_frame = ctk.CTkFrame(self, fg_color="#bbada0", corner_radius=10)
        self.grid_frame.pack(padx=20, pady=10)

        self.cells = []
        for r in range(4):
            row_cells = []
            for c in range(4):
                cell = ctk.CTkLabel(self.grid_frame, text="", width=90, height=90, 
                                    fg_color="#cdc1b4", corner_radius=5, font=("Arial", 32, "bold"))
                cell.grid(row=r, column=c, padx=5, pady=5)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def load_best_score(self):
        if os.path.exists(self.best_score_file):
            try:
                with open(self.best_score_file, "r") as f:
                    return int(f.read())
            except:
                return 0
        return 0

    def save_best_score(self):
        with open(self.best_score_file, "w") as f:
            f.write(str(self.best_score))

    def new_game(self):
        self.board = [[0]*4 for _ in range(4)]
        self.score = 0
        self.history = []
        self.add_new_tile()
        self.add_new_tile()
        self.update_ui()

    def add_new_tile(self):
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.board[r][c] = 2 if random.random() < 0.9 else 4

    def update_ui(self):
        colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        text_colors = {2: "#776e65", 4: "#776e65"}
        
        for r in range(4):
            for c in range(4):
                val = self.board[r][c]
                self.cells[r][c].configure(text=str(val) if val > 0 else "", 
                                           fg_color=colors.get(val, "#3c3a32"),
                                           text_color=text_colors.get(val, "white"))
        
        self.score_label.configure(text=str(self.score))
        if self.score > self.best_score:
            self.best_score = self.score
            self.best_label.configure(text=str(self.best_score))
            self.save_best_score()

    def handle_keypress(self, event):
        key = event.keysym
        if key not in ["Up", "Down", "Left", "Right"]:
            return

        # Save state for undo
        prev_state = ([row[:] for row in self.board], self.score)
        
        moved = False
        if key == "Up":
            moved = self.move_up()
        elif key == "Down":
            moved = self.move_down()
        elif key == "Left":
            moved = self.move_left()
        elif key == "Right":
            moved = self.move_right()

        if moved:
            self.history.append(prev_state)
            if len(self.history) > 1: # Keep only 1 move as requested (though keeping more is easy)
                self.history = self.history[-1:]
            
            self.add_new_tile()
            self.update_ui()
            if self.check_game_over():
                messagebox.showinfo("2048", f"Game Over! Your score: {self.score}")

    def undo(self):
        if self.history:
            self.board, self.score = self.history.pop()
            self.update_ui()

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (4 - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(3):
            if row[i] != 0 and row[i] == row[i+1]:
                row[i] *= 2
                self.score += row[i]
                row[i+1] = 0
        return row

    def move_left(self):
        new_board = []
        for row in self.board:
            row = self.compress(row)
            row = self.merge(row)
            row = self.compress(row)
            new_board.append(row)
        moved = new_board != self.board
        self.board = new_board
        return moved

    def move_right(self):
        self.board = [row[::-1] for row in self.board]
        moved = self.move_left()
        self.board = [row[::-1] for row in self.board]
        return moved

    def move_up(self):
        self.board = [list(row) for row in zip(*self.board)]
        moved = self.move_left()
        self.board = [list(row) for row in zip(*self.board)]
        return moved

    def move_down(self):
        self.board = [list(row) for row in zip(*self.board)]
        moved = self.move_right()
        self.board = [list(row) for row in zip(*self.board)]
        return moved

    def check_game_over(self):
        for r in range(4):
            for c in range(4):
                if self.board[r][c] == 0: return False
        for r in range(4):
            for c in range(3):
                if self.board[r][c] == self.board[r][c+1]: return False
        for r in range(3):
            for c in range(4):
                if self.board[r][c] == self.board[r+1][c]: return False
        return True

if __name__ == "__main__":
    app = Game2048()
    app.mainloop()
