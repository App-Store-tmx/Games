import customtkinter as ctk
import tkinter as tk
import random

ctk.set_appearance_mode("dark")

class FlappyBirdApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Flappy Bird")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            # Fallback if icon.png is missing or loading fails
            pass
        self.geometry("400x600")
        self.resizable(False, False)

        self.canvas = tk.Canvas(self, width=400, height=600, bg="#4EC0CA", highlightthickness=0)
        self.canvas.pack()

        self.bird = None
        self.bird_y = 300
        self.bird_v = 0
        self.gravity = 0.5
        self.jump_power = -8

        self.pipes = []
        self.pipe_speed = 3
        self.pipe_gap = 150

        self.score = 0
        self.game_running = False
        
        self.label_score = self.canvas.create_text(200, 50, text="Press Space to Start", font=("Arial", 20, "bold"), fill="white")

        self.bind("<space>", self.on_space)
        self.reset_game()

    def reset_game(self):
        self.canvas.delete("pipe")
        if self.bird:
            self.canvas.delete(self.bird)
        
        self.bird = self.canvas.create_oval(50, 285, 80, 315, fill="yellow", outline="black", width=2)
        self.bird_y = 300
        self.bird_v = 0
        self.pipes = []
        self.score = 0
        self.game_running = False
        self.canvas.itemconfig(self.label_score, text="Press Space to Start")

    def spawn_pipe(self):
        gap_y = random.randint(150, 450)
        top_pipe = self.canvas.create_rectangle(400, 0, 450, gap_y - self.pipe_gap//2, fill="green", outline="black", tags="pipe")
        bot_pipe = self.canvas.create_rectangle(400, gap_y + self.pipe_gap//2, 450, 600, fill="green", outline="black", tags="pipe")
        self.pipes.append((top_pipe, bot_pipe, False))

    def on_space(self, event):
        if not self.game_running:
            self.game_running = True
            self.canvas.itemconfig(self.label_score, text="0")
            self.game_loop()
        
        self.bird_v = self.jump_power

    def game_loop(self):
        if not self.game_running:
            return

        # Bird physics
        self.bird_v += self.gravity
        self.bird_y += self.bird_v
        self.canvas.move(self.bird, 0, self.bird_v)

        # Pipe spawning
        if not self.pipes or self.canvas.coords(self.pipes[-1][0])[0] < 200:
            self.spawn_pipe()

        # Pipe movement and scoring
        for i, (top, bot, passed) in enumerate(self.pipes):
            self.canvas.move(top, -self.pipe_speed, 0)
            self.canvas.move(bot, -self.pipe_speed, 0)
            
            coords = self.canvas.coords(top)
            if not passed and coords[2] < 50:
                self.score += 1
                self.canvas.itemconfig(self.label_score, text=str(self.score))
                self.pipes[i] = (top, bot, True)

        # Cleanup off-screen pipes
        if self.canvas.coords(self.pipes[0][0])[2] < 0:
            p = self.pipes.pop(0)
            self.canvas.delete(p[0])
            self.canvas.delete(p[1])

        # Collision detection
        bird_coords = self.canvas.coords(self.bird)
        if bird_coords[1] < 0 or bird_coords[3] > 600:
            self.game_over()
            return

        overlapping = self.canvas.find_overlapping(*bird_coords)
        for obj in overlapping:
            if "pipe" in self.canvas.gettags(obj):
                self.game_over()
                return

        self.after(20, self.game_loop)

    def game_over(self):
        self.game_running = False
        self.canvas.itemconfig(self.label_score, text=f"Game Over! Score: {self.score}\nSpace to Restart")
        # To avoid immediate restart
        self.unbind("<space>")
        self.after(1000, lambda: self.bind("<space>", self.on_space))

if __name__ == "__main__":
    app = FlappyBirdApp()
    app.mainloop()
