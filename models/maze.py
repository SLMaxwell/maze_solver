import time
import random
from models.cell import Cell, Point

class Maze:
  def __init__(self, x1, y1, num_cols, num_rows,
               cell_size, win=None, seed=None):
    self.win = win
    self.x = x1
    self.y = y1
    self.num_rows = num_rows
    self.num_cols = num_cols
    self.cell_size = cell_size
    self.solved = False
    self.build_count = 0
    random.seed(seed)

  def _create_cells(self):
    self._cells = []
    self.build_count = 0
    for i in range(self.num_cols):
      self._cells.append([])
      for j in range(self.num_rows):
        self._cells[i].append(
          Cell(self.win, self._cell_loc(i, j), self.cell_size))
    
    if self.win.show_build:
      for i in range(self.num_cols):
        for j in range(self.num_rows):
          self._draw_cell(i, j)

  def _cell_loc(self, i, j):
    return Point(
      x = self.x + (self.cell_size * i),
      y = self.y + (self.cell_size * j))

  def _break_entrance_and_exit(self):
    self._cells[0][0].top = False
    if self.win.show_build:
      self._draw_cell(0, 0)
    self._cells[self.num_cols-1][self.num_rows-1].bottom = False
    if self.win.show_build:
      self._draw_cell(self.num_cols-1, self.num_rows-1)

  def _need_to_visit(self, p):
    c = self._cells[p.x][p.y] if (
        p.x >= 0 and p.y >= 0 and
        p.x < self.num_cols and p.y < self.num_rows) else None
    return (c is not None and not c.visited)

  def _get_visit_list(self, i, j):
    visit = []

    # Above
    p = Point(i, j-1)
    if (self._need_to_visit(p)):
      visit.append(p)
    # Below
    p = Point(i, j+1)
    if (self._need_to_visit(p)):
      visit.append(p)
    # Left
    p = Point(i-1, j)
    if (self._need_to_visit(p)):
      visit.append(p)
    # Right
    p = Point(i+1, j)
    if (self._need_to_visit(p)):
      visit.append(p)

    return visit

  def _break_walls_r(self, i, j):
    self._cells[i][j].visited = True
    while (True):
      visit = self._get_visit_list(i, j)
      if len(visit) == 0:
        self._draw_cell(i, j, self.win.show_build, True)
        return

      pd = visit.pop(random.randint(0, len(visit)-1))
      self.build_count += 1
      self._cells[pd.x][pd.y].num = self.build_count
      if (i == pd.x and j > pd.y):
        # pd is Above current
        self._cells[i][j].top = False
        self._cells[pd.x][pd.y].bottom = False
      if (i == pd.x and j < pd.y):
        # pd is Below current
        self._cells[i][j].bottom = False
        self._cells[pd.x][pd.y].top = False
      if (i > pd.x and j == pd.y):
        # pd is Left of current
        self._cells[i][j].left = False
        self._cells[pd.x][pd.y].right = False
      if (i < pd.x and j == pd.y):
        # pd is Right of current
        self._cells[i][j].right = False
        self._cells[pd.x][pd.y].left = False

      self._break_walls_r(pd.x, pd.y)

  def _reset_cells_visited(self):
    for col in self._cells:
      for cell in col:
        cell.visited = False

  def _solve_r(self, i, j):
    if self.win.animate_solve:
      self._animate()

    current_cell = self._cells[i][j]
    current_cell.visited = True

    if (i==0 and j==0):
      # First Cell Draw entrance
      p1 = current_cell.center()
      p2 = Point(p1.x, p1.y - current_cell.size)
      current_cell.draw_line(p1, p2, "light green")
    
    if (i == self.num_cols-1 and j == self.num_rows-1):
      # Last Cell Show Exit and stop solving.
      p1 = current_cell.center()
      p2 = Point(p1.x, p1.y + current_cell.size)
      current_cell.draw_line(p1, p2, "light green")
      return True
    
    # Above
    p = Point(i, j-1)
    if (not current_cell.top and self._need_to_visit(p)):
      if (self._move_to_r(current_cell, p)):
        return True
    # Below
    p = Point(i, j+1)
    if (not current_cell.bottom and self._need_to_visit(p)):
      if (self._move_to_r(current_cell, p)):
        return True
    # Left
    p = Point(i-1, j)
    if (not current_cell.left and self._need_to_visit(p)):
      if (self._move_to_r(current_cell, p)):
        return True
    # Right
    p = Point(i+1, j)
    if (not current_cell.right and self._need_to_visit(p)):
      if (self._move_to_r(current_cell, p)):
        return True
    
    return False

  def _move_to_r(self, current_cell, p):
    next_cell = self._cells[p.x][p.y]
    current_cell.draw_move(next_cell, show_wrong_turns=self.win.show_wrong_turns, show_num=self.win.show_build_num)
    result = self._solve_r(p.x, p.y)
    if (not result):
      current_cell.draw_move(next_cell, True, self.win.show_wrong_turns, self.win.show_build_num)
    if self.win.animate_solve:
      self._animate()
    return result

  def _draw_cell(self, i, j, animate=True, draw_num=False):
    self._cells[i][j].draw(show_num=self.win.show_build_num and draw_num)
    if animate:
      self._animate()

  def _animate(self):
    if self.win:
      self.win.redraw()
      time.sleep(0.005)
  
  def solve(self):
    self.solved = False
    self._create_cells()
    self._break_entrance_and_exit()
    self._break_walls_r(random.randint(0, self.num_cols-1),
                        random.randint(0, self.num_rows-1))
    self._reset_cells_visited()
    self.solved = self._solve_r(0,0)
    return self.solved