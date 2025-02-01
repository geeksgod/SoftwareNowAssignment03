from .BaseWidget import BASEWIDGET
class ErrorMessage(BASEWIDGET):
    widget=None
    def __init__(self,canvas,message):
        super().__init__(canvas)
        self.widget = self.tk.Label(
        canvas, 
        text=message, 
        bg="white", 
        fg="red", 
        font=("Arial", 9)
        )        
    
    def show(self,x,y,anchor='center'):
        self.widget.place(x=x,y =y, anchor=anchor)
    def hide(self):
        print("here hide")
        self.widget.place_forget()
        
    
    