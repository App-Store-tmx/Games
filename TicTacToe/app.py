import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import math
import random
import os

class TicTacToe(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tic Tac Toe - Pro")
        self.geometry("450x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Icon logic
        try:
            # Get the directory where the script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "icon.png")
            self.icon_img = tk.PhotoImage(file=icon_path)
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass

        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []
        self.game_mode = "Single Player"  # Default
        self.game_active = True

        self.setup_ui()

    def setup_ui(self):
        # Header
        self.title_label = ctk.CTkLabel(self, text="TIC TAC TOE", font=("Helvetica", 32, "bold"))
        self.title_label.pack(pady=(20, 10))

        # Mode Selection
        self.mode_frame = ctk.CTkFrame(self)
        self.mode_frame.pack(pady=10)
        
        self.mode_switch = ctk.CTkSegmentedButton(
            self.mode_frame, 
            values=["Single Player", "Two Players"],
            command=self.change_mode
        )
        self.mode_switch.set("Single Player")
        self.mode_switch.pack()

        # Turn Indicator
        self.status_label = ctk.CTkLabel(
            self, 
            text="Player X's Turn", 
            font=("Helvetica", 18),
            text_color="#3B8ED0"
        )
        self.status_label.pack(pady=10)

        # Game Grid
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(padx=20, pady=10)

        for i in range(9):
            btn = ctk.CTkButton(
                self.grid_frame, 
                text="", 
                width=110, 
                height=110, 
                font=("Helvetica", 40, "bold"),
                fg_color="#2B2B2B",
                hover_color="#3B3B3B",
                corner_radius=10,
                command=lambda i=i: self.on_click(i)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        # Control Buttons
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.pack(pady=20)

        self.reset_btn = ctk.CTkButton(
            self.control_frame, 
            text="Reset Game", 
            font=("Helvetica", 16),
            command=self.reset_game,
            fg_color="#1F6AA5",
            hover_color="#144870"
        )
        self.reset_btn.pack()

    def change_mode(self, mode):
        self.game_mode = mode
        self.reset_game()

    def on_click(self, i):
        if self.board[i] == "" and self.game_active:
            self.make_move(i, "X")
            
            if not self.check_game_over():
                if self.game_mode == "Single Player":
                    self.status_label.configure(text="AI is thinking...", text_color="#E74C3C")
                    self.after(500, self.ai_move)
                else:
                    self.current_player = "O"
                    self.status_label.configure(text="Player O's Turn", text_color="#E74C3C")

    def make_move(self, i, player):
        self.board[i] = player
        color = "#3B8ED0" if player == "X" else "#E74C3C"
        self.buttons[i].configure(text=player, text_color=color)
        
    def ai_move(self):
        if not self.game_active:
            return
        
        move = self.get_best_move()
        if move is not None:
            self.make_move(move, "O")
            if not self.check_game_over():
                self.current_player = "X"
                self.status_label.configure(text="Player X's Turn", text_color="#3B8ED0")

    def get_best_move(self):
        best_score = -math.inf
        move = None
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    move = i
        return move

    def minimax(self, board, depth, is_maximizing):
        winner = self.check_winner_logic()
        if winner == "O": return 10 - depth
        if winner == "X": return depth - 10
        if "" not in board: return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def check_winner_logic(self):
        win_coords = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in win_coords:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return self.board[a]
        return None

    def check_game_over(self):
        winner = self.check_winner_logic()
        if winner:
            self.game_active = False
            self.status_label.configure(text=f"Player {winner} Wins!", text_color="#2ECC71")
            messagebox.showinfo("Game Over", f"Player {winner} Wins!")
            return True
        elif "" not in self.board:
            self.game_active = False
            self.status_label.configure(text="It's a Draw!", text_color="#F1C40F")
            messagebox.showinfo("Game Over", "It's a Draw!")
            return True
        return False

    def reset_game(self):
        self.current_player = "X"
        self.board = [""] * 9
        self.game_active = True
        for btn in self.buttons:
            btn.configure(text="")
        self.status_label.configure(text="Player X's Turn", text_color="#3B8ED0")

if __name__ == "__main__":
    app = TicTacToe()
    app.mainloop()
