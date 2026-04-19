import customtkinter as ctk
import random
from tkinter import messagebox
import tkinter as tk

ctk.set_appearance_mode("dark")

class FifteenPuzzleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("15 Puzzle")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            # Fallback if icon.png is missing or loading fails
            pass
        self.geometry("500x600")
        self.resizable(False, False)

        self.tiles = list(range(1, 16)) + [None]
        self.grid_size = 4
        self.buttons = []

        self.setup_ui()
        self.shuffle_tiles()

    def setup_ui(self):
        self.header = ctk.CTkFrame(self)
        self.header.pack(pady=20, fill="x")

        self.title_label = ctk.CTkLabel(self.header, text="15 Puzzle", font=("Arial", 24))
        self.title_label.pack()

        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(pady=10, padx=20)

        for i in range(16):
            btn = ctk.CTkButton(self.grid_frame, text="", width=80, height=80, font=("Arial", 20),
                                command=lambda idx=i: self.tile_click(idx))
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.buttons.append(btn)

        self.reset_btn = ctk.CTkButton(self, text="New Game", command=self.shuffle_tiles)
        self.reset_btn.pack(pady=20)

    def update_buttons(self):
        for i, val in enumerate(self.tiles):
            if val is None:
                self.buttons[i].configure(text="", fg_color="transparent", state="disabled")
            else:
                self.buttons[i].configure(text=str(val), fg_color=["#3B8ED0", "#1F6AA5"], state="normal")

    def tile_click(self, idx):
        empty_idx = self.tiles.index(None)
        
        # Check if adjacent
        r1, c1 = idx // 4, idx % 4
        r2, c2 = empty_idx // 4, empty_idx % 4
        
        if abs(r1 - r2) + abs(c1 - c2) == 1:
            self.tiles[empty_idx], self.tiles[idx] = self.tiles[idx], self.tiles[empty_idx]
            self.update_buttons()
            if self.is_solved():
                messagebox.showinfo("Success", "You solved the puzzle!")

    def is_solved(self):
        return self.tiles == list(range(1, 16)) + [None]

    def shuffle_tiles(self):
        # To ensure solvability, we start from solved state and make random moves
        self.tiles = list(range(1, 16)) + [None]
        empty_idx = 15
        for _ in range(200):
            r, c = empty_idx // 4, empty_idx % 4
            neighbors = []
            if r > 0: neighbors.append(empty_idx - 4)
            if r < 3: neighbors.append(empty_idx + 4)
            if c > 0: neighbors.append(empty_idx - 1)
            if c < 3: neighbors.append(empty_idx + 1)
            
            move = random.choice(neighbors)
            self.tiles[empty_idx], self.tiles[move] = self.tiles[move], self.tiles[empty_idx]
            empty_idx = move
        self.update_buttons()

if __name__ == "__main__":
    app = FifteenPuzzleApp()
    app.mainloop()
