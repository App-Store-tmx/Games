import customtkinter as ctk
import random
from tkinter import messagebox
import tkinter as tk

class Game2048(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("2048")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            # Fallback if icon.png is missing or loading fails
            pass
        self.geometry("400x500")
        ctk.set_appearance_mode("dark")

        self.grid_size = 4
        self.board = [[0]*4 for _ in range(4)]
        self.score = 0

        self.score_label = ctk.CTkLabel(self, text="Score: 0", font=("Arial", 24))
        self.score_label.pack(pady=20)

        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(padx=20, pady=10)

        self.cells = []
        for r in range(4):
            row_cells = []
            for c in range(4):
                cell = ctk.CTkLabel(self.grid_frame, text="", width=80, height=80, 
                                    fg_color="gray30", corner_radius=5, font=("Arial", 24))
                cell.grid(row=r, column=c, padx=5, pady=5)
                row_cells.append(cell)
            self.cells.append(row_cells)

        self.bind("<Key>", self.handle_keypress)
        self.init_game()

    def init_game(self):
        self.board = [[0]*4 for _ in range(4)]
        self.score = 0
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
            0: "gray30", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        for r in range(4):
            for c in range(4):
                val = self.board[r][c]
                self.cells[r][c].configure(text=str(val) if val > 0 else "", 
                                           fg_color=colors.get(val, "#3c3a32"),
                                           text_color="black" if val <= 4 else "white")
        self.score_label.configure(text=f"Score: {self.score}")

    def handle_keypress(self, event):
        key = event.keysym
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
            self.add_new_tile()
            self.update_ui()
            if self.check_game_over():
                messagebox.showinfo("2048", "Game Over!")
                self.init_game()

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
