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
    self.num = 0
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

  def draw(self, loc=None, size=None, show_num=False):
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
    
    self.win.canvas.itemconfigure(self.top_id, fill="black" if self.top else "white")
    self.win.canvas.itemconfigure(self.left_id, fill="black" if self.left else "white")
    self.win.canvas.itemconfigure(self.bottom_id, fill="black" if self.bottom else "white")
    self.win.canvas.itemconfigure(self.right_id, fill="black" if self.right else "white")

    if show_num:
      self.draw_num()

  def draw_move(self, to_cell, undo=False, show_wrong_turns=False, show_num=False):
    backtrack_color = "light grey" if show_wrong_turns else "white"
    color = backtrack_color if undo else "red"
    if to_cell.num not in self.move_ids:
      self.move_ids[to_cell.num] = self.draw_line(self.center(), to_cell.center(), color)
    else:
      self.win.canvas.itemconfigure(self.move_ids[to_cell.num], fill=color)

    if undo and show_num:
      self.draw_num()
      to_cell.draw_num()

  def draw_line(self, p1, p2, color):
    id = 0
    if self.win:
      id = self.win.draw_line(Line(p1, p2), color)
    return id
  
  def draw_num(self):
    if self.win:
      c = self.center()
      if self.num_id == 0:
        self.num_id = self.win.canvas.create_text(
        c.x,c.y, fill="darkblue", font="Arial 8 italic bold", text=self.num)
      self.win.canvas.tag_raise(self.num_id)