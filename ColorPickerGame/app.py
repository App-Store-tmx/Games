import customtkinter as ctk
import random

class ColorPickerGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Color Picker Game")
        self.geometry("500x400")
        ctk.set_appearance_mode("dark")

        self.target_color = ""
        self.options = []

        self.label = ctk.CTkLabel(self, text="Which color is this?", font=("Arial", 20))
        self.label.pack(pady=20)

        self.color_display = ctk.CTkFrame(self, width=200, height=100)
        self.color_display.pack(pady=10)

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=20)

        self.buttons = []
        for i in range(3):
            btn = ctk.CTkButton(self.btn_frame, text="", command=lambda i=i: self.check_answer(i))
            btn.grid(row=0, column=i, padx=10)
            self.buttons.append(btn)

        self.result_label = ctk.CTkLabel(self, text="", font=("Arial", 16))
        self.result_label.pack(pady=10)

        self.new_game()

    def generate_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def new_game(self):
        self.target_color = self.generate_color()
        self.color_display.configure(fg_color=self.target_color)
        
        self.options = [self.target_color, self.generate_color(), self.generate_color()]
        random.shuffle(self.options)

        for i in range(3):
            self.buttons[i].configure(text=self.options[i])
        
        self.result_label.configure(text="")

    def check_answer(self, i):
        if self.options[i] == self.target_color:
            self.result_label.configure(text="Correct! Next color...", text_color="green")
            self.after(1000, self.new_game)
        else:
            self.result_label.configure(text="Wrong! Try again.", text_color="red")

if __name__ == "__main__":
    app = ColorPickerGame()
    app.mainloop()
