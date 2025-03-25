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
  
def log_points(p1, p2):
  print(f"p1: {p1} - p2: {p2}")
  print(f"  eq: {p1 == p2}")
  print(f"  ne: {p1 != p2}")
  print(f"  lt: {p1 < p2}")
  print(f"  le: {p1 <= p2}")
  print(f"  gt: {p1 > p2}")
  print(f"  ge: {p1 >= p2}")
  print()


p1 = Point(10, 20)
p2 = Point(10, 20)
log_points(p1, p2)
p2.y = 15
log_points(p1, p2)
p2.y = 25
log_points(p1, p2)
p2.y = 20
p2.x = 5
log_points(p1, p2)
p2.x = 15
log_points(p1, p2)
p2.y = 25
log_points(p1, p2)
p2.x = 5
p2.y = 15
log_points(p1, p2)