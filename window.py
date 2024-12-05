from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title = "My window"
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.__root, width=self.width, height=self.height)
        self.canvas.pack(fill=BOTH, expand=True)
        self.running = False
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
    
    def close(self):
        self.running = False
        self.__root.destroy()
    
    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

class Point():
    def __init__(self, x , y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, 
            self.p2.x, self.p2.y, 
            fill=fill_color, width=2
            )     
    
class Cell:
    def __init__(self, x1, y1, x2, y2, win = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win

    def draw(self):
        canvas = self._win.canvas
        bg_color = "white"
        
        if self.has_left_wall:
            canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill="black")
        else:
            canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill=bg_color)

        if self.has_top_wall:
            canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill="black")
        else:
            canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill=bg_color)

        if self.has_right_wall:
            canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill="black")
        else:
            canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill=bg_color)

        if self.has_bottom_wall:
            canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill="black")
        else:
            canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill=bg_color)
    def draw_move(self, to_cell, undo=False):
        if self._win == None:
            return
        canvas = self._win.canvas

        from_x = (self._x1 + self._x2) // 2
        from_y = (self._y1 + self._y2) // 2

        to_x = (to_cell._x1 + to_cell._x2) // 2
        to_y = (to_cell._y1 + to_cell._y2) // 2

        color = "gray" if undo else "red"

        canvas.create_line(from_x, from_y, to_x, to_y, fill=color, width=2)



    