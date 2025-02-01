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
        cropped_pil_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

        # Convert to PhotoImage for displaying in Tkinter
        cropped_photo = ImageTk.PhotoImage(cropped_pil_image)

        self.show_cropped_image(cropped_photo,cropped_pil_image)

    def show_cropped_image(self, cropped_photo,cropped_pil_image):
        """ Show cropped image in a new dialog box with Yes/No options. """
        dialog = tk.Toplevel(self.canvas)
        dialog.title("Cropped Image")

        # Display the cropped image in the dialog
        label = tk.Label(dialog, text="Do you want to save the image?")
        label.pack()
        label = tk.Label(dialog, image=cropped_photo)
        label.pack()

        # Function to handle Yes button click
        def on_yes():
            folder_path = "saved_crops"  # Define the folder path

            # Check if folder exists, if not create it
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Save the cropped image inside the folder
            saved_image_path = os.path.join(folder_path, "cropped_image.jpg")
            cropped_pil_image.save(saved_image_path)

            messagebox.showinfo("Image Saved", f"The cropped image has been saved to: {saved_image_path}")
            dialog.destroy()

        # Function to handle No button click
        def on_no():
            messagebox.showinfo("No Clicked", "You clicked No!")
            dialog.destroy()
        # Create Yes and No buttons
        yes_button = tk.Button(dialog, text="Yes", command=on_yes)
        yes_button.pack(side="left", padx=10, pady=10)

        no_button = tk.Button(dialog, text="No", command=on_no)
        no_button.pack(side="right", padx=10, pady=10)

        # Keep reference to avoid garbage collection
        dialog.image = cropped_photo
