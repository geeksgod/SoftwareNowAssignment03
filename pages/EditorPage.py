import tkinter as tk
from helper.Globalstore import global_store
import cv2
import numpy as np
from PIL import Image, ImageTk

class EDITORPAGE(tk.Frame):
     
    def __init__(self, parent, controller):         
        tk.Frame.__init__(self, parent)
       
        label = tk.Label(self, text = global_store.data['imgPath'])
        label.pack()
        img = cv2.imread(global_store.data['imgPath'])
        
        resized_img = self.resize_image(img,600,300)
            # Convert the image to RGB (OpenCV loads images in BGR)
        img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
        # Convert the image to a Tkinter-compatible format
        
        img_pil = Image.fromarray(img_rgb)
       
        img_tk = ImageTk.PhotoImage(img_pil)
        # Display the image on the Tkinter window
        self.image_label = tk.Label(self)
        self.image_label.pack(padx=20, pady=10, fill="both", expand=True)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk  # Keep a reference to avoid garbage collection
    
    def resize_image(self, img, width, height):
        """Resize the image to the given width and height using OpenCV."""
        # Check if img is a valid NumPy array
        if isinstance(img, np.ndarray):
            return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        else:
            print("Error: Invalid image format.")
            return None