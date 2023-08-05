import random
from pymote3.algorithm import NodeAlgorithm
from pymote3.message import Message


class PTConstruction(NodeAlgorithm):
    """
    Construction of the initiator (source) node shortest path routing table.

    It differs from the book in following:

    1. To be able to perform routing table construction selected node was
       added to IterationComplete message data so when source receives
       IterationComplete message it can update its routing table.

    2. At the end all nodes are in status DONE, and source node is INITIATOR

    """
    required_params = ()
    default_params = {
        'neighborsKey': 'Neighbors',
        'routingTableKey': 'routingTable',
        'weightKey': 'weight',
    }

    def initializer(self):
        # set weights
        for node in self.network.nodes_list():
            node.memory[self.weightKey] = dict()
        for u, v, data in self.network.edges(data=True):
            u.memory[self.weightKey][v] = data[self.weightKey]
            v.memory[self.weightKey][u] = data[self.weightKey]

        # set statuses and neighbors
        for node in self.network.nodes_list():
            sensor_readings = node.compositeSensor.read()
            node.memory[self.neighborsKey] = sensor_readings['Neighbors']
            node.status = 'IDLE'

        # ini_node = random.choice(self.network.nodes_list())
        ini_node = self.network.nodes_list()[0]
        ini_node.status = 'INITIATOR'

        # send Spontaneously
        self.network.outbox.insert(0, Message(
            header=NodeAlgorithm.INI,
            destination=ini_node
        ))

    def initiator(self, node, message):
        pass

    def idle(self, node, message):
        pass

    def awake(self, node, message):
        pass

    def waiting_for_ack(self, node, message):
        pass

    def active(self, node, message):
        pass

    def computing(self, node, message):
        pass

    def done(self, node, message):
        pass

    # Procedures
    def check_for_termination(self, node, message):
        pass

    def compute_local_minimum(self, node, message):
        pass

    STATUS = {
        'INITIATOR': initiator,
        'IDLE': idle,
        'AWAKE': awake,
        'WAITING_FOR_ACK': waiting_for_ack,
        'ACTIVE': active,
        'COMPUTING': computing,
        'DONE': done
    }
