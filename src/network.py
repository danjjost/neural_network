from src.sigmoid_node import SigmoidNode
from src.synapse import Synapse


class Network():

    def __init__(self, dimensions: list[int]):
        self.node_layers: list[list[SigmoidNode]] = []
        self.synapse_layers: list[list[Synapse]] = []
        
        self.initialize(dimensions)


    def initialize(self, dimensions: list[int]):
        self.initialize_node_layers(dimensions)
        self.initialize_synapse_layers(dimensions)

    def initialize_node_layers(self, dimensions: list[int]):
        for layer_index in range(len(dimensions)):
            self.node_layers.append(self.create_node_layer(dimensions[layer_index]))
            
    def create_node_layer(self, size: int):
        layer: SigmoidNode = []

        for node_index in range(size):
            layer.append(SigmoidNode())

        return layer
            
    def initialize_synapse_layers(self, dimensions: list[int]):
        number_of_synapse_layers = len(dimensions) - 1
        
        for synapse_layer_index in range(number_of_synapse_layers):
            self.synapse_layers.append([])
            
        for synapse_layer_index in range(number_of_synapse_layers):
            current_layer_index = synapse_layer_index
            next_layer_index = synapse_layer_index + 1
            
            self.synapse_layers[current_layer_index] = self.create_synapse_layer(current_layer_index, next_layer_index)


    def create_synapse_layer(self, current_layer_index: int, next_layer_index: int):
        synapse_layer = []
        
        for current_node in self.node_layers[current_layer_index]:
            for next_node in self.node_layers[next_layer_index]:        
                synapse_layer.append(Synapse(current_node, next_node))
                
        return synapse_layer
    
    
    def clear_evaluation_state(self):
        for layer in self.node_layers:
            for node in layer:
                node.clear_evaluation_state()
                
                
    def evaluate(self):
        for layer in range(len(self.node_layers)):
            for node in range(len(self.node_layers[layer])):
                self.node_layers[layer][node].determine_activation()
                
                
    def get_results(self) -> list[float]:
        return [node.activation for node in self.node_layers[-1]]
