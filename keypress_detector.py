import time
import tkinter as tk

chosen_key = "z"
last_key_press_time = None

def on_key_press(event):
    global last_key_press_time
    global chosen_key
    # Check if the pressed key matches the chosen key
    # and update the last key press time
    if event.keysym == chosen_key:
        last_key_press_time = time.time()
        print(f"Key '{chosen_key}' pressed at {last_key_press_time}")

root = tk.Tk()
root.bind("<KeyPress>", on_key_press)
root.mainloop()

