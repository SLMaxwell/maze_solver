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
    self.man_solved = False
    self.build_count = 0
    self.man_index = Point(0,0)

    random.seed(seed)

  def _create_cells(self):
    self._cells = []
    self.build_count = 0
    for i in range(self.num_cols):
      self._cells.append([])
      for j in range(self.num_rows):
        self._cells[i].append(
          Cell(self.win, self._cell_loc(i, j), self.cell_size))
    
    for i in range(self.num_cols):
      for j in range(self.num_rows):
        self._draw_cell(i, j)

  def _cell_loc(self, i, j):
    return Point(
      x = self.x + (self.cell_size * i),
      y = self.y + (self.cell_size * j))

  def _break_entrance_and_exit(self):
    self._cells[0][0].top = False
    self._draw_cell(0, 0)
    self._cells[self.num_cols-1][self.num_rows-1].bottom = False
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
    cur_cell = self._cells[i][j]
    cur_cell.visited = True
    if cur_cell.num is None:
      cur_cell.num = self.build_count
    while (True):
      visit = self._get_visit_list(i, j)
      if len(visit) == 0:
        self._draw_cell(i, j)
        return

      pd = visit.pop(random.randint(0, len(visit)-1))
      self.build_count += 1
      next_cell = self._cells[pd.x][pd.y]
      next_cell.num = self.build_count
      if (i == pd.x and j > pd.y):
        # pd is Above current
        cur_cell.top = False
        next_cell.bottom = False
      if (i == pd.x and j < pd.y):
        # pd is Below current
        cur_cell.bottom = False
        next_cell.top = False
      if (i > pd.x and j == pd.y):
        # pd is Left of current
        cur_cell.left = False
        next_cell.right = False
      if (i < pd.x and j == pd.y):
        # pd is Right of current
        cur_cell.right = False
        next_cell.left = False

      self._break_walls_r(pd.x, pd.y)

  def _reset_cells_visited(self):
    for col in self._cells:
      for cell in col:
        cell.reset()

  def _solve_r(self, i, j):
    self._animate(self.win.animate_solve)

    current_cell = self._cells[i][j]
    current_cell.visited = True

    if (i==0 and j==0):
      # First Cell Draw entrance
      p1 = current_cell.center()
      p2 = Point(p1.x, p1.y - current_cell.size)
      current_cell.draw_line(p1, p2, self.win.colors['entrance'], 'entrance')
    
    if (i == self.num_cols-1 and j == self.num_rows-1):
      # Last Cell Show Exit and stop solving.
      p1 = current_cell.center()
      p2 = Point(p1.x, p1.y + current_cell.size)
      current_cell.draw_line(p1, p2, self.win.colors['exit'], 'exit')
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
    current_cell.draw_move(next_cell)
    self._animate(self.win.animate_solve)

    result = self._solve_r(p.x, p.y)
    if (not result):
      current_cell.draw_move(next_cell)
      self._animate(self.win.animate_solve)

    return result

  def _draw_cell(self, i, j):
    self._cells[i][j].draw()
    self._animate(self.win.show_build)

  def _animate(self, process):
    if self.win and process:
      self.win.redraw()
      time.sleep(0.005)
  
  def solve(self, new_maze=True):
    if new_maze:
      self._create_cells()
      self._break_entrance_and_exit()
      self._break_walls_r(random.randint(0, self.num_cols-1),
                          random.randint(0, self.num_rows-1))
    self.solved = False
    self._reset_cells_visited()
    self.solved = self._solve_r(0,0)
    self._reset_cells_visited()
    self.man_solved = False
    self.man_index = Point(0,0)
    self._cells[self.man_index.x][self.man_index.y].visited = True
    return self.solved
  
  def manual_move(self, direction):
    # Only allow moving when in manual mode.
    if self.man_solved == True:
      return
    
    current_cell = self._cells[self.man_index.x][self.man_index.y]
    next_index = Point(self.man_index.x, self.man_index.y)
    match direction:
      case 'up':
        if not current_cell.top and next_index.y > 0:
          next_index.y -= 1
      case 'down':
        if not current_cell.bottom:
          next_index.y += 1
      case 'left':
        if not current_cell.left:
          next_index.x -= 1
      case 'right':
        if not current_cell.right:
          next_index.x += 1

    # print(f"moving: {direction.lower()} - Curr Cell: {current_cell} - Man index: {self.man_index} - Next Index: {next_index}")
    if next_index.y == self.num_rows:
      self.man_solved = True
      self.win.canvas.itemconfig("manual_solution-good", fill=self.win.colors['exit'])
    elif next_index != self.man_index:
      next_cell = self._cells[next_index.x][next_index.y]
      current_cell.draw_move(next_cell, "manual_solution")
      next_cell.visited = True
      self.man_index = next_index
      self._animate(True)