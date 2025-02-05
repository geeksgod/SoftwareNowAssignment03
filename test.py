import tkinter as tk
from PIL import Image, ImageTk

class DrawSquareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Draw a Square Over an Image in a Label")

        # Create a frame to contain the label and canvas
        self.frame = tk.Frame(root, bg="lightgray", width=500, height=400)
        self.frame.pack(pady=20, padx=20)

        # Load and display the image inside a label
        self.image_path = "your_image_path.jpg"  # Replace with your image path
        self.img = Image.open(self.image_path)
        self.img = self.img.resize((500, 400), Image.Resampling.LANCZOS)  # Resize image to fit frame
        self.photo = ImageTk.PhotoImage(self.img)

        # Create a label to display the image
        self.label = tk.Label(self.frame, image=self.photo)
        self.label.pack()

        # Create a canvas over the label for drawing
        self.canvas = tk.Canvas(self.frame, width=500, height=400, highlightthickness=0)
        self.canvas.place(x=0, y=0)

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

# Run the application
root = tk.Tk()
app = DrawSquareApp(root)
root.mainloop()
