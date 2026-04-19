import customtkinter as ctk
import tkinter as tk
import random

class Pong(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pong")
        self.geometry("600x450")
        ctk.set_appearance_mode("dark")

        self.canvas = tk.Canvas(self, width=600, height=400, bg="black", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.paddle_h = 80
        self.paddle_w = 10
        self.ball_size = 15

        self.left_paddle = self.canvas.create_rectangle(10, 160, 10+self.paddle_w, 160+self.paddle_h, fill="white")
        self.right_paddle = self.canvas.create_rectangle(580, 160, 580+self.paddle_w, 160+self.paddle_h, fill="white")
        self.ball = self.canvas.create_oval(292, 192, 292+self.ball_size, 192+self.ball_size, fill="white")

        self.ball_dx = 4
        self.ball_dy = 4
        self.left_score = 0
        self.right_score = 0

        self.score_label = ctk.CTkLabel(self, text="0 - 0", font=("Arial", 24))
        self.score_label.pack()

        self.bind("<w>", lambda e: self.move_paddle(self.left_paddle, -20))
        self.bind("<s>", lambda e: self.move_paddle(self.left_paddle, 20))
        self.bind("<Up>", lambda e: self.move_paddle(self.right_paddle, -20))
        self.bind("<Down>", lambda e: self.move_paddle(self.right_paddle, 20))

        self.game_loop()

    def move_paddle(self, paddle, dy):
        y1, y2 = self.canvas.coords(paddle)[1], self.canvas.coords(paddle)[3]
        if 0 <= y1 + dy and y2 + dy <= 400:
            self.canvas.move(paddle, 0, dy)

    def game_loop(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        bx1, by1, bx2, by2 = self.canvas.coords(self.ball)

        if by1 <= 0 or by2 >= 400:
            self.ball_dy *= -1

        if bx1 <= 0:
            self.right_score += 1
            self.reset_ball()
        elif bx2 >= 600:
            self.left_score += 1
            self.reset_ball()

        # Paddle collisions
        if self.canvas.find_overlapping(bx1, by1, bx2, by2):
            overlap = self.canvas.find_overlapping(bx1, by1, bx2, by2)
            if self.left_paddle in overlap or self.right_paddle in overlap:
                self.ball_dx *= -1.1 # Speed up slightly

        self.score_label.configure(text=f"{self.left_score} - {self.right_score}")
        self.after(20, self.game_loop)

    def reset_ball(self):
        self.canvas.coords(self.ball, 292, 192, 292+self.ball_size, 192+self.ball_size)
        self.ball_dx = 4 * random.choice([1, -1])
        self.ball_dy = 4 * random.choice([1, -1])

if __name__ == "__main__":
    app = Pong()
    app.mainloop()
