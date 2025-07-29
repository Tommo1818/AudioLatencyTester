import time
import tkinter as tk
chosen_key = "z"
current_key_press_time = None
previous_key_press_time = None

def on_key_press(event):
    global current_key_press_time, previous_key_press_time
    if event.keysym == chosen_key:
        current_key_press_time = time.time()
        print(f"Key '{chosen_key}' pressed at {current_key_press_time}")
        if previous_key_press_time is not None:
            latency = current_key_press_time - previous_key_press_time
            print(f"Latency since last key press: {latency:.6f} seconds")
        previous_key_press_time = current_key_press_time

# Create a simple GUI to test keypress detection
root = tk.Tk()
root.bind("<KeyPress>", on_key_press)
root.title("Audio Latency Tester")
label = tk.Label(root, text="Press the 'z' key to test keypress detection.")
label.pack(padx=10, pady=10)
root.mainloop()

