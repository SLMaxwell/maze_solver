import platform
import sys
sys.dont_write_bytecode = True

from models.window import Window, Cell, Line
from models.maze import Maze

def main() -> int:
  win = Window(660, 660, platform.system())
  win.maze = Maze(30, 30, 20, 16, 30, win)
  win.maze.solve()
  win.wait_for_close()
  
if __name__ == '__main__':
  main()  # next section explains the use of sys.exit