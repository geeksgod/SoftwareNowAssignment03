from .BaseWidget import BASEWIDGET


class LABEL(BASEWIDGET):
    def __init__(self,canvas):
        super().__init__(canvas)
       
    
    def createLabel(self,msg):
        label = self.tk.Label(
            self.canvas, 
            text= msg, 
            bg="white", 
            fg="black", 
            font=("Arial", 14)
        )  
        label.place(x=250, y=35, anchor='center') 