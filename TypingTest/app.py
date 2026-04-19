import customtkinter as ctk
import time
import random
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TypingTestApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Typing Test")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            # Fallback if icon.png is missing or loading fails
            pass
        self.geometry("600x400")

        self.sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "Programming is the art of telling another human what one wants the computer to do.",
            "CustomTkinter is a great library for creating modern looking GUIs in Python.",
            "Termux provides a powerful Linux environment on Android devices.",
            "Practice makes perfect when it comes to improving your typing speed."
        ]

        self.target_sentence = ""
        self.start_time = 0
        self.running = False

        self.setup_ui()
        self.new_test()

    def setup_ui(self):
        self.label_title = ctk.CTkLabel(self, text="Typing Test", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=20)

        self.label_sentence = ctk.CTkLabel(self, text="", font=("Arial", 16), wraplength=500)
        self.label_sentence.pack(pady=20)

        self.entry_input = ctk.CTkEntry(self, width=500, font=("Arial", 14))
        self.entry_input.pack(pady=10)
        self.entry_input.bind("<KeyRelease>", self.check_typing)

        self.label_results = ctk.CTkLabel(self, text="WPM: 0 | Accuracy: 0%", font=("Arial", 14))
        self.label_results.pack(pady=20)

        self.button_restart = ctk.CTkButton(self, text="Restart", command=self.new_test)
        self.button_restart.pack(pady=10)

    def new_test(self):
        self.target_sentence = random.choice(self.sentences)
        self.label_sentence.configure(text=self.target_sentence)
        self.entry_input.delete(0, 'end')
        self.entry_input.focus()
        self.start_time = 0
        self.running = False
        self.label_results.configure(text="WPM: 0 | Accuracy: 0%")

    def check_typing(self, event):
        if not self.running:
            self.start_time = time.time()
            self.running = True

        current_input = self.entry_input.get()
        
        if current_input == self.target_sentence:
            self.end_test()
        
        # Color feedback
        if self.target_sentence.startswith(current_input):
            self.entry_input.configure(fg_color="transparent")
        else:
            self.entry_input.configure(fg_color="#552222")

    def end_test(self):
        end_time = time.time()
        time_taken = end_time - self.start_time
        
        words = len(self.target_sentence.split())
        wpm = round((words / time_taken) * 60)
        
        accuracy = 100 # In this simple version, they must match exactly to finish
        
        self.label_results.configure(text=f"WPM: {wpm} | Accuracy: {accuracy}%")
        self.running = False
        self.entry_input.unbind("<KeyRelease>")
        # Re-bind after a delay if needed, or just let them click restart
        
if __name__ == "__main__":
    app = TypingTestApp()
    app.mainloop()
