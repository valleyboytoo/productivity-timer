import tkinter as tk
from tkinter import ttk
import random
import winsound

class ProductivityTimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Productivity Timer")

        # default values
        self.focus_minutes = 25
        self.break_minutes = 5
        self.remaining_seconds = 0
        self.is_running = False
        self.current_mode = "focus"
        self.timer_id = None
        self.session_count = 0

        self.current_lang = "en"
        self.current_theme = "light"
        self.current_sound = "None"
        self.base_font_size = 12

        # text library
        self.texts = {
            "en": {
                "title": "Productivity Timer",
                "focus_label": "Focus (minutes):",
                "break_label": "Break (minutes):",
                "start": "Start",
                "pause": "Pause",
                "reset": "Reset",
                "mode_focus": "Mode: Focus",
                "mode_break": "Mode: Break",
                "sessions": "Completed focus sessions:",
                "theme": "Theme:",
                "font": "Font size:",
                "language": "Language:",
                "sound": "Sound:",
                "status_ready": "Ready to start.",
                "status_running": "Timer is running.",
                "status_paused": "Timer is paused.",
                "quote_title": "Reminder:"
            },
            "cn": {
                "title": "专注计时器",
                "focus_label": "专注时间（分钟）:",
                "break_label": "休息时间（分钟）:",
                "start": "开始",
                "pause": "暂停",
                "reset": "重置",
                "mode_focus": "模式：专注",
                "mode_break": "模式：休息",
                "sessions": "已完成的专注次数：",
                "theme": "主题：",
                "font": "字体大小：",
                "language": "语言：",
                "sound": "背景音：",
                "status_ready": "可以开始了。",
                "status_running": "计时进行中。",
                "status_paused": "计时已暂停。",
                "quote_title": "提示："
            },
            "kr": {
                "title": "집중 타이머",
                "focus_label": "집중 시간(분):",
                "break_label": "휴식 시간(분):",
                "start": "시작",
                "pause": "일시정지",
                "reset": "초기화",
                "mode_focus": "모드: 집중",
                "mode_break": "모드: 휴식",
                "sessions": "완료한 집중 세션:",
                "theme": "테마:",
                "font": "글꼴 크기:",
                "language": "언어:",
                "sound": "배경음:",
                "status_ready": "시작할 준비가 되었습니다.",
                "status_running": "타이머 작동 중.",
                "status_paused": "타이머 일시정지됨.",
                "quote_title": "알림:"
            }
        }

        # quotes
        self.quotes = {
            "en": [
                "Small steps still move you forward.",
                "Take a breath. You are doing fine.",
                "Progress matters more than perfection."
            ],
            "cn": [
                "一点点前进也算进步。",
                "先深呼吸一下，你已经很努力了。",
                "专注比完美更重要。"
            ],
            "kr": [
                "작은 걸음도 앞으로 나아가는 것입니다.",
                "잠시 숨을 고르세요. 잘하고 있습니다.",
                "완벽보다 진행이 더 중요합니다."
            ]
        }

        # layout
        self.build_ui()
        self.apply_theme()
        self.apply_language()

    def build_ui(self):
        self.main_frame = ttk.Frame(self.master, padding=10)
        self.main_frame.pack(fill="both", expand=True)

        settings = ttk.Frame(self.main_frame)
        settings.pack(fill="x", pady=(0, 10))

        # focus time
        self.focus_label = ttk.Label(settings)
        self.focus_label.grid(row=0, column=0, sticky="w")
        self.focus_entry = ttk.Entry(settings, width=5)
        self.focus_entry.insert(0, "25")
        self.focus_entry.grid(row=0, column=1, padx=10)

        # break time
        self.break_label = ttk.Label(settings)
        self.break_label.grid(row=0, column=2, sticky="w")
        self.break_entry = ttk.Entry(settings, width=5)
        self.break_entry.insert(0, "5")
        self.break_entry.grid(row=0, column=3, padx=10)

        # language
        lang_frame = ttk.Frame(settings)
        lang_frame.grid(row=1, column=0, columnspan=2, pady=8, sticky="w")
        self.lang_label = ttk.Label(lang_frame)
        self.lang_label.pack(side="left")
        self.lang_var = tk.StringVar(value="en")
        self.lang_menu = ttk.Combobox(
            lang_frame, values=["en", "cn", "kr"],
            textvariable=self.lang_var, width=5, state="readonly"
        )
        self.lang_menu.pack(side="left", padx=5)
        self.lang_menu.bind("<<ComboboxSelected>>", self.set_language)

        # theme
        theme_frame = ttk.Frame(settings)
        theme_frame.grid(row=1, column=2, columnspan=2, pady=8, sticky="w")
        self.theme_label = ttk.Label(theme_frame)
        self.theme_label.pack(side="left")
        self.theme_var = tk.StringVar(value="light")
        self.theme_menu = ttk.Combobox(
            theme_frame, values=["light", "dark", "soft"],
            textvariable=self.theme_var, width=7, state="readonly"
        )
        self.theme_menu.pack(side="left", padx=5)
        self.theme_menu.bind("<<ComboboxSelected>>", self.set_theme)

        # Sound Selection
        sound_frame = ttk.Frame(settings)
        sound_frame.grid(row=2, column=0, columnspan=4, pady=5, sticky="w")
        self.sound_label_text = ttk.Label(sound_frame, text="Sound:")
        self.sound_label_text.pack(side="left")
        self.sound_var = tk.StringVar(value="None")
        self.sound_menu = ttk.Combobox(
            sound_frame, values=["None", "Rain", "Coffee", "White Noise"],
            textvariable=self.sound_var, width=12, state="readonly"
        )
        self.sound_menu.pack(side="left", padx=5)
        self.sound_menu.bind("<<ComboboxSelected>>", self.set_sound)

        # font slider setup
        font_frame = ttk.Frame(self.main_frame)
        font_frame.pack(fill="x", pady=5)
        self.font_label = ttk.Label(font_frame)
        self.font_label.pack(side="left")
        self.font_scale = ttk.Scale(
            font_frame, from_=10, to=20, command=self.update_font
        )
        # Note: We do NOT set the value here yet to avoid crashing
        self.font_scale.pack(side="left", padx=10)

        # timer mode
        self.mode_label = ttk.Label(self.main_frame, anchor="center")
        self.mode_label.pack(pady=5)

        # timer display
        self.timer_label = ttk.Label(
            self.main_frame, text="00:00", font=("Arial", 32), anchor="center"
        )
        self.timer_label.pack(pady=5)

        # Buttons
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        self.start_button = ttk.Button(btn_frame, command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=5)
        self.pause_button = ttk.Button(btn_frame, command=self.pause_timer)
        self.pause_button.grid(row=0, column=1, padx=5)
        self.reset_button = ttk.Button(btn_frame, command=self.reset_timer)
        self.reset_button.grid(row=0, column=2, padx=5)

        # status
        self.status_label = ttk.Label(self.main_frame)
        self.status_label.pack(pady=5)

        # sessions
        self.sessions_label = ttk.Label(self.main_frame)
        self.sessions_label.pack()

        # quote
        self.quote_title_label = ttk.Label(self.main_frame)
        self.quote_title_label.pack()
        self.quote_label = ttk.Label(self.main_frame, wraplength=300)
        self.quote_label.pack(pady=5)
        
        # Now that all widgets exist, we can safely set the font scale default
        self.font_scale.set(12)

    # language
    def set_language(self, event=None):
        self.current_lang = self.lang_var.get()
        self.apply_language()

    def apply_language(self):
        t = self.texts[self.current_lang]
        self.master.title(t["title"])
        self.focus_label.config(text=t["focus_label"])
        self.break_label.config(text=t["break_label"])
        self.start_button.config(text=t["start"])
        self.pause_button.config(text=t["pause"])
        self.reset_button.config(text=t["reset"])
        self.lang_label.config(text=t["language"])
        self.theme_label.config(text=t["theme"])
        self.font_label.config(text=t["font"])
        self.quote_title_label.config(text=t["quote_title"])
        self.sound_label_text.config(text=t["sound"])
        self.update_mode_label()
        self.update_session_label()
        self.set_status("status_ready")

    # theme
    def set_theme(self, event=None):
        self.current_theme = self.theme_var.get()
        self.apply_theme()

    def apply_theme(self):
            if self.current_theme == "light":
                bg = "#f5f5f5"
                fg = "#222"
                button_bg = "#e0e0e0" # optional button color
            elif self.current_theme == "dark":
                bg = "#222"
                fg = "#f5f5f5"
                button_bg = "#444"
            else:
                # "Soft" Theme (Old Book Style)
                bg = "#FDF5E6"  # Old Lace (Vintage Paper)
                fg = "#5D4037"  # Warm Brown (Old Ink)
                button_bg = "#E6D0B3" # Tan (Book Binding)
    
            self.master.config(bg=bg)
            style = ttk.Style()
            style.theme_use('clam') # 'clam' allows us to change button colors easily
            
            # Apply colors to generic widgets
            style.configure("TLabel", background=bg, foreground=fg)
            style.configure("TFrame", background=bg)
            style.configure("TButton", background=button_bg, foreground=fg, bordercolor=fg)
            
            # Force update for specific widgets
            for w in self.main_frame.winfo_children():
                if isinstance(w, ttk.Label):
                    w.config(background=bg, foreground=fg)
                # Check for frames inside main_frame (like settings frame)
                elif isinstance(w, ttk.Frame):
                    for child in w.winfo_children():
                        if isinstance(child, ttk.Label):
                            child.config(background=bg, foreground=fg)
    
    # Sound Logic
    def set_sound(self, event=None):
        self.current_sound = self.sound_var.get()
        if self.is_running:
            self.play_bg_sound()
            
    def play_bg_sound(self):
        if self.current_sound == "None":
            winsound.PlaySound(None, winsound.SND_PURGE)
            return
            
        filename = ""
        if self.current_sound == "Rain":
            filename = "rain.wav"
        elif self.current_sound == "Coffee":
            filename = "coffee.wav"
        elif self.current_sound == "White Noise":
            filename = "white_noise.wav"
            
        try:
            winsound.PlaySound(filename, winsound.SND_LOOP | winsound.SND_ASYNC)
        except:
            pass 

    def stop_bg_sound(self):
        winsound.PlaySound(None, winsound.SND_PURGE)

    # font
    def update_font(self, value):
        size = int(float(value))
        font = ("Arial", size)
        big = ("Arial", size + 16)

        # Check if all widgets exist before configuring
        if not hasattr(self, 'sound_label_text') or not hasattr(self, 'quote_label'):
            return

        for w in [
            self.focus_label, self.break_label, self.lang_label, self.theme_label,
            self.font_label, self.mode_label, self.status_label,
            self.sessions_label, self.quote_title_label, self.quote_label,
            self.sound_label_text
        ]:
            w.config(font=font)
        self.timer_label.config(font=big)

    # status
    def set_status(self, key):
        msg = self.texts[self.current_lang][key]
        self.status_label.config(text=msg)

    # mode
    def update_mode_label(self):
        t = self.texts[self.current_lang]
        if self.current_mode == "focus":
            self.mode_label.config(text=t["mode_focus"])
        else:
            self.mode_label.config(text=t["mode_break"])

    # sessions
    def update_session_label(self):
        t = self.texts[self.current_lang]
        self.sessions_label.config(text=f"{t['sessions']} {self.session_count}")

    # timer logic
    def start_timer(self):
        if self.is_running:
            return

        try:
            self.focus_minutes = int(self.focus_entry.get())
            self.break_minutes = int(self.break_entry.get())
        except:
            self.status_label.config(text="Invalid minutes.")
            return

        if self.remaining_seconds == 0:
            if self.current_mode == "focus":
                self.remaining_seconds = self.focus_minutes * 60
            else:
                self.remaining_seconds = self.break_minutes * 60

        self.is_running = True
        self.set_status("status_running")
        self.play_bg_sound()
        self.run_timer()

    def run_timer(self):
        if not self.is_running:
            return

        mins = self.remaining_seconds // 60
        secs = self.remaining_seconds % 60
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

        if self.remaining_seconds == 0:
            self.end_timer()
            return

        self.remaining_seconds -= 1
        self.timer_id = self.master.after(1000, self.run_timer)

    def end_timer(self):
        self.stop_bg_sound()
        self.master.bell()

        if self.current_mode == "focus":
            self.session_count += 1
            self.update_session_label()
            q = random.choice(self.quotes[self.current_lang])
            self.quote_label.config(text=q)
            self.current_mode = "break"
            self.remaining_seconds = self.break_minutes * 60
        else:
            self.current_mode = "focus"
            self.remaining_seconds = self.focus_minutes * 60
            self.quote_label.config(text="")

        self.update_mode_label()
        self.is_running = False
        self.set_status("status_ready")

    def pause_timer(self):
        if not self.is_running:
            return
        self.is_running = False
        self.stop_bg_sound()
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        self.set_status("status_paused")

    def reset_timer(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        self.is_running = False
        self.stop_bg_sound()
        self.remaining_seconds = 0
        self.current_mode = "focus"
        self.update_mode_label()
        self.timer_label.config(text="00:00")
        self.quote_label.config(text="")
        self.set_status("status_ready")


def main():
    root = tk.Tk()
    app = ProductivityTimerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
