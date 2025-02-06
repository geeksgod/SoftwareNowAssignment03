import os
import cv2
import tkinter as tk
from tkinter import messagebox


def save_image(folder_path,photo):
     if not os.path.exists(folder_path): #create folder if it doesnot exist
            os.makedirs(folder_path)
     cv2.imwrite(folder_path + "/output.png", photo)  # Save using OpenCV
     messagebox.showinfo("Photo saved sucessfully","Image saved to "+ folder_path)
     print(f"Image saved to {folder_path}")
                
                
def get_tk_image(photo):
    coloured_image = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
    return tk.PhotoImage(data=cv2.imencode('.ppm', coloured_image)[1].tobytes())   