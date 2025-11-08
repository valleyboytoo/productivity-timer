# Focus+ Productivity Timer

## 📝 Project Description

This project is a Python-based GUI application, **Focus+ Timer**, designed as a productivity tool for neurodiverse users, particularly those with ADHD or other attention-related challenges. It provides a simple, customizable, and non-distracting interface to help manage work and break sessions effectively.

The application is built using Python's built-in **Tkinter** library and incorporates several socio-cultural and accessibility features to create a more inclusive user experience.

## ✨ Key Features

  * [cite\_start]**Customizable Timers:** Set custom durations for both **Focus** and **Break** sessions[cite: 21, 22].
  * [cite\_start]**Quick Presets:** Buttons for quickly setting common Pomodoro intervals like 25/5 and 50/10[cite: 26, 27, 28].
  * [cite\_start]**Gamification:** Earn **XP** for completed focus minutes [cite: 1, 57][cite\_start], **Level Up** [cite: 15, 59][cite\_start], maintain a **Streak** [cite: 15, 57][cite\_start], and earn **Badges** (Bronze, Silver, Gold) for consistency[cite: 1, 15, 32, 58].
  * [cite\_start]**Session Logging:** All completed and interrupted sessions are logged[cite: 15, 49, 57, 81].
  * [cite\_start]**CSV Export:** Users can export their entire session history to a CSV file for analysis[cite: 36, 74].
  * [cite\_start]**Auto-Start:** The timer automatically cycles between focus and break sessions to maintain flow[cite: 1].
  * [cite\_start]**Persistent State:** All settings, progress, and session logs are saved locally in a `.json` file and reloaded on start[cite: 8, 14, 79, 80].

### ♿ Accessibility & Socio-Cultural Features

  * [cite\_start]**Multilingual Support:** The entire interface can be switched between **English**, **Korean**, and **Chinese**[cite: 2, 4, 6, 37].
  * [cite\_start]**Dyslexia-Friendly Font:** A toggle in the settings enables a detected dyslexia-friendly font (like OpenDyslexic or Comic Sans) for improved readability[cite: 1, 17, 68].
  * [cite\_start]**Adjustable Font Size:** Users can scale the application's font size up or down for comfort[cite: 17, 67].
  * [cite\_start]**Customizable Themes:** Includes a default "Soft" theme with non-distracting colors and a "Playful" theme for a different feel[cite: 1, 7, 16].
  * [cite\_start]**Sensory-Friendly Audio:** Uses a simple system beep (`winsound.Beep` or the system bell) for notifications, avoiding jarring MP3s[cite: 62, 63, 65]. [cite\_start]A **Mute** option is also available[cite: 16, 68].

## ⚙️ Requirements

  * **Python 3**
  * **Tkinter** (This is included in most standard Python installations).
  * [cite\_start]**`winsound`** (This module is built-in on Windows systems for audio notifications [cite: 2]). [cite\_start]The app will fall back to the system `bell()` if it's not available[cite: 63, 65].

## 🚀 How to Run

1.  Ensure you have Python 3 installed.

2.  Save the code as a Python file (e.g., `focus_timer.py`).

3.  Open your terminal or command prompt.

4.  Navigate to the directory where you saved the file.

5.  Run the following command:

    ```bash
    python focus_timer.py
    ```

## Example of Use

1.  When you run the program, the main timer window will appear.
2.  [cite\_start]On the right side, use the **"Focus (min)"** and **"Break (min)"** spinboxes to set your desired times[cite: 21, 22].
3.  [cite\_start]Click the **"Start"** button (or press the `Spacebar`) to begin your first focus session[cite: 23].
4.  [cite\_start]The timer will display a visual countdown and a progress arc on the canvas[cite: 20, 52, 55].
5.  [cite\_start]When the session ends, a system beep will sound [cite: 62][cite\_start], and the timer will automatically start the next session (e.g., switch from focus to break)[cite: 1, 58, 59].
6.  [cite\_start]Click **"Settings"** to open a new window where you can[cite: 35, 66]:
      * [cite\_start]Change the theme (Soft/Playful)[cite: 67].
      * [cite\_start]Adjust the font size[cite: 67].
      * [cite\_start]Toggle the **Dyslexia font**[cite: 68].
      * [cite\_start]**Mute** all sounds[cite: 68].
      * [cite\_start]**Reset** all your saved progress and settings[cite: 68].
7.  [cite\_start]Click **"Export CSV"** to save a file containing your session history[cite: 36, 74].