
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font as tkfont
import json, csv, time, math, os

# optional audio libs (only winsound)
try:
    import winsound
    HAVE_WINSOUND = True
except Exception:
    HAVE_WINSOUND = False

APP_STATE_FILE = "productivity_timer_state.json"

# Localization (en, ko, cn)
LOCALES = {
    "en": {
        "title": "Focus+ Timer",
        "start": "Start", "pause": "Pause", "reset": "Reset",
        "focus_min": "Focus (min)", "break_min": "Break (min)",
        "quick_25_5": "Quick 25/5", "quick_50_10": "Quick 50/10",
        "mute": "Mute", "settings": "Settings", "language": "Language",
        "theme": "Theme", "font_size": "Font size", "dyslexia_font": "Dyslexia font",
        "xp": "XP", "level": "Level", "streak": "Streak", "badges": "Badges",
        "export": "Export CSV", "session_log_saved": "Session log saved.", "save_error": "Error saving file",
        "badge_earned": "Badge earned", "confirm_reset": "Reset current timer?",
        "focus_label_note": "Step 5", "break_label_note": "Step 1",
        "theme_soft": "Soft (default)", "theme_playful": "Playful",
        "badge_message": "You got {name} badge now. Congratulations!",
        "reset_data": "Reset Data", "reset_data_confirm": "Clear all saved settings and session history?"
    },
    "ko": {
        "title": "집중+ 타이머",
        "start": "시작", "pause": "중지", "reset": "초기화",
        "focus_min": "집중 (분)", "break_min": "휴식 (분)",
        "quick_25_5": "빠른 25/5", "quick_50_10": "빠른 50/10",
        "mute": "음소거", "settings": "설정", "language": "언어",
        "theme": "테마", "font_size": "글꼴 크기", "dyslexia_font": "난독증 친화 글꼴",
        "xp": "경험치", "level": "레벨", "streak": "연속 성공", "badges": "배지",
        "export": "CSV 내보내기", "session_log_saved": "세션 기록이 저장되었습니다.", "save_error": "파일 저장 중 오류",
        "badge_earned": "배지 획득", "confirm_reset": "현재 타이머를 초기화할까요?",
        "focus_label_note": "증분 5", "break_label_note": "증분 1",
        "theme_soft": "부드러운 (기본)", "theme_playful": "게임형",
        "badge_message": "{name} 배지를 획득했습니다. 축하합니다!",
        "reset_data": "데이터 초기화", "reset_data_confirm": "모든 설정과 기록을 삭제하시겠습니까?"
    },
    "cn": {
        "title": "专注+ 计时器",
        "start": "开始", "pause": "暂停", "reset": "重置",
        "focus_min": "专注 (分钟)", "break_min": "休息 (分钟)",
        "quick_25_5": "快速 25/5", "quick_50_10": "快速 50/10",
        "mute": "静音", "settings": "设置", "language": "语言",
        "theme": "主题", "font_size": "字体大小", "dyslexia_font": "阅读友好字体",
        "xp": "经验值", "level": "等级", "streak": "连胜", "badges": "徽章",
        "export": "导出 CSV", "session_log_saved": "会话记录已保存。", "save_error": "保存文件出错",
        "badge_earned": "获得徽章", "confirm_reset": "要重置当前计时器吗？",
        "focus_label_note": "步长 5", "break_label_note": "步长 1",
        "theme_soft": "柔和 (默认)", "theme_playful": "活泼",
        "badge_message": "你获得了{name}徽章。恭喜！",
        "reset_data": "重置数据", "reset_data_confirm": "是否清除所有保存的设置和会话记录？"
    }
}

# Themes
THEMES = {
    "Soft": {"bg": "#FFF9F3", "fg": "#222", "accent": "#4A90E2", "accent2": "#6EC6A5", "progress_bg": "#F1F7FF"},
    "Playful": {"bg": "#FFF6EE", "fg": "#071122", "accent": "#FF6B00", "accent2": "#FF3B30", "accent3": "#00B3FF", "accent4": "#32D74B", "progress_bg": "#FFF6F6"}
}

# Helpers for persistence
def load_state():
    if os.path.exists(APP_STATE_FILE):
        try:
            with open(APP_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_state(state):
    try:
        with open(APP_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def now_iso():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# Dyslexia font helpers
def detect_preferred_dyslexia_font():
    candidates = ["OpenDyslexic3", "OpenDyslexic", "Comic Sans MS", "DejaVu Sans", "Verdana", "Arial"]
    available = list(tkfont.families())
    for c in candidates:
        for fam in available:
            if fam.lower().startswith(c.lower()):
                return fam
    return None

def get_normal_font_family():
    candidates = ["Helvetica", "Segoe UI", "Arial", "DejaVu Sans", "Verdana"]
    available = list(tkfont.families())
    for c in candidates:
        for fam in available:
            if fam.lower().startswith(c.lower()):
                return fam
    return "Helvetica"

class ProductivityTimerApp:
    def __init__(self, root):
        self.root = root
        self.state = load_state()
        self.locale = self.state.get("locale", "en")
        self.strings = LOCALES.get(self.locale, LOCALES["en"])

        # progress / badges
        self.xp = self.state.get("xp", 0)
        self.level = self.state.get("level", 1)
        self.streak = self.state.get("streak", 0)
        self.badge_thresholds = {3: "Bronze", 5: "Silver", 10: "Gold"}
        self.badges = set(self.state.get("badges", []))
        self.session_log = self.state.get("session_log", [])

        # timer settings
        self.focus_min = tk.IntVar(value=self.state.get("focus_min", 25))
        self.break_min = tk.IntVar(value=self.state.get("break_min", 5))
        self.is_focus = True
        self.remaining = self.focus_min.get() * 60
        self.is_running = False

        # prefs
        self.muted = tk.BooleanVar(value=self.state.get("muted", False))
        self.theme_name = tk.StringVar(value=self.state.get("theme", "Soft"))
        self.font_size = tk.IntVar(value=self.state.get("font_size", 14))
        self.dyslexia_font = tk.BooleanVar(value=self.state.get("dyslexia_font", False))

        # build UI
        self.build_ui()
        self.apply_font_family()
        self.apply_theme()
        self.update_all_texts()
        self.update_timer_display()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_ui(self):
        self.root.title(self.strings["title"])
        self.root.geometry("800x520") # Changed width from 760 to 800
        style = ttk.Style(self.root);
        style.theme_use("clam")

        main = ttk.Frame(self.root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")
        self.root.rowconfigure(0, weight=1);
        self.root.columnconfigure(0, weight=1)

        # canvas
        # We use a canvas so we can draw the circular progress bar
        self.canvas = tk.Canvas(main, width=380, height=380, highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=4, padx=12, pady=12)
        # Center the text in the canvas (380/2 = 190, but 200 looked better)
        self.timer_text = self.canvas.create_text(200, 160, text="", font=("Helvetica", 36, "bold"))
        self.session_label = self.canvas.create_text(200, 220, text="", font=("Helvetica", 12))

        # right controls
        right = ttk.Frame(main)
        right.grid(row=0, column=1, sticky="nw", padx=8)

        # focus
        self.focus_label = ttk.Label(right, text="")
        self.focus_label.grid(row=0, column=0, sticky="w")
        self.focus_spin = ttk.Spinbox(right, from_=5, to=120, increment=5, textvariable=self.focus_min, width=6, command=self.on_duration_change)
        self.focus_spin.grid(row=0, column=1, sticky="w", padx=(6,0))
        self.focus_note = ttk.Label(right, text="")
        self.focus_note.grid(row=0, column=2, sticky="w", padx=(8,0))

        # break
        self.break_label = ttk.Label(right, text="")
        self.break_label.grid(row=1, column=0, sticky="w", pady=(8,0))
        self.break_spin = ttk.Spinbox(right, from_=0, to=60, increment=1, textvariable=self.break_min, width=6, command=self.on_duration_change)
        self.break_spin.grid(row=1, column=1, sticky="w", padx=(6,0), pady=(8,0))
        self.break_note = ttk.Label(right, text="")
        self.break_note.grid(row=1, column=2, sticky="w", padx=(8,0), pady=(8,0))

        # start/reset
        btn_frame = ttk.Frame(right);
        btn_frame.grid(row=2, column=0, columnspan=3, pady=(12,0))
        self.start_btn = ttk.Button(btn_frame, text="", command=self.toggle_start_pause, width=14);
        self.start_btn.grid(row=0, column=0, padx=6)
        self.reset_btn = ttk.Button(btn_frame, text="", command=self.reset_timer, width=14);
        self.reset_btn.grid(row=0, column=1, padx=6)

        # quick presets
        qp = ttk.Frame(right);
        qp.grid(row=3, column=0, columnspan=3, pady=(12,0))
        self.q25_btn = ttk.Button(qp, text="", command=lambda: self.set_quick(25,5), width=14);
        self.q25_btn.grid(row=0, column=0, padx=6)
        self.q50_btn = ttk.Button(qp, text="", command=lambda: self.set_quick(50,10), width=14);
        self.q50_btn.grid(row=0, column=1, padx=6)

        # XP / Level / Streak under quicks
        stats_frame = ttk.Frame(right);
        stats_frame.grid(row=4, column=0, columnspan=3, pady=(14,0), sticky="w")
        self.xp_label = ttk.Label(stats_frame, text="");
        self.xp_label.grid(row=0, column=0, sticky="w")
        self.level_label = ttk.Label(stats_frame, text="");
        self.level_label.grid(row=1, column=0, sticky="w")
        self.streak_label = ttk.Label(stats_frame, text="");
        self.streak_label.grid(row=2, column=0, sticky="w")

        # Badges compact area under stats with visible "Badges" heading
        badges_heading = ttk.Label(right, text=self.strings.get("badges", "Badges"), font=(None, 10, "bold"))
        badges_heading.grid(row=5, column=0, columnspan=3, sticky="w", pady=(10,0))
        badge_frame = ttk.Frame(right);
        badge_frame.grid(row=6, column=0, columnspan=3, pady=(6,0))
        self.badge_labels = {}
        col = 0
        for threshold, name in sorted(self.badge_thresholds.items()):
            lbl = ttk.Label(badge_frame, text=f"{name} ({threshold})", width=10, anchor="center", relief="ridge")
            lbl.grid(row=0, column=col, padx=4, pady=2)
            self.badge_labels[threshold] = lbl
            col += 1

        # bottom: settings, export, language
        bottom = ttk.Frame(self.root, padding=8);
        bottom.grid(row=1, column=0, sticky="ew"); bottom.columnconfigure(2, weight=1)
        self.settings_btn = ttk.Button(bottom, text="", command=self.open_settings);
        self.settings_btn.grid(row=0, column=0, padx=6)
        self.export_btn = ttk.Button(bottom, text="", command=self.export_csv);
        self.export_btn.grid(row=0, column=1, padx=6)
        self.lang_var = tk.StringVar(value=self.locale)
        self.lang_menu = ttk.OptionMenu(bottom, self.lang_var, self.locale, "en", "ko", "cn", command=self.change_language);
        self.lang_menu.grid(row=0, column=2, sticky="e")

        # shortcuts
        self.root.bind("<space>", lambda e: self.toggle_start_pause())
        self.root.bind("r", lambda e: self.reset_timer(confirm=False))
        self.root.bind("q", lambda e: self.set_quick(25,5))

    # Fonts / Dyslexia mode
    def apply_font_family(self):
        if self.dyslexia_font.get():
            fam = detect_preferred_dyslexia_font() or get_normal_font_family()
        else:
            fam = get_normal_font_family()
        style = ttk.Style()
        style.configure("TButton", font=(fam, max(10, self.font_size.get())))
        style.configure("TLabel", font=(fam, max(10, self.font_size.get())))
        self.canvas.itemconfig(self.timer_text, font=(fam, self.font_size.get()+18, "bold"))
        self.canvas.itemconfig(self.session_label, font=(fam, max(10, self.font_size.get()-2)))
        self.update_all_texts()

    # Theme
    def apply_theme(self):
        theme = THEMES.get(self.theme_name.get(), THEMES["Soft"])
        bg = theme.get("bg", "#fff");
        fg = theme.get("fg", "#000")
        self.root.configure(bg=bg)
        for w in self.root.winfo_children():
            try:
                w.configure(background=bg)
            except Exception:
                pass
        self.canvas.configure(bg=theme.get("progress_bg", "#fff"))
        self.canvas.itemconfig(self.timer_text, fill=fg)
        self.canvas.itemconfig(self.session_label, fill=fg)
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", max(10, self.font_size.get())))
        if self.theme_name.get() == "Playful":
            try:
                style.configure("Accent.TButton", background=theme.get("accent"), foreground=theme.get("fg"))
                self.start_btn.configure(style="Accent.TButton")
                self.q25_btn.configure(style="Accent.TButton")
                self.q50_btn.configure(style="Accent.TButton")
            except Exception:
                pass
        else:
            try:
                self.start_btn.configure(style="TButton")
                self.q25_btn.configure(style="TButton")
                self.q50_btn.configure(style="TButton")
            except Exception:
                pass
        for k, lbl in self.badge_labels.items():
            if k in self.badges:
                lbl.configure(background=theme.get("accent2"), foreground=theme.get("fg"))
            else:
                lbl.configure(background=bg, foreground=theme.get("fg"))

    # Timer logic
    def on_duration_change(self):
        self.is_focus = True
        self.remaining = max(0, self.focus_min.get()) * 60
        self.update_timer_display()

    def set_quick(self, f, b):
        self.focus_min.set(f);
        self.break_min.set(b)
        self.is_focus = True;
        self.remaining = self.focus_min.get() * 60
        self.is_running = False
        self.update_all_texts();
        self.update_timer_display()

    def toggle_start_pause(self):
        if not self.is_running:
            self.start_timer()
        else:
            self.pause_timer()

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.config(text=self.strings["pause"])
            self.countdown_tick()

    def pause_timer(self):
        self.is_running = False
        self.start_btn.config(text=self.strings["start"])

    def reset_timer(self, confirm=True):
        proceed = True
        if confirm:
            proceed = messagebox.askyesno(self.strings["reset"], self.strings["confirm_reset"])
        if proceed:
            if self.is_running:
                elapsed_seconds = (self.focus_min.get()*60 if self.is_focus else self.break_min.get()*60) - self.remaining
                minutes_elapsed = max(0, elapsed_seconds // 60)
                typ = "focus" if self.is_focus else "break"
                self.session_log.append({"time": now_iso(), "type": typ, "minutes": minutes_elapsed, "xp": 0, "success": False})
            self.is_running = False
            self.is_focus = True
            self.remaining = self.focus_min.get() * 60
            self.start_btn.config(text=self.strings["start"])
            self.update_timer_display()

    def countdown_tick(self):
        # This is the main timer loop that runs every second
        # Stop the function if the user pressed Pause
        if not self.is_running:
            return
        # Check if time is up
        if self.remaining <= 0:
            self.complete_session(natural=True)
            return # Stop this tick, complete_session will start the next one
        # Update the visual display (MM:SS and circle)
        self.update_timer_display()
        # Decrement the time
        self.remaining -= 1
        # Ask tkinter to call this function again after 1000ms (1 second)
        self.root.after(1000, self.countdown_tick)

    def update_timer_display(self):
        mins = max(0, self.remaining // 60);
        secs = max(0, self.remaining % 60)
        mmss = f"{mins:02d}:{secs:02d}"
        self.canvas.itemconfig(self.timer_text, text=mmss)
        self.canvas.itemconfig(self.session_label, text=(self.strings["focus_min"] if self.is_focus else self.strings["break_min"]))
        total = (self.focus_min.get()*60) if self.is_focus else (self.break_min.get()*60)
        if total <= 0: total = 1
        frac = 1 - (self.remaining / total)
        self.draw_progress(frac)

    def draw_progress(self, fraction):
        self.canvas.delete("arc") # Clear the old arc before drawing a new one
        theme = THEMES.get(self.theme_name.get(), THEMES["Soft"])
        acc = theme.get("accent", "#4A90E2");
        acc2 = theme.get("accent2", "#6EC6A5")

        # Coords for the bounding box of the circle
        x0, y0, x1, y1 = 40, 20, 360, 340;

        start = -90 # Start at 12 o'clock (top of the circle)
        extent = int(360 * fraction) # The size of the arc (e.g., 0.5 fraction = 180 degrees)
        # 1. Draw the background "track" circle first (in light grey)
        self.canvas.create_oval(x0, y0, x1, y1, outline=theme.get("progress_bg", "#EEE"), width=28, tags="arc")
        # 2. Draw the actual progress arc on top
        if extent > 0:
            self.canvas.create_arc(x0, y0, x1, y1, start=start, extent=extent, style="arc", outline=acc, width=22, tags="arc")
            angle = math.radians(start + extent)

            # Center X changed from 180 to 200
            cx, cy = 200 + math.cos(angle) * 140, 180 + math.sin(angle) * 140
            self.canvas.create_oval(cx-9, cy-9, cx+9, cy+9, fill=acc2, outline="", tags="arc")

    def complete_session(self, natural=True):
        if natural:
            typ = "focus" if self.is_focus else "break"
            minutes = self.focus_min.get() if self.is_focus else self.break_min.get()
            xp_gained = minutes if self.is_focus else 0
            if self.is_focus:
                self.xp += xp_gained
                self._level_up_if_needed()
                self.streak += 1
            self.session_log.append({"time": now_iso(), "type": typ, "minutes": minutes, "xp": xp_gained, "success": True})
            if self.is_focus:
                self.check_badges()

        # Play sound for each session end (no URL)
        self.play_end_sound()

        # Next session logic
        if self.break_min.get() <= 0:
            self.is_focus = True
            self.remaining = self.focus_min.get() * 60
        else:
            self.is_focus = not self.is_focus
            self.remaining = (self.focus_min.get()*60) if self.is_focus else (self.break_min.get()*60)

        # Auto-start next
        self.is_running = True
        self.start_btn.config(text=self.strings["pause"])
        self.save_progress()
        self.update_all_texts()
        self.update_timer_display()
        self.root.after(1000, self.countdown_tick)

    def _level_up_if_needed(self):
        new_level = 1 + (self.xp // 50)
        if new_level > self.level:
            self.level = new_level

    def check_badges(self):
        for threshold in sorted(self.badge_thresholds):
            if self.streak >= threshold and threshold not in self.badges:
                self.badges.add(threshold)
                name = self.badge_thresholds[threshold]
                msg = self.strings.get("badge_message", "You got {name} badge now. Congratulations!").format(name=name)
                messagebox.showinfo(self.strings.get("badge_earned", "Badge"), msg)
        self.apply_theme()

    def play_end_sound(self):
        # Simplified sound player (no MP3, no URL)
        if self.muted.get():
            return
        try:
            if HAVE_WINSOUND:
                # Use Windows system sound
                winsound.Beep(880, 300)
            else:
                # Fallback for non-Windows
                self.root.bell()
        except Exception:
            try:
                # Secondary fallback
                self.root.bell()
            except Exception:
                pass # Sound failed

    # settings / export / reset
    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title(self.strings["settings"]); win.transient(self.root);
        win.grab_set()
        ttk.Label(win, text=self.strings["theme"]).grid(row=0, column=0, sticky="w", padx=6, pady=6)
        ttk.Radiobutton(win, text=self.strings["theme_soft"], variable=self.theme_name, value="Soft", command=self.on_theme_change).grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(win, text=self.strings["theme_playful"], variable=self.theme_name, value="Playful", command=self.on_theme_change).grid(row=0, column=2, sticky="w")
        ttk.Label(win, text=self.strings["font_size"]).grid(row=1, column=0, sticky="w", padx=6, pady=6)
        fs = ttk.Scale(win, from_=10, to=28, orient="horizontal", variable=self.font_size, command=lambda e: self.on_font_change());
        fs.grid(row=1, column=1, columnspan=2, padx=6, pady=6, sticky="ew")
        # Dyslexia toggle restored (no description)
        ttk.Checkbutton(win, text=self.strings.get("dyslexia_font", "Dyslexia font"), variable=self.dyslexia_font, command=self.on_dyslexia_toggle).grid(row=2, column=0, columnspan=3, padx=6, pady=6, sticky="w")
        ttk.Checkbutton(win, text=self.strings["mute"], variable=self.muted).grid(row=3, column=0, columnspan=3, padx=6, pady=6, sticky="w")
        ttk.Button(win, text=self.strings.get("reset_data", "Reset Data"), command=self.reset_data_confirm).grid(row=4, column=0, columnspan=3, pady=(8,10))
        ttk.Button(win, text="Close", command=win.destroy).grid(row=5, column=0, columnspan=3, pady=6)

    def on_dyslexia_toggle(self):
        self.apply_font_family()
        self.save_settings()

    def reset_data_confirm(self):
        ok = messagebox.askyesno(self.strings.get("reset_data", "Reset Data"), self.strings.get("reset_data_confirm", "Clear all saved settings and session history?"))
        if not ok:
            return
        try:
            if os.path.exists(APP_STATE_FILE):
                os.unlink(APP_STATE_FILE)
        except Exception:
            pass
        self.state = {}
        self.xp = 0; self.level = 1; self.streak = 0; self.badges = set(); self.session_log = []
        self.focus_min.set(25); self.break_min.set(5); self.theme_name.set("Soft"); self.font_size.set(14)
        self.dyslexia_font.set(False); self.muted.set(False)
        messagebox.showinfo(self.strings.get("reset_data", "Reset Data"), "Data cleared.")
        self.apply_font_family(); self.apply_theme(); self.update_all_texts(); self.update_timer_display()

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")], title=self.strings["export"])
        if not file_path:
            return
        try:
            with open(file_path, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["time", "type", "minutes", "xp", "success"])
                for r in self.session_log:
                    writer.writerow([r.get("time",""), r.get("type",""), r.get("minutes",""), r.get("xp",""), r.get("success", False)])
            messagebox.showinfo(self.strings["export"], self.strings["session_log_saved"])
        except Exception:
            messagebox.showerror(self.strings["export"], self.strings["save_error"])

    def change_language(self, code):
        if code not in LOCALES:
            return
        self.locale = code
        self.strings = LOCALES[self.locale]
        self.save_settings()
        self.update_all_texts()

    def update_all_texts(self):
        self.root.title(self.strings["title"])
        self.start_btn.config(text=self.strings["start"] if not self.is_running else self.strings["pause"])
        self.reset_btn.config(text=self.strings["reset"])
        self.q25_btn.config(text=self.strings["quick_25_5"])
        self.q50_btn.config(text=self.strings["quick_50_10"])
        self.xp_label.config(text=f"{self.strings['xp']}: {self.xp}")
        self.level_label.config(text=f"{self.strings['level']}: {self.level}")
        self.streak_label.config(text=f"{self.strings['streak']}: {self.streak}")
        self.focus_label.config(text=self.strings["focus_min"])
        self.break_label.config(text=self.strings["break_min"])
        self.focus_note.config(text=self.strings["focus_label_note"])
        self.break_note.config(text=self.strings["break_label_note"])
        self.settings_btn.config(text=self.strings["settings"])
        self.export_btn.config(text=self.strings["export"])
        self.apply_theme()
        self.update_timer_display()

    def on_theme_change(self):
        self.apply_theme(); self.save_settings()

    def on_font_change(self):
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", max(10, self.font_size.get())))
        style.configure("TLabel", font=("Helvetica", max(10, self.font_size.get())))
        self.canvas.itemconfig(self.timer_text, font=("Helvetica", self.font_size.get()+18, "bold"))
        self.canvas.itemconfig(self.session_label, font=("Helvetica", max(10, self.font_size.get()-2)))
        self.save_settings()

    def save_settings(self):
        self.state["locale"] = self.locale
        self.state["theme"] = self.theme_name.get()
        self.state["font_size"] = self.font_size.get()
        self.state["dyslexia_font"] = self.dyslexia_font.get()
        self.state["muted"] = self.muted.get()
        self.state["focus_min"] = self.focus_min.get()
        self.state["break_min"] = self.break_min.get()
        save_state(self.state)

    def save_progress(self):
        self.state["xp"] = self.xp
        self.state["level"] = self.level
        self.state["streak"] = self.streak
        self.state["badges"] = list(self.badges)
        self.state["session_log"] = self.session_log
        self.save_settings()

    def on_close(self):
        if self.is_running:
            elapsed_seconds = (self.focus_min.get()*60 if self.is_focus else self.break_min.get()*60) - self.remaining
            minutes_elapsed = max(0, elapsed_seconds // 60)
            typ = "focus" if self.is_focus else "break"
            self.session_log.append({"time": now_iso(), "type": typ, "minutes": minutes_elapsed, "xp": 0, "success": False})
        self.save_progress()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ProductivityTimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
