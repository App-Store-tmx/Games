import customtkinter as ctk
import tkinter as tk
import random

ctk.set_appearance_mode("dark")

class SpaceInvadersApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Space Invaders")
        self.geometry("600x700")
        self.resizable(False, False)

        self.canvas = tk.Canvas(self, width=600, height=600, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.player = self.canvas.create_rectangle(275, 560, 325, 580, fill="#00ff00")
        self.bullets = []
        self.aliens = []
        self.alien_bullets = []
        self.score = 0
        self.game_running = False

        self.score_label = ctk.CTkLabel(self, text=f"Score: {self.score}", font=("Arial", 20))
        self.score_label.pack(pady=10)

        self.start_btn = ctk.CTkButton(self, text="Start Game", command=self.start_game)
        self.start_btn.pack(pady=5)

        self.canvas.bind_all("<Left>", lambda e: self.move_player(-20))
        self.canvas.bind_all("<Right>", lambda e: self.move_player(20))
        self.canvas.bind_all("<space>", lambda e: self.shoot())

    def start_game(self):
        if self.game_running: return
        self.canvas.delete("alien", "bullet", "alien_bullet")
        self.aliens = []
        self.bullets = []
        self.alien_bullets = []
        self.score = 0
        self.score_label.configure(text=f"Score: {self.score}")
        self.setup_aliens()
        self.game_running = True
        self.start_btn.configure(state="disabled")
        self.alien_direction = 1
        self.game_loop()

    def setup_aliens(self):
        for row in range(4):
            for col in range(8):
                x1 = col * 60 + 50
                y1 = row * 40 + 50
                alien = self.canvas.create_rectangle(x1, y1, x1+40, y1+30, fill="red", tags="alien")
                self.aliens.append(alien)

    def move_player(self, dx):
        if not self.game_running: return
        coords = self.canvas.coords(self.player)
        if coords[0] + dx >= 0 and coords[2] + dx <= 600:
            self.canvas.move(self.player, dx, 0)

    def shoot(self):
        if not self.game_running: return
        p_coords = self.canvas.coords(self.player)
        bullet = self.canvas.create_rectangle(p_coords[0]+22, p_coords[1]-10, p_coords[0]+28, p_coords[1], fill="yellow", tags="bullet")
        self.bullets.append(bullet)

    def game_loop(self):
        if not self.game_running: return

        # Move bullets
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, -10)
            b_coords = self.canvas.coords(bullet)
            if b_coords[1] < 0:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
                continue
            
            # Hit detection
            hit = self.canvas.find_overlapping(*b_coords)
            for item in hit:
                if item in self.aliens:
                    self.canvas.delete(item)
                    self.aliens.remove(item)
                    self.canvas.delete(bullet)
                    self.bullets.remove(bullet)
                    self.score += 10
                    self.score_label.configure(text=f"Score: {self.score}")
                    break

        # Move aliens
        move_down = False
        for alien in self.aliens:
            self.canvas.move(alien, 5 * self.alien_direction, 0)
            a_coords = self.canvas.coords(alien)
            if a_coords[2] >= 600 or a_coords[0] <= 0:
                move_down = True

        if move_down:
            self.alien_direction *= -1
            for alien in self.aliens:
                self.canvas.move(alien, 0, 20)
                if self.canvas.coords(alien)[3] >= 560:
                    self.game_over("Aliens reached the bottom!")
                    return

        if not self.aliens:
            self.game_over("You Win!")
            return

        # Alien shooting
        if random.random() < 0.05 and self.aliens:
            shooter = random.choice(self.aliens)
            s_coords = self.canvas.coords(shooter)
            ab = self.canvas.create_rectangle(s_coords[0]+15, s_coords[3], s_coords[0]+25, s_coords[3]+10, fill="white", tags="alien_bullet")
            self.alien_bullets.append(ab)

        for ab in self.alien_bullets[:]:
            self.canvas.move(ab, 0, 7)
            ab_coords = self.canvas.coords(ab)
            if ab_coords[1] > 600:
                self.canvas.delete(ab)
                self.alien_bullets.remove(ab)
                continue
            
            hit = self.canvas.find_overlapping(*ab_coords)
            if self.player in hit:
                self.game_over("You got hit!")
                return

        self.after(50, self.game_loop)

    def game_over(self, msg):
        self.game_running = False
        self.start_btn.configure(state="normal", text="Restart Game")
        tk.messagebox.showinfo("Game Over", msg)

if __name__ == "__main__":
    app = SpaceInvadersApp()
    app.mainloop()
