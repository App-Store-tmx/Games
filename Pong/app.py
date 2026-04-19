import customtkinter as ctk
import tkinter as tk
import random
import os

ctk.set_appearance_mode("dark")

class Pong(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pong Pro")
        self.geometry("700x550")
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
        self.canvas_width = 680
        self.canvas_height = 400
        self.paddle_h = 80
        self.paddle_w = 12
        self.ball_size = 15
        self.winning_score = 5

        # Difficulty settings (AI speed)
        self.difficulties = {
            "Slow": 3,
            "Fast": 6,
            "Smart": 8
        }
        self.current_difficulty = tk.StringVar(value="Slow")

        # UI Components
        self.setup_ui()

        # Game state
        self.ball_dx = 0
        self.ball_dy = 0
        self.left_score = 0
        self.right_score = 0
        self.game_running = False
        self.shake_remaining = 0

        self.reset_game_state()

    def setup_ui(self):
        # Header with scores and difficulty
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(pady=10, fill="x", padx=20)

        self.score_label = ctk.CTkLabel(self.header_frame, text="0 - 0", font=("Orbitron", 32, "bold"))
        self.score_label.pack(side="left", expand=True)

        self.diff_label = ctk.CTkLabel(self.header_frame, text="AI Difficulty:")
        self.diff_label.pack(side="left", padx=5)

        self.diff_menu = ctk.CTkOptionMenu(
            self.header_frame, 
            values=list(self.difficulties.keys()),
            variable=self.current_difficulty,
            command=self.on_difficulty_change
        )
        self.diff_menu.pack(side="left", padx=10)

        # Canvas
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="#1a1a1a", highlightthickness=2, highlightbackground="#333")
        self.canvas.pack(pady=5)

        # Draw elements
        self.left_paddle = self.canvas.create_rectangle(15, 160, 15+self.paddle_w, 160+self.paddle_h, fill="#3498db", outline="")
        self.right_paddle = self.canvas.create_rectangle(653, 160, 653+self.paddle_w, 160+self.paddle_h, fill="#e74c3c", outline="")
        self.ball = self.canvas.create_oval(332, 192, 332+self.ball_size, 192+self.ball_size, fill="#f1c40f", outline="")

        # Instructions / Control
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(pady=10, fill="x", padx=20)

        self.info_label = ctk.CTkLabel(self.control_frame, text="W/S: Left Paddle | Right: AI | Press SPACE to Start", font=("Arial", 14))
        self.info_label.pack(pady=5)

        self.bind("<w>", lambda e: self.move_paddle(self.left_paddle, -25))
        self.bind("<s>", lambda e: self.move_paddle(self.left_paddle, 25))
        self.bind("<space>", self.start_game)

    def on_difficulty_change(self, choice):
        if not self.game_running:
            self.reset_game_state()

    def reset_game_state(self):
        self.left_score = 0
        self.right_score = 0
        self.update_score()
        self.reset_ball()
        self.game_running = False
        self.info_label.configure(text="W/S: Move | SPACE to Start")

    def reset_ball(self):
        self.canvas.coords(self.ball, 332, 192, 332+self.ball_size, 192+self.ball_size)
        self.ball_dx = 5 * random.choice([1, -1])
        self.ball_dy = random.uniform(-4, 4)

    def start_game(self, event=None):
        if not self.game_running:
            if self.left_score >= self.winning_score or self.right_score >= self.winning_score:
                self.reset_game_state()
            self.game_running = True
            self.info_label.configure(text="Match Point is 5! GO!")
            self.game_loop()

    def update_score(self):
        self.score_label.configure(text=f"{self.left_score} - {self.right_score}")

    def move_paddle(self, paddle, dy):
        coords = self.canvas.coords(paddle)
        if not coords: return
        y1, y2 = coords[1], coords[3]
        if 0 <= y1 + dy and y2 + dy <= self.canvas_height:
            self.canvas.move(paddle, 0, dy)

    def ai_move(self):
        # AI logic for right paddle
        ball_coords = self.canvas.coords(self.ball)
        paddle_coords = self.canvas.coords(self.right_paddle)
        if not ball_coords or not paddle_coords: return

        ball_center = (ball_coords[1] + ball_coords[3]) / 2
        paddle_center = (paddle_coords[1] + paddle_coords[3]) / 2
        
        speed = self.difficulties[self.current_difficulty.get()]
        
        # Smart AI adds a bit of prediction
        if self.current_difficulty.get() == "Smart":
            if self.ball_dx > 0: # Ball coming towards AI
                # Target the future position roughly
                target_y = ball_center + (random.uniform(-10, 10))
            else:
                target_y = self.canvas_height / 2
        else:
            target_y = ball_center

        if abs(paddle_center - target_y) > 10:
            if paddle_center < target_y:
                self.move_paddle(self.right_paddle, speed)
            else:
                self.move_paddle(self.right_paddle, -speed)

    def screen_shake(self):
        self.shake_remaining = 8
        self._perform_shake()

    def _perform_shake(self):
        if self.shake_remaining > 0:
            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)
            self.canvas.place(x=10 + dx, y=70 + dy) # Adjust y based on packing
            self.shake_remaining -= 1
            self.after(20, self._perform_shake)
        else:
            self.canvas.place(x=10, y=70)

    def color_flash(self):
        original_bg = self.canvas.cget("bg")
        self.canvas.configure(bg="#444")
        self.after(50, lambda: self.canvas.configure(bg=original_bg))

    def game_loop(self):
        if not self.game_running:
            return

        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        self.ai_move()
        
        bx1, by1, bx2, by2 = self.canvas.coords(self.ball)

        # Wall collisions
        if by1 <= 0 or by2 >= self.canvas_height:
            self.ball_dy *= -1
            self.color_flash()

        # Goal detection
        if bx1 <= 0:
            self.right_score += 1
            self.update_score()
            self.screen_shake()
            if self.right_score >= self.winning_score:
                self.end_game("AI Wins!")
            else:
                self.reset_ball()
        elif bx2 >= self.canvas_width:
            self.left_score += 1
            self.update_score()
            self.screen_shake()
            if self.left_score >= self.winning_score:
                self.end_game("You Win!")
            else:
                self.reset_ball()

        # Paddle collisions
        items = self.canvas.find_overlapping(bx1, by1, bx2, by2)
        if self.left_paddle in items or self.right_paddle in items:
            self.ball_dx *= -1.05 # Speed up
            self.ball_dy += random.uniform(-1, 1) # Add some randomness to trajectory
            self.color_flash()
            # Push ball out of paddle to prevent sticking
            if self.left_paddle in items:
                self.canvas.coords(self.ball, 15+self.paddle_w+1, by1, 15+self.paddle_w+1+self.ball_size, by2)
            else:
                self.canvas.coords(self.ball, 653-self.ball_size-1, by1, 653-1, by2)

        self.after(16, self.game_loop)

    def end_game(self, winner):
        self.game_running = False
        self.info_label.configure(text=f"{winner} Press SPACE to Restart")

if __name__ == "__main__":
    app = Pong()
    app.mainloop()
