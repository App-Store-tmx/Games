import customtkinter as ctk
import time
import random

class ReactionTime(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Reaction Time Test")
        self.geometry("400x400")
        ctk.set_appearance_mode("dark")

        self.state = "WAITING"
        self.start_time = 0

        self.label = ctk.CTkLabel(self, text="Press the button to start", font=("Arial", 20))
        self.label.pack(expand=True)

        self.btn = ctk.CTkButton(self, text="Start", command=self.on_click, width=200, height=100)
        self.btn.pack(pady=50)

    def on_click(self):
        if self.state == "WAITING":
            self.state = "GET_READY"
            self.btn.configure(text="Wait for RED...", fg_color="gray")
            self.label.configure(text="Wait for the background to change!")
            delay = random.uniform(2, 5)
            self.after(int(delay * 1000), self.trigger)
        elif self.state == "GET_READY":
            # Clicked too early
            self.state = "WAITING"
            self.label.configure(text="Too early! Click Start to try again.")
            self.btn.configure(text="Start", fg_color=["#3a7ebf", "#1f538d"])
            self.after_cancel(self.trigger)
        elif self.state == "TRIGGERED":
            reaction = time.time() - self.start_time
            self.state = "WAITING"
            self.label.configure(text=f"Your time: {int(reaction * 1000)}ms")
            self.btn.configure(text="Try Again", fg_color=["#3a7ebf", "#1f538d"])
            self.configure(fg_color=["#242424", "#242424"])

    def trigger(self):
        if self.state == "GET_READY":
            self.state = "TRIGGERED"
            self.start_time = time.time()
            self.btn.configure(text="CLICK NOW!", fg_color="red")
            self.configure(fg_color="red")

if __name__ == "__main__":
    app = ReactionTime()
    app.mainloop()
