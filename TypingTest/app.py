import customtkinter as ctk
import time
import random
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TypingTestApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Typing Test - Master")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass
        self.geometry("700x550")

        self.categories = {
            "Programming": [
                "def hello_world(): print('Hello, World!')",
                "for i in range(10): if i % 2 == 0: continue",
                "const express = require('express'); const app = express();",
                "public static void main(String[] args) { System.out.println('Java'); }",
                "while (alive) { code(); sleep(); eat(); repeat(); }"
            ],
            "Literature": [
                "It was the best of times, it was the worst of times.",
                "To be, or not to be, that is the question.",
                "Call me Ishmael. Some years ago, never mind how long precisely.",
                "All animals are equal, but some animals are more equal than others.",
                "In a hole in the ground there lived a hobbit."
            ],
            "Famous Quotes": [
                "I think, therefore I am.",
                "The only thing we have to fear is fear itself.",
                "That's one small step for man, one giant leap for mankind.",
                "Spread love everywhere you go. Let no one ever come to you without leaving happier.",
                "Life is what happens when you're busy making other plans."
            ]
        }

        self.target_sentence = ""
        self.start_time = 0
        self.running = False
        self.total_chars = 0
        self.mistakes = 0

        self.setup_ui()
        self.change_category("Programming")

    def setup_ui(self):
        self.label_title = ctk.CTkLabel(self, text="Typing Test", font=("Arial", 28, "bold"))
        self.label_title.pack(pady=20)

        self.cat_frame = ctk.CTkFrame(self)
        self.cat_frame.pack(pady=10)
        
        for cat in self.categories.keys():
            btn = ctk.CTkButton(self.cat_frame, text=cat, width=120, command=lambda c=cat: self.change_category(c))
            btn.pack(side="left", padx=5)

        self.text_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.text_frame.pack(pady=20, padx=20, fill="both")

        # Display area for target text with highlighting
        self.display_text = tk.Text(self.text_frame, font=("Courier", 18), height=4, 
                                   bg="#2b2b2b", fg="white", insertofftime=0, 
                                   relief="flat", padx=10, pady=10)
        self.display_text.pack(fill="both")
        self.display_text.tag_config("correct", foreground="#00ff00")
        self.display_text.tag_config("wrong", foreground="#ff0000", background="#440000")
        self.display_text.configure(state="disabled")

        self.entry_input = ctk.CTkEntry(self, width=600, font=("Courier", 16), placeholder_text="Start typing here...")
        self.entry_input.pack(pady=10)
        self.entry_input.bind("<KeyRelease>", self.check_typing)

        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(pady=20, fill="x", padx=50)

        self.label_wpm = ctk.CTkLabel(self.stats_frame, text="WPM: 0", font=("Arial", 18, "bold"))
        self.label_wpm.pack(side="left", expand=True)

        self.label_acc = ctk.CTkLabel(self.stats_frame, text="Accuracy: 100%", font=("Arial", 18, "bold"))
        self.label_acc.pack(side="left", expand=True)

        self.button_restart = ctk.CTkButton(self, text="NEW TEST", command=self.new_test, font=("Arial", 16, "bold"), fg_color="green", hover_color="#006400")
        self.button_restart.pack(pady=10)

    def change_category(self, cat):
        self.current_category = cat
        self.new_test()

    def new_test(self):
        self.target_sentence = random.choice(self.categories[self.current_category])
        self.display_text.configure(state="normal")
        self.display_text.delete("1.0", "end")
        self.display_text.insert("1.0", self.target_sentence)
        self.display_text.configure(state="disabled")
        
        self.entry_input.delete(0, 'end')
        self.entry_input.configure(state="normal")
        self.entry_input.focus()
        
        self.start_time = 0
        self.running = False
        self.mistakes = 0
        self.total_chars = 0
        self.label_wpm.configure(text="WPM: 0")
        self.label_acc.configure(text="Accuracy: 100%")

    def check_typing(self, event):
        if event.keysym in ["Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R"]:
            return

        if not self.running and self.entry_input.get():
            self.start_time = time.time()
            self.running = True

        current_input = self.entry_input.get()
        self.total_chars = len(current_input)
        
        # Highlight logic
        self.display_text.configure(state="normal")
        self.display_text.tag_remove("correct", "1.0", "end")
        self.display_text.tag_remove("wrong", "1.0", "end")
        
        self.mistakes = 0
        for i in range(len(current_input)):
            if i < len(self.target_sentence):
                if current_input[i] == self.target_sentence[i]:
                    self.display_text.tag_add("correct", f"1.{i}", f"1.{i+1}")
                else:
                    self.display_text.tag_add("wrong", f"1.{i}", f"1.{i+1}")
                    self.mistakes += 1
        
        self.display_text.configure(state="disabled")

        # Live stats
        if self.running:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                words = len(current_input) / 5
                wpm = round((words / elapsed) * 60)
                self.label_wpm.configure(text=f"WPM: {wpm}")
                
                acc = 100
                if len(current_input) > 0:
                    acc = round(((len(current_input) - self.mistakes) / len(current_input)) * 100)
                self.label_acc.configure(text=f"Accuracy: {acc}%")

        if current_input == self.target_sentence:
            self.end_test()

    def end_test(self):
        self.running = False
        self.entry_input.configure(state="disabled")
        tk.messagebox.showinfo("Test Complete", f"Great job!\n{self.label_wpm.cget('text')}\n{self.label_acc.cget('text')}")

if __name__ == "__main__":
    app = TypingTestApp()
    app.mainloop()
