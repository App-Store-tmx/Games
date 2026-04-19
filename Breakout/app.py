import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("dark")

class BreakoutApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Breakout")
        self.geometry("600x400")
        self.resizable(False, False)

        self.canvas = tk.Canvas(self, width=600, height=400, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.paddle = self.canvas.create_rectangle(250, 370, 350, 385, fill="white")
        self.ball = self.canvas.create_oval(290, 350, 310, 370, fill="red")
        
        self.ball_dx = 3
        self.ball_dy = -3
        
        self.bricks = []
        self.setup_bricks()

        self.game_running = False
        self.score = 0
        self.label_msg = self.canvas.create_text(300, 200, text="Press Space to Start", fill="white", font=("Arial", 20))

        self.canvas.bind_all("<KeyPress-Left>", lambda e: self.move_paddle(-20))
        self.canvas.bind_all("<KeyPress-Right>", lambda e: self.move_paddle(20))
        self.canvas.bind_all("<space>", self.start_game)

    def setup_bricks(self):
        colors = ["red", "orange", "yellow", "green", "blue"]
        for row in range(5):
            for col in range(10):
                x1 = col * 60 + 2
                y1 = row * 20 + 30
                x2 = x1 + 56
                y2 = y1 + 16
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[row], tags="brick")
                self.bricks.append(brick)

    def move_paddle(self, dx):
        coords = self.canvas.coords(self.paddle)
        if coords[0] + dx >= 0 and coords[2] + dx <= 600:
            self.canvas.move(self.paddle, dx, 0)

    def start_game(self, event):
        if not self.game_running:
            self.game_running = True
            self.canvas.itemconfig(self.label_msg, text="")
            self.game_loop()

    def game_loop(self):
        if not self.game_running:
            return

        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        ball_coords = self.canvas.coords(self.ball)

        # Wall collisions
        if ball_coords[0] <= 0 or ball_coords[2] >= 600:
            self.ball_dx *= -1
        if ball_coords[1] <= 0:
            self.ball_dy *= -1
        if ball_coords[3] >= 400:
            self.game_over("Game Over!")
            return

        # Paddle collision
        paddle_coords = self.canvas.coords(self.paddle)
        if ball_coords[3] >= paddle_coords[1] and \
           ball_coords[2] >= paddle_coords[0] and \
           ball_coords[0] <= paddle_coords[2]:
            self.ball_dy = -abs(self.ball_dy)

        # Brick collision
        items = self.canvas.find_overlapping(*ball_coords)
        for item in items:
            if "brick" in self.canvas.gettags(item):
                self.canvas.delete(item)
                self.bricks.remove(item)
                self.ball_dy *= -1
                self.score += 10
                if not self.bricks:
                    self.game_over("You Win!")
                break

        self.after(16, self.game_loop)

    def game_over(self, msg):
        self.game_running = False
        self.canvas.itemconfig(self.label_msg, text=f"{msg}\nSpace to Restart")
        # Simple reset for next time
        self.after(1000, self.reset_game)

    def reset_game(self):
        self.canvas.delete("brick")
        self.setup_bricks()
        self.canvas.coords(self.paddle, 250, 370, 350, 385)
        self.canvas.coords(self.ball, 290, 350, 310, 370)
        self.ball_dx = 3
        self.ball_dy = -3
        self.score = 0

if __name__ == "__main__":
    app = BreakoutApp()
    app.mainloop()
