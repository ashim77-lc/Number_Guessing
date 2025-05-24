import tkinter as tk
import random
# this make window pop up
window = tk.Tk()
window.title("Guess the Number Game")
window.geometry("500x280")
window.config(bg="#1e1e2e")

target_number = random.randint(1, 100)
guesses = 0
game_started = False

# Animation state for blinking
blink_on = True

def set_placeholder(text, color="grey"):
    entry.config(fg=color)
    entry.delete(0, tk.END)
    entry.insert(0, text)

def reset_entry():
    set_placeholder("Guess here", "grey")

def on_entry_click(event):
    current = entry.get()
    if current in ("Guess here", "Give another attempt"):
        entry.delete(0, tk.END)
        entry.config(fg="black")

def on_focus_out(event):
    if entry.get() == "":
        if game_started:
            set_placeholder("Give another attempt", "orange")
        else:
            reset_entry()

def on_keypress(event):
    current = entry.get()
    if current in ("Guess here", "Give another attempt"):
        entry.delete(0, tk.END)
        entry.config(fg="black")

def start_game(event=None):
    global game_started
    if not game_started:
        instruction_label.config(text="")
        game_started = True
        stop_pulse_instruction()  # stop pulse animation once game starts
    check_guess()

def check_guess():
    global guesses, target_number
    guess_text = entry.get()

    if guess_text in ("Guess here", "Give another attempt") or not guess_text.isdigit():
        hint_label.config(text="Please enter a valid number!", fg="red")
        return

    guess = int(guess_text)
    guesses += 1

    if guess < target_number:
        hint_label.config(text="Please enter a higher number!", fg="orange")
        set_placeholder("Give another attempt", "orange")
        start_blink_hint()
    elif guess > target_number:
        hint_label.config(text="Please enter a lower number!", fg="orange")
        set_placeholder("Give another attempt", "orange")
        start_blink_hint()
    else:
        stop_blink_hint()
        hint_label.config(text="")
        entry.config(state="disabled")
        result_label.config(
            text=f"🎉 Correct! It was {target_number}\nYou guessed it in {guesses} attempts!",
            fg="lightgreen"
        )
        restart_btn.pack(pady=10)
        confetti_animation()

def restart_game():
    global target_number, guesses, game_started
    target_number = random.randint(1, 100)
    guesses = 0
    game_started = False
    entry.config(state="normal")
    reset_entry()
    hint_label.config(text="")
    result_label.config(text="")
    instruction_label.config(text="Guess the number between 1 and 100")
    restart_btn.pack_forget()
    start_pulse_instruction()

# --- Animation functions ---

def pulse_instruction():
    # Pulse text color from grey to white and back
    current_color = instruction_label.cget("fg")
    new_color = "#bbbbbb" if current_color == "white" else "white"
    instruction_label.config(fg=new_color)
    global pulse_job
    pulse_job = window.after(700, pulse_instruction)

def start_pulse_instruction():
    global pulse_job
    pulse_job = window.after(700, pulse_instruction)

def stop_pulse_instruction():
    global pulse_job
    if pulse_job:
        window.after_cancel(pulse_job)

def blink_hint():
    global blink_on
    if blink_on:
        hint_label.config(fg="orange")
    else:
        hint_label.config(fg="#1e1e2e")  # same as background to "hide"
    blink_on = not blink_on
    global blink_job
    blink_job = window.after(500, blink_hint)

def start_blink_hint():
    global blink_job, blink_on
    blink_on = True
    blink_hint()

def stop_blink_hint():
    global blink_job
    if blink_job:
        window.after_cancel(blink_job)
    hint_label.config(fg="orange")

# Simple confetti animation using colored dots on window after win
import random as rnd

confetti_dots = []
confetti_running = False

def confetti_animation():
    global confetti_running
    confetti_running = True
    for _ in range(30):
        x = rnd.randint(20, 480)
        y = rnd.randint(50, 220)
        size = rnd.randint(5, 10)
        color = rnd.choice(["#ff4757", "#ffa502", "#2ed573", "#1e90ff", "#ff6b81"])
        dot = tk.Canvas(window, width=size, height=size, bg="#1e1e2e", highlightthickness=0)
        dot.place(x=x, y=y)
        oval = dot.create_oval(0, 0, size, size, fill=color, outline="")
        confetti_dots.append((dot, oval))
    window.after(1500, clear_confetti)

def clear_confetti():
    global confetti_dots, confetti_running
    for dot, oval in confetti_dots:
        dot.destroy()
    confetti_dots = []
    confetti_running = False

# Button hover effect

def on_enter(e):
    e.widget.config(bg="#5a6d8a")

def on_leave(e):
    e.widget.config(bg="#4e5d6c")

# Widgets
instruction_label = tk.Label(window, text="Guess the number between 1 and 100", font=("Arial", 14), bg="#1e1e2e", fg="white")
instruction_label.pack(pady=10)

entry = tk.Entry(window, font=("Arial", 20), justify="center", width=25, fg="grey")
entry.pack(pady=10)
reset_entry()
entry.bind("<FocusIn>", on_entry_click)
entry.bind("<FocusOut>", on_focus_out)
entry.bind("<Key>", on_keypress)
entry.bind("<Return>", start_game)

hint_label = tk.Label(window, text="", font=("Arial", 13), bg="#1e1e2e", fg="white")
hint_label.pack()

submit_btn = tk.Button(window, text="Guess", font=("Arial", 12), command=start_game, bg="#4e5d6c", fg="white")
submit_btn.pack(pady=10)
submit_btn.bind("<Enter>", on_enter)
submit_btn.bind("<Leave>", on_leave)

result_label = tk.Label(window, text="", font=("Arial", 13), bg="#1e1e2e", fg="white")
result_label.pack()

restart_btn = tk.Button(window, text="Play Again", font=("Arial", 12), command=restart_game, bg="#00b894", fg="white")

# Start pulsing instruction on app start
pulse_job = None
blink_job = None
start_pulse_instruction()

window.mainloop()
