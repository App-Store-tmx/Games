import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

ctk.set_appearance_mode("dark")

class ConnectFourApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Connect Four")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            # Fallback if icon.png is missing or loading fails
            pass
        self.geometry("600x650")
        self.resizable(False, False)

        self.rows = 6
        self.cols = 7
        self.current_player = 1  # 1 for Red, 2 for Yellow
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        # Header
        self.header = ctk.CTkFrame(self)
        self.header.pack(pady=10, fill="x")
        
        self.info_label = ctk.CTkLabel(self.header, text="Red's Turn", font=("Arial", 24), text_color="#ff5555")
        self.info_label.pack()

        # Board Frame
        self.board_frame = ctk.CTkFrame(self, fg_color="#2244ff")
        self.board_frame.pack(pady=10, padx=20)

        self.cells = []
        for r in range(self.rows):
            row_cells = []
            for c in range(self.cols):
                cell = tk.Canvas(self.board_frame, width=70, height=70, bg="#2244ff", highlightthickness=0)
                cell.grid(row=r, column=c, padx=5, pady=5)
                cell.create_oval(5, 5, 65, 65, fill="#1a1a1a", outline="#0022cc", width=2)
                cell.bind("<Button-1>", lambda e, col=c: self.make_move(col))
                row_cells.append(cell)
            self.cells.append(row_cells)

        self.reset_btn = ctk.CTkButton(self, text="Reset Game", command=self.reset_game)
        self.reset_btn.pack(pady=10)

    def make_move(self, col):
        # Find the lowest empty row in this column
        for r in reversed(range(self.rows)):
            if self.board[r][col] == 0:
                self.board[r][col] = self.current_player
                color = "#ff5555" if self.current_player == 1 else "#ffff55"
                self.cells[r][col].create_oval(5, 5, 65, 65, fill=color, outline="#0022cc", width=2)
                
                if self.check_win(r, col):
                    winner = "Red" if self.current_player == 1 else "Yellow"
                    messagebox.showinfo("Game Over", f"{winner} Wins!")
                    self.reset_game()
                elif self.is_full():
                    messagebox.showinfo("Game Over", "It's a Draw!")
                    self.reset_game()
                else:
                    self.current_player = 3 - self.current_player
                    p_name = "Red" if self.current_player == 1 else "Yellow"
                    p_color = "#ff5555" if self.current_player == 1 else "#ffff55"
                    self.info_label.configure(text=f"{p_name}'s Turn", text_color=p_color)
                return

    def check_win(self, r, c):
        p = self.board[r][c]
        # Directions: (dr, dc)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            # Check one way
            nr, nc = r + dr, c + dc
            while 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[nr][nc] == p:
                count += 1
                nr += dr
                nc += dc
            # Check other way
            nr, nc = r - dr, c - dc
            while 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[nr][nc] == p:
                count += 1
                nr -= dr
                nc -= dc
            if count >= 4:
                return True
        return False

    def is_full(self):
        return all(self.board[0][c] != 0 for c in range(self.cols))

    def reset_game(self):
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 1
        self.info_label.configure(text="Red's Turn", text_color="#ff5555")
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].delete("all")
                self.cells[r][c].create_oval(5, 5, 65, 65, fill="#1a1a1a", outline="#0022cc", width=2)

if __name__ == "__main__":
    app = ConnectFourApp()
    app.mainloop()
