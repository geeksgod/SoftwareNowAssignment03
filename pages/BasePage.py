import tkinter as tk
from .FileUploadPage import FILEUPLOADPAGE
from .EditorPage import EDITORPAGE
class APP(tk.Tk):
     
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        self.wm_state('zoomed')

        # creating a container
        self.container = tk.Frame(self)  
        self.container.pack(fill="both", expand=True)
  
       
        # initializing frames to an empty array
        self.current_frame = None
        self.show_file_upload_page()  # Initially show the start page
       
    def show_file_upload_page(self):    
        """function to activaate the file upload page"""    
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = FILEUPLOADPAGE(self.container, self)
        self.current_frame.pack(fill="both", expand=True)
        
    def show_editor_page(self):
        """Function to activate the editor page"""        
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = EDITORPAGE(self.container, self)
        self.current_frame.pack(fill="both", expand=True)

        
        
  
   
        
  