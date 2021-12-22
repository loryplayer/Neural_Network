from Neural_Network import Neural_network

neural_n = Neural_network()
x0 = neural_n.input_layer.add_neuron("x0")
x0.sigma = 0
x1 = neural_n.input_layer.add_neuron("x1")
x1.sigma = 1
x2 = neural_n.input_layer.add_neuron("x2")
x2.sigma = 1
x3 = neural_n.input_layer.add_neuron("x3")
x3.sigma = 0

neural_n.add_hidden_layer("h0")

h00 = neural_n.get_hidden_layer("h0").add_neuron("h00")
h00.bias = (1, 10)

x0.connect_to(h00, -20)

neural_n.add_hidden_layer("h1")

h10 = neural_n.get_hidden_layer("h1").add_neuron("h10")
h10.bias = (1, -30)

h00.connect_to(h10, 20)
x1.connect_to(h10, 20)

output = neural_n.output_layer.add_neuron("Y")
output.bias = (1, 10)

h10.connect_to(output, -20)

neural_n.print_network()
