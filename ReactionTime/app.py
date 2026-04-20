import customtkinter as ctk
import time
import random
import tkinter as tk
VERSION = "1.0.0"

ctk.set_appearance_mode("dark")

class ReactionTimeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Reaction Time - Elite")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass
        self.geometry("500x600")

        self.state = "WAITING"
        self.start_time = 0
        self.history = []
        
        self.setup_ui()

    def setup_ui(self):
        self.label_title = ctk.CTkLabel(self, text="Reaction Test", font=("Arial", 32, "bold"))
        self.label_title.pack(pady=20)

        # Main Interaction Area
        self.main_frame = ctk.CTkFrame(self, width=400, height=250, corner_radius=20, fg_color="#333333")
        self.main_frame.pack(pady=20, padx=20)
        self.main_frame.pack_propagate(False)

        self.status_label = ctk.CTkLabel(self.main_frame, text="Press START to begin", font=("Arial", 22))
        self.status_label.pack(expand=True)

        self.btn_action = ctk.CTkButton(self, text="START", command=self.handle_click, 
                                       width=250, height=60, font=("Arial", 20, "bold"))
        self.btn_action.pack(pady=10)

        # Stats Area
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(pady=20, fill="both", padx=40, expand=True)

        self.label_avg = ctk.CTkLabel(self.stats_frame, text="Average: -- ms", font=("Arial", 18, "bold"), text_color="cyan")
        self.label_avg.pack(pady=10)

        self.label_history_title = ctk.CTkLabel(self.stats_frame, text="Last 5 attempts:", font=("Arial", 14))
        self.label_history_title.pack()

        self.history_list = ctk.CTkLabel(self.stats_frame, text="No data yet", font=("Courier", 16))
        self.history_list.pack(pady=10)

    def handle_click(self):
        if self.state == "WAITING":
            self.start_preparation()
        elif self.state == "READY":
            self.too_early()
        elif self.state == "GO":
            self.record_reaction()

    def start_preparation(self):
        self.state = "READY"
        self.main_frame.configure(fg_color="#cc9900") # Yellow/Orange for "Wait"
        self.status_label.configure(text="Wait for GREEN...", text_color="black")
        self.btn_action.configure(text="WAIT", state="disabled", fg_color="gray")
        
        # Random delay between 2 and 5 seconds
        delay = random.uniform(2, 5)
        self.trigger_id = self.after(int(delay * 1000), self.trigger_go)

    def trigger_go(self):
        if self.state == "READY":
            self.state = "GO"
            self.start_time = time.time()
            self.main_frame.configure(fg_color="#2eb82e") # Green for "GO"
            self.status_label.configure(text="CLICK NOW!", text_color="white")
            self.btn_action.configure(text="CLICK!", state="normal", fg_color="#1f7a1f")

    def too_early(self):
        self.after_cancel(self.trigger_id)
        self.state = "WAITING"
        self.main_frame.configure(fg_color="#b30000") # Red for "Too Early"
        self.status_label.configure(text="TOO EARLY!", text_color="white")
        self.btn_action.configure(text="TRY AGAIN", state="normal", fg_color="#3a7ebf")

    def record_reaction(self):
        reaction_time = int((time.time() - self.start_time) * 1000)
        self.state = "WAITING"
        
        self.history.insert(0, reaction_time)
        if len(self.history) > 5:
            self.history.pop()
            
        self.update_stats()
        
        self.main_frame.configure(fg_color="#333333")
        self.status_label.configure(text=f"{reaction_time} ms", text_color="white")
        self.btn_action.configure(text="PLAY AGAIN", fg_color="#3a7ebf")

    def update_stats(self):
        # Update History List
        history_text = "\n".join([f"#{i+1}: {t} ms" for i, t in enumerate(self.history)])
        self.history_list.configure(text=history_text)
        
        # Update Average
        avg = sum(self.history) // len(self.history)
        self.label_avg.configure(text=f"Average: {avg} ms")

if __name__ == "__main__":
    app = ReactionTimeApp()
    app.mainloop()
