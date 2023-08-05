from pymote3.algorithm import NodeAlgorithm
from pymote3.message import Message


class Shout(NodeAlgorithm):
    required_params = ()
    default_params = {
        'neighborsKey': 'Neighbors', 
        'treeNeighborsKey': 'treeNeighbors'
    }

    def initializer(self):
        for node in self.network.nodes_list():
            node.memory[self.neighborsKey] = node.compositeSensor.read()['Neighbors']
            node.memory[self.treeNeighborsKey] = []
            node.status = 'IDLE'

        ini_node = self.network.nodes_list()[0]
        ini_node.status = 'INITIATOR'

        self.network.outbox.insert(0, Message(
            header=NodeAlgorithm.INI,
            destination=ini_node
        ))

    def initiator(self, node, message):
        if message.header == NodeAlgorithm.INI:
            node.send(Message(
                header='Question'
            ))

            node.status = 'AVAILABLE'

    def idle(self, node, message):
        if message.header == 'Question':
            node.memory[self.treeNeighborsKey].append(message.source)

            node.send(Message(
                header='Yes',
                destination=message.source
            ))

            destination_nodes = list(node.memory[self.neighborsKey])
            destination_nodes.remove(message.source)
            node.send(Message(
                header='Question',
                destination=destination_nodes
            ))

            node.status = 'AVAILABLE'

    def available(self, node, message):
        if message.header == 'Yes':
            node.memory[self.treeNeighborsKey].append(message.source)

    STATUS = {
        'INITIATOR': initiator,
        'IDLE': idle,
        'AVAILABLE': available,
    }