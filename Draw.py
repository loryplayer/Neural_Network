import math
import random

import Neural_Network
from Canvas import Draggable_canvas
import tkinter as tk


class Draw:
    def __init__(self, neural_network: Neural_Network, width=800, height=500):
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(True, False)
        self.m_canvas = Draggable_canvas(self.root)
        self.m_canvas.pack(fill="both", expand=True)
        self.neural_network = neural_network

        self.layers = self.Layers(self.m_canvas)

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

        self.layers.connect_neurons()

    class Layers:
        def __init__(self, draggable_canvas):
            self.draggable_canvas = draggable_canvas
            self.radius = 50
            self.layers = []

        def add(self, name):
            self.layers.append(
                self.Layer(self.draggable_canvas, name, self.radius,
                           0 if len(self.layers) == 0 else self.layers[
                                                               len(self.layers) - 1].x_pointer + 3 * self.radius))

        class Layer:
            def __init__(self, canvas: Draggable_canvas, name, radius, initial_x=0):
                self.name = name
                self.radius = radius
                self.canvas = canvas
                self.neuron_colors = "#" + "".join([random.choice('0123456789ABCDEF') for j in range(6)])
                self.neurons = {}
                self._x_pointer = initial_x
                self.y_pointer = 75

            def draw_neuron(self, neuron):
                x0 = self._x_pointer
                y0 = self.y_pointer
                x1 = x0 + self.radius
                y1 = y0 + self.radius
                neuron_drew = self.canvas.canvas.create_oval(x0, y0, x1, y1, outline="black", fill=self.neuron_colors)
                neuron_name = self.canvas.canvas.create_text(x0 + self.radius / 2, y0 - 5 + self.radius / 2,
                                                             text=neuron.name,
                                                             font=("Purisa", 12))
                neuron_sigma = self.canvas.canvas.create_text(x0 + self.radius / 2, y0 + 15 + self.radius / 2,
                                                              text=round(neuron.sigma),
                                                              font=("Purisa", 12))
                self.y_pointer = y1 + self.radius
                self.neurons.update({neuron_drew: neuron})

            @property
            def x_pointer(self):
                return self._x_pointer

        def get(self, name) -> Layer:
            for layer in self.layers:
                if layer.name == name:
                    return layer

        def connect_neurons(self):
            for k, layer in enumerate(self.layers):
                for neuron_info in layer.neurons.items():
                    neuron_coords = (self.draggable_canvas.canvas.bbox(neuron_info[0])[0] + self.radius / 2,
                                     self.draggable_canvas.canvas.bbox(neuron_info[0])[1] + self.radius / 2)
                    for neuron_connected in neuron_info[1].neurons_connected:
                        neuron_connected_ = []
                        for next_layer in self.layers[k + 1:]:
                            for next_neuron in next_layer.neurons.items():
                                if neuron_connected.name == next_neuron[1].name:
                                    neuron_connected_.append(neuron_connected.input.get(neuron_info[1].name)[1])
                                    neuron_connected_.append((
                                        self.draggable_canvas.canvas.bbox(next_neuron[0])[0] + self.radius / 2,
                                        self.draggable_canvas.canvas.bbox(next_neuron[0])[1] + self.radius / 2))
                        weight = self.draggable_canvas.canvas.create_text(
                            neuron_coords[0] + (neuron_connected_[1][0] - neuron_coords[0]) / 2,
                            neuron_coords[1] + (neuron_connected_[1][1] - neuron_coords[1]) / 2 + 10,
                            text=neuron_connected_[0],
                            font=("Purisa", 12))
                        deltaY = abs(neuron_coords[1] - neuron_connected_[1][1])
                        deltaX = abs(neuron_connected_[1][0] - neuron_coords[0])
                        angle = (math.atan2(deltaY, deltaX))
                        x_offset = (self.radius * math.cos(angle)) / 2
                        y_offset = (self.radius * math.sin(angle)) / 2
                        self.draggable_canvas.canvas.create_line(neuron_coords[0] + x_offset,
                                                                 neuron_coords[1] - y_offset,
                                                                 neuron_connected_[1][0] - x_offset,
                                                                 neuron_connected_[1][1] + y_offset,
                                                                 arrow=tk.LAST)

    def go(self):
        self.m_canvas.set_scrollregion(*self.m_canvas.get_more_distant_points())
        while True:
            self.root.update()
