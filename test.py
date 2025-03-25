import unittest
import sys
sys.dont_write_bytecode = True

from models.maze import Maze

class Tests(unittest.TestCase):
  def test_maze_create_eq(self):
    num_cols = 10
    num_rows = 10
    m1 = Maze(0, 0, num_cols, num_rows, 10)
    self.assertEqual(
      len(m1._cells),
      num_cols,
    )
    self.assertEqual(
      len(m1._cells[0]),
      num_rows,
    )

  def test_maze_create_sm(self):
    num_cols = 1
    num_rows = 1
    m1 = Maze(0, 0, num_cols, num_rows, 100)
    self.assertEqual(
      len(m1._cells),
      num_cols,
    )
    self.assertEqual(
      len(m1._cells[0]),
      num_rows,
    )
  
  def test_maze_create_lg(self):
    num_cols = 100
    num_rows = 10
    m1 = Maze(0, 0, num_cols, num_rows, 10)
    self.assertEqual(
      len(m1._cells),
      num_cols,
    )
    self.assertEqual(
      len(m1._cells[0]),
      num_rows,
    )

  def test_entrance_exit_size(self):
    num_cols = 16
    num_rows = 16
    size = 30
    m1 = Maze(0, 0, num_cols, num_rows, size)
    self.assertFalse(m1._cells[0][0].top) # Entrance Open
    self.assertFalse(m1._cells[15][15].bottom) # Exit Open
    self.assertEqual(m1._cells[7][3].size, size)

  def test_all_cells_free(self):
    num_cols = 16
    num_rows = 16
    size = 30
    m1 = Maze(0, 0, num_cols, num_rows, size, None, 0)
    for col in m1._cells:
      for cell in col:
        self.assertFalse(cell.visited)

  def test_maze_solved(self):
    num_cols = 16
    num_rows = 16
    size = 30
    m1 = Maze(0, 0, num_cols, num_rows, size, None, 0)
    self.assertTrue(m1.solve())
    # for col in m1._cells:
    #   for cell in col:
    #     self.assertTrue(cell.visited)
  
if __name__ == "__main__":
  unittest.main()