import customtkinter as ctk
import tkinter as tk
import random
import os

ctk.set_appearance_mode("dark")

class FlappyBirdApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Flappy Bird Parallax")
        self.geometry("400x700")
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
        self.canvas_width = 400
        self.canvas_height = 600
        self.gravity = 0.6
        self.jump_force = -9
        self.pipe_speed = 3.5
        self.pipe_gap = 160
        self.pipe_width = 60

        # Game state
        self.score = 0
        self.high_score = 0
        self.game_running = False
        self.bird_v = 0
        
        self.pipes = []
        self.background_elements = [] # (id, speed, x_pos)
        
        self.setup_ui()
        self.reset_game()

    def setup_ui(self):
        # Top bar
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=10, fill="x", padx=10)

        self.score_label = ctk.CTkLabel(self.top_frame, text="Score: 0", font=("Arial", 18, "bold"))
        self.score_label.pack(side="left", padx=10)

        self.high_score_label = ctk.CTkLabel(self.top_frame, text="Best: 0", font=("Arial", 18), text_color="#f1c40f")
        self.high_score_label.pack(side="right", padx=10)

        # Canvas
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="#2c3e50", highlightthickness=0)
        self.canvas.pack()

        # Instructions
        self.info_label = ctk.CTkLabel(self, text="Press SPACE to Jump / Start", font=("Arial", 16))
        self.info_label.pack(pady=10)

        self.bind("<space>", self.on_jump)

    def create_background(self):
        self.canvas.delete("bg")
        self.background_elements = []
        
        # Mountains (slowest)
        for i in range(2):
            x = i * 400
            m = self.canvas.create_polygon(x, 600, x+100, 450, x+200, 600, x+300, 480, x+400, 600, fill="#34495e", tags=("bg", "mountain"))
            self.background_elements.append({'id': m, 'speed': 0.5, 'x': x, 'type': 'mountain'})
            
        # Clouds (mid)
        for _ in range(5):
            x = random.randint(0, 800)
            y = random.randint(50, 200)
            c = self.canvas.create_oval(x, y, x+60, y+30, fill="#7f8c8d", outline="", tags=("bg", "cloud"))
            self.background_elements.append({'id': c, 'speed': 1.0, 'x': x, 'type': 'cloud'})

        # Floor (fastest - matches pipes)
        for i in range(2):
            x = i * 400
            f = self.canvas.create_rectangle(x, 580, x+400, 600, fill="#27ae60", tags=("bg", "floor"))
            self.background_elements.append({'id': f, 'speed': self.pipe_speed, 'x': x, 'type': 'floor'})

    def reset_game(self):
        self.canvas.delete("pipe")
        self.canvas.delete("bird")
        
        self.create_background()
        
        self.bird = self.canvas.create_oval(60, 280, 95, 315, fill="#f1c40f", outline="black", width=2, tags="bird")
        
        self.score = 0
        self.bird_v = 0
        self.pipes = []
        self.game_running = False
        self.update_score()
        self.info_label.configure(text="Press SPACE to Start")

    def update_score(self):
        self.score_label.configure(text=f"Score: {self.score}")
        self.high_score_label.configure(text=f"Best: {self.high_score}")

    def spawn_pipe(self):
        gap_y = random.randint(150, 450)
        top = self.canvas.create_rectangle(400, 0, 400+self.pipe_width, gap_y - self.pipe_gap//2, fill="#2ecc71", outline="black", tags="pipe")
        bot = self.canvas.create_rectangle(400, gap_y + self.pipe_gap//2, 400+self.pipe_width, 600, fill="#2ecc71", outline="black", tags="pipe")
        self.pipes.append({'top': top, 'bot': bot, 'passed': False})

    def on_jump(self, event=None):
        if not self.game_running:
            self.game_running = True
            self.info_label.configure(text="Flap away!")
            self.game_loop()
        
        self.bird_v = self.jump_force

    def update_parallax(self):
        for el in self.background_elements:
            self.canvas.move(el['id'], -el['speed'], 0)
            el['x'] -= el['speed']
            
            if el['x'] <= -400 and el['type'] in ('mountain', 'floor'):
                self.canvas.move(el['id'], 800, 0)
                el['x'] += 800
            elif el['x'] <= -100 and el['type'] == 'cloud':
                self.canvas.move(el['id'], 500, 0)
                el['x'] += 500

    def game_loop(self):
        if not self.game_running:
            return

        # Bird physics
        self.bird_v += self.gravity
        self.canvas.move(self.bird, 0, self.bird_v)
        
        # Parallax background
        self.update_parallax()

        # Pipes
        if not self.pipes or self.canvas.coords(self.pipes[-1]['top'])[0] < 220:
            self.spawn_pipe()

        pipes_to_remove = []
        for p in self.pipes:
            self.canvas.move(p['top'], -self.pipe_speed, 0)
            self.canvas.move(p['bot'], -self.pipe_speed, 0)
            
            coords = self.canvas.coords(p['top'])
            if not p['passed'] and coords[2] < 60:
                self.score += 1
                p['passed'] = True
                self.update_score()
            
            if coords[2] < 0:
                pipes_to_remove.append(p)

        for p in pipes_to_remove:
            self.canvas.delete(p['top'])
            self.canvas.delete(p['bot'])
            self.pipes.remove(p)

        # Collision
        bird_coords = self.canvas.coords(self.bird)
        if bird_coords[1] <= 0 or bird_coords[3] >= 580:
            self.game_over()
            return

        overlap = self.canvas.find_overlapping(*bird_coords)
        for item in overlap:
            if "pipe" in self.canvas.gettags(item):
                self.game_over()
                return

        self.after(20, self.game_loop)

    def game_over(self):
        self.game_running = False
        if self.score > self.high_score:
            self.high_score = self.score
        self.update_score()
        self.info_label.configure(text="CRASHED! Press SPACE to Restart")
        # To avoid immediate jump on restart
        self.unbind("<space>")
        self.after(500, lambda: self.bind("<space>", self.on_jump))

if __name__ == "__main__":
    app = FlappyBirdApp()
    app.mainloop()
