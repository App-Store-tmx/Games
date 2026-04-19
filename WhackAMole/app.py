import customtkinter as ctk
import tkinter as tk
import random

ctk.set_appearance_mode("dark")

class WhackAMoleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Whack-A-Mole")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            # Fallback if icon.png is missing or loading fails
            pass
        self.geometry("600x650")
        self.resizable(False, False)

        # UI Header
        self.header = ctk.CTkFrame(self)
        self.header.pack(pady=10, fill="x")

        self.score = 0
        self.score_label = ctk.CTkLabel(self.header, text=f"Score: {self.score}", font=("Arial", 20))
        self.score_label.pack(side="left", padx=20)

        self.time_left = 30
        self.time_label = ctk.CTkLabel(self.header, text=f"Time: {self.time_left}", font=("Arial", 20))
        self.time_label.pack(side="right", padx=20)

        # Canvas for holes
        self.canvas = tk.Canvas(self, width=600, height=500, bg="#2d5a27", highlightthickness=0)
        self.canvas.pack()

        # Grid setup
        self.holes = []
        self.mole = None
        self.setup_holes()

        self.game_running = False
        self.start_btn = ctk.CTkButton(self, text="Start Game", command=self.start_game)
        self.start_btn.pack(pady=10)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def setup_holes(self):
        # 3x3 Grid
        for r in range(3):
            for c in range(3):
                x = c * 200 + 100
                y = r * 150 + 100
                hole = self.canvas.create_oval(x-60, y-30, x+60, y+30, fill="#3d2a1a", outline="#221100", width=2)
                self.holes.append((x, y))

    def start_game(self):
        if self.game_running:
            return
        self.score = 0
        self.time_left = 30
        self.game_running = True
        self.start_btn.configure(state="disabled")
        self.update_ui()
        self.spawn_mole()
        self.countdown()

    def update_ui(self):
        self.score_label.configure(text=f"Score: {self.score}")
        self.time_label.configure(text=f"Time: {self.time_left}")

    def spawn_mole(self):
        if not self.game_running:
            return
        
        if self.mole:
            self.canvas.delete(self.mole)
        
        pos = random.choice(self.holes)
        x, y = pos
        # Mole head
        self.mole = self.canvas.create_oval(x-40, y-60, x+40, y+10, fill="#8B4513", outline="black")
        
        # Eyes
        self.canvas.create_oval(x-15, y-40, x-5, y-30, fill="black", tags="mole_part")
        self.canvas.create_oval(x+5, y-40, x+15, y-30, fill="black", tags="mole_part")
        
        # Add mole_part tag to the mole body too
        self.canvas.addtag_withtag("mole_part", self.mole)

        # Random interval for mole to stay
        wait_time = random.randint(700, 1500)
        self.after(wait_time, self.spawn_mole)

    def on_canvas_click(self, event):
        if not self.game_running:
            return
        
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        hit = False
        for item in items:
            if "mole_part" in self.canvas.gettags(item):
                hit = True
                break
        
        if hit:
            self.score += 1
            self.update_ui()
            self.canvas.delete("mole_part")
            self.mole = None

    def countdown(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_ui()
            self.after(1000, self.countdown)
        else:
            self.game_over()

    def game_over(self):
        self.game_running = False
        self.start_btn.configure(state="normal", text="Restart Game")
        if self.mole:
            self.canvas.delete("mole_part")
            self.mole = None
        tk.messagebox.showinfo("Time's Up!", f"Final Score: {self.score}")

if __name__ == "__main__":
    app = WhackAMoleApp()
    app.mainloop()
