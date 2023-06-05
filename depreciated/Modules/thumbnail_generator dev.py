# thumbnail_generator.py

import cv2
from PIL import Image

def generate_thumbnail(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Read the first frame
    ret, frame = video.read()

    # If reading the frame was successful, convert it to PIL Image
    if ret:
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Rescale the image to thumbnail size
        thumbnail_size = (200, 150)
        image.thumbnail(thumbnail_size)

        # Close the video file
        video.release()

        # Return the rescaled thumbnail image
        print("Sucessfully generated thumbnail for: " + video_path)
        return image

    # If the video frame couldn't be read, return None
    print("Could not read video frame of: " + video_path)
    return None
