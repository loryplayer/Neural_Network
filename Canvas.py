import tkinter as tk


class Draggable_canvas(tk.Frame):
    def __init__(self, root_: tk.Tk):
        tk.Frame.__init__(self, root_)
        self.canvas = tk.Canvas(self, width=root_.winfo_width(), height=root_.winfo_height(), background="bisque")
        self.xsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)

        # self.xsb.grid(row=1, column=0, sticky="ew")
        # self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)

    def scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def get_more_distant_points(self) -> tuple:
        min_x, min_y = self.canvas.bbox(self.canvas.find_all()[0])[0], self.canvas.bbox(self.canvas.find_all()[0])[1]
        max_x, max_y = 0, 0
        for object_id in self.canvas.find_all():
            object_y_min = self.canvas.bbox(object_id)[0]
            if min_x > object_y_min:
                min_x = object_y_min
            object_x_min = self.canvas.bbox(object_id)[1]
            if min_y > object_x_min:
                min_y = object_x_min
            object_y_max = self.canvas.bbox(object_id)[3]
            if max_y < object_y_max:
                max_y = object_y_max
            object_x_max = self.canvas.bbox(object_id)[2]
            if max_x < object_x_max:
                max_x = object_x_max

        return (round(min_x / 10) - 0.5) * 10, (round(min_y / 10) - 0.5) * 10, (round(max_x / 10) + 0.5) * 10, (
                round(max_y / 10) + 0.5) * 10

    def set_scrollregion(self, x_min, y_min, x_f: float, y_f: float):
        self.canvas.configure(scrollregion=(x_min, y_min, x_f, y_f))
