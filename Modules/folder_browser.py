import os
import tkinter as tk
from tkinter import filedialog

def select_recordings_folder():
    # Check if there are any mp4 files in the current working directory
    mp4_files = [file for file in os.listdir() if file.endswith(".mp4")]
    
    # Determine the initial directory for the folder browser
    initial_dir = os.getcwd() if mp4_files else os.path.expanduser("~/Videos")
    
    # Create a temporary root window for the folder browser
    root = tk.Tk()
    root.withdraw()

    icon_file = r"C:\Program Files\NVIDIA Corporation\NVIDIA GeForce Experience\NVIDIA GeForce Experience.exe".replace("\\", "/")  # Replace with the path to your executable file
    root.iconbitmap(default=icon_file)
    
    # Open the folder browser dialog
    folder_selected = filedialog.askdirectory(initialdir=initial_dir, title="Select Recordings Folder")
    
    # Destroy the temporary root window
    root.destroy()
    
    return folder_selected
