#  Copyright ~Lorenzo Londero 2021.

from Neural_Network import Neural_network

neural_n = Neural_network()
x0 = neural_n.input_layer.add_neuron()
x0.sigma = 1
x1 = neural_n.input_layer.add_neuron()
x1.sigma = 2

x2 = neural_n.input_layer.add_neuron()
x2.sigma = 3

neural_n.add_hidden_layer("h0")

h00 = neural_n.get_hidden_layer("h0").add_neuron()
h00.bias = (1, 2)

x0.connect_to(h00, 1)
x2.connect_to(h00, 5)

h01 = neural_n.get_hidden_layer("h0").add_neuron()
h01.bias = (1, 1)

x0.connect_to(h01, 2)
x1.connect_to(h01, 4)
x2.connect_to(h01, 6)

h10 = neural_n.output_layer.add_neuron()
h10.bias = (1, 3)

h00.connect_to(h10, 7)
h01.connect_to(h10, 8)

neural_n.print_network()
neural_n.show_network()
