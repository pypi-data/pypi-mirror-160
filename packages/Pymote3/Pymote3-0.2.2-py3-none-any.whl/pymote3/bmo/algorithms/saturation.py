from pymote3.algorithm import NodeAlgorithm
from pymote3.message import Message
from numpy import random


class Saturation(NodeAlgorithm):
    required_params = {}
    default_params = {
        'neighborsKey': 'Neighbors', 
        'treeNeighborsKey': ''
    }

    def initializer(self):
        if self.treeNeighborsKey != '':
            self.neighborsKey = self.treeNeighborsKey
        else:
            for node in self.network.nodes_list():
                node.memory[self.neighborsKey] = node.compositeSensor.read()['Neighbors']
                node.status = 'AVAILABLE'

        for node in self.network.nodes_list():
            node.memory['parent'] = None
            node.memory['remainingNeighbors'] = []
            node.memory['temp'] = node.compositeSensor.read()['Temperature']

        ini_nodes = []
        for i in range(len(self.network.nodes_list())):
            if random.random() > 0.5:
                ini_nodes.append(self.network.nodes_list()[i])

        for n in ini_nodes:
            self.network.outbox.insert(0, Message(
                header=NodeAlgorithm.INI,
                destination=n
            ))

    def available(self, node, message):
        if message.header == NodeAlgorithm.INI:
            node.send(Message(
                header='Activate',
                destination=node.memory[self.neighborsKey]
            ))

            self.initialize(node, message)

            node.memory['remainingNeighbors'] = list(node.memory[self.neighborsKey])

            if len(node.memory['remainingNeighbors']) == 1:
                msg = self.prepare_message(node, message)

                node.memory['parent'] = node.memory['remainingNeighbors'][0]

                msg.destination = node.memory['parent']
                node.send(msg)

                node.status = 'PROCESSING'
            else:
                node.status = 'ACTIVE'

        elif message.header == 'Activate':
            destination_nodes = list(node.memory[self.neighborsKey])
            destination_nodes.remove(message.source)
            node.send(Message(
                header='Activate',
                destination=destination_nodes
            ))

            self.initialize(node, message)

            node.memory['remainingNeighbors'] = list(node.memory[self.neighborsKey])

            if len(node.memory['remainingNeighbors']) == 1:
                msg = self.prepare_message(node, message)

                node.memory['parent'] = node.memory['remainingNeighbors'][0]

                msg.destination = node.memory['parent']
                node.send(msg)

                node.status = 'PROCESSING'
            else:
                node.status = 'ACTIVE'

    def active(self, node, message):
        if message.header == 'M':
            self.process_message(node, message)

            node.memory['remainingNeighbors'].remove(message.source)            

            if len(node.memory['remainingNeighbors']) == 1:
                msg = self.prepare_message(node, message)

                node.memory['parent'] = node.memory['remainingNeighbors'][0]

                msg.destination = node.memory['parent']
                node.send(msg)

                node.status = 'PROCESSING'

    def processing(self, node, message):
        if message.header == 'M':
            self.process_message(node, message)
            
            self.resolve(node, message)

    def saturated(self, node, message):
        pass

    # Procedures
    def initialize(self, node, message):
        pass

    def prepare_message(self, node, message):
        # If overridden header should stay 'M'
        return Message(
            header='M',
            data=node.memory['temp']
        )

    def process_message(self, node, message):
        if message.data < node.memory['temp']:
            node.memory['temp'] = message.data

    def resolve(self, node, message):
        # Start the Resolution stage
        msg = self.prepare_message(node, message)
        
        destination_nodes = list(node.memory[self.neighborsKey])
        destination_nodes.remove(node.memory['parent'])
        
        msg.destination=destination_nodes

        node.send(msg)

        node.status = 'SATURATED'


    STATUS = {
        'AVAILABLE': available,
        'ACTIVE': active,
        'PROCESSING': processing,
        'SATURATED': saturated
    }
