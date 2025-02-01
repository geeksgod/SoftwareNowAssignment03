class DrawSquareApp:
    def __init__(self, canvas):       
        # Create a canvas over the label for drawing
        self.canvas = canvas
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
        
    