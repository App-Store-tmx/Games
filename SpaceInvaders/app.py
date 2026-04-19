import customtkinter as ctk
import tkinter as tk
import random
import os

ctk.set_appearance_mode("dark")

class SpaceInvadersApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Space Invaders - Pro")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass
        self.geometry("600x750")
        self.resizable(False, False)

        self.canvas = tk.Canvas(self, width=600, height=600, bg="#050505", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Game State
        self.score = 0
        self.high_score = self.load_high_score()
        self.lives = 3
        self.wave = 1
        self.game_running = False
        self.alien_speed = 2
        self.alien_direction = 1
        
        self.player = None
        self.bullets = []
        self.aliens = []
        self.alien_bullets = []
        self.shields = []
        self.bonus_saucer = None
        
        self.setup_ui()
        self.canvas.bind_all("<Left>", lambda e: self.move_player(-20))
        self.canvas.bind_all("<Right>", lambda e: self.move_player(20))
        self.canvas.bind_all("<space>", lambda e: self.shoot())

    def setup_ui(self):
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(fill="x", padx=20)
        
        self.score_label = ctk.CTkLabel(self.info_frame, text=f"Score: {self.score}", font=("Courier", 18, "bold"))
        self.score_label.pack(side="left", padx=10)
        
        self.high_score_label = ctk.CTkLabel(self.info_frame, text=f"High Score: {self.high_score}", font=("Courier", 18, "bold"))
        self.high_score_label.pack(side="left", expand=True)
        
        self.lives_label = ctk.CTkLabel(self.info_frame, text=f"Lives: {'❤' * self.lives}", font=("Courier", 18, "bold"), text_color="red")
        self.lives_label.pack(side="right", padx=10)

        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(pady=5)
        
        self.start_btn = ctk.CTkButton(self.control_frame, text="START MISSION", command=self.start_game, font=("Courier", 16, "bold"))
        self.start_btn.pack(side="left", padx=10)
        
        self.wave_label = ctk.CTkLabel(self.control_frame, text=f"Wave: {self.wave}", font=("Courier", 16))
        self.wave_label.pack(side="left", padx=10)

    def load_high_score(self):
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                try: return int(f.read())
                except: return 0
        return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))
            self.high_score_label.configure(text=f"High Score: {self.high_score}")

    def start_game(self):
        if self.game_running: return
        self.canvas.delete("all")
        self.aliens = []
        self.bullets = []
        self.alien_bullets = []
        self.shields = []
        self.bonus_saucer = None
        self.score = 0
        self.lives = 3
        self.wave = 1
        self.alien_speed = 2
        self.update_labels()
        
        self.player = self.canvas.create_rectangle(275, 560, 325, 580, fill="#00ff00", outline="#00aa00", width=2)
        self.setup_shields()
        self.setup_aliens()
        self.game_running = True
        self.start_btn.configure(state="disabled")
        self.alien_direction = 1
        self.game_loop()

    def setup_shields(self):
        for i in range(4):
            start_x = 80 + i * 140
            for row in range(3):
                for col in range(5):
                    x1 = start_x + col * 12
                    y1 = 480 + row * 10
                    s = self.canvas.create_rectangle(x1, y1, x1+10, y1+8, fill="#5555ff", tags="shield")
                    self.shields.append({"id": s, "hp": 3})

    def setup_aliens(self):
        rows = min(3 + self.wave // 2, 6)
        cols = min(6 + self.wave // 3, 10)
        for row in range(rows):
            for col in range(cols):
                x1 = col * 50 + 50
                y1 = row * 35 + 50
                colors = ["#ff0000", "#ff7700", "#ffff00", "#00ff00", "#00ffff"]
                alien = self.canvas.create_rectangle(x1, y1, x1+35, y1+25, fill=colors[row % len(colors)], tags="alien")
                self.aliens.append(alien)

    def update_labels(self):
        self.score_label.configure(text=f"Score: {self.score}")
        self.lives_label.configure(text=f"Lives: {'❤' * self.lives}")
        self.wave_label.configure(text=f"Wave: {self.wave}")

    def move_player(self, dx):
        if not self.game_running: return
        coords = self.canvas.coords(self.player)
        if coords[0] + dx >= 0 and coords[2] + dx <= 600:
            self.canvas.move(self.player, dx, 0)

    def shoot(self):
        if not self.game_running: return
        if len(self.bullets) < 2 + (self.wave // 3): # Allow more bullets as wave increases
            p_coords = self.canvas.coords(self.player)
            bullet = self.canvas.create_rectangle(p_coords[0]+22, p_coords[1]-10, p_coords[0]+28, p_coords[1], fill="white", tags="bullet")
            self.bullets.append(bullet)

    def spawn_saucer(self):
        if not self.bonus_saucer and random.random() < 0.005:
            self.bonus_saucer = self.canvas.create_oval(-50, 20, 0, 40, fill="#ff00ff", outline="white", tags="saucer")

    def move_saucer(self):
        if self.bonus_saucer:
            self.canvas.move(self.bonus_saucer, 4, 0)
            coords = self.canvas.coords(self.bonus_saucer)
            if coords[0] > 600:
                self.canvas.delete(self.bonus_saucer)
                self.bonus_saucer = None

    def handle_collisions(self):
        # Player bullets
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, -12)
            b_coords = self.canvas.coords(bullet)
            if b_coords[1] < 0:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
                continue
            
            hit = self.canvas.find_overlapping(*b_coords)
            hit_something = False
            for item in hit:
                if item in self.aliens:
                    self.canvas.delete(item)
                    self.aliens.remove(item)
                    self.score += 10 * self.wave
                    hit_something = True
                elif item == self.bonus_saucer:
                    self.canvas.delete(item)
                    self.bonus_saucer = None
                    self.score += random.choice([50, 100, 150]) * self.wave
                    hit_something = True
                elif any(s["id"] == item for s in self.shields):
                    self.damage_shield(item)
                    hit_something = True
                
                if hit_something:
                    self.canvas.delete(bullet)
                    self.bullets.remove(bullet)
                    self.update_labels()
                    break

        # Alien bullets
        for ab in self.alien_bullets[:]:
            self.canvas.move(ab, 0, 6 + (self.wave * 0.5))
            ab_coords = self.canvas.coords(ab)
            if ab_coords[1] > 600:
                self.canvas.delete(ab)
                self.alien_bullets.remove(ab)
                continue
            
            hit = self.canvas.find_overlapping(*ab_coords)
            for item in hit:
                if item == self.player:
                    self.canvas.delete(ab)
                    self.alien_bullets.remove(ab)
                    self.player_hit()
                    return
                elif any(s["id"] == item for s in self.shields):
                    self.damage_shield(item)
                    self.canvas.delete(ab)
                    self.alien_bullets.remove(ab)
                    break

    def damage_shield(self, shield_id):
        for s in self.shields:
            if s["id"] == shield_id:
                s["hp"] -= 1
                if s["hp"] <= 0:
                    self.canvas.delete(shield_id)
                    self.shields.remove(s)
                else:
                    colors = {2: "#3333aa", 1: "#111155"}
                    self.canvas.itemconfig(shield_id, fill=colors[s["hp"]])
                break

    def player_hit(self):
        self.lives -= 1
        self.update_labels()
        if self.lives <= 0:
            self.game_over("MISSION FAILED: Earth is doomed!")
        else:
            # Brief invincibility or just clear bullets
            for ab in self.alien_bullets: self.canvas.delete(ab)
            self.alien_bullets = []

    def game_loop(self):
        if not self.game_running: return

        # Move aliens
        move_down = False
        for alien in self.aliens:
            self.canvas.move(alien, self.alien_speed * self.alien_direction, 0)
            a_coords = self.canvas.coords(alien)
            if a_coords[2] >= 600 or a_coords[0] <= 0:
                move_down = True

        if move_down:
            self.alien_direction *= -1
            for alien in self.aliens:
                self.canvas.move(alien, 0, 15)
                if self.canvas.coords(alien)[3] >= 560:
                    self.game_over("ALIENS LANDED!")
                    return

        # Alien shooting
        shoot_chance = 0.02 + (self.wave * 0.01)
        if random.random() < shoot_chance and self.aliens:
            shooter = random.choice(self.aliens)
            s_coords = self.canvas.coords(shooter)
            ab = self.canvas.create_rectangle(s_coords[0]+15, s_coords[3], s_coords[0]+20, s_coords[3]+12, fill="red", tags="alien_bullet")
            self.alien_bullets.append(ab)

        self.spawn_saucer()
        self.move_saucer()
        self.handle_collisions()

        if not self.aliens:
            self.next_wave()
            return

        self.after(30, self.game_loop)

    def next_wave(self):
        self.wave += 1
        self.alien_speed += 0.5
        # Clear bullets
        for b in self.bullets: self.canvas.delete(b)
        for ab in self.alien_bullets: self.canvas.delete(ab)
        self.bullets = []
        self.alien_bullets = []
        self.setup_aliens()
        self.update_labels()
        self.after(1000, self.game_loop)

    def game_over(self, msg):
        self.game_running = False
        self.save_high_score()
        self.start_btn.configure(state="normal", text="RETRY MISSION")
        tk.messagebox.showinfo("Game Over", f"{msg}\nFinal Score: {self.score}")

if __name__ == "__main__":
    app = SpaceInvadersApp()
    app.mainloop()
