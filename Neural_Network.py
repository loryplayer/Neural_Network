#  Copyright ~Lorenzo Londero 2021.

from __future__ import annotations
from Draw import Draw

import math


class Neural_network:
    def __init__(self):
        self.input_layer = self.Layer("X")
        self.hidden_layers: list[Neural_network.Layer] = []
        self.output_layer = self.Layer("Y")

    class Layer:
        def __init__(self, name: str):
            self.neurons = []
            self.name = name

        class Neuron:

            def __init__(self, name: str):
                self.name = name
                self.circle_id: int = ...
                self.input = self.Input()
                self._bias = (0, 0)
                self._sigma = None
                self.neurons_connected: list[Neural_network.Layer.Neuron] = []

            def connect_to(self, neuron: Neural_network.Layer.Neuron, weight: float):
                neuron.input.add(self,
                                 self._sigma if self._sigma is not None else self.sigma, weight)
                self.neurons_connected.append(neuron)

            def replace(self, neuron: Neural_network.Layer.Neuron):
                for neuron_connected in self.neurons_connected:
                    backup_weight = neuron_connected.input.get(self)[1]
                    neuron_connected.input.remove(self)
                    neuron.connect_to(neuron_connected, backup_weight)

            def sum(self) -> float:
                summation = self._bias[0] * self._bias[1]
                for k, a in self.input.inputs.items():
                    summation += a[1] * a[0]
                return summation

            @property
            def sigma(self) -> float:
                if self._sigma is not None:
                    return self._sigma
                sig = 1 / (1 + pow(math.e, -self.sum()))
                return sig

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

                def add(self, neuron_input: Neural_network.Layer.Neuron or str, value: float, weight: float):
                    self.inputs.update({neuron_input: (value, weight)})
                    self.number_inputs += 1

                def get(self, neuron_input: Neural_network.Layer.Neuron or str) -> (float, float) or None:
                    if neuron_input in self.inputs.keys():
                        return self.inputs[neuron_input]
                    return None

                def get_all(self):
                    return self.inputs

                def remove(self, neuron_input: Neural_network.Layer.Neuron):
                    if neuron_input in self.inputs:
                        del self.inputs[neuron_input]
                        self.number_inputs -= 1

        def add_neuron(self, name=None) -> Neuron:
            neuron = self.Neuron(self.name + str(len(self.neurons)) if name is None else name)
            self.neurons.append(neuron)
            return neuron

        def add_exist_neuron(self, neuron: Neuron, name=None):
            self.neurons.append(neuron)

    def add_hidden_layer(self, name: str):
        self.hidden_layers.append(self.Layer(name))

    def get_hidden_layer(self, name: str) -> Layer | None:
        layer = None
        for hidden_layer in self.hidden_layers:
            if hidden_layer.name == name:
                layer = hidden_layer
                return layer
        return None

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
                    f"{'|' if k < len(hidden_layer.neurons) - 1 else chr(92)}->Name: {neuron.name}; "
                    f"Sigma: {neuron.sigma}; "
                    f"Inputs: {(str([k for k, input_ in neuron.input.inputs.items() if k != 'bias']).replace('[', '(').replace(']', ')'))}")
        if self.hidden_layers:
            print("\n")
        print(f"Output Layer:")
        for k, neuron in enumerate(self.output_layer.neurons):
            print(
                f"{'|' if k < len(self.output_layer.neurons) - 1 else chr(92)}->Name: {neuron.name}; "
                f"Sigma: {neuron.sigma}; "
                f"Inputs: {(str([k for k, input_ in neuron.input.inputs.items() if k != 'bias']).replace('[', '(').replace(']', ')'))}")

    def show_network(self):
        draw = Draw(self)
        draw.go()
