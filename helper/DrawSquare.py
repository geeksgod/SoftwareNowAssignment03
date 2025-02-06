import cv2
from tkinter import messagebox
import numpy as np
import tkinter as tk
import os
from .cvutils import *

class DrawSquareApp:
    def __init__(self, canvas,image):       
        # Create a canvas over the label for drawing
        self.canvas = canvas
        self.canvas.place(x=0, y=0)        
        self.cv_image = np.array(image)
        self.cv_image = cv2.cvtColor(self.cv_image, cv2.COLOR_RGB2BGR) 

        # Variables for tracking drawing
        self.start_x = None
        self.start_y = None
        self.square = None  # Only one square at a time

        # Bind mouse events to the canvas (not the root window)
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_square)
        self.canvas.bind("<ButtonRelease-1>", self.finish_draw)

    def start_draw(self, event):
        """ Start drawing when the mouse is clicked over the label. """
        self.start_x = event.x
        self.start_y = event.y

        # Delete previous square (only one at a time)
        if self.square:
            self.canvas.delete(self.square)

        # Create new square with a dotted outline
        self.square = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="blue", width=3, dash=(4, 2)
        )

    def draw_square(self, event):
        """ Resize the square while dragging the mouse. """
        if self.start_x and self.start_y:
            end_x = event.x
            end_y = event.y
            self.canvas.coords(self.square, self.start_x, self.start_y, end_x, end_y)

    def finish_draw(self, event):
        """ Finalize the square when the mouse is released. """
        self.start_x, self.start_y = None, None  # Reset start position
        self.crop_inside_square()
        
        
    def crop_inside_square(self):
        """ Crop the image inside the square using OpenCV. """
        if not self.square:
            return
        
        # Get the coordinates of the square
        coords = self.canvas.coords(self.square)
        x1, y1, x2, y2 = map(int, coords)  # Coordinates of the square

        # Crop the image using OpenCV (use NumPy slicing)
        self.cropped_image = self.cv_image[y1:y2, x1:x2]

        # Convert the cropped image back to PIL for Tkinter
        cropped_rgb = cv2.cvtColor(self.cropped_image, cv2.COLOR_BGR2RGB)


        # Convert OpenCV image to Tkinter PhotoImage (using numpy and Tkinter)
        cropped_photo = tk.PhotoImage(data=cv2.imencode('.ppm', cropped_rgb)[1].tobytes())
        
        self.show_cropped_image(cropped_photo)

    def show_cropped_image(self, cropped_photo):
        """ Show cropped image in a new dialog box with Yes/No options. """
        dialog = tk.Toplevel(self.canvas,height=1100,width= 900)
        dialog.geometry("900x600")
        dialog.title("Cropped Image")
        dialog.resizable(False,False)
        #Make the dialog full screen
        # dialog.attributes("-fullscreen", True)
        
        dialog.bind("<Escape>", lambda e: dialog.destroy())
        # Display the cropped image in the dialog
        label = tk.Label(dialog, text="Do you want to save the image?")
        label.pack()
        image_frame = tk.Frame(dialog, width=600, height=350, bg="gray")
        image_frame.pack_propagate(False)  # Prevent resizing
        image_frame.pack(fill=tk.BOTH, expand=True)
        
        self.crop_image_label = tk.Label(image_frame, image=cropped_photo)
        self.crop_image_label.pack()
        
       
        
        # Function to handle Yes button click
        def on_yes():            
            folder_path = "output"  # Define the folder path
            save_image(folder_path,self.resized_img)
            messagebox.showinfo("Sucess!!", f"Image saved to {folder_path}")
            dialog.destroy()
                
        def on_no():
            messagebox.showinfo("Sucess!!", "The Image has been discarded")
            dialog.destroy()
        # Create Yes and No buttons
        
        frame = tk.Frame(dialog)
        frame.pack(side='bottom',fill= "none")
        
        yes_button = tk.Button(frame, text="Yes", command=on_yes)
        yes_button.pack(side="left",padx=10, pady=10)
        

        no_button = tk.Button(frame, text="No", command=on_no)
        no_button.pack(side='right',padx=10, pady=10)
        
        
        slider = tk.Scale(dialog, from_=50, to=150, orient="horizontal", label="Resize Image (%)", command=self.slider_resize_image)
        slider.set(100)  # Default at 100%
        slider.pack(side='bottom')
        
        

        # Keep reference to avoid garbage collection
        dialog.image = cropped_photo
        
    def slider_resize_image(self,scale_value):
            scale_factor = float(scale_value) / 100
            new_width = int(self.cropped_image.shape[1] * scale_factor)
            new_height = int(self.cropped_image.shape[0] * scale_factor)
            print(new_height,new_width)
            self.resized_img = cv2.resize(self.cropped_image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    
            # Convert BGR (OpenCV) to RGB (for Tkinter display)
            resized_rgb = cv2.cvtColor(self.resized_img, cv2.COLOR_BGR2RGB)

            # Convert the resized OpenCV image to Tkinter PhotoImage
            self.resized_photo = tk.PhotoImage(data=cv2.imencode('.ppm', resized_rgb)[1].tobytes())

            # Update label with the resized image
            self.crop_image_label.config(image=self.resized_photo)
            self.crop_image_label.image = self.resized_photo
