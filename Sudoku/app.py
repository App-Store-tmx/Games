import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random
import os
VERSION = "1.0.0"

ctk.set_appearance_mode("dark")

class SudokuApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sudoku Pro")
        self.icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
        try:
            self.icon_img = tk.PhotoImage(file=self.icon_path)
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass

        self.geometry("600x750")
        self.resizable(False, False)

        # Game State
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.difficulty = "Easy"

        self.setup_ui()
        self.new_game()

    def setup_ui(self):
        # Header
        self.header = ctk.CTkFrame(self)
        self.header.pack(pady=10, fill="x", padx=20)

        self.title_label = ctk.CTkLabel(self.header, text="Sudoku", font=("Arial", 32, "bold"))
        self.title_label.pack(side="left", padx=20)

        self.diff_var = ctk.StringVar(value=self.difficulty)
        self.diff_menu = ctk.CTkOptionMenu(self.header, values=["Easy", "Medium", "Hard"],
                                           variable=self.diff_var, command=self.change_difficulty)
        self.diff_menu.pack(side="right", padx=20)

        # Grid container
        self.grid_container = ctk.CTkFrame(self, fg_color="#333333", corner_radius=10)
        self.grid_container.pack(pady=10, padx=20)

        for r in range(9):
            for c in range(9):
                # 3x3 block separators
                px = (1 if c % 3 != 0 else 4, 1 if c % 3 != 2 else 4)
                py = (1 if r % 3 != 0 else 4, 1 if r % 3 != 2 else 4)
                
                # We use a standard Entry since CTK Entry is a bit bulky for 9x9
                entry = tk.Entry(self.grid_container, width=2, font=("Arial", 22, "bold"), 
                                 justify="center", bg="#1a1a1a", fg="white", 
                                 insertbackground="white", relief="flat", borderwidth=0)
                entry.grid(row=r, column=c, padx=px, pady=py, ipady=8)
                entry.bind("<KeyRelease>", lambda e, r=r, c=c: self.validate_entry(r, c))
                self.cells[r][c] = entry

        # Controls
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.check_btn = ctk.CTkButton(self.btn_frame, text="Check Progress", command=self.check_progress,
                                       fg_color="#3B8ED0", hover_color="#1F6AA5")
        self.check_btn.grid(row=0, column=0, padx=10)

        self.solve_btn = ctk.CTkButton(self.btn_frame, text="Solve", command=self.solve_game,
                                       fg_color="#E74C3C", hover_color="#C0392B")
        self.solve_btn.grid(row=0, column=1, padx=10)

        self.new_btn = ctk.CTkButton(self.btn_frame, text="New Game", command=self.new_game,
                                     fg_color="#2ECC71", hover_color="#27AE60")
        self.new_btn.grid(row=0, column=2, padx=10)

    def change_difficulty(self, choice):
        self.difficulty = choice
        self.new_game()

    def validate_entry(self, r, c):
        val = self.cells[r][c].get()
        if len(val) > 1:
            self.cells[r][c].delete(1, tk.END)
        if val and not val.isdigit() or val == '0':
            self.cells[r][c].delete(0, tk.END)
        
        # Reset color on change
        self.cells[r][c].config(fg="white")

    def is_valid(self, board, r, c, n):
        for i in range(9):
            if board[r][i] == n or board[i][c] == n:
                return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if board[i][j] == n:
                    return False
        return True

    def find_empty(self, board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return r, c
        return None

    def solve_backtrack(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
        r, c = empty
        
        nums = list(range(1, 10))
        random.shuffle(nums)
        for n in nums:
            if self.is_valid(board, r, c, n):
                board[r][c] = n
                if self.solve_backtrack(board):
                    return True
                board[r][c] = 0
        return False

    def new_game(self):
        # Generate full solution
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_backtrack(self.solution)

        # Create puzzle
        self.board = [row[:] for row in self.solution]
        
        # Difficulties: Easy (45 clues), Medium (35 clues), Hard (25 clues)
        clue_counts = {"Easy": 45, "Medium": 35, "Hard": 25}
        cells_to_remove = 81 - clue_counts[self.difficulty]
        
        while cells_to_remove > 0:
            r, c = random.randint(0, 8), random.randint(0, 8)
            if self.board[r][c] != 0:
                self.board[r][c] = 0
                cells_to_remove -= 1

        # Update UI
        for r in range(9):
            for c in range(9):
                self.cells[r][c].config(state="normal")
                self.cells[r][c].delete(0, tk.END)
                if self.board[r][c] != 0:
                    self.cells[r][c].insert(0, str(self.board[r][c]))
                    self.cells[r][c].config(state="disabled", disabledbackground="#2d2d2d", disabledforeground="#aaaaaa")
                else:
                    self.cells[r][c].config(bg="#1a1a1a", fg="white")

    def check_progress(self):
        errors = 0
        filled = 0
        for r in range(9):
            for c in range(9):
                val = self.cells[r][c].get()
                if val:
                    filled += 1
                    if int(val) != self.solution[r][c]:
                        self.cells[r][c].config(fg="#E74C3C")
                        errors += 1
                    else:
                        self.cells[r][c].config(fg="#2ECC71")
        
        if errors == 0 and filled == 81:
            messagebox.showinfo("Sudoku", "Congratulations! You solved it!")
        elif errors == 0:
            messagebox.showinfo("Sudoku", "So far so good! No errors found.")
        else:
            messagebox.showwarning("Sudoku", f"Found {errors} incorrect entries.")

    def solve_game(self):
        if messagebox.askyesno("Sudoku", "Are you sure you want to see the solution?"):
            for r in range(9):
                for c in range(9):
                    self.cells[r][c].config(state="normal")
                    self.cells[r][c].delete(0, tk.END)
                    self.cells[r][c].insert(0, str(self.solution[r][c]))
                    self.cells[r][c].config(state="disabled", disabledbackground="#2d2d2d", disabledforeground="#aaaaaa")

if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()
