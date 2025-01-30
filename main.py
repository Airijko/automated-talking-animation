import sounddevice as sd
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

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

# Set up tkinter window
root = tk.Tk()
root.title("Talking Animation")

# Create a label to display the image
image_label = tk.Label(root)
image_label.pack()

# Start audio stream
stream = sd.InputStream(callback=audio_callback)
stream.start()

# Run the tkinter main loop
root.mainloop()

# Stop the audio stream when the window is closed
stream.stop()
stream.close()