from __future__ import annotations
from Draw import Draw

import math

class Neural_network:
    def __init__(self):
        self.input_layer = self.Layer("input")
        self.hidden_layers = []
        self.output_layer = self.Layer("output")

    class Layer:
        def __init__(self, name: str):
            self.neurons = []
            self.name = name

        class Neuron:
            def __init__(self, name: str):
                self.name = name
                self.input = self.Input()
                self._bias = (0, 0)
                self._sigma = None
                self.neurons_connected = []

            def connect_to(self, neuron: Neuron, weight: float):
                neuron.input.add(self.name,
                                 self._sigma if self._sigma is not None else self.sigma, weight)
                self.neurons_connected.append(neuron)

            def sum(self) -> float:
                # print(self.input.inputs)
                summation = self._bias[0] * self._bias[1]
                for k, a in self.input.inputs.items():
                    summation += a[0] * a[1]
                return summation

            @property
            def sigma(self) -> float:
                sig = 1 / (1 + pow(math.e, -self.sum()))
                return sig if self._sigma is None else self._sigma

            @sigma.setter
            def sigma(self, value):
                self._sigma = value

            @property
            def bias(self):
                return self.input.get("bias")

            @bias.setter
            def bias(self, value: tuple):
                self.input.add("bias", *value)

            class Input:
                def __init__(self):
                    self.inputs = {}
                    self.number_inputs = 0

                def add(self, name_input: str, value: float, weight: float):
                    # print(f"{name_input}, {value}, {weight}")
                    self.inputs.update({name_input: (value, weight)})
                    # print(self.inputs)
                    self.number_inputs += 1

                def get(self, name_input: str) -> dict:
                    return self.inputs[name_input]

        def add_neuron(self, name) -> Neuron:
            neuron = self.Neuron(name)
            self.neurons.append(neuron)
            return neuron

    def add_hidden_layer(self, name):
        self.hidden_layers.append(self.Layer(name))

    def get_hidden_layer(self, name) -> Layer:
        layer = None
        for hidden_layer in self.hidden_layers:
            if hidden_layer.name == name:
                layer = hidden_layer
        return layer

    def print_network(self):
        print("Input layer:")
        for k, neuron in enumerate(self.input_layer.neurons):
            print(
                f"{'|' if k < len(self.input_layer.neurons) - 1 else chr(92)}->Name: {neuron.name}; Sigma: {neuron.sigma}")
        print("\n")
        for hidden_layer in self.hidden_layers:
            print(f"Hidden Layer: {hidden_layer.name}")
            for k, neuron in enumerate(hidden_layer.neurons):
                print(
                    f"{'|' if k < len(hidden_layer.neurons) - 1 else chr(92)}->Name: {neuron.name}; Sigma: {neuron.sigma}")
        print("\n")
        print(f"Output Layer:")
        for k, neuron in enumerate(self.output_layer.neurons):
            print(
                f"{'|' if k < len(self.output_layer.neurons) - 1 else chr(92)}->Name: {neuron.name}; Sigma: {neuron.sigma}")

    def show_network(self):
        draw = Draw(self)
        draw.go()
        '''
        print("Input layer:")
        for k, neuron in enumerate(self.input_layer.neurons):

        print("\n")
        for hidden_layer in self.hidden_layers:
            print(f"Hidden Layer: {hidden_layer.name}")
            for k, neuron in enumerate(hidden_layer.neurons):
                print(
                    f"{'|' if k < len(hidden_layer.neurons) - 1 else chr(92)}->Name: {neuron.name}; Sigma: {neuron.sigma}")
        print("\n")
        print(f"Output Layer:")
        for k, neuron in enumerate(self.output_layer.neurons):
            print(
                f"{'|' if k < len(self.output_layer.neurons) - 1 else chr(92)}->Name: {neuron.name}; Sigma: {neuron.sigma}")
        m_canvas.set_scrollregion(*m_canvas.get_more_distant_points())
        root.mainloop()
        '''
