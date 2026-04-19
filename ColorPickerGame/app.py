import customtkinter as ctk
import random
import tkinter as tk
import math

ctk.set_appearance_mode("dark")

class ColorPickerGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Color Match - Pro")
        try:
            self.icon_img = tk.PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass
        self.geometry("600x650")

        self.target_rgb = (0, 0, 0)
        self.user_rgb = [128, 128, 128]
        self.score = 0
        self.total_attempts = 0

        self.setup_ui()
        self.new_round()

    def setup_ui(self):
        self.label_title = ctk.CTkLabel(self, text="Color Match", font=("Arial", 32, "bold"))
        self.label_title.pack(pady=20)

        self.display_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.display_frame.pack(pady=10)

        # Target Color
        self.target_box = ctk.CTkFrame(self.display_frame, width=200, height=150, corner_radius=10)
        self.target_box.grid(row=0, column=0, padx=20)
        ctk.CTkLabel(self.target_box, text="TARGET", font=("Arial", 16, "bold"), text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        # User Color
        self.user_box = ctk.CTkFrame(self.display_frame, width=200, height=150, corner_radius=10)
        self.user_box.grid(row=0, column=1, padx=20)
        ctk.CTkLabel(self.user_box, text="YOUR GUESS", font=("Arial", 16, "bold"), text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        # Sliders
        self.slider_frame = ctk.CTkFrame(self)
        self.slider_frame.pack(pady=30, padx=50, fill="x")

        # Red Slider
        ctk.CTkLabel(self.slider_frame, text="R", text_color="#ff4444", font=("Arial", 18, "bold")).grid(row=0, column=0, padx=10)
        self.r_slider = ctk.CTkSlider(self.slider_frame, from_=0, to=255, command=self.update_user_color, button_color="#ff4444")
        self.r_slider.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.r_val_label = ctk.CTkLabel(self.slider_frame, text="128")
        self.r_val_label.grid(row=0, column=2, padx=10)

        # Green Slider
        ctk.CTkLabel(self.slider_frame, text="G", text_color="#44ff44", font=("Arial", 18, "bold")).grid(row=1, column=0, padx=10)
        self.g_slider = ctk.CTkSlider(self.slider_frame, from_=0, to=255, command=self.update_user_color, button_color="#44ff44")
        self.g_slider.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        self.g_val_label = ctk.CTkLabel(self.slider_frame, text="128")
        self.g_val_label.grid(row=1, column=2, padx=10)

        # Blue Slider
        ctk.CTkLabel(self.slider_frame, text="B", text_color="#4444ff", font=("Arial", 18, "bold")).grid(row=2, column=0, padx=10)
        self.b_slider = ctk.CTkSlider(self.slider_frame, from_=0, to=255, command=self.update_user_color, button_color="#4444ff")
        self.b_slider.grid(row=2, column=1, sticky="ew", padx=10, pady=10)
        self.b_val_label = ctk.CTkLabel(self.slider_frame, text="128")
        self.b_val_label.grid(row=2, column=2, padx=10)

        self.slider_frame.columnconfigure(1, weight=1)

        self.btn_submit = ctk.CTkButton(self, text="CHECK MATCH", command=self.check_match, 
                                       font=("Arial", 20, "bold"), height=50)
        self.btn_submit.pack(pady=10)

        self.label_score = ctk.CTkLabel(self, text="Total Score: 0", font=("Arial", 18))
        self.label_score.pack(pady=10)

        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 16))
        self.label_feedback.pack(pady=10)

    def rgb_to_hex(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

    def update_user_color(self, _=None):
        r = int(self.r_slider.get())
        g = int(self.g_slider.get())
        b = int(self.b_slider.get())
        self.user_rgb = [r, g, b]
        
        hex_color = self.rgb_to_hex(self.user_rgb)
        self.user_box.configure(fg_color=hex_color)
        
        self.r_val_label.configure(text=str(r))
        self.g_val_label.configure(text=str(g))
        self.b_val_label.configure(text=str(b))

    def new_round(self):
        self.target_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.target_box.configure(fg_color=self.rgb_to_hex(self.target_rgb))
        
        # Reset sliders to middle or random
        for s in [self.r_slider, self.g_slider, self.b_slider]:
            s.set(128)
        self.update_user_color()
        self.label_feedback.configure(text="")

    def check_match(self):
        # Calculate Euclidean distance in RGB space
        dist = math.sqrt(
            (self.target_rgb[0] - self.user_rgb[0])**2 +
            (self.target_rgb[1] - self.user_rgb[1])**2 +
            (self.target_rgb[2] - self.user_rgb[2])**2
        )
        
        # Max distance is sqrt(255^2 * 3) ≈ 441.67
        max_dist = 441.67
        accuracy = max(0, 100 - (dist / max_dist * 100))
        
        points = int(accuracy)
        self.score += points
        self.total_attempts += 1
        
        self.label_score.configure(text=f"Total Score: {self.score}")
        
        msg = f"Accuracy: {accuracy:.1f}%\nPoints: +{points}"
        if accuracy > 95:
            self.label_feedback.configure(text=f"PERFECT! {msg}", text_color="gold")
        elif accuracy > 85:
            self.label_feedback.configure(text=f"Great Match! {msg}", text_color="green")
        elif accuracy > 70:
            self.label_feedback.configure(text=f"Good Try! {msg}", text_color="yellow")
        else:
            self.label_feedback.configure(text=f"Not Close Enough! {msg}", text_color="red")

        self.after(2000, self.new_round)

if __name__ == "__main__":
    app = ColorPickerGame()
    app.mainloop()
