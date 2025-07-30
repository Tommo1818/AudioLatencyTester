import time
import tkinter as tk
import pygame
import sounddevice as sd
import numpy as np
import threading

press_time = None
pygame.mixer.init()
SPIKE_THRESHOLD = 0.5


input_devices = [
    d for d in sd.query_devices()
    if d['max_input_channels'] > 0
]

for idx, each in enumerate(input_devices):
    print(f"Index: {idx} Input Device: {each['name']} - Channels: {each['max_input_channels']}")

# Function to detect audio spikes
def audio_callback(indata, frames, time_info, status):
    volume_norm = np.linalg.norm(indata)
    if volume_norm > SPIKE_THRESHOLD:
        print("Audio spike detected!")
        check_latency()

def start_audio_listener():
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=44100, blocksize=1024):
        threading.Event().wait()

# Start audio listener in a background thread
threading.Thread(target=start_audio_listener, daemon=True).start()

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

# Function to check the time difference between key press and sound playback
def check_latency():
    if press_time is not None:
        current_time = time.time()
        latency = current_time - press_time
        print(f"Latency: {latency:.6f} seconds")
    else:
        print("No key press detected yet.")

# Create a simple GUI to test keypress detection
root = tk.Tk()
root.bind("<KeyPress>", get_press_time)
root.title("Audio Latency Tester")
label = tk.Label(root, text="Select this window and press\na key to test audio latency", font=("Arial", 12))
label.pack(padx=10, pady=50)
root.mainloop()

