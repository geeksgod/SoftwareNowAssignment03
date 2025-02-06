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
        #variable intialization 
        self.controller = controller     
        tk.Frame.__init__(self, parent)
        self.columnconfigure(0, weight=1)  # 20%
        self.columnconfigure(1, weight=4)  # 80%
        self.rowconfigure(0, weight=1)  # Make rows expand if neede
        self.blur_strength = 0
        # Create two frames
        menu_frame = tk.Frame(self)  # 20% width
        editor_frame = tk.Frame(self)  # 80% width
        self.blured_image = None
        self.real_image = None
        self.slidervalue = None
        self.crop_canvas = tk.Canvas(editor_frame)
        
        # Place frames in grid
        menu_frame.grid(row=0, column=0, sticky="nsew")  # 20% width        
        editor_frame.grid(row=0, column=1, sticky="nsew")  # 80% width
        
        #saves the height and width of frame to variable
        self.editor_frameWidth = editor_frame.winfo_width() 
        self.editor_frameHeigth = editor_frame.winfo_height()     
            
        #display the path of file being edited
        file_path_label = tk.Label(editor_frame, text = global_store.data['imgPath'])
        file_path_label.pack(fill="both", expand=True)
        
        #display image being edited
        self.image_edit_label = tk.Label(editor_frame)
        self.image_edit_label.pack(fill="both", expand=True)
        editor_frame.bind("<Configure>", lambda e: self.resize_image(e, editor_frame, global_store.data['imgPath'], self.image_edit_label))
        
        #button to select new image to edit
        label3 = tk.Button(menu_frame, text = "New",command =self.show_file_page)
        label3.pack(padx=10,pady=10,fill="both", expand=False)
        
        #dispaly shortcut information
        suggestion_text = """Shortcut:\nNew: Ctrl + N\nCut: Ctrl + C \nUndo:Ctrl + Z\nSave:Ctrl + S"""
        suggestion = tk.Text(menu_frame,wrap="word", width=30, height=10)
        suggestion.insert("1.0",suggestion_text)
        suggestion.pack(side='bottom')
        
        self.imageCropFrame = editor_frame        
        crop_button = tk.Button(menu_frame, text = "Crop",command=self.crop_image)
        crop_button.pack(padx=10,pady=10,fill="both", expand=False)
        
         #shortcut for new button
        self.bind_all("<Control-n>", lambda event: self.show_file_page())
        self.bind_all("<Control-c>", lambda event: self.crop_image())
        self.bind_all("<Control-z>", lambda event: self.undo_action())
        self.bind_all("<Control-s>", lambda event: self.save_action())

        #slider for blur
        self.blur_slider = tk.Scale(menu_frame,to=30, orient="horizontal", label="Blur Image (%)", command=self.blur_imge)
        self.blur_slider.set(0)  # Default at 100%
        self.blur_slider.pack() 
    
        #button for undo
        undo_button = tk.Button(menu_frame,text="Undo blur",command=self.undo_action)   
        undo_button.pack(padx=10,pady=10,fill="both", expand=False)
        
        #button for save
        save_button = tk.Button(menu_frame,text="Save",command=self.save_action) 
        save_button.pack(padx=10,pady=10,fill="both", expand=False)
    
           
    def resize_image(self,event, frame, image_path, label):
        new_width, new_height = frame.winfo_width(), frame.winfo_height()
        img = cv2.imread(image_path)
        # Open and resize the image to fill the exact dimensions
        self.reimg = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
        self.real_image = self.reimg
        resized_img_rgb = cv2.cvtColor(self.reimg, cv2.COLOR_BGR2RGB)

        # Convert OpenCV image to Tkinter-compatible format
        self.photo = tk.PhotoImage(data=cv2.imencode('.ppm', resized_img_rgb)[1].tobytes())

        
        label.config(image=self.photo)
        label.image = self.photo  # Keep reference to avoid garbage collection
        self.editor_frameWidth = frame.winfo_width() 
        self.editor_frameHeigth = frame.winfo_height()
    
    def crop_image(self):
        self.crop_canvas = tk.Canvas(self.imageCropFrame, width=self.editor_frameWidth, height=self.editor_frameHeigth, highlightthickness=0)
        self.image_on_canvas = self.crop_canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.crop_canvas.place(x=0, y=0)
        
        #Calling class to open the crop editor
        DrawSquareApp(self.crop_canvas,self.reimg)


        
         
    def show_file_page(self):
        #THis function activates the fileupload page 
        response = mb.askyesno("Confirmation", "Do you want to continue?")
        if response:
            self.controller.show_file_upload_page()
        else:
            print("User clicked No")
            
    def blur_imge(self,scale_valued):   
        blur_strength = int(scale_valued) * 2 + 1 #scalevalue need to be odd for gaussian blur
        if(self.crop_canvas.winfo_exists()):
            self.crop_canvas.place_forget()  #hides the crop canvas with crop function activated
        if blur_strength > self.blur_strength: #only blurs image if the blur strnegth is higher than previous strength to reduce blur effect after reset
            self.blur_strength = blur_strength
            blur_image = cv2.GaussianBlur(self.reimg, (blur_strength, blur_strength), 0) #opencv function blur image
            self.reimg = blur_image
            self.blured_image = blur_image
            
            coloured_image = cv2.cvtColor(blur_image, cv2.COLOR_BGR2RGB)  # color the image
            
            self.photo = tk.PhotoImage(data=cv2.imencode('.ppm', coloured_image)[1].tobytes())  #convert np array to tkimage    
            
            #update the label      
            self.image_edit_label.config(image=self.photo) 
            self.image_edit_label.image = self.photo
    
    def save_action(self):
        if(self.crop_canvas.winfo_exists()):self.crop_canvas.place_forget()    #hides the crop canvas with crop function activated

        if(self.is_cv2_image(self.blured_image)):
            folder_path = "saved_crops"  # Define the folder path
            save_image(folder_path,self.blured_image) #saves np array in png format
        else:
            folder_path = "saved_crops"  # Define the folder path
            save_image(folder_path,self.reimg)
    
    def undo_action(self):
        #triggers when undo button is pressed
            if(self.crop_canvas.winfo_exists()):self.crop_canvas.place_forget()
            self.blur_slider.set(0) #set the slider to 0
            self.blur_strength = 0
            
            self.reimg=  self.real_image #reset image variable
            coloured_image = cv2.cvtColor(self.real_image, cv2.COLOR_BGR2RGB) # color the image
            self.photo = tk.PhotoImage(data=cv2.imencode('.ppm', coloured_image)[1].tobytes())    #convert np array to tkimage    
            #update the label
            self.image_edit_label.config(image=self.photo) 
            self.image_edit_label.image = self.photo
            self.blured_image =  None
        
    def is_cv2_image(self,var):
        #check in the variable contain np array of the image
        return isinstance(var, np.ndarray)

         