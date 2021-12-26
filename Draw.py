from __future__ import annotations
import math
import random

import Neural_Network
from Draggable_Frame import Draggable_frame
import tkinter as tk


class Draw:
    def __init__(self, neural_network: Neural_Network, width=800, height=500):
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(True, False)
        self.draggable_frame = Draggable_frame(self.root)
        self.draggable_frame.pack(fill="both", expand=True)
        self.neural_network = neural_network

        self.layers = self.Layers(self.draggable_frame)

        self.layers.add("input")
        self.input_layer = self.layers.get("input")
        for k, neuron in enumerate(self.neural_network.input_layer.neurons):
            self.input_layer.draw_neuron(neuron)

        for j, hidden_layer in enumerate(self.neural_network.hidden_layers):
            self.layers.add(hidden_layer.name)
            self.hidden_layer = self.layers.get(hidden_layer.name)
            # print(f"Hidden Layer: {hidden_layer.name}")
            for k, neuron in enumerate(hidden_layer.neurons):
                self.hidden_layer.draw_neuron(neuron)

        self.layers.add("output")
        self.output_layer = self.layers.get("output")
        for k, neuron in enumerate(self.neural_network.output_layer.neurons):
            self.output_layer.draw_neuron(neuron)
        self.layers.adjust_neurons()
        self.layers.connect_neurons()

    class Layers:
        def __init__(self, draggable_frame: Draggable_frame):
            self.draggable_frame = draggable_frame
            self.radius = 30
            self.layers = []

        def add(self, name: str):
            self.layers.append(
                self.Layer(self.draggable_frame, name, self.radius,
                           0 if len(self.layers) == 0 else self.layers[
                                                               len(self.layers) - 1].x_pointer + 5 * self.radius))

        class Layer:
            def __init__(self, draggable_frame: Draggable_frame, name: str, radius: float, initial_x=0):
                self.name = name
                self.radius = radius
                self.draggable_frame = draggable_frame
                self.neuron_colors = "#" + "".join([random.choice('0123456789ABCDEF') for j in range(6)])
                self.neurons = {}
                self.object_on_layer = []
                self._x_pointer = initial_x
                self.y_pointer = 75

            def draw_neuron(self, neuron: Neuron):
                x0 = self._x_pointer
                y0 = self.y_pointer
                y1 = y0 + self.radius
                neuron_drew = self.draggable_frame.canvas.draw_circle(x0, y0, self.radius, outline="black",
                                                                      fill=self.neuron_colors)
                neuron_name = self.draggable_frame.canvas.create_text(x0, y0 - 5,
                                                                      text=neuron.name,
                                                                      font=("Purisa", 12))
                neuron_sigma = self.draggable_frame.canvas.create_text(x0, y0 + 15,
                                                                       text=round(neuron.sigma),
                                                                       font=("Purisa", 12))
                self.y_pointer = y1 + self.radius * 3
                self.neurons.update({neuron_drew: neuron})
                self.object_on_layer.append(neuron_drew)
                self.object_on_layer.append(neuron_name)
                self.object_on_layer.append(neuron_sigma)

            def move_objects(self, y: float, x=0):
                for item in self.object_on_layer:
                    self.draggable_frame.canvas.move(item, x, y)

            @property
            def x_pointer(self):
                return self._x_pointer

        def get(self, name: str) -> Layer:
            for layer in self.layers:
                if layer.name == name:
                    return layer

        def connect_neurons(self):
            # self.draggable_frame.canvas.draw_circle(23.206933092733937, 414.63445352581283, 5, outline='red',
            #                                        consider=False)
            # self.draggable_frame.canvas.draw_circle(124.79306690726607,
            #                                        333.36554647418717, 5, outline='red', consider=False)
            # self.draggable_frame.canvas.draw_line(-1,434, 124.79306690726607,
            #                                      333.36554647418717,
            #                                      arrow=tk.LAST, show_intersections=True)
            aaa = True
            for k, layer in enumerate(self.layers):
                for neuron_info in layer.neurons.items():
                    neuron_coords = (self.draggable_frame.canvas.bbox(neuron_info[0])[0] + self.radius,
                                     self.draggable_frame.canvas.bbox(neuron_info[0])[1] + self.radius)
                    for neuron_connected in neuron_info[1].neurons_connected:
                        neuron_connected_ = ()
                        weight_value = 0
                        for next_layer in self.layers[k + 1:]:
                            for next_neuron in next_layer.neurons.items():
                                if neuron_connected.name == next_neuron[1].name:
                                    weight_value = neuron_connected.input.get(neuron_info[1].name)[1]
                                    neuron_connected_ += (
                                        self.draggable_frame.canvas.bbox(next_neuron[0])[0] + self.radius,
                                        self.draggable_frame.canvas.bbox(next_neuron[0])[1] + self.radius)
                        weight = self.draggable_frame.canvas.draw_txt(
                            neuron_coords[0] + (neuron_connected_[0] - neuron_coords[0]) / 2,
                            neuron_coords[1] + (neuron_connected_[1] - neuron_coords[1]) / 2 + 15,
                            text=weight_value,
                            font=("Purisa", 12))
            # self.draggable_frame.canvas.draw_line(-1,194,268.6019990535815,247.9203998107163,
            #                                     arrow=tk.LAST, show_intersections=True)

            for k, layer in enumerate(self.layers):
                for neuron_info in layer.neurons.items():
                    neuron_coords = (self.draggable_frame.canvas.bbox(neuron_info[0])[0] + self.radius,
                                     self.draggable_frame.canvas.bbox(neuron_info[0])[1] + self.radius)
                    for neuron_connected in neuron_info[1].neurons_connected:
                        neuron_connected_ = ()
                        for next_layer in self.layers[k + 1:]:
                            for next_neuron in next_layer.neurons.items():
                                if neuron_connected.name == next_neuron[1].name:
                                    neuron_connected_ += (
                                        self.draggable_frame.canvas.bbox(next_neuron[0])[0] + self.radius,
                                        self.draggable_frame.canvas.bbox(next_neuron[0])[1] + self.radius)
                        deltaY = (neuron_coords[1] - neuron_connected_[1])
                        deltaX = (neuron_connected_[0] - neuron_coords[0])
                        xy = self.draggable_frame.canvas.bbox(neuron_info[0])
                        # print(xy)
                        x = xy[2] - xy[0]
                        # print(x / 2)
                        angle = (math.atan2(deltaY, deltaX))
                        x_offset = ((x / 2) * math.cos(angle))
                        y_offset = ((x / 2) * math.sin(angle))
                        line_xa = neuron_coords[0]
                        line_ya = neuron_coords[1]
                        line_xb = neuron_connected_[0] - x_offset
                        line_yb = neuron_connected_[1] + y_offset

                        # self.draggable_frame.canvas.draw_circle(line_xa, line_ya, 5, outline='red', consider=False)
                        # self.draggable_frame.canvas.draw_circle(line_xb, line_yb, 5, outline='red', consider=False)
                        # print(neuron_info[1].name)
                        # print(line_xa, line_ya, line_xb, line_yb, sep=',')
                        self.draggable_frame.canvas.draw_line(line_xa, line_ya, line_xb, line_yb,
                                                              arrow=tk.LAST, offset_collision=5,
                                                              show_intersections=False)

        def adjust_neurons(self):
            max_y = 0
            for k, layer in enumerate(self.layers):
                for neuron_info in layer.neurons.items():
                    # print(neuron_info)
                    if self.draggable_frame.canvas.bbox(neuron_info[0])[3] > max_y:
                        max_y = self.draggable_frame.canvas.bbox(neuron_info[0])[3]
            # print(max_y)
            for k, layer in enumerate(self.layers):
                max_y_for_this_layer = 0
                for neuron_info in layer.neurons.items():
                    if self.draggable_frame.canvas.bbox(neuron_info[0])[3] > max_y_for_this_layer:
                        max_y_for_this_layer = self.draggable_frame.canvas.bbox(neuron_info[0])[3]
                # print(max_y - max_y_for_this_layer)
                layer.move_objects((max_y - max_y_for_this_layer) / 2)

    def go(self):
        self.draggable_frame.set_scrollregion(*self.draggable_frame.get_more_distant_points())
        while True:
            self.root.update()
