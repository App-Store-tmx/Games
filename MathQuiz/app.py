import customtkinter as ctk
import random
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MathQuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Math Quiz")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            # Fallback if icon.png is missing or loading fails
            pass
        self.geometry("400x350")

        self.score = 0
        self.question_count = 0
        self.current_answer = 0

        self.setup_ui()
        self.next_question()

    def setup_ui(self):
        self.label_score = ctk.CTkLabel(self, text="Score: 0", font=("Arial", 16))
        self.label_score.pack(pady=10)

        self.label_question = ctk.CTkLabel(self, text="", font=("Arial", 28, "bold"))
        self.label_question.pack(pady=30)

        self.entry_answer = ctk.CTkEntry(self, width=200, font=("Arial", 20), justify="center")
        self.entry_answer.pack(pady=10)
        self.entry_answer.bind("<Return>", lambda e: self.check_answer())

        self.button_submit = ctk.CTkButton(self, text="Submit", command=self.check_answer)
        self.button_submit.pack(pady=20)

        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.label_feedback.pack(pady=10)

    def next_question(self):
        ops = ['+', '-', '*']
        op = random.choice(ops)
        
        if op == '+':
            num1 = random.randint(1, 50)
            num2 = random.randint(1, 50)
            self.current_answer = num1 + num2
        elif op == '-':
            num1 = random.randint(1, 50)
            num2 = random.randint(1, num1)
            self.current_answer = num1 - num2
        else: # '*'
            num1 = random.randint(1, 12)
            num2 = random.randint(1, 12)
            self.current_answer = num1 * num2

        self.label_question.configure(text=f"{num1} {op} {num2} = ?")
        self.entry_answer.delete(0, 'end')
        self.entry_answer.focus()

    def check_answer(self):
        try:
            user_ans = int(self.entry_answer.get())
            if user_ans == self.current_answer:
                self.score += 1
                self.label_feedback.configure(text="Correct!", text_color="green")
            else:
                self.label_feedback.configure(text=f"Wrong! Answer was {self.current_answer}", text_color="red")
            
            self.label_score.configure(text=f"Score: {self.score}")
            self.next_question()
        except ValueError:
            self.label_feedback.configure(text="Please enter a number", text_color="yellow")

if __name__ == "__main__":
    app = MathQuizApp()
    app.mainloop()
