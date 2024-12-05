from tkinter import Tk, BOTH, Canvas
import time
from window import Window, Point, Line, Cell
import random
class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        if seed is not None:
            random.seed(seed)

        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        

    def _create_cells(self):
        for row in range(self.num_rows):
            row_cells = []
            for col in range(self.num_cols):
                x1 = self.x1 + col * self.cell_size_x
                y1 = self.y1 + row * self.cell_size_y
                x2 = x1 + self.cell_size_x
                y2 = y1 + self.cell_size_y

                # Initialize Cell
                cell = Cell(x1, y1, x2, y2, self.win)
                row_cells.append(cell)
           
            # Append row to _cells
            self._cells.append(row_cells)
        
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self._draw_cell(row, col)
               
    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        if self.win is not None:
            cell.draw()
        
        self._animate()

    def _animate(self):
        if self.win is None:
            return 
        self.win.redraw()
        time.sleep(0.05)
    
    def _break_entrance_and_exit(self):
        
        top_left_cell = self._cells[0][0]
        bottom_right_cell = self._cells[self.num_rows - 1][self.num_cols - 1]
                
        top_left_cell.has_top_wall = False
        self._draw_cell(0, 0)
               
        bottom_right_cell.has_bottom_wall = False
        self._draw_cell(self.num_rows - 1, self.num_cols - 1)

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True

        while True:
            directions = []
            if i > 0 and not self._cells[i - 1][j].visited:  # Up
                directions.append((-1, 0, "top", "bottom"))
            if i < self.num_rows - 1 and not self._cells[i + 1][j].visited:  # Down
                directions.append((1, 0, "bottom", "top"))
            if j > 0 and not self._cells[i][j - 1].visited:  # Left
                directions.append((0, -1, "left", "right"))
            if j < self.num_cols - 1 and not self._cells[i][j + 1].visited:  # Right
                directions.append((0, 1, "right", "left"))

            if not directions:
                # No more moves; return to exit recursion
                self._draw_cell(i, j)
                return

            # Pick a random direction
            di, dj, wall_to_remove, opposite_wall = random.choice(directions)

            # Knock down the walls between current and chosen cells
            next_cell = self._cells[i + di][j + dj]
            setattr(current_cell, f"has_{wall_to_remove}_wall", False)
            setattr(next_cell, f"has_{opposite_wall}_wall", False)

            # Move to the next cell recursively
            self._break_walls_r(i + di, j + dj)
    def _reset_cells_visited(self):
        """Resets the 'visited' property of all cells in the maze to False."""
        for row in self._cells:
            for cell in row:
                cell.visited = False    
    def solve(self):
        """Attempts to solve the maze starting from the top-left cell (0, 0)."""
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True

        if i == self.num_rows - 1 and j == self.num_cols - 1:  # Goal cell
            return True

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dy, dx in directions:
            ni, nj = i + dy, j + dx

            if 0 <= ni < self.num_rows and 0 <= nj < self.num_cols:  # Bounds check
                next_cell = self._cells[ni][nj]
                if not next_cell.visited and self._can_move(current_cell, next_cell, dy, dx):
                    current_cell.draw_move(next_cell)  # Draw move
                    if self._solve_r(ni, nj):  # Recursive call
                        return True
                    current_cell.draw_move(next_cell, undo=True)  # Undo move

        return False
    
    def _can_move(self, current_cell, next_cell, dy, dx):
        """Determines if the move between two cells is valid based on walls."""
        if dy == -1:  # Moving up
            return not current_cell.has_top_wall and not next_cell.has_bottom_wall
        elif dy == 1:  # Moving down
            return not current_cell.has_bottom_wall and not next_cell.has_top_wall
        elif dx == -1:  # Moving left
            return not current_cell.has_left_wall and not next_cell.has_right_wall
        elif dx == 1:  # Moving right
            return not current_cell.has_right_wall and not next_cell.has_left_wall
        return False