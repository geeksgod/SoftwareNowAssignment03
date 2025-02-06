import tkinter as tk
from widgets.FileUpload import FILEUPLOAD
from tkinter import filedialog
from widgets.ErrorMssage import ErrorMessage
from .EditorPage import EDITORPAGE
from helper.Globalstore import global_store


class FILEUPLOADPAGE(tk.Frame):
    upload_controller = None
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.upload_controller = controller
        self.file_canvas = tk.Canvas(self, width=500, height=200, bg="white", highlightthickness=0)    
        f = FILEUPLOAD(self.file_canvas,upload_action=self.upload_action)
        self.image_path = f.get_image_path()
        self.bind_all("<Control-o>",lambda event:self.upload_action())
        print("here",self.image_path)
    
    def upload_action(self):
        """Funtion to open the file selector"""
        filename = filedialog.askopenfilename() #display the dialog box
        file_error_msg = ErrorMessage(self.file_canvas,"Please!! Choose the correct file") #create a error message 
        
        #display error messaage if wrong file is selected
        if(filename.endswith(('.jpg','.png','.jpeg'))):
            self.file = filename 
            global_store.data["imgPath"] = filename  #saves file path to instance of a class so that it can be accessed globally
            print(global_store.data["imgPath"])
            file_error_msg.hide()           
            self.upload_controller.show_editor_page()
        else:
            file_error_msg.show(250,150,"center")