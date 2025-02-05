from PIL import Image, ImageTk
import cv2
from tkinter import messagebox
import numpy as np
import tkinter as tk
import os

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
        cropped_image = self.cv_image[y1:y2, x1:x2]

        # Convert the cropped image back to PIL for Tkinter
        self.cropped_pil_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

        # Convert to PhotoImage for displaying in Tkinter
        cropped_photo = ImageTk.PhotoImage(self.cropped_pil_image)

        self.show_cropped_image(cropped_photo)

    def show_cropped_image(self, cropped_photo):
        """ Show cropped image in a new dialog box with Yes/No options. """
        dialog = tk.Toplevel(self.canvas,height=800,width= 900)
        dialog.title("Cropped Image")
        
        #Make the dialog full screen
        dialog.attributes("-fullscreen", True)
        
        dialog.bind("<Escape>", lambda e: dialog.destroy())
        # Display the cropped image in the dialog
        label = tk.Label(dialog, text="Do you want to save the image?")
        label.pack()
        self.crop_image_label = tk.Label(dialog, image=cropped_photo)
        self.crop_image_label.pack()
        
       
        
        # Function to handle Yes button click
        def on_yes():
            folder_path = "saved_crops"  # Define the folder path

            # Check if folder exists, if not create it
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Save the cropped image inside the folder
            saved_image_path = os.path.join(folder_path, "cropped_image.jpg")
            self.cropped_pil_image.save(saved_image_path)

            messagebox.showinfo("Image Saved", f"The cropped image has been saved to: {saved_image_path}")
            dialog.destroy()

        # Function to handle No button click
        def on_no():
            messagebox.showinfo("No Clicked", "You clicked No!")
            dialog.destroy()
        # Create Yes and No buttons
        
        frame = tk.Frame(dialog)
        frame.pack(side='bottom',fill= "none")
        
        yes_button = tk.Button(frame, text="Yes", command=on_yes)
        yes_button.pack(side="left",padx=10, pady=10)
        

        no_button = tk.Button(frame, text="No", command=on_no)
        no_button.pack(side='right',padx=10, pady=10)
        
        
        slider = tk.Scale(dialog, from_=50, to=200, orient="horizontal", label="Resize Image (%)", command=self.slider_resize_image)
        slider.set(100)  # Default at 100%
        slider.pack(side='bottom')
        
        

        # Keep reference to avoid garbage collection
        dialog.image = cropped_photo
        
    def slider_resize_image(self,scale_value):
            scale_factor = float(scale_value) / 100
            new_width = int(self.cropped_pil_image.width * scale_factor)
            new_height = int(self.cropped_pil_image.height * scale_factor)
            print(new_height,new_width)
            resized_img = self.cropped_pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.resized_photo = ImageTk.PhotoImage(resized_img)
            self.resized_photo = ImageTk.PhotoImage(resized_img)
            self.crop_image_label.config(image=self.resized_photo)
            self.crop_image_label.image = self.resized_photo
