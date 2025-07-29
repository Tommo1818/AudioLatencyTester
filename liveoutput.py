
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import threading
import time

# Parameters
samplerate = 44100  # Hertz
blocksize = 1024    # Samples per block
window_sec = 1      # Seconds to display
peaks = []
stream = None
running = False
selected_device = None
key_press_times = []

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    # Calculate peak (max absolute value) for this block
    peak = np.abs(indata).max()
    peaks.append(peak)
    # Keep only the last N peaks (for 1 second window)
    blocks_in_window = int(samplerate / blocksize * window_sec)
    if len(peaks) > blocks_in_window:
        del peaks[:len(peaks)-blocks_in_window]

def start_stream():
    global stream, running, peaks, selected_device
    peaks = []
    running = True
    blocks_in_window = int(samplerate / blocksize * window_sec)

    def run_audio_stream():
        global stream
        try:
            stream = sd.InputStream(
                channels=1,
                samplerate=samplerate,
                blocksize=blocksize,
                callback=audio_callback,
                device=selected_device
            )
            stream.start()
            while running:
                sd.sleep(50)
            stream.stop()
            stream.close()
        except Exception as e:
            print(f"Error: {e}")

    audio_thread = threading.Thread(target=run_audio_stream)
    audio_thread.start()

    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    ax.set_ylim(0, 1)
    ax.set_xlim(0, blocks_in_window)
    ax.set_xlabel('Block (last 1 second)')
    ax.set_ylabel('Peak Amplitude')
    ax.set_title('Live Microphone Peak (1s window)')

    try:
        while running:
            plt.pause(0.01)
            x = np.arange(len(peaks))
            y = np.array(peaks)
            line.set_xdata(x)
            line.set_ydata(y)
            ax.set_xlim(0, blocks_in_window)
            ax.set_ylim(0, 1)
            plt.draw()
    except Exception as e:
        print(f"Plotting error: {e}")
    finally:
        plt.ioff()
        plt.close(fig)
        stop_stream()
        audio_thread.join()

def stop_stream():
    global running
    running = False

def on_start():
    global selected_device
    selected_device = int(device_var.get())
    start_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)
    root.after(100, start_stream)

def on_stop():
    stop_stream()
    start_btn.config(state=tk.NORMAL)
    stop_btn.config(state=tk.DISABLED)

# Tkinter GUI
root = tk.Tk()
root.title("Audio Latency Tester")

# Device selector
devices = sd.query_devices()
input_devices = [(i, d['name']) for i, d in enumerate(devices) if d['max_input_channels'] > 0]
device_var = tk.StringVar()
device_names = [f"{i}: {n}" for i, n in input_devices]
device_indices = [str(i) for i, n in input_devices]
if input_devices:
    device_var.set(device_indices[0])
device_label = tk.Label(root, text="Input Device:")
device_label.pack(padx=10, pady=5)
device_menu = ttk.Combobox(root, textvariable=device_var, values=device_indices, state='readonly')
device_menu.pack(padx=10, pady=5)
# Show device names in a listbox for reference
device_list_label = tk.Label(root, text="Available Devices:")
device_list_label.pack(padx=10, pady=(5,0))
device_listbox = tk.Listbox(root, height=min(10, len(device_names)), width=50)
for name in device_names:
    device_listbox.insert(tk.END, name)
device_listbox.pack(padx=10, pady=(0,5))

# Start/Stop buttons
start_btn = tk.Button(root, text="Start", command=on_start)
start_btn.pack(padx=10, pady=5)
stop_btn = tk.Button(root, text="Stop", command=on_stop, state=tk.DISABLED)
stop_btn.pack(padx=10, pady=5)

root.mainloop()