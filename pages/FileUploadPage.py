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
        self.canvas = tk.Canvas(self, width=500, height=200, bg="white", highlightthickness=0)    
        f = FILEUPLOAD(self.canvas,upload_action=self.upload_action)
        self.image_path = f.get_image_path()
        print("here",self.image_path)
    
    def upload_action(self):
        filename = filedialog.askopenfilename()
        file_error_msg = ErrorMessage(self.canvas,"Please!! Choose the correct file") 
        if(filename.endswith(('.jpg','.png','.jpeg'))):
            self.file = filename 
            global_store.data["imgPath"] = filename
            print(global_store.data["imgPath"])
            file_error_msg.hide()           
            self.upload_controller.show_editor_page()
        else:
            file_error_msg.show(250,150,"center")