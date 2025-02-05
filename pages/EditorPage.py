import tkinter as tk
from helper.Globalstore import global_store
import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import messagebox as mb
from helper.DrawSquare import DrawSquareApp


class EDITORPAGE(tk.Frame):
     
    def __init__(self, parent, controller):    
        self.controller = controller     
        tk.Frame.__init__(self, parent)
        self.columnconfigure(0, weight=1)  # 20%
        self.columnconfigure(1, weight=4)  # 80%
        self.rowconfigure(0, weight=1)  # Make rows expand if neede

        # Create two frames
        frame1 = tk.Frame(self, bg="red")  # 20% width
        frame2 = tk.Frame(self, bg="blue")  # 80% width

        # Place frames in grid
        frame1.grid(row=0, column=0, sticky="nsew")  # 20% width
        
        
        frame2.grid(row=0, column=1, sticky="nsew")  # 80% width
        self.frame2Width = frame2.winfo_width() 
        self.frame2Heigth = frame2.winfo_height()     
            
        
        label = tk.Label(frame2, text = global_store.data['imgPath'])
        label.pack(fill="both", expand=True)
        
        label2 = tk.Label(frame2)
        label2.pack(fill="both", expand=True)
        frame2.bind("<Configure>", lambda e: self.resize_image(e, frame2, global_store.data['imgPath'], label2))
        
        label3 = tk.Button(frame1, text = "New",command =self.show_file_page)
        label3.pack(padx=10,pady=10,fill="both", expand=False)
        self.imageCropFrame = frame2
        label4 = tk.Button(frame1, text = "Crop",command=self.crop_image)
        label4.pack(padx=10,pady=10,fill="both", expand=False)
        
        label5 = tk.Button(frame1, text = "Resize")
        label5.pack(padx=10,pady=10,fill="both", expand=False)       
        
        

      
    
    def resize_image(self,event, frame, image_path, label):
        new_width, new_height = frame.winfo_width(), frame.winfo_height()
    
        # Open and resize the image to fill the exact dimensions
        self.img = Image.open(image_path).resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.img)
        
        label.config(image=self.photo)
        label.image = self.photo  # Keep reference to avoid garbage collection
        self.frame2Width = frame.winfo_width() 
        self.frame2Heigth = frame.winfo_height()
    
    def crop_image(self):
        print(self.frame2Width,self.frame2Heigth)
        canvas = tk.Canvas(self.imageCropFrame, width=self.frame2Width, height=self.frame2Heigth, highlightthickness=0)
        self.image_on_canvas = canvas.create_image(0, 0, anchor="nw", image=self.photo)
        canvas.place(x=0, y=0)
        ds = DrawSquareApp(canvas,self.img)
         
    def show_file_page(self):
        response = mb.askyesno("Confirmation", "Do you want to continue?")
        if response:
            self.controller.show_file_upload_page()
        else:
            print("User clicked No")
         