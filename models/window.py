from tkinter import Tk, BOTH, Canvas
from models.cell import Cell, Line, Point

class Window:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.root_tk = Tk()
    self.root_tk.title("Maze Solver")
    self.canvas = Canvas(
      self.root_tk, bg="white",
      height=self.height, width=self.width)
    self.canvas.pack()
    self.running = False
    self.root_tk.protocol("WM_DELETE_WINDOW", self.close)
    self.root_tk.bind("<KeyPress>", self.handle_keypress)
    self.maze = None

    self.show_build = True
    self.show_solve = False
    self.animate_solve = True
    self.animate_fast_solve = False

  def redraw(self):
    self.root_tk.update_idletasks()
    self.root_tk.update()

  def wait_for_close(self):
    self.running = True

    while self.running:
      self.redraw()

  def close(self):
    self.running = False

  def draw_line(self, line, fill_color):
    line.draw(self.canvas, fill_color)

  def handle_keypress(self, event):
    print(f"char: {event.char} - sym: {event.keysym} - num: {event.keysym_num}")
    
    if (event.keysym == 'space' and self.maze and self.maze.solved):
      self.canvas.delete("all")
      self.maze.solve()

    if (event.keysym == 'b'):
      self.show_build = not self.show_build
      print(f"Show build: {"On" if self.show_build else "Off"}!")
    if (event.keysym == 'f'):
      self.animate_fast_solve = not self.animate_fast_solve
      print(f"Animate Fast Solve: {"On" if self.animate_fast_solve else "Off"}!")
    if (event.keysym == 'a'):
      self.animate_solve = not self.animate_solve
      print(f"Animate Solve: {"On" if self.animate_solve else "Off"}!")
    if (event.keysym == 's'):
      self.show_solve = not self.show_solve
      print(f"Show Solve: {"On" if self.show_solve else "Off"}!")

    if (event.keysym == 'Escape'):
      self.close()
