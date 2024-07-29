#!/usr/bin/env python
from maze import Window, Maze, Point


def main():

    width, height = (400, 300)
    win = Window(width, height)

    size = 25
    padding = 2
    rows = (height - (padding * 2)) // size
    cols = (width - (padding * 2)) // size
    print(f"size: {size}, padding: {padding}, rows: {rows}, cols: {cols}")

    maze = Maze(2, 2, rows, cols, size, win)

    maze._break_entrance_and_exit()

    win.wait_for_close()



if __name__ == "__main__":
    main()
