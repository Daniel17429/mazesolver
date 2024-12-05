import unittest
from maze import Maze

class Tests(unittest.TestCase):
    
    def test_maze_create_cells(self):
        num_cols = 10
        num_rows = 12
        cell_size_x = 10
        cell_size_y = 10

        # Create a Maze instance
        m1 = Maze(0, 0, num_rows, num_cols, cell_size_x, cell_size_y)

        # Test that the number of columns matches the input
        self.assertEqual(len(m1._cells), num_rows)

        # Test that the number of rows matches the input
        self.assertEqual(len(m1._cells[0]), num_cols)
    
    def test_maze_with_different_sizes(self):
        # Test for a small maze
        small_maze = Maze(0, 0, 2, 3, 20, 20)
        self.assertEqual(len(small_maze._cells), 2)
        self.assertEqual(len(small_maze._cells[0]), 3)

        # Test for a larger maze
        large_maze = Maze(0, 0, 20, 15, 15, 15)
        self.assertEqual(len(large_maze._cells), 20)
        self.assertEqual(len(large_maze._cells[0]), 15)
    
        
    def test_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        # Call the method
        m1._break_entrance_and_exit()

        # Check entrance
        self.assertFalse(m1._cells[0][0].has_top_wall, "Top wall of entrance not removed")

        # Check exit
        self.assertFalse(m1._cells[num_rows - 1][num_cols - 1].has_bottom_wall, "Bottom wall of exit not removed")
        
    def test_reset_cells_visited(self):
        num_rows, num_cols = 5, 5
        maze = Maze(0, 0, num_rows, num_cols, 20, 20)

        # Simulate setting some cells to visited
        maze._cells[0][0].visited = True
        maze._cells[2][2].visited = True
        maze._cells[4][4].visited = True

        # Call the method to reset visited status
        maze._reset_cells_visited()

        # Assert all cells have visited set to False
        for row in maze._cells:
            for cell in row:
                self.assertFalse(cell.visited, "Cell's visited property should be False")

    def test_maze_solver(self):
        num_rows, num_cols = 3, 3
        maze = Maze(0, 0, num_rows, num_cols, 20, 20)
        maze._break_walls_r(0, 0)  # Generate a solvable maze
        maze._reset_cells_visited()
        
        solved = maze.solve()
        self.assertTrue(solved, "Maze should be solvable")

if __name__ == "__main__":
    unittest.main()