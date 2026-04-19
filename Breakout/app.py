import customtkinter as ctk
import tkinter as tk
import random
import os

ctk.set_appearance_mode("dark")

class BreakoutApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Breakout Ultra")
        self.geometry("600x600")
        self.resizable(False, False)

        # Icon logic
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            try:
                self.icon_img = tk.PhotoImage(file=icon_path)
                self.iconphoto(False, self.icon_img)
            except:
                pass

        # Game constants
        self.canvas_width = 600
        self.canvas_height = 400
        self.paddle_y = 370
        self.initial_paddle_width = 100
        self.paddle_height = 15
        
        # Game state
        self.lives = 3
        self.score = 0
        self.level = 1
        self.game_running = False
        
        self.balls = []
        self.bricks = []
        self.powerups = []
        
        self.setup_ui()
        self.reset_game_state()

    def setup_ui(self):
        # Stats bar
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(pady=10, fill="x", padx=20)

        self.score_label = ctk.CTkLabel(self.stats_frame, text=f"Score: 0", font=("Arial", 18))
        self.score_label.pack(side="left", padx=20)

        self.level_label = ctk.CTkLabel(self.stats_frame, text=f"Level: 1", font=("Arial", 18))
        self.level_label.pack(side="left", expand=True)

        self.lives_label = ctk.CTkLabel(self.stats_frame, text=f"Lives: 3", font=("Arial", 18), text_color="#e74c3c")
        self.lives_label.pack(side="right", padx=20)

        # Canvas
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="#111", highlightthickness=0)
        self.canvas.pack()

        # Paddle
        self.paddle_width = self.initial_paddle_width
        self.paddle = self.canvas.create_rectangle(
            250, self.paddle_y, 250 + self.paddle_width, self.paddle_y + self.paddle_height, 
            fill="#3498db", outline="white"
        )

        # Info label
        self.info_label = ctk.CTkLabel(self, text="Use Left/Right Arrows | SPACE to Start", font=("Arial", 16))
        self.info_label.pack(pady=15)

        self.bind("<Left>", lambda e: self.move_paddle(-30))
        self.bind("<Right>", lambda e: self.move_paddle(30))
        self.bind("<space>", self.start_game)

    def reset_game_state(self):
        self.lives = 3
        self.score = 0
        self.level = 1
        self.update_stats()
        self.clear_canvas()
        self.setup_level()
        self.spawn_ball()
        self.game_running = False
        self.info_label.configure(text="Level 1 - Press SPACE to Start")

    def clear_canvas(self):
        for b in self.balls: self.canvas.delete(b['id'])
        self.balls = []
        for p in self.powerups: self.canvas.delete(p['id'])
        self.powerups = []
        for br in self.bricks: self.canvas.delete(br)
        self.bricks = []

    def setup_level(self):
        # Different brick layouts based on level
        colors = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6"]
        
        if self.level % 3 == 1: # Standard rows
            rows = 4 + (self.level // 3)
            for r in range(rows):
                for c in range(10):
                    self.create_brick(c * 60 + 2, r * 25 + 40, colors[r % len(colors)])
        elif self.level % 3 == 2: # Pyramid
            for r in range(6):
                for c in range(r, 10-r):
                    self.create_brick(c * 60 + 2, r * 25 + 40, colors[r % len(colors)])
        else: # Zig-zag / Alternating
            for r in range(6):
                for c in range(10):
                    if (r + c) % 2 == 0:
                        self.create_brick(c * 60 + 2, r * 25 + 40, colors[r % len(colors)])

    def create_brick(self, x, y, color):
        brick = self.canvas.create_rectangle(x, y, x + 56, y + 20, fill=color, outline="black", tags="brick")
        self.bricks.append(brick)

    def spawn_ball(self):
        ball_id = self.canvas.create_oval(290, 350, 310, 370, fill="#f1c40f", outline="white")
        self.balls.append({
            'id': ball_id,
            'dx': random.choice([-4, 4]),
            'dy': -4
        })

    def start_game(self, event=None):
        if not self.game_running:
            if self.lives <= 0:
                self.reset_game_state()
            self.game_running = True
            self.info_label.configure(text="Break them all!")
            self.game_loop()

    def update_stats(self):
        self.score_label.configure(text=f"Score: {self.score}")
        self.level_label.configure(text=f"Level: {self.level}")
        self.lives_label.configure(text=f"Lives: {self.lives}")

    def move_paddle(self, dx):
        coords = self.canvas.coords(self.paddle)
        if coords[0] + dx >= 0 and coords[2] + dx <= self.canvas_width:
            self.canvas.move(self.paddle, dx, 0)

    def spawn_powerup(self, x, y):
        types = ["Extra Ball", "Paddle Grow", "Slow Ball"]
        p_type = random.choice(types)
        colors = {"Extra Ball": "#2ecc71", "Paddle Grow": "#3498db", "Slow Ball": "#f1c40f"}
        
        p_id = self.canvas.create_oval(x, y, x+20, y+20, fill=colors[p_type], outline="white")
        self.powerups.append({'id': p_id, 'type': p_type})

    def apply_powerup(self, p_type):
        if p_type == "Extra Ball":
            self.spawn_ball()
        elif p_type == "Paddle Grow":
            coords = self.canvas.coords(self.paddle)
            new_width = min(200, self.paddle_width + 40)
            self.paddle_width = new_width
            self.canvas.coords(self.paddle, coords[0], coords[1], coords[0] + new_width, coords[3])
        elif p_type == "Slow Ball":
            for b in self.balls:
                b['dx'] = 3 if b['dx'] > 0 else -3
                b['dy'] = -3 if b['dy'] < 0 else 3

    def game_loop(self):
        if not self.game_running:
            return

        # Move balls
        balls_to_remove = []
        for b in self.balls:
            self.canvas.move(b['id'], b['dx'], b['dy'])
            b_coords = self.canvas.coords(b['id'])

            # Wall collisions
            if b_coords[0] <= 0 or b_coords[2] >= self.canvas_width:
                b['dx'] *= -1
            if b_coords[1] <= 0:
                b['dy'] *= -1
            
            # Paddle collision
            p_coords = self.canvas.coords(self.paddle)
            if b_coords[3] >= p_coords[1] and b_coords[2] >= p_coords[0] and b_coords[0] <= p_coords[2]:
                b['dy'] = -abs(b['dy'])
                # Add some directional influence from paddle movement
                b['dx'] += (b_coords[0] + 10 - (p_coords[0] + p_coords[2])/2) / 10

            # Brick collision
            items = self.canvas.find_overlapping(*b_coords)
            for item in items:
                if item in self.bricks:
                    self.canvas.delete(item)
                    self.bricks.remove(item)
                    b['dy'] *= -1
                    self.score += 10
                    self.update_stats()
                    
                    if random.random() < 0.2: # 20% chance for powerup
                        self.spawn_powerup((b_coords[0]+b_coords[2])/2, b_coords[3])
                    
                    if not self.bricks:
                        self.level_up()
                        return
                    break

            # Out of bounds
            if b_coords[3] >= self.canvas_height:
                balls_to_remove.append(b)

        for b in balls_to_remove:
            self.canvas.delete(b['id'])
            self.balls.remove(b)

        if not self.balls:
            self.lives -= 1
            self.update_stats()
            # Reset paddle size
            coords = self.canvas.coords(self.paddle)
            self.paddle_width = self.initial_paddle_width
            self.canvas.coords(self.paddle, coords[0], coords[1], coords[0] + self.paddle_width, coords[3])
            
            if self.lives <= 0:
                self.game_over()
                return
            else:
                self.spawn_ball()
                self.game_running = False
                self.info_label.configure(text="Life Lost! Press SPACE to continue")
                return

        # Powerups
        pu_to_remove = []
        for p in self.powerups:
            self.canvas.move(p['id'], 0, 3)
            p_coords = self.canvas.coords(p['id'])
            
            # Paddle catch
            p_p_coords = self.canvas.coords(self.paddle)
            if p_coords[3] >= p_p_coords[1] and p_coords[2] >= p_p_coords[0] and p_coords[0] <= p_p_coords[2]:
                self.apply_powerup(p['type'])
                pu_to_remove.append(p)
            elif p_coords[3] >= self.canvas_height:
                pu_to_remove.append(p)

        for p in pu_to_remove:
            self.canvas.delete(p['id'])
            self.powerups.remove(p)

        self.after(16, self.game_loop)

    def level_up(self):
        self.level += 1
        self.update_stats()
        self.game_running = False
        self.clear_canvas()
        self.setup_level()
        self.spawn_ball()
        self.info_label.configure(text=f"Level {self.level} - Press SPACE")

    def game_over(self):
        self.game_running = False
        self.info_label.configure(text="GAME OVER - Press SPACE to Restart")

if __name__ == "__main__":
    app = BreakoutApp()
    app.mainloop()
