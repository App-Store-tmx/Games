import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random

ctk.set_appearance_mode("dark")

class SudokuApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sudoku")
        self.geometry("600x700")
        self.resizable(False, False)

        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.cells = [[None for _ in range(9)] for _ in range(9)]

        self.setup_ui()
        self.new_game()

    def setup_ui(self):
        self.header = ctk.CTkFrame(self)
        self.header.pack(pady=10, fill="x")

        self.title_label = ctk.CTkLabel(self.header, text="Sudoku", font=("Arial", 24))
        self.title_label.pack()

        # Grid container
        self.grid_frame = ctk.CTkFrame(self, fg_color="#333333")
        self.grid_frame.pack(pady=10, padx=20)

        for r in range(9):
            for c in range(9):
                # We use different padding to show 3x3 blocks
                padx = (2 if c % 3 != 0 else 5, 2 if c % 3 != 2 else 5)
                pady = (2 if r % 3 != 0 else 5, 2 if r % 3 != 2 else 5)
                
                entry = tk.Entry(self.grid_frame, width=3, font=("Arial", 18), justify="center", 
                                 bg="#1a1a1a", fg="white", insertbackground="white", relief="flat")
                entry.grid(row=r, column=c, padx=padx, pady=pady, ipady=5)
                self.cells[r][c] = entry

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=20)

        self.check_btn = ctk.CTkButton(self.btn_frame, text="Check Solution", command=self.check_solution)
        self.check_btn.grid(row=0, column=0, padx=10)

        self.new_btn = ctk.CTkButton(self.btn_frame, text="New Game", command=self.new_game)
        self.new_btn.grid(row=0, column=1, padx=10)

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

    def solve(self, board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for n in nums:
                        if self.is_valid(board, r, c, n):
                            board[r][c] = n
                            if self.solve(board):
                                return True
                            board[r][c] = 0
                    return False
        return True

    def new_game(self):
        # Generate full solution
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.solve(self.solution)

        # Create puzzle by removing numbers
        self.board = [row[:] for row in self.solution]
        cells_to_remove = 45  # Difficulty
        while cells_to_remove > 0:
            r, c = random.randint(0, 8), random.randint(0, 8)
            if self.board[r][c] != 0:
                self.board[r][c] = 0
                cells_to_remove -= 1

        # Update UI
        for r in range(9):
            for c in range(9):
                self.cells[r][c].delete(0, tk.END)
                if self.board[r][c] != 0:
                    self.cells[r][c].insert(0, str(self.board[r][c]))
                    self.cells[r][c].config(state="disabled", disabledbackground="#2d2d2d", disabledforeground="#aaaaaa")
                else:
                    self.cells[r][c].config(state="normal", bg="#1a1a1a")

    def check_solution(self):
        for r in range(9):
            for c in range(9):
                val = self.cells[r][c].get()
                if not val or not val.isdigit():
                    messagebox.showwarning("Incomplete", "Please fill all cells.")
                    return
                if int(val) != self.solution[r][c]:
                    messagebox.showerror("Incorrect", f"There's an error at row {r+1}, column {c+1}.")
                    return
        messagebox.showinfo("Success", "Congratulations! You solved the Sudoku!")

if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()
