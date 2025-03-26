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
    self.show_build_num = False
    self.animate_solve = True
    self.show_wrong_turns = False
    self.manual_solve = False

    self.reset_window()

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
    return line.draw(self.canvas, fill_color)
  
  def reset_window(self):
    self.canvas.delete("all")
    self.instructions={}
    self.show_instructions()
  
  def show_instructions(self):

    build = f"b: Animate Build - [{"On" if self.show_build else "Off"}]"
    build_nums = f"n: Show Build Numbers - [{"On" if self.show_build_num else "Off"}]"
    wrong_turns = f"s: Show Wrong Turns - [{"On" if self.show_wrong_turns else "Off"}]"
    animate = f"a: Animate Solve - [{"On" if self.animate_solve else "Off"}]"
    manual_solve = f"m: Manual Solve Mode - [{"On" if self.manual_solve else "Off"}]"

    if len(self.instructions) == 0:
      self.instructions['controls'] = self.draw_text(Point(30, 540), "Controls", "underline")
      self.instructions['esc'] = self.draw_text(Point(30, 570), "ESC: Exit Maze Solver")
      self.instructions['space'] = self.draw_text(Point(30, 590), "Space: Generate New Maze")

      self.instructions['settings'] = self.draw_text(Point(400, 540), "Settings", "underline")
      self.instructions['build'] = self.draw_text(Point(400, 570), build)
      self.instructions['build_nums'] = self.draw_text(Point(400, 590), build_nums)
      self.instructions['animate'] = self.draw_text(Point(400, 610), animate)
      self.instructions['wrong_turns'] = self.draw_text(Point(400, 630), wrong_turns)
      self.instructions['manual_solve'] = self.draw_text(Point(400, 650), manual_solve)
    else:
      self.canvas.itemconfigure(self.instructions['build'], text = build)
      self.canvas.itemconfigure(self.instructions['build_nums'], text = build_nums)
      self.canvas.itemconfigure(self.instructions['animate'], text = animate)
      self.canvas.itemconfigure(self.instructions['manual_solve'], text = manual_solve)
      self.canvas.itemconfigure(self.instructions['wrong_turns'], text = wrong_turns)

  def draw_text(self, p, text, font=''):
    return self.canvas.create_text(
        p.x,p.y, anchor="sw", fill="black", font=f"Arial 10 {font}", text=text)

  def handle_keypress(self, event):
    # print(f"char: {event.char} - sym: {event.keysym} - num: {event.keysym_num}")
    match event.keysym:
      case 'space':
        if self.maze and self.maze.solved:
          self.reset_window()
          self.maze.solve()
      case 'Escape':
        self.close()
      case 'b':
        self.show_build = not self.show_build
        self.show_instructions()
      case 'a':
        self.animate_solve = not self.animate_solve
        self.manual_solve = False
        self.show_instructions()
      case 's':
        self.show_wrong_turns = not self.show_wrong_turns
        self.show_instructions()
      case 'n':
        self.show_build_num = not self.show_build_num
        self.show_instructions()
      case 'm':
        self.manual_solve = not self.manual_solve
        self.animate_solve = False
        self.show_instructions()
