import time
import tkinter as tk
import pygame

current_key_press_time = None
previous_key_press_time = None

# Initialize Pygame mixer for audio playback
pygame.mixer.init()
# Function to play a sound
def play_sound():
    sound = pygame.mixer.Sound("click_sound.wav")
    sound.play()

# Function to handle key press events
def get_press_time(event):
    play_sound()
    press_time = time.time()
    print(f"Key pressed at {press_time}")
    return press_time

def on_key_press(event):
    global current_key_press_time, previous_key_press_time
    current_key_press_time = get_press_time(event)
    if previous_key_press_time is not None:
        latency = current_key_press_time - previous_key_press_time
        print(f"Latency since last key press: {latency:.6f} seconds")
    previous_key_press_time = current_key_press_time

# Create a simple GUI to test keypress detection
root = tk.Tk()
root.bind("<KeyPress>", on_key_press)
root.title("Audio Latency Tester")
label = tk.Label(root, text="Press a key to test audio latency", font=("Arial", 16))
label.pack(padx=10, pady=10)
root.mainloop()
