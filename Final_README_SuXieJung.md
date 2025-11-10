Focus+ Productivity Timer

📝 About This Project
This is a GUI application built with Python and Tkinter for our final project.

The goal is to help users, especially those with ADHD or other attention challenges, manage their work and break sessions. It's a "Pomodoro" style timer but includes extra features to make it more engaging, accessible, and user-friendly.

✨ Features
Custom Timers: You can set your own times for Focus and Break sessions using the spinboxes.

Quick Presets: Includes "25/5" and "50/10" buttons to quickly set common timer intervals.

Auto-Cycling: The timer automatically cycles between focus and break sessions so you can stay in the flow.

Gamification System: To help with motivation, the app includes:

XP: Earn experience points for every minute of focused work.

Levels: Level up as you accumulate XP.

Streaks: Build a streak for every focus session you complete in a row.

Badges: Earn Bronze, Silver, and Gold badges for reaching streak milestones.

Accessibility Options:

Themes: Choose between a "Soft" (default) theme with calm colors or a "Playful" theme.

Adjustable Font Size: A slider in the settings lets you make the text bigger or smaller.

Dyslexia-Friendly Font: A toggle that switches the app to use a font like OpenDyslexic (if you have it installed) for better readability.

Simple Audio: Uses a simple system beep for notifications that isn't jarring. There is also a Mute button.

Multi-Language: The entire app can be switched between English, Korean, and Chinese.

Progress Saving: All your settings, XP, level, and session history are automatically saved to a productivity_timer_state.json file. When you reopen the app, you start right where you left off.

Session Log & Export: The app logs every session (even incomplete ones). You can click "Export CSV" to save your full history to a file to see your work patterns.

⚙️ How to Run
The project is built using only standard Python libraries, so you don't need to install anything extra.

You just need Python 3. (Tkinter and winsound are included with standard Python on Windows).

Save the code as a Python file (e.g., Final_PY_SuXieJung.py).

Open your terminal or Command Prompt.

Navigate (cd) to the folder where you saved the file.

Run the script:

Bash

python final_project.py
📖 How to Use
When the app opens, set your "Focus (min)" and "Break (min)" times on the right.

Click the "Start" button (or just press the Spacebar) to begin.

You will see the timer count down and a circular progress bar fill up.

When the time is up, the app will make a "beep" sound and automatically start the next session (switching from focus to break, or vice-versa).

Click "Settings" to:

Change the theme.

Adjust the font size.

Toggle the dyslexia font or mute sounds.

Reset all your saved progress if you want to start over.


Click "Export CSV" at any time to save a file of your session history.
