#!/usr/bin/env python
import tkinter


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def draw(self, canvas: tkinter.Canvas, fill_color: str):
        canvas.create_line(
            self.start.x, self.start.y,
            self.end.x, self.end.y,
            fill=fill_color, width=2,
        )


class Window:
    def __init__(self, width: int, height: int):
        self.__root = tkinter.Tk()
        self.__root.title('A-Maze-ing MAZE')
        self.__root.protocol('WM_DELETE_WINDOW', self.close)

        self.__canvas = tkinter.Canvas(width=width, height=height)
        self.__canvas.pack()

        self._running = False
    
    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.__canvas, fill_color=fill_color)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self._running = True
        while self._running:
            self.redraw()

    def running(self) -> bool:
        return self._running

    def close(self):
        self._running = False


class Cell:
    def __init__(self, top_left: Point, bottom_right: Point, window: Window):
        self._top_left = top_left
        self._top_right = Point(bottom_right.x, top_left.y)
        self._bottom_left = Point(top_left.x, bottom_right.y)
        self._bottom_right = bottom_right
        self._window = window

        self.left_wall = True
        self.right_wall = True
        self.top_wall = True
        self.bottom_wall = True

    def draw(self):
        lines = []
        if self.top_wall:
            lines.append(Line(self._top_left, self._top_right))
        if self.right_wall:
            lines.append(Line(self._top_right, self._bottom_right))
        if self.bottom_wall:
            lines.append(Line(self._bottom_right, self._bottom_left))
        if self.left_wall:
            lines.append(Line(self._bottom_left, self._top_left))
        
        for line in lines:
            self._window.draw_line(line, "black")


def main():
    win = Window(800, 600)

    cell = Cell(Point(2, 2), Point(22, 22), win)
    cell.draw()

    win.wait_for_close()


main()
