import time
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
        self.root = tkinter.Tk()
        self.root.title('A-Maze-ing MAZE')
        self.root.protocol('WM_DELETE_WINDOW', self.close)

        self.canvas = tkinter.Canvas(width=width, height=height)
        self.canvas.pack()

        self._running = False
    
    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color=fill_color)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()
    
    def wait_for_close(self):
        self._running = True
        while self._running:
            self.redraw()

    def running(self) -> bool:
        return self._running

    def close(self):
        self._running = False


class Cell:
    def __init__(
        self,
        top_left: Point,
        size: int,
        window: Window,
        has_left: bool = True,
        has_right: bool = True,
        has_top: bool = True,
        has_bottom: bool = True,
    ):
        bottom_right = Point(top_left.x + size, top_left.y + size)
        self.top_left = top_left
        self.bottom_right = bottom_right

        self.top_right = Point(self.bottom_right.x, self.top_left.y)
        self.bottom_left = Point(self.top_left.x, self.bottom_right.y)
        self.window = window

        self.has_left = has_left
        self.has_right = has_right
        self.has_top = has_top
        self.has_bottom = has_bottom

    def draw(self):
        clr = lambda has: "black" if has else "#d9d9d9"
        lines = [
            (Line(self.top_left, self.top_right), clr(self.has_top)),
            (Line(self.top_right, self.bottom_right), clr(self.has_right)),
            (Line(self.bottom_right, self.bottom_left), clr(self.has_bottom)),
            (Line(self.bottom_left, self.top_left), clr(self.has_left)),
        ]
        for line, color in lines:
            self.window.draw_line(line, color)

    def middle_point(self) -> Point:
        x = self.top_left.x + ((self.top_right.x - self.top_left.x) // 2)
        y = self.top_left.y + ((self.bottom_left.y - self.top_left.y) // 2)
        return Point(x, y)

    def draw_move(self, to_cell: 'Cell', undo: bool = False):
        color = "gray" if undo else "red"
        line = Line(self.middle_point(), to_cell.middle_point())
        self.window.draw_line(line, color)


class Maze:
    def __init__(
        self,
        x: int, 
        y: int,
        rows: int,
        cols: int,
        size: int,
        window: Window | None = None,
    ):
        self.start = Point(x, y)
        self.rows = rows
        self.cols = cols
        self.size = size

        if not window:
            window = Window(400, 300)
        self.window = window

        self.cells = []
        self.create_cells()

    def create_cells(self):
        for i in range(self.rows):
            self.cells.append([])
            y = self.start.y + (self.size * i)
            for j in range(self.cols):
                x = self.start.x + (self.size * j)
                point = Point(x, y)
                self.cells[i].append(Cell(point, self.size, self.window))
                self.draw_cell(i, j)
    
    def break_entrance_and_exit(self):
        if not self.cells:
            return
        self.cells[0][0].has_top = False
        self.draw_cell(0, 0)
        self.cells[-1][-1].has_bottom = False
        self.draw_cell(-1, -1)

    def draw_cell(self, row: int, col: int):
        self.cells[row][col].draw()
        self.animate()

    def animate(self):
        self.window.redraw()
        time.sleep(.01)
