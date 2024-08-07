import unittest

from src.neuralnet.network import Network
from src.neuralnet.sigmoid_node import SigmoidNode
from src.neuralnet.synapse import Synapse
from src.pipeline.population_modifiers.cross.network_crosser import NetworkCrosser
from src.pipeline.population_modifiers.population_generator import PopulationGenerator


class TestNetworkCrosser(unittest.TestCase):
    def test_cross_network_swaps_one_weight_or_bias(self):
        population = PopulationGenerator().generate(2, [1,1])
        
        network = population.population[0]
        donor_network = population.population[1]
        
        
        NetworkCrosser().cross(network, donor_network)

        assert self.has_one_matching_synapse(network, donor_network) or self.has_one_matching_bias(network, donor_network)
    
    
    def has_one_matching_synapse(self, network1: Network, network2: Network) -> bool:
        network1_synapses = self.list_all_synapses(network1)            
        network2_synapses = self.list_all_synapses(network2)
        
        for synapse_index in range(len(network1_synapses)):
            if network1_synapses[synapse_index] == network2_synapses[synapse_index]:
                return True
            
        return False
    
    
    def has_one_matching_bias(self, network1: Network, network2: Network) -> bool:
        network1_biases = self.list_all_nodes(network1)
        network2_biases = self.list_all_nodes(network2)
        
        for bias_index in range(len(network1_biases)):
            if network1_biases[bias_index] == network2_biases[bias_index]:
                return True
            
        return False
    
    
    def list_all_nodes(self, network: Network) -> list[SigmoidNode]:
        nodes: list[SigmoidNode] = []
        
        for layer in network.node_layers:
            for node in layer:
                nodes.append(node)
                
        return nodes
    
    
    def list_all_synapses(self, network: Network) -> list[Synapse]:
        synapses: list[Synapse] = []
        
        for layer in network.synapse_layers:
            for synapse in layer:
                synapses.append(synapse)
                
        return synapses