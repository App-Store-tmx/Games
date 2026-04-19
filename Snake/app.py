import customtkinter as ctk
import tkinter as tk
import random
from tkinter import messagebox
import os

class SnakeGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Snake - Pro")
        self.geometry("500x650")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Icon logic
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "icon.png")
            self.icon_img = tk.PhotoImage(file=icon_path)
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass

        self.cell_size = 20
        self.grid_width = 20
        self.grid_height = 20
        self.canvas_width = self.cell_size * self.grid_width
        self.canvas_height = self.cell_size * self.grid_height

        self.highscore_file = os.path.join(os.path.dirname(__file__), "highscore.txt")
        self.high_score = self.load_high_score()
        
        self.reset_game_state()
        self.setup_ui()
        
        self.bind("<KeyPress>", self.change_direction)
        self.after(500, self.update_game)

    def load_high_score(self):
        if os.path.exists(self.highscore_file):
            try:
                with open(self.highscore_file, "r") as f:
                    return int(f.read())
            except:
                return 0
        return 0

    def save_high_score(self):
        with open(self.highscore_file, "w") as f:
            f.write(str(self.high_score))

    def reset_game_state(self):
        self.score = 0
        self.level = 1
        self.speed = 150
        self.direction = "Right"
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.food = (15, 15)
        self.running = True
        self.paused = False

    def setup_ui(self):
        # Stats Frame
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(pady=20, padx=20, fill="x")

        self.score_label = ctk.CTkLabel(self.stats_frame, text=f"Score: {self.score}", font=("Helvetica", 18, "bold"))
        self.score_label.grid(row=0, column=0, padx=20, pady=10)

        self.level_label = ctk.CTkLabel(self.stats_frame, text=f"Level: {self.level}", font=("Helvetica", 18, "bold"), text_color="#3B8ED0")
        self.level_label.grid(row=0, column=1, padx=20, pady=10)

        self.hi_score_label = ctk.CTkLabel(self.stats_frame, text=f"Best: {self.high_score}", font=("Helvetica", 18, "bold"), text_color="#E74C3C")
        self.hi_score_label.grid(row=0, column=2, padx=20, pady=10)

        # Canvas
        self.canvas_frame = ctk.CTkFrame(self, fg_color="#1A1A1A", border_width=2, border_color="#333333")
        self.canvas_frame.pack(padx=20, pady=10)

        self.canvas = tk.Canvas(
            self.canvas_frame, 
            bg="#1A1A1A", 
            width=self.canvas_width, 
            height=self.canvas_height, 
            highlightthickness=0
        )
        self.canvas.pack(padx=5, pady=5)

        # Controls Hint
        self.hint_label = ctk.CTkLabel(self, text="Use Arrow Keys to Move • Press 'P' to Pause", font=("Helvetica", 12))
        self.hint_label.pack(pady=10)

        self.reset_btn = ctk.CTkButton(self, text="RESTART GAME", command=self.restart_game, font=("Helvetica", 16, "bold"))
        self.reset_btn.pack(pady=10)

    def spawn_food(self):
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def change_direction(self, event):
        key = event.keysym
        if key.lower() == 'p':
            self.paused = not self.paused
            return

        opposites = {("Up", "Down"), ("Down", "Up"), ("Left", "Right"), ("Right", "Left")}
        if key in ["Up", "Down", "Left", "Right"]:
            if (self.direction, key) not in opposites:
                self.direction = key

    def update_game(self):
        if not self.running:
            return
        
        if self.paused:
            self.after(100, self.update_game)
            return

        head_x, head_y = self.snake[0]
        if self.direction == "Up": head_y -= 1
        elif self.direction == "Down": head_y += 1
        elif self.direction == "Left": head_x -= 1
        elif self.direction == "Right": head_x += 1

        new_head = (head_x, head_y)

        # Collision Check
        if (head_x < 0 or head_x >= self.grid_width or 
            head_y < 0 or head_y >= self.grid_height or
            new_head in self.snake):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # Food Check
        if new_head == self.food:
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            
            # Level and Speed System
            new_level = (self.score // 5) + 1
            if new_level > self.level:
                self.level = new_level
                self.speed = max(60, 150 - (self.level - 1) * 10)
            
            self.update_labels()
            self.spawn_food()
        else:
            self.snake.pop()

        self.draw()
        self.after(self.speed, self.update_game)

    def update_labels(self):
        self.score_label.configure(text=f"Score: {self.score}")
        self.level_label.configure(text=f"Level: {self.level}")
        self.hi_score_label.configure(text=f"Best: {self.high_score}")

    def draw(self):
        self.canvas.delete("all")
        
        # Draw Food
        fx, fy = self.food
        self.canvas.create_oval(
            fx*self.cell_size+2, fy*self.cell_size+2, 
            (fx+1)*self.cell_size-2, (fy+1)*self.cell_size-2, 
            fill="#E74C3C", outline="#C0392B"
        )
        
        # Draw Snake
        for i, (x, y) in enumerate(self.snake):
            color = "#2ECC71" if i == 0 else "#27AE60"
            # Rounded segments using ovals
            self.canvas.create_oval(
                x*self.cell_size+1, y*self.cell_size+1, 
                (x+1)*self.cell_size-1, (y+1)*self.cell_size-1, 
                fill=color, outline=""
            )
            # Add a small eye to the head
            if i == 0:
                eye_size = 3
                if self.direction in ["Right", "Left"]:
                    self.canvas.create_oval(x*self.cell_size+12, y*self.cell_size+5, x*self.cell_size+15, y*self.cell_size+8, fill="white")
                else:
                    self.canvas.create_oval(x*self.cell_size+5, y*self.cell_size+5, x*self.cell_size+8, y*self.cell_size+8, fill="white")

    def game_over(self):
        self.running = False
        messagebox.showinfo("Game Over", f"Final Score: {self.score}\nLevel: {self.level}")
        self.restart_game()

    def restart_game(self):
        self.reset_game_state()
        self.update_labels()
        self.spawn_food()
        if not self.running: # If coming from game over
            self.running = True
            self.update_game()

if __name__ == "__main__":
    app = SnakeGame()
    app.mainloop()
