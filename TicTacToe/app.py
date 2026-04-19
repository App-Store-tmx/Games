import customtkinter as ctk
from tkinter import messagebox

class TicTacToe(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tic Tac Toe")
        self.geometry("400x450")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []

        self.label = ctk.CTkLabel(self, text="Player X's Turn", font=("Arial", 20))
        self.label.pack(pady=20)

        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(padx=20, pady=10)

        for i in range(9):
            btn = ctk.CTkButton(self.grid_frame, text="", width=100, height=100, 
                                font=("Arial", 24), command=lambda i=i: self.click(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        self.reset_btn = ctk.CTkButton(self, text="Reset Game", command=self.reset_game)
        self.reset_btn.pack(pady=20)

    def click(self, i):
        if self.board[i] == "" and not self.check_winner():
            self.board[i] = self.current_player
            self.buttons[i].configure(text=self.current_player)
            
            if self.check_winner():
                self.label.configure(text=f"Player {self.current_player} Wins!")
                messagebox.showinfo("Game Over", f"Player {self.current_player} Wins!")
            elif "" not in self.board:
                self.label.configure(text="It's a Draw!")
                messagebox.showinfo("Game Over", "It's a Draw!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.label.configure(text=f"Player {self.current_player}'s Turn")

    def check_winner(self):
        win_coords = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in win_coords:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return True
        return False

    def reset_game(self):
        self.current_player = "X"
        self.board = [""] * 9
        for btn in self.buttons:
            btn.configure(text="")
        self.label.configure(text="Player X's Turn")

if __name__ == "__main__":
    app = TicTacToe()
    app.mainloop()
