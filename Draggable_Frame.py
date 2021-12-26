import math
import tkinter as tk
from pygame.math import Vector2


class Vector2_extended(Vector2):
    def __init__(self, *args):
        Vector2.__init__(self, *args)

    def is_in_range(self, pa, pb):
        # print(self, pa, pb, sep=', ')
        '''if pa.y < pb.y else pb.y  if pb.y > pa.y else pa.y'''
        if pa.x <= self.x <= pb.x and (pa.y if pa.y < pb.y else pb.y) <= self.y <= (pb.y if pb.y > pa.y else pa.y):
            return True
        return False


class Canvas(tk.Canvas):
    def __init__(self, root_win, **kwargs):
        tk.Frame(root_win, kwargs)
        tk.Canvas.__init__(self, root_win, kwargs)
        self.objects = {'q': [], 'c': [], 'l': [], 't': []}

    def draw_rectangle(self, x0, y0, x1, y1, **kwargs):
        type_of_object = 'q'
        rectangle_id = self.create_rectangle(x0, y0, x1, y1, **kwargs)
        self.objects.get(type_of_object).append(rectangle_id)
        return rectangle_id

    def draw_circle(self, cx, cy, r, **kwargs):
        type_of_object = 'c'
        coords = (cx - r, cy - r, cx + r, cy + r)
        consider = kwargs.get('consider') if kwargs.get('consider') is not None else True
        if kwargs.get('consider') is not None:
            kwargs.__delitem__('consider')
        circle_id = self.create_oval(*coords, **kwargs)
        if consider:
            self.objects.get(type_of_object).append(circle_id)
        return circle_id

    def draw_txt(self, x0, y0, **kwargs):
        type_of_object = 't'
        txt_id = self.create_text(x0, y0, **kwargs)
        self.objects.get(type_of_object).append(txt_id)
        return txt_id

    def draw_line(self, x0, y0, x1, y1, **kwargs):
        arrow = kwargs.get('arrow')
        show_intersections = kwargs.get('show_intersections') if kwargs.get('show_intersections') is not None else False
        offset_collision = kwargs.get('offset_collision') if kwargs.get('offset_collision') is not None else 0
        if arrow is not None:
            kwargs.__delitem__('arrow')
        type_of_object = 'l'
        line_coord_of_collisions = []
        a = y1 - y0
        b = x0 - x1
        ab = (y1 - y0, x1 - x0)
        c = y0 * x1 - x0 * y1
        # print(f"a: {a}, b: {b}, c: {c}")
        angle = (math.atan2(y1 - y0, x1 - x0))
        # print(angle)
        m = -a / b
        q = -c / b
        line_xy = [(x0, x1), (y0, y1)]
        for object_id in self.objects.get('q') + self.objects.get('t'):
            bbox = self.bbox(object_id)
            # print(f"bbox: {bbox}")
            # print(f"NUOVO OGGETTO: {object_id}")
            for n_ in range(2):
                for k in range(2):
                    # print(2 * k)
                    if n_ == 1 and m == 0: break
                    value = (bbox[2 * k] * m + q) if n_ == 0 else ((bbox[1 + 2 * k] - q) / m)
                    # print(
                    #    f"bbox: {bbox[n_ + 2 * k]}; ab: {ab}; linea: {line_xy[n_][0 if ab[n_] > 0 else 1]}; "
                    #    f"lineb: {line_xy[n_][1 if ab[n_] > 0 else 0]}")

                    if Vector2_extended(
                            Vector2((bbox[2 * k], value) if n_ == 0 else (value, bbox[1 + 2 * k]))).is_in_range(
                        Vector2(x0, y0), Vector2(x1, y1)):
                        # print("dentro")
                        if bbox[1 - n_] <= value <= bbox[3 - n_]:
                            # print("collisione")
                            # radius = 5
                            line_coord_of_collisions.append((bbox[2 * k], value) if n_ == 0 else (
                                value, bbox[1 + 2 * k]))

        # print(self.objects.get('q') + self.objects.get('t'))
        # def is_in_range(point: Vector2, : Vector2, P2: Vector2):
        # print(line_coord_of_collisions)
        for object_id in self.objects.get('c'):
            bbox = self.bbox(object_id)
            radius = abs(bbox[2] - bbox[0]) / 2
            cx = bbox[0] + radius
            cy = bbox[1] + radius
            Q = Vector2_extended(cx, cy)
            P1 = Vector2_extended(x0, y0)
            P2 = Vector2_extended(x1, y1)
            # print(P2)
            V: [Vector2_extended] = P2 - P1
            a_circle = V.dot(V)
            b_circle = 2 * V.dot(P1 - Q)
            c_circle = P1.dot(P1) + Q.dot(Q) - 2 * P1.dot(Q) - radius ** 2
            disc = b_circle ** 2 - 4 * a_circle * c_circle
            # print(f"Disc: {disc}")
            if disc > 0:
                sqrt_disc = math.sqrt(disc)
                t1 = (-b_circle + sqrt_disc) / (2 * a_circle)
                t2 = (-b_circle - sqrt_disc) / (2 * a_circle)
                point_a: [Vector2_extended] = Vector2_extended(P1 + t1 * V)
                point_b: [Vector2_extended] = Vector2_extended(P1 + t2 * V)
                # if P1 >= point_a >= P2 and P1 >= point_b >= P2:
                if point_a.is_in_range(P1, P2):
                    line_coord_of_collisions.append((point_a[0], point_a[1]))
                    # self.draw_circle(point_a[0], point_a[1], 5, consider=False)
                # else:
                # print(f"Punto a: {point_a}")
                if point_b.is_in_range(P1, P2):
                    line_coord_of_collisions.append((point_b[0], point_b[1]))
                    # self.draw_circle(point_b[0], point_b[1], 5, consider=False)
                # else:
                # print(f"Punto b: {point_b}")
        line_coord_of_collisions.sort(reverse=False if (x0, y0) < (x1, y1) else True)
        # print(line_coord_of_collisions)

        if show_intersections:
            for coords in line_coord_of_collisions:
                print(coords)
                self.draw_circle(*coords, 5, consider=False)

        def adder(list_obj: tuple, value_: float) -> tuple:
            diff = ()
            value_cos = value_ * math.cos(angle)
            value_sin = value_ * math.sin(angle)
            for k, item in enumerate(list_obj):
                val = value_cos if k == 0 else value_sin
                # print(val)
                diff += (item + val,)
            # self.draw_circle(*(109, 84.17931034482758), 5, outline='red', consider=False)
            return diff

        def check_collision(point):
            for object_id_ in self.objects.get('q') + self.objects.get('t'):
                bbox_ = self.bbox(object_id_)
                if bbox_[0] <= point[0] <= bbox_[2] and bbox_[1] <= point[1] <= bbox_[3]:
                    return True
            for object_id_ in self.objects.get('c'):
                bbox_ = self.bbox(object_id_)
                radius_ = (abs(bbox_[2] - bbox_[0]) / 2)
                cx_ = bbox_[0] + radius_
                cy_ = bbox_[1] + radius_
                if point.distance_to(Vector2(cx_, cy_)) < radius_:
                    return True
            return False

        line_coord_of_collisions_fixed = []
        for k, tuple_ in enumerate(line_coord_of_collisions):
            # print((1 if k % 2 == (0 if angle > 0 else 1) else -1))
            # print(f"check_collision(Vector2({x0}, {y0})): {check_collision(Vector2(x0, y0))}")
            line_coord_of_collisions_fixed.append(
                adder(tuple_, offset_collision * (
                    1 if k % 2 == 0 else -1)))
        # print(line_coord_of_collisions_fixed)

        # self.create_oval(*line_coord_of_collisions[0], outline="red")
        # self.create_oval(*line_coord_of_collisions[1], outline="red")
        # self.create_line(x0, y0, x1, y1, **kwargs)

        # self.draw_circle(x0, y0, 5, consider=False)
        # print(check_collision(Vector2(x0, y0)))
        divided_coordinates = [] if check_collision(Vector2(x0, y0)) else [(x0, y0)]
        divided_coordinates += line_coord_of_collisions_fixed + [adder((x1, y1), -offset_collision)]
        divided_coordinates.sort(reverse=False if (x0, y0) < (x1, y1) else True)
        line_created = []
        temp_coords = ()
        for k, coords in enumerate(divided_coordinates):
            temp_coords += coords
            if k % 2 == 1:
                # print(temp_coords)
                line_created.append(
                    self.create_line(*temp_coords, arrow=arrow if k == len(divided_coordinates) - 1 else ''))
                temp_coords = ()
        self.objects.get(type_of_object).append([line_created])


class Draggable_frame(tk.Frame):
    def __init__(self, root_: tk.Tk):
        tk.Frame.__init__(self, root_)
        self.canvas = Canvas(self, width=root_.winfo_width(), height=root_.winfo_height(), background="bisque")
        self.xsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)

        # self.xsb.grid(row=1, column=0, sticky="ew")
        # self.ysb.grid(row=0, column=1, sticky="ns")

        self.canvas.pack(expand=True, fill=tk.BOTH)  # .grid(row=0, column=0, sticky="nsew")
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
