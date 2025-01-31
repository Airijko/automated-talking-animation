import sounddevice as sd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import soundfile as sf
import os

def audio_callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    update_image(volume_norm)

def update_image(volume):
    global image_label
    if volume > 10:
        img = Image.open("images/open3.png")
    elif 5 < volume <= 10:
        img = Image.open("images/open2.png")
    elif 1 < volume <= 5:
        img = Image.open("images/open1.png")
    else:
        img = Image.open("images/close.png")
    
    img = img.resize((200, 200), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

def stop_recording():
    global stream
    if stream:
        stream.stop()
        stream.close()
        stream = None
        mic_status_button.config(text="Mic Off", command=start_recording, state=tk.NORMAL)

def start_recording():
    global stream
    stream = sd.InputStream(callback=audio_callback)
    stream.start()
    mic_status_button.config(text="Mic On", command=stop_recording, state=tk.NORMAL)

def upload_audio_file():
    global audio_data, audio_samplerate
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
    if file_path:
        stop_recording()
        audio_data, audio_samplerate = sf.read(file_path)
        volume_norm = np.linalg.norm(audio_data) * 10
        update_image(volume_norm)
        file_name = os.path.basename(file_path)
        file_label.config(text=f"File selected: {file_name}")
        play_button.config(state=tk.NORMAL)

def play_pause_audio():
    global is_playing, audio_stream
    if is_playing:
        sd.stop()
        audio_stream.close()
        play_button.config(text="Play")
        mic_status_button.config(state=tk.NORMAL)
        start_recording()
    else:
        stop_recording()
        audio_stream = sd.OutputStream(callback=playback_callback, samplerate=audio_samplerate, channels=len(audio_data.shape))
        audio_stream.start()
        sd.play(audio_data, audio_samplerate)
        play_button.config(text="Pause")
        mic_status_button.config(state=tk.DISABLED)
    is_playing = not is_playing

def playback_callback(outdata, frames, time, status):
    global audio_data
    volume_norm = np.linalg.norm(audio_data[:frames]) * 10
    update_image(volume_norm)
    outdata[:] = audio_data[:frames]
    audio_data = audio_data[frames:]

# Set up tkinter window
root = tk.Tk()
root.title("Talking Animation")

# Create a label to display the image
image_label = tk.Label(root)
image_label.pack()

# Create a button to upload audio file
upload_button = tk.Button(root, text="Upload Audio File", command=upload_audio_file)
upload_button.pack()

# Create a label to display the file name
file_label = tk.Label(root, text="No file selected")
file_label.pack()

# Create a button to show mic status
mic_status_button = tk.Button(root, text="Mic On", command=stop_recording)
mic_status_button.pack()

# Create a play/pause button
play_button = tk.Button(root, text="Play", command=play_pause_audio, state=tk.DISABLED)
play_button.pack()

# Start audio stream
stream = None
audio_data = None
audio_samplerate = None
is_playing = False
audio_stream = None
start_recording()

# Run the tkinter main loop
root.mainloop()