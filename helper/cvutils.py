import os
import cv2
import tkinter as tk

def save_image(folder_path,photo):
     if not os.path.exists(folder_path):
            os.makedirs(folder_path)
     cv2.imwrite(folder_path + "/screenshot.png", photo)  # Save using OpenCV
     print(f"Image saved to {folder_path}")
                # Function to handle No button click
                
def get_tk_image(photo):
    coloured_image = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
    return tk.PhotoImage(data=cv2.imencode('.ppm', coloured_image)[1].tobytes())   