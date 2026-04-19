import customtkinter as ctk
import random
from tkinter import messagebox

class Minesweeper(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Minesweeper")
        self.geometry("500x600")
        ctk.set_appearance_mode("dark")

        self.rows = 10
        self.cols = 10
        self.num_mines = 15
        self.buttons = []
        self.mines = set()
        self.revealed = set()
        self.flags = set()

        self.label = ctk.CTkLabel(self, text="Minesweeper", font=("Arial", 24))
        self.label.pack(pady=10)

        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(padx=20, pady=10)

        self.reset_game()

    def reset_game(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        self.mines = set()
        self.revealed = set()
        self.flags = set()

        # Place mines
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        self.mines = set(random.sample(all_positions, self.num_mines))

        for r in range(self.rows):
            row_btns = []
            for c in range(self.cols):
                btn = ctk.CTkButton(self.grid_frame, text="", width=40, height=40,
                                    command=lambda r=r, c=c: self.click(r, c))
                btn.grid(row=r, column=c, padx=1, pady=1)
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.toggle_flag(r, c))
                row_btns.append(btn)
            self.buttons.append(row_btns)

    def toggle_flag(self, r, c):
        if (r, c) in self.revealed:
            return
        if (r, c) in self.flags:
            self.flags.remove((r, c))
            self.buttons[r][c].configure(text="", fg_color=["#3B8ED0", "#1F6AA5"])
        else:
            self.flags.add((r, c))
            self.buttons[r][c].configure(text="🚩", fg_color="orange")

    def click(self, r, c):
        if (r, c) in self.flags or (r, c) in self.revealed:
            return

        if (r, c) in self.mines:
            self.game_over(False)
            return

        self.reveal(r, c)
        if len(self.revealed) == (self.rows * self.cols) - self.num_mines:
            self.game_over(True)

    def reveal(self, r, c):
        if (r, c) in self.revealed or (r, c) in self.mines:
            return
        
        self.revealed.add((r, c))
        count = self.count_adjacent_mines(r, c)
        
        self.buttons[r][c].configure(text=str(count) if count > 0 else "", 
                                     fg_color="gray25", state="disabled")
        
        if count == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.reveal(nr, nc)

    def count_adjacent_mines(self, r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                if (r + dr, c + dc) in self.mines:
                    count += 1
        return count

    def game_over(self, win):
        for r, c in self.mines:
            self.buttons[r][c].configure(text="💣", fg_color="red")
        
        if win:
            messagebox.showinfo("Minesweeper", "Congratulations! You won!")
        else:
            messagebox.showinfo("Minesweeper", "BOOM! Game Over.")
        self.reset_game()

if __name__ == "__main__":
    app = Minesweeper()
    app.mainloop()
