import time
import tkinter as tk
import pygame
import sounddevice as sd
import numpy as np
import threading

press_time = None
pygame.mixer.init()
SPIKE_THRESHOLD = 0.5
SELECTED_DEVICE = 0
listening_for_spikes = False
list_of_latencies = []
measurements = 0

# show the sound devices available
input_devices = [
    d for d in sd.query_devices()
    if d['max_input_channels'] > 0
]

# Function to detect audio spikes
def audio_callback(indata, frames, time_info, status):
    global listening_for_spikes
    volume_norm = np.linalg.norm(indata)
    if listening_for_spikes and volume_norm > SPIKE_THRESHOLD:
        print("Audio spike detected!")
        check_latency()
        listening_for_spikes = False

def start_audio_listener():
    device_info = sd.query_devices(SELECTED_DEVICE, 'input')
    device_index = sd.query_devices().index(device_info)
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=44100, blocksize=1024, device=device_index):
        threading.Event().wait()

# Start audio listener in a background thread
threading.Thread(target=start_audio_listener, daemon=True).start()

# Function to play a sound
def play_sound():
    sound = pygame.mixer.Sound("click_sound.wav")
    sound.play()

# Function to handle key press events
def get_press_time(event):
    global press_time, listening_for_spikes
    play_sound()
    press_time = time.time()
    listening_for_spikes = True
    print(f"Key pressed at {press_time}")
    return press_time

# Function to check the time difference between key press and sound playback
def check_latency():
    global press_time, measurements, list_of_latencies
    if press_time is not None:
        current_time = time.time()
        latency = current_time - press_time
        print(f"Latency: {latency:.6f} seconds")
        list_of_latencies.append(latency)
        measurements += 1
        currentAverage = np.mean(list_of_latencies) if list_of_latencies else 0
        print("Average Latency after",measurements,"measurements: ",currentAverage)

# Create a simple GUI to test keypress detection
root = tk.Tk()
root.bind("<KeyPress>", get_press_time)
root.title("Audio Latency Tester")
label = tk.Label(root, text="Select this window and press\na key to test audio latency", font=("Arial", 12))
label.pack(padx=10, pady=50)
root.mainloop()