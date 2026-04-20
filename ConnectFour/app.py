import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random
import os
VERSION = "1.0.0"

ctk.set_appearance_mode("dark")

class ConnectFourApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Connect Four Pro")
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        try:
            icon_path = os.path.join(self.base_path, "icon.png")
            self.icon_img = tk.PhotoImage(file=icon_path)
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass
            
        self.geometry("700x800")
        self.resizable(False, False)

        self.rows = 6
        self.cols = 7
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 1 # 1 for Red, 2 for Yellow
        self.game_mode = "PvP" # "PvP" or "PvE"
        self.is_animating = False

        self.setup_ui()

    def setup_ui(self):
        # Header
        self.header = ctk.CTkFrame(self, corner_radius=10)
        self.header.pack(pady=10, padx=20, fill="x")

        self.info_label = ctk.CTkLabel(self.header, text="Red's Turn", font=("Segoe UI", 24, "bold"), text_color="#ff5555")
        self.info_label.pack(pady=10)

        # Mode Selection
        self.mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mode_frame.pack(pady=5)

        self.pvp_btn = ctk.CTkButton(self.mode_frame, text="Two Player", width=120, command=lambda: self.set_mode("PvP"))
        self.pvp_btn.grid(row=0, column=0, padx=10)
        
        self.pve_btn = ctk.CTkButton(self.mode_frame, text="Single Player", width=120, command=lambda: self.set_mode("PvE"), fg_color="gray")
        self.pve_btn.grid(row=0, column=1, padx=10)

        # Board Canvas
        self.canvas = tk.Canvas(self, width=640, height=560, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(pady=20, padx=30)
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()

        self.reset_btn = ctk.CTkButton(self, text="Reset Game", font=("Segoe UI", 16), command=self.reset_game)
        self.reset_btn.pack(pady=10)

    def draw_board(self):
        self.canvas.delete("all")
        # Draw Blue Board
        self.canvas.create_rectangle(0, 0, 640, 560, fill="#2244ff", outline="#0022cc", width=4)
        
        # Draw Holes
        for r in range(self.rows):
            for c in range(self.cols):
                x = c * 90 + 50
                y = r * 90 + 50
                # Polished circles: inner shadow effect
                self.canvas.create_oval(x-40, y-40, x+40, y+40, fill="#121212", outline="#0022cc", width=2)

    def set_mode(self, mode):
        self.game_mode = mode
        if mode == "PvP":
            self.pvp_btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
            self.pve_btn.configure(fg_color="gray")
        else:
            self.pve_btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
            self.pvp_btn.configure(fg_color="gray")
        self.reset_game()

    def on_click(self, event):
        if self.is_animating:
            return
        
        col = event.x // 90
        if 0 <= col < self.cols:
            self.make_move(col)

    def make_move(self, col):
        # Find the lowest empty row
        row = -1
        for r in reversed(range(self.rows)):
            if self.board[r][col] == 0:
                row = r
                break
        
        if row != -1:
            self.board[row][col] = self.current_player
            self.animate_drop(row, col)

    def animate_drop(self, target_row, col):
        self.is_animating = True
        color = "#ff5555" if self.current_player == 1 else "#ffff55"
        outline = "#cc3333" if self.current_player == 1 else "#cccc33"
        
        x = col * 90 + 50
        start_y = -40
        chip = self.canvas.create_oval(x-38, start_y-38, x+38, start_y+38, fill=color, outline=outline, width=2)
        
        target_y = target_row * 90 + 50
        self.step_animate(chip, start_y, target_y, target_row, col)

    def step_animate(self, chip, current_y, target_y, target_row, col):
        speed = 25
        if current_y < target_y:
            current_y += speed
            if current_y > target_y:
                current_y = target_y
            self.canvas.coords(chip, (col * 90 + 50)-38, current_y-38, (col * 90 + 50)+38, current_y+38)
            self.after(20, lambda: self.step_animate(chip, current_y, target_y, target_row, col))
        else:
            self.is_animating = False
            if self.check_win(target_row, col):
                winner = "Red" if self.current_player == 1 else "Yellow"
                messagebox.showinfo("Game Over", f"{winner} Wins!")
                self.reset_game()
            elif self.is_full():
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.reset_game()
            else:
                self.current_player = 3 - self.current_player
                self.update_info()
                if self.game_mode == "PvE" and self.current_player == 2:
                    self.after(500, self.ai_move)

    def ai_move(self):
        valid_cols = [c for c in range(self.cols) if self.board[0][c] == 0]
        if valid_cols:
            col = random.choice(valid_cols)
            self.make_move(col)

    def update_info(self):
        name = "Red" if self.current_player == 1 else "Yellow"
        color = "#ff5555" if self.current_player == 1 else "#ffff55"
        self.info_label.configure(text=f"{name}'s Turn", text_color=color)

    def check_win(self, r, c):
        p = self.board[r][c]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            # Forward
            nr, nc = r + dr, c + dc
            while 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[nr][nc] == p:
                count += 1
                nr += dr
                nc += dc
            # Backward
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
        self.update_info()
        self.draw_board()
        self.is_animating = False

if __name__ == "__main__":
    app = ConnectFourApp()
    app.mainloop()
