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

    self.draw_line(Point(xl,yt), Point(xr,yt), "black" if self.top else "white")
    self.draw_line(Point(xl,yt), Point(xl,yb), "black" if self.left else "white")
    self.draw_line(Point(xl,yb), Point(xr,yb), "black" if self.bottom else "white")
    self.draw_line(Point(xr,yb), Point(xr,yt), "black" if self.right else "white")

  def draw_move(self, to_cell, undo=False, show_solve=False):
    backtrack_color = "light grey" if show_solve else "white"
    self.draw_line(self.center(), to_cell.center(), backtrack_color if undo else "red")

  def draw_line(self, p1, p2, color):
    if self.win:
      self.win.draw_line(Line(p1, p2), color)