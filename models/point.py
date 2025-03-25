class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  def __eq__(self, other):
    if isinstance(other, Point):
      return (self.x == other.x) and (self.y == other.y)
    return False

  def __ne__(self, other):
    return not self.__eq__(other)
  
  def __gt__(self, other):
    if isinstance(other, Point):
      return (self.x > other.x or (self.x == other.x and self.y > other.y))
    return False
  
  def __ge__(self, other):
    return self.__eq__(other) or self.__gt__(other)
  
  def __lt__(self, other):
    return not self.__eq__(other) and not self.__gt__(other)
  
  def __le__(self, other):
    return self.__eq__(other) or not self.__gt__(other)
  
  def __repr__(self):
    return f"x: {self.x} - y: {self.y}"