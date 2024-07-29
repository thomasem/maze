import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10)
        self.assertEqual(
            len(m1.cells),
            num_rows,
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_cols,
        )

    def test_maze_break_entrance_and_exit(self):
        m1 = Maze(0, 0, 12, 10, 10)
        m1.break_entrance_and_exit()
        self.assertFalse(m1.cells[0][0].has_top)
        self.assertFalse(m1.cells[-1][-1].has_bottom)


if __name__ == "__main__":
    unittest.main()
