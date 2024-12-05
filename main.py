from window import Window, Point, Line, Cell
from maze import Maze

def main():
    win = Window(800, 800)
    
    num_rows = 15
    num_cols = 15
    m1 = Maze(15, 15, num_rows, num_cols, 50, 50, win)
    
    m1.solve()

    win.wait_for_close()


main()
