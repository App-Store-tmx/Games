import customtkinter as ctk
import tkinter as tk
import random
from tkinter import messagebox

class SnakeGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Snake Game")
        self.geometry("400x450")
        ctk.set_appearance_mode("dark")

        self.score = 0
        self.direction = "Right"
        self.snake = [(20, 20), (20, 10), (20, 0)]
        self.food = (100, 100)
        self.running = True

        self.score_label = ctk.CTkLabel(self, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack(pady=10)

        self.canvas = tk.Canvas(self, bg="black", width=380, height=340, highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        self.bind("<KeyPress>", self.change_direction)
        
        self.spawn_food()
        self.update_game()

    def spawn_food(self):
        x = random.randint(0, 18) * 20
        y = random.randint(0, 16) * 20
        self.food = (x, y)

    def change_direction(self, event):
        new_dir = event.keysym
        all_dirs = {"Up", "Down", "Left", "Right"}
        opposites = {("Up", "Down"), ("Down", "Up"), ("Left", "Right"), ("Right", "Left")}
        
        if new_dir in all_dirs and (self.direction, new_dir) not in opposites:
            self.direction = new_dir

    def update_game(self):
        if not self.running:
            return

        head_x, head_y = self.snake[0]
        if self.direction == "Up": head_y -= 20
        elif self.direction == "Down": head_y += 20
        elif self.direction == "Left": head_x -= 20
        elif self.direction == "Right": head_x += 20

        new_head = (head_x, head_y)

        # Collision Check
        if (head_x < 0 or head_x >= 380 or head_y < 0 or head_y >= 340 or
            new_head in self.snake):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # Food Check
        if new_head == self.food:
            self.score += 10
            self.score_label.configure(text=f"Score: {self.score}")
            self.spawn_food()
        else:
            self.snake.pop()

        self.draw()
        self.after(150, self.update_game)

    def draw(self):
        self.canvas.delete("all")
        # Draw Food
        self.canvas.create_oval(self.food[0], self.food[1], self.food[0]+20, self.food[1]+20, fill="red")
        # Draw Snake
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x+20, y+20, fill="green", outline="white")

    def game_over(self):
        self.running = False
        messagebox.showinfo("Game Over", f"Final Score: {self.score}")
        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.direction = "Right"
        self.snake = [(20, 20), (20, 10), (20, 0)]
        self.running = True
        self.score_label.configure(text=f"Score: {self.score}")
        self.spawn_food()
        self.update_game()

if __name__ == "__main__":
    app = SnakeGame()
    app.mainloop()
