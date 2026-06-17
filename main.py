import customtkinter as ctk

class Pomodoro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro")
        self.geometry("450x600")

        self.work_time_s = 60 * 25
        self.break_time_s = 60 * 5
        self.long_break_s = 60 * 20
        
        self.time_left = self.work_time_s
        self.is_running = False
        self.is_break = False

        self.task_title = ctk.CTkEntry(self, placeholder_text="Zadanie... ", font=("Helvetica", 18))
        self.task_title.pack(pady=40, padx=20, fill="x")

        self.header = ctk.CTkLabel(self, text="Zadanie: ", font=("Helvetica", 42, "bold"), text_color="#FFFFFF")
        self.header.pack(pady=20)

        self.progressbar = ctk.CTkProgressBar(self, width=350, height=15)
        self.progressbar.pack(pady=30)
        self.progressbar.set(1.0)

        self.time_label = ctk.CTkLabel(self, text="25:00", font=("Helvetica", 100, "bold"), text_color="#FFFFFF")
        self.time_label.pack(pady=20)

        self.dots_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.dots_frame.pack(pady=20)
        self.dots = []
        
        for i in range(4):
            dot = ctk.CTkFrame(self.dots_frame, width=25, height=25, corner_radius=12, fg_color="gray")
            dot.pack(side="left", padx=8)
            self.dots.append(dot)
            
        self.current_cycle = 0

        self.start_button = ctk.CTkButton(
            self, 
            text="TRYB SKUPIENIA", 
            font=("Helvetica", 20, "bold"), 
            height=50,
            command=self.start_action
        )
        self.start_button.pack(pady=30)

    def start_action(self):
        self.get_title()
        self.start_timer()
        self.task_title.pack_forget()
        # Zmiana UX: wyłączamy przycisk, żeby nie dało się go przeklikać
        self.start_button.configure(state="disabled", text="SKUPIENIE TRWA...")

    def get_progress_color(self, progress):
        if self.is_break: return "#2ECC71"
        if progress > 0.5: return "#3B8ED0"
        if progress > 0.2: return "#E67E22"
        return "#E74C3C"

    def get_title(self):
        string_header = self.task_title.get()
        if string_header:
            self.header.configure(text=string_header.strip())

    def mark_cycle_done(self):
        if self.current_cycle < 4:
            self.dots[self.current_cycle].configure(fg_color="#FF6347") 
            self.current_cycle += 1
            
        if self.current_cycle == 4:
            self.after(5000, self.reset_dots)
            self.current_cycle = 0

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.update_timer()

    def update_timer(self):
        if self.is_running:
            if self.time_left > 0:
                mins, secs = divmod(self.time_left, 60)
                total = self.break_time_s if self.is_break else self.work_time_s
                progress = self.time_left / total

                self.time_label.configure(text=f"{mins:02d}:{secs:02d}")
                self.progressbar.set(progress)
                self.progressbar.configure(progress_color=self.get_progress_color(progress))

                self.time_left -= 1
                self.after(1000, self.update_timer)
            else:
                self.switch_mode()

    def reset_dots(self):
        for dot in self.dots:
            dot.configure(fg_color="gray")

    def show_modern_alert(self, title, message, color="#2ECC71"):
        alert = ctk.CTkToplevel(self)
        alert.overrideredirect(True)
        alert.attributes("-topmost", True)
        alert.attributes("-alpha", 0.95)
        alert.configure(fg_color="#1a1a1a")

        sw = alert.winfo_screenwidth()
        sh = alert.winfo_screenheight()
        alert.geometry(f"350x120+{sw-370}+{sh-150}")

        side_bar = ctk.CTkFrame(alert, width=8, fg_color=color, corner_radius=0)
        side_bar.pack(side="left", fill="y")

        ctk.CTkLabel(alert, text=title, font=("Helvetica", 16, "bold"), text_color=color).pack(pady=(20, 0), padx=20, anchor="w")
        ctk.CTkLabel(alert, text=message, font=("Helvetica", 13), text_color="white").pack(pady=(5, 20), padx=20, anchor="w")

        alert.lift()
        alert.after(5000, alert.destroy)
        self.bell()

    def switch_mode(self):
        if not self.is_break:
            self.is_break = True
            self.mark_cycle_done()
            
            if self.current_cycle == 0:
                self.time_left = self.long_break_s
                self.show_modern_alert("DŁUGA PRZERWA! 🏆", "Zasłużyłeś! 20 minut odpoczynku.", "#FFD700")
                self.header.configure(text="DŁUGA PRZERWA 🔋", text_color="#FFD700")
            else:
                self.time_left = self.break_time_s
                self.show_modern_alert("PRZERWA! 🍅", "5 minut dla Ciebie.", "#2ECC71")
                self.header.configure(text="CHWILA ODDECHU ☕", text_color="#2ECC71")
            
            self.configure(fg_color="#1e2a1e") 
        else:
            self.is_break = False
            self.time_left = self.work_time_s
            self.configure(fg_color="#121212")
            self.header.configure(text="DO ROBOTY! 💻", text_color="#FFFFFF")
            self.show_modern_alert("KONIEC PRZERWY", "Wracamy do skupienia!", "#3B8ED0")

        self.update_timer()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = Pomodoro()
    app.mainloop()
