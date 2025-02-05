import tkinter as tk
from helper.Globalstore import global_store
import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import messagebox as mb
from helper.DrawSquare import DrawSquareApp
from helper.cvutils import *


class EDITORPAGE(tk.Frame):
     
    def __init__(self, parent, controller):    
        self.controller = controller     
        tk.Frame.__init__(self, parent)
        self.columnconfigure(0, weight=1)  # 20%
        self.columnconfigure(1, weight=4)  # 80%
        self.rowconfigure(0, weight=1)  # Make rows expand if neede
        self.blur_strength = 0
        # Create two frames
        menu_frame = tk.Frame(self)  # 20% width
        editor_frame = tk.Frame(self)  # 80% width

        # Place frames in grid
        menu_frame.grid(row=0, column=0, sticky="nsew")  # 20% width
        
        
        editor_frame.grid(row=0, column=1, sticky="nsew")  # 80% width
        self.editor_frameWidth = editor_frame.winfo_width() 
        self.editor_frameHeigth = editor_frame.winfo_height()     
            
        
        file_path_label = tk.Label(editor_frame, text = global_store.data['imgPath'])
        file_path_label.pack(fill="both", expand=True)
        
        self.image_edit_label = tk.Label(editor_frame)
        self.image_edit_label.pack(fill="both", expand=True)
        editor_frame.bind("<Configure>", lambda e: self.resize_image(e, editor_frame, global_store.data['imgPath'], self.image_edit_label))
        
        label3 = tk.Button(menu_frame, text = "New",command =self.show_file_page)
        self.bind_all("<Control-n>", lambda event: self.show_file_page())

        label3.pack(padx=10,pady=10,fill="both", expand=False)
        
        
        suggestion_text = """Shortcut:\nNew: Ctrl + N\nCut: Ctrl + C"""
        suggestion = tk.Text(menu_frame,wrap="word", width=30, height=10)
        suggestion.insert("1.0",suggestion_text)
        suggestion.pack(side='bottom')
        
        self.imageCropFrame = editor_frame
        
        label4 = tk.Button(menu_frame, text = "Crop",command=self.crop_image)
        self.bind_all("<Control-c>", lambda event: self.crop_image())
        label4.pack(padx=10,pady=10,fill="both", expand=False)
        
        blur_slider = tk.Scale(menu_frame,to=30, orient="horizontal", label="Blur Image (%)", command=self.blur_imge)
        blur_slider.set(0)  # Default at 100%
        blur_slider.pack()      
       
           
    def resize_image(self,event, frame, image_path, label):
        new_width, new_height = frame.winfo_width(), frame.winfo_height()
        img = cv2.imread(image_path)
        # Open and resize the image to fill the exact dimensions
        self.reimg = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
        resized_img_rgb = cv2.cvtColor(self.reimg, cv2.COLOR_BGR2RGB)

        # Convert OpenCV image to Tkinter-compatible format
        self.photo = tk.PhotoImage(data=cv2.imencode('.ppm', resized_img_rgb)[1].tobytes())

        
        label.config(image=self.photo)
        label.image = self.photo  # Keep reference to avoid garbage collection
        self.editor_frameWidth = frame.winfo_width() 
        self.editor_frameHeigth = frame.winfo_height()
    
    def crop_image(self):
        print(self.editor_frameWidth,self.editor_frameHeigth)
        canvas = tk.Canvas(self.imageCropFrame, width=self.editor_frameWidth, height=self.editor_frameHeigth, highlightthickness=0)
        self.image_on_canvas = canvas.create_image(0, 0, anchor="nw", image=self.photo)
        canvas.place(x=0, y=0)
        ds = DrawSquareApp(canvas,self.reimg)
         
    def show_file_page(self):
        response = mb.askyesno("Confirmation", "Do you want to continue?")
        if response:
            self.controller.show_file_upload_page()
        else:
            print("User clicked No")
            
    def blur_imge(self,scale_valued):   
        blur_strength = int(scale_valued) * 2 + 1
        if blur_strength > self.blur_strength:
            self.blur_strength = blur_strength
            blured_image = cv2.GaussianBlur(self.reimg, (blur_strength, blur_strength), 0)
            self.reimg = blured_image
            coloured_image = cv2.cvtColor(blured_image, cv2.COLOR_BGR2RGB)
            self.photo = tk.PhotoImage(data=cv2.imencode('.ppm', coloured_image)[1].tobytes())        
            self.image_edit_label.config(image=self.photo)
            self.image_edit_label.image = self.photo
        
        

         