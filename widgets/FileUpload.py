from .Label import LABEL
from .BaseWidget import BASEWIDGET


class FILEUPLOAD(BASEWIDGET): 
    file = None
    def __init__(self,canvas,upload_action): 
        super().__init__(canvas)       
        self.canvas.pack(pady=20)
        self.canvas.create_rectangle(
        10, 10, 490, 190,  
        outline="gray",   
        dash=(5, 2),       
        width=2            
        )
        upload_label =  LABEL(self.canvas)
        upload_label.createLabel("Please!! Select the file you want to edit\nor Press CTRL+ O")
        button = self.tk.Button(self.canvas, text='Browse Picture', command=upload_action)
        button.place(x=250,y =80, anchor='center')
    
   
    
    def get_image_path(self):
        return self.file
    
    