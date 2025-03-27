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
    self.visited = False
    self.num = None
    self.num_id = 0
    self.top_id = 0
    self.left_id = 0
    self.bottom_id = 0
    self.right_id = 0
    self.move_ids = {}

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
    return f"({self.loc.x//self.size}, {self.loc.y//self.size})"

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
      self.top_id = self.draw_line(Point(xl,yt), Point(xr,yt), "black")
      self.left_id = self.draw_line(Point(xl,yt), Point(xl,yb), "black")
      self.bottom_id = self.draw_line(Point(xl,yb), Point(xr,yb), "black")
      self.right_id = self.draw_line(Point(xr,yb), Point(xr,yt), "black")
    
    self.win.canvas.itemconfig(self.top_id, state=self.win.view_state(self.top))
    self.win.canvas.itemconfig(self.left_id, state=self.win.view_state(self.left))
    self.win.canvas.itemconfig(self.bottom_id, state=self.win.view_state(self.bottom))
    self.win.canvas.itemconfig(self.right_id, state=self.win.view_state(self.right))

    self.draw_num()

  def draw_move(self, to_cell, undo=False, tag="solution"):
    color = "light grey" if undo else "red"
    if to_cell.num not in self.move_ids:
      self.move_ids[to_cell.num] = self.draw_line(self.center(), to_cell.center(), color, tags=tag)
    
    visible = False
    if tag == "solution" and not self.win.manual_solve:
      visible = True
    if tag == "manual_solution" and self.win.manual_solve:
      visible = True
    if undo and visible and not self.win.show_wrong_turns:
      visible = False
    if undo:
      tag += "-wrong_turns"

    self.win.canvas.itemconfig(self.move_ids[to_cell.num], fill=color, tags=tag, state=self.win.view_state(visible))

    if undo:
      self.draw_num()
      to_cell.draw_num()

  def draw_line(self, p1, p2, color, tags=None):
    id = 0
    if self.win:
      id = self.win.draw_line(Line(p1, p2), color, tags)
    return id
  
  def draw_num(self):
    if self.win:
      if self.num_id == 0 and self.num is not None:
        c = self.center()
        self.num_id = self.win.canvas.create_text(
          c.x, c.y, fill="darkblue",
          font=(self.win.font, self.win.font_size, 'italic'),
          state=self.win.view_state(self.win.show_build_num),
          text=self.num, tags="build_num")
        
      self.win.canvas.tag_raise(self.num_id)