import customtkinter as ctk
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class WordScrambleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Word Scramble")
        self.geometry("400x400")

        self.words = ["PYTHON", "TERMUX", "LINUX", "ANDROID", "GAME", "CODE", "PROGRAM", "WIDGET", "MOBILE", "DESKTOP"]
        self.current_word = ""
        self.scrambled_word = ""
        self.score = 0

        self.setup_ui()
        self.next_word()

    def setup_ui(self):
        self.label_score = ctk.CTkLabel(self, text="Score: 0", font=("Arial", 16))
        self.label_score.pack(pady=10)

        self.label_title = ctk.CTkLabel(self, text="Unscramble this word:", font=("Arial", 18))
        self.label_title.pack(pady=10)

        self.label_word = ctk.CTkLabel(self, text="", font=("Arial", 32, "bold"), text_color="cyan")
        self.label_word.pack(pady=20)

        self.entry_guess = ctk.CTkEntry(self, width=250, font=("Arial", 20), justify="center")
        self.entry_guess.pack(pady=10)
        self.entry_guess.bind("<Return>", lambda e: self.check_guess())

        self.button_submit = ctk.CTkButton(self, text="Submit", command=self.check_guess)
        self.button_submit.pack(pady=20)

        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.label_feedback.pack(pady=10)

        self.button_skip = ctk.CTkButton(self, text="Skip", fg_color="gray", command=self.next_word)
        self.button_skip.pack(pady=5)

    def next_word(self):
        self.current_word = random.choice(self.words)
        word_list = list(self.current_word)
        random.shuffle(word_list)
        self.scrambled_word = "".join(word_list)
        
        # Ensure it's actually scrambled
        if self.scrambled_word == self.current_word and len(self.current_word) > 1:
            self.next_word()
            return

        self.label_word.configure(text=self.scrambled_word)
        self.entry_guess.delete(0, 'end')
        self.entry_guess.focus()
        self.label_feedback.configure(text="")

    def check_guess(self):
        guess = self.entry_guess.get().strip().upper()
        if guess == self.current_word:
            self.score += 1
            self.label_score.configure(text=f"Score: {self.score}")
            self.label_feedback.configure(text="Correct!", text_color="green")
            self.after(1000, self.next_word)
        else:
            self.label_feedback.configure(text="Try again!", text_color="red")

if __name__ == "__main__":
    app = WordScrambleApp()
    app.mainloop()
