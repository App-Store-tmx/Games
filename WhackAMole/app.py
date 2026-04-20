import customtkinter as ctk
import tkinter as tk
import random
import os
import json
from tkinter import messagebox
VERSION = "1.0.0"

ctk.set_appearance_mode("dark")

class WhackAMoleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Whack-A-Mole Deluxe")
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        try:
            icon_path = os.path.join(self.base_path, "icon.png")
            self.icon_img = tk.PhotoImage(file=icon_path)
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass
            
        self.geometry("600x750")
        self.resizable(False, False)

        # High Score setup
        self.high_score_file = os.path.join(self.base_path, "highscore.json")
        self.high_score = self.load_high_score()

        # UI Header
        self.header = ctk.CTkFrame(self, corner_radius=10)
        self.header.pack(pady=10, padx=10, fill="x")

        self.score = 0
        self.score_label = ctk.CTkLabel(self.header, text=f"Score: {self.score}", font=("Segoe UI", 20, "bold"))
        self.score_label.grid(row=0, column=0, padx=20, pady=10)

        self.high_score_label = ctk.CTkLabel(self.header, text=f"Best: {self.high_score}", font=("Segoe UI", 16))
        self.high_score_label.grid(row=0, column=1, padx=20, pady=10)

        self.time_left = 30
        self.time_label = ctk.CTkLabel(self.header, text=f"Time: {self.time_left}s", font=("Segoe UI", 20, "bold"), text_color="#ffcc00")
        self.time_label.grid(row=0, column=2, padx=20, pady=10)

        # Canvas for holes
        self.canvas = tk.Canvas(self, width=600, height=500, bg="#1a3d16", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Grid setup
        self.holes = []
        self.mole_id = None
        self.mole_type = None
        self.setup_holes()

        # Controls
        self.controls = ctk.CTkFrame(self, fg_color="transparent")
        self.controls.pack(pady=10)

        self.game_running = False
        self.start_stop_btn = ctk.CTkButton(self.controls, text="START GAME", font=("Segoe UI", 16, "bold"), 
                                            fg_color="#28a745", hover_color="#218838",
                                            command=self.toggle_game)
        self.start_stop_btn.pack(side="left", padx=10)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def load_high_score(self):
        if os.path.exists(self.high_score_file):
            try:
                with open(self.high_score_file, 'r') as f:
                    return json.load(f).get("high_score", 0)
            except:
                return 0
        return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open(self.high_score_file, 'w') as f:
                json.dump({"high_score": self.high_score}, f)
            self.high_score_label.configure(text=f"Best: {self.high_score}")

    def setup_holes(self):
        for r in range(3):
            for c in range(3):
                x = c * 200 + 100
                y = r * 150 + 100
                # Hole
                self.canvas.create_oval(x-70, y-35, x+70, y+35, fill="#2a1a0a", outline="#1a0a00", width=2)
                self.holes.append((x, y))

    def toggle_game(self):
        if not self.game_running:
            self.start_game()
        else:
            self.game_over(stopped=True)

    def start_game(self):
        self.score = 0
        self.time_left = 30
        self.game_running = True
        self.start_stop_btn.configure(text="STOP GAME", fg_color="#dc3545", hover_color="#c82333")
        self.update_ui()
        self.spawn_mole()
        self.countdown()

    def update_ui(self):
        self.score_label.configure(text=f"Score: {self.score}")
        self.time_label.configure(text=f"Time: {self.time_left}s")

    def spawn_mole(self):
        if not self.game_running:
            return
        
        self.canvas.delete("mole")
        
        pos = random.choice(self.holes)
        x, y = pos
        
        # Decide mole type
        rand = random.random()
        if rand < 0.1: # 10% Golden
            self.mole_type = "golden"
            color = "#FFD700"
            outline = "#B8860B"
        elif rand < 0.3: # 20% Red
            self.mole_type = "red"
            color = "#FF4500"
            outline = "#8B0000"
        else: # 70% Regular
            self.mole_type = "regular"
            color = "#8B4513"
            outline = "#5D2E0C"

        # Mole Body
        self.mole_id = self.canvas.create_oval(x-45, y-70, x+45, y+15, fill=color, outline=outline, width=2, tags="mole")
        
        # Eyes
        self.canvas.create_oval(x-18, y-45, x-6, y-33, fill="black", tags="mole")
        self.canvas.create_oval(x+6, y-45, x+18, y-33, fill="black", tags="mole")
        
        # Nose
        self.canvas.create_oval(x-5, y-30, x+5, y-20, fill="#FF69B4", tags="mole")

        # Stay duration based on type
        wait_time = random.randint(600, 1200)
        if self.mole_type == "golden":
            wait_time = 500 # Harder to catch
        
        self.mole_timer = self.after(wait_time, self.spawn_mole)

    def on_canvas_click(self, event):
        if not self.game_running:
            return
        
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        hit = False
        for item in items:
            if "mole" in self.canvas.gettags(item):
                hit = True
                break
        
        if hit:
            if self.mole_type == "golden":
                self.score += 5
            elif self.mole_type == "red":
                self.score -= 3
            else:
                self.score += 1
            
            self.update_ui()
            self.canvas.delete("mole")
            self.after_cancel(self.mole_timer)
            self.spawn_mole()

    def countdown(self):
        if not self.game_running:
            return
            
        if self.time_left > 0:
            self.time_left -= 1
            self.update_ui()
            self.after(1000, self.countdown)
        else:
            self.game_over()

    def game_over(self, stopped=False):
        self.game_running = False
        if hasattr(self, 'mole_timer'):
            self.after_cancel(self.mole_timer)
            
        self.start_stop_btn.configure(text="START GAME", fg_color="#28a745", hover_color="#218838")
        self.canvas.delete("mole")
        
        self.save_high_score()
        
        if not stopped:
            messagebox.showinfo("Time's Up!", f"Game Over!\nFinal Score: {self.score}")

if __name__ == "__main__":
    app = WhackAMoleApp()
    app.mainloop()
