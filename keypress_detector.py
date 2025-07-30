import time
import tkinter as tk
import pygame

press_time = None

# Initialize Pygame mixer for audio playback
pygame.mixer.init()

# Function to play a sound
def play_sound():
    sound = pygame.mixer.Sound("click_sound.wav")
    sound.play()

# Function to handle key press events
def get_press_time(event):
    global press_time
    play_sound()
    press_time = time.time()
    print(f"Key pressed at {press_time}")
    return press_time

# Create a simple GUI to test keypress detection
root = tk.Tk()
root.bind("<KeyPress>", get_press_time)
root.title("Audio Latency Tester")
label = tk.Label(root, text="Select this window and press\na key to test audio latency", font=("Arial", 12))
label.pack(padx=10, pady=50)
root.mainloop()
