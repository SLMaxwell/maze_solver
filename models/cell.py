from models.point import Point
from models.line import Line

class Cell:
  def __init__(self, win, loc=Point(0,0), size=0,
               top=True, left=True, bottom=True, right=True):
    self.win = win
    self.loc = loc
    self.size = size
    self.top = top
    self.left = left
    self.bottom = bottom
    self.right = right

    # Build state
    self.num = None
    self.num_id = 0
    self.top_id = 0
    self.left_id = 0
    self.bottom_id = 0
    self.right_id = 0

    # Solve State
    self.visited = False # Used in Build too.
    self.move_ids = {'solution':{}, 'manual_solution':{}}

  def __eq__(self, other):
    if isinstance(other, Cell):
      return self.loc == other.loc
    return False

  def __ne__(self, other):
    return not self.__eq__(other)
  
  def __gt__(self, other):
    if isinstance(other, Point):
      return self.loc > other.loc
    return False
  
  def __ge__(self, other):
    return self.__eq__(other) or self.__gt__(other)
  
  def __lt__(self, other):
    return not self.__eq__(other) and not self.__gt__(other)
  
  def __le__(self, other):
    return self.__eq__(other) or not self.__gt__(other)

  def __repr__(self):
    return f"{self.num} ({self.num_id}): ({self.loc.x//self.size}, {self.loc.y//self.size})"

  def center(self):
    return Point(self.loc.x + self.size/2, self.loc.y + self.size/2)

  def draw(self, loc=None, size=None):
    if (loc is not None and self.loc != loc):
      self.loc = loc
    if (size is not None and self.size != size):
      self.size = size

    xl = self.loc.x
    yt = self.loc.y
    xr = xl + self.size
    yb = yt + self.size

    if self.top_id == 0:
      self.top_id = self.draw_line(Point(xl,yt), Point(xr,yt), self.win.colors['wall'])
      self.left_id = self.draw_line(Point(xl,yt), Point(xl,yb), self.win.colors['wall'])
      self.bottom_id = self.draw_line(Point(xl,yb), Point(xr,yb), self.win.colors['wall'])
      self.right_id = self.draw_line(Point(xr,yb), Point(xr,yt), self.win.colors['wall'])
    
    self.win.canvas.itemconfig(self.top_id, state=self.win.view_state(self.top))
    self.win.canvas.itemconfig(self.left_id, state=self.win.view_state(self.left))
    self.win.canvas.itemconfig(self.bottom_id, state=self.win.view_state(self.bottom))
    self.win.canvas.itemconfig(self.right_id, state=self.win.view_state(self.right))

    self.draw_num()

  def draw_move(self, to_cell, solution="solution"):
    # The move line key will always be the 2 cells that it connects.
    key = f"{min(self.num, to_cell.num)}-{max(self.num, to_cell.num)}"
    if key not in self.move_ids[solution]:
      # First Time Move - draw the base line and add it to both cells
      line = {'id': None, 'color': None}
      line['id'] = self.draw_line(self.center(), to_cell.center())
      self.move_ids[solution][key] = line
      to_cell.move_ids[solution][key] = line
    else:
      # Get the line data from either cell
      line = self.move_ids[solution][key]

    # Toggle the color based upon what it was the last time it was drawn.
    # This allows us to see the wrong_turn only when "backtracking" over the same path.
    last_color = line['color']
    color = self.win.colors['wrong_turns'] if last_color == self.win.colors[solution] else self.win.colors[solution]
    line['color'] = color

    # The Move is an undo only when it was a "wrong turn"
    undo = (color == self.win.colors['wrong_turns'])

    # Set visiblity based upon the users settings.
    visible = False
    if solution == "solution" and not self.win.manual_solve:
      visible = True
    if solution == "manual_solution" and self.win.manual_solve:
      visible = True
    if undo and visible and not self.win.show_wrong_turns:
      visible = False
    
    wrong_turns = f"{solution}-wrong_turns" if undo else f"{solution}-good"
    tags = (solution, wrong_turns, 'moves')
    state = self.win.view_state(visible)

    # print(f"To: {to_cell} - Visited: {to_cell.visited} Line: {line['id']} undo: {undo} color: {color} solution: {solution}")
    self.win.canvas.itemconfig(line['id'], fill=color, tags=tags, state=state)
    self.win.canvas.tag_raise(self.num_id)
    self.win.canvas.tag_raise(to_cell.num_id)

  def draw_line(self, p1, p2, color=None, tags=None):
    id = 0
    if self.win:
      id = self.win.draw_line(Line(p1, p2), color, tags)
    return id

  def draw_num(self):
    if self.win:
      if self.num_id == 0 and self.num is not None:
        c = self.center()
        self.num_id = self.win.canvas.create_text(
          c.x, c.y, fill=self.win.colors['num'],
          font=(self.win.font, self.win.font_size, 'italic'),
          state=self.win.view_state(self.win.show_build_num),
          text=self.num, tags="build_num")

  def reset(self):
    self.visited = False
    self.move_ids = {'solution':{}, 'manual_solution':{}}