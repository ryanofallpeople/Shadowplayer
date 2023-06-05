import json
import os
import shutil
import subprocess
import tkinter as tk
from PIL import Image, ImageTk
from Modules.thumbnail_generator import generate_thumbnail
from tkinter import filedialog

# Folder containing video files
folder_target = "J:/Ryans Videos/Nvidia Shadowplay/Recorded Videos/Fortnite"

# JSON array to store video metadata
video_data = []

# Gather metadata and create JSON array of video objects
for filename in os.listdir(folder_target):
    if filename.endswith(".mp4") or filename.endswith(".avi"):
        file_path = os.path.join(folder_target, filename)
        file_stats = os.stat(file_path)
        date_modified = file_stats.st_mtime
        thumbnail = generate_thumbnail(file_path)  # Implement this function using PIL
        video_obj = {
            "filepath": file_path,
            "date_modified": date_modified,
            "thumbnail": thumbnail,
            "isWatched": False,
            "isSelected": False,
            "deletionMarked": False
        }
        video_data.append(video_obj)


# Create GUI
window = tk.Tk()
window.geometry("1546x873")


# Set frame color and background color
window.configure(bg="#CCCCCC")
window.attributes("-alpha", 0.95)  # Adjust window opacity if desired

# Set frame color
window.tk_setPalette(background="#333333")

# Custom window dragging functionality
def start_drag(event):
    window.x = event.x
    window.y = event.y

def drag(event):
    deltax = event.x - window.x
    deltay = event.y - window.y
    x = window.winfo_x() + deltax
    y = window.winfo_y() + deltay
    window.geometry(f"+{x}+{y}")

window.bind("<ButtonPress-1>", start_drag)
window.bind("<B1-Motion>", drag)

# Add custom minimize and exit buttons
def minimize_window():
    window.iconify()

def exit_window():
    window.destroy()

# Dark-themed title bar
title_bar = tk.Frame(window, bg="#222222", height=30, relief="raised")
title_bar.pack(fill="x")

minimize_button = tk.Button(title_bar, text="_", width=5, height=2, command=minimize_window)
minimize_button.pack(side="left", padx=5)

exit_button = tk.Button(title_bar, text="X", width=5, height=2, command=exit_window)
exit_button.pack(side="right", padx=5)

# Create frame for thumbnail labels
thumbnail_frame = tk.Frame(window, bg="#333333")
thumbnail_frame.pack(fill="both", expand=True)

thumbnail_images = []  # Store references to thumbnail images
marked_videos = []  # Array to store marked video file paths
checkbox_vars = [] # Checkbutton variables
thumbnail_labels = []  # Store references to thumbnail labels


# Converts unix or mishmoshed file path format to windows
def convert_path(path):
    # Normalize the path
    normalized_path = os.path.normpath(path)
    
    # Replace forward slashes with backslashes
    converted_path = normalized_path.replace("/", "\\")
    
    return converted_path

# Function to play video using VLC
def play_video(file_path):
    subprocess.run(["vlc", "--sout-all", "--sout", "#display", convert_path(file_path)])


def checkbutton_changed(index):
    # Update the isSelected property in the video_data array
    video_data[index]["isSelected"] = checkbox_vars[index].get()

    # Update the marked_videos array based on the current selection
    marked_videos.clear()
    for video in video_data:
        if video["isSelected"]:
            marked_videos.append(video["filepath"])

    # Update the thumbnail border based on the checkbutton state
    update_thumbnail_border(index)


def update_thumbnail_border(index):
    thumbnail_label = thumbnail_labels[index]
    thumbnail_image = thumbnail_images[index]

    if checkbox_vars[index].get():
        thumbnail_label.config(borderwidth=10, relief="sunken")
    else:
        thumbnail_label.config(borderwidth=4, relief="ridge")


for i, video in enumerate(video_data):
    # Display thumbnail image
    thumbnail_image = ImageTk.PhotoImage(video["thumbnail"])
    thumbnail_images.append(thumbnail_image)  # Retain reference to the PhotoImage

    thumbnail_label = tk.Label(thumbnail_frame, image=thumbnail_image)
    thumbnail_label.grid(row=i // 4, column=i % 4, sticky="nsew", padx=5, pady=5)  # Add padding
    thumbnail_labels.append(thumbnail_label)  # Store the thumbnail label

    # Add checkbox to top right corner of thumbnail
    checkbox_var = tk.BooleanVar()
    checkbox_var.set(video["isSelected"])  # Set the initial value based on video["isSelected"]
    checkbox_vars.append(checkbox_var)  # Store the checkbox variable
    checkbox = tk.Checkbutton(thumbnail_frame, variable=checkbox_var, command=lambda idx=i: checkbutton_changed(idx))
    checkbox.grid(row=i // 4, column=i % 4, sticky="NE")

    # Add play button on top of the thumbnail
    play_button = tk.Button(thumbnail_frame, text="Play", command=lambda path=video["filepath"]: play_video(path))
    play_button.grid(row=i // 4, column=i % 4)

    # Update the thumbnail border based on the initial checkbutton state
    update_thumbnail_border(i)


# Function to handle the folder selection
def select_output_folder():
    folder_selected = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_selected)

# Control bar
control_frame = tk.Frame(window)
control_frame.pack(fill="x")

# Folder selector
folder_label = tk.Label(control_frame, text="Output Folder:")
folder_label.pack(side="left")
folder_entry = tk.Entry(control_frame)
folder_entry.pack(side="left")
folder_button = tk.Button(control_frame, text="Browse", command=select_output_folder)
folder_button.pack(side="left")

# Video name entry
name_label = tk.Label(control_frame, text="Video Name:")
name_label.pack(side="left")
name_entry = tk.Entry(control_frame)
name_entry.pack(side="left")

# Submit button
def copy_videos():
    output_folder = folder_entry.get()
    video_name = name_entry.get()

    if not output_folder or not video_name:
        # Handle empty fields, display an error message, etc.
        return

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Determine the suffix format based on the number of marked videos
    suffix_format = "_{:03d}" if len(marked_videos) > 1 else ""

    for i, video_path in enumerate(marked_videos):
        video_name_with_suffix = video_name + (suffix_format.format(i+1) if suffix_format else "")
        destination_path = os.path.join(output_folder, video_name_with_suffix + os.path.splitext(video_path)[1])
        shutil.copy2(video_path, destination_path)
        print(f"Copied {video_path} to {destination_path}")

submit_button = tk.Button(control_frame, text="Submit", command=copy_videos)
submit_button.pack(side="right")

# Configure grid weights to expand the thumbnails
for i in range(len(video_data)//4 + 1):
    thumbnail_frame.grid_rowconfigure(i, weight=1)
for i in range(4):
    thumbnail_frame.grid_columnconfigure(i, weight=1)

# Resize the window to fit snuggly around the labels
# Calculate the aspect ratio of the thumbnail labels
label_aspect_ratio = thumbnail_images[0].width() / thumbnail_images[0].height()

# Calculate the desired window width and height based on the aspect ratio and number of rows
rows = len(video_data) // 4 + 1
thumbnail_width = 200  # Adjust the desired thumbnail width
thumbnail_height = thumbnail_width / label_aspect_ratio
window_width = int(thumbnail_width * 4)
window_height = int(thumbnail_height * rows) + control_frame.winfo_height()
window.geometry(f"{window_width}x{window_height}")

# Prevent window resizing
window.resizable(False, False)

# Set the window title
window.title("Shadowplayer")

# Set the window icon using an embedded icon file
icon_file = r"C:\Program Files\NVIDIA Corporation\NVIDIA GeForce Experience\NVIDIA GeForce Experience.exe".replace("\\", "/")  # Replace with the path to your executable file
window.iconbitmap(default=icon_file)

# Function to show the application on the Windows taskbar
def show_on_taskbar():
    window.deiconify()
    window.iconbitmap(icon_file)

# Hide windows border and top bar
window.overrideredirect(True)
window.withdraw()

# Show the application on the taskbar after a delay
window.after(2000, show_on_taskbar)

window.mainloop()
