from pymote3.algorithm import NodeAlgorithm
from pymote3.message import Message


class DFT(NodeAlgorithm):
    required_params = ()
    default_params = {'neighborsKey': 'Neighbors'}

    def initializer(self):
        for node in self.network.nodes_list():
            node.memory[self.neighborsKey] = node.compositeSensor.read()['Neighbors']
            node.status = 'IDLE'
            
        ini_node = self.network.nodes_list()[0]
        ini_node.status = 'INITIATOR'
        
        self.network.outbox.insert(0, Message(
            header=NodeAlgorithm.INI, 
            destination=ini_node
        ))

    def initiator(self, node, message):
        if message.header == NodeAlgorithm.INI:
            node.memory["parent"] = None
            node.memory["unvisited"] = list(node.memory[self.neighborsKey])
            self.visit(node)

    def idle(self, node, message):
        if message.header == 'Token':
            node.memory["parent"] = message.source
            node.memory["unvisited"] = list(node.memory[self.neighborsKey])
            node.memory["unvisited"].remove(node.memory["parent"])
            self.visit(node)

    def visited(self, node, message):
        if message.header == 'Token':
            node.memory["unvisited"].remove(message.source)
            node.send(Message(
                header='Backedge', 
                destination=message.source
            ))
            
        elif message.header == 'Return':
            self.visit(node)
            
        elif message.header == 'Backedge':
            self.visit(node)

    def done(self, node, message):
        pass

    def visit(self, node):
        if len(node.memory["unvisited"]) == 0:
            if node.memory["parent"] is not None:
                node.send(Message(
                    header='Return', 
                    destination=node.memory["parent"]
                ))
            node.status = "DONE"
        else:
            next_unvisited = node.memory["unvisited"].pop()
            node.send(Message(
                header='Token', 
                destination=next_unvisited
            ))
            node.status = "VISITED"

    STATUS = {
        'INITIATOR': initiator,
        'IDLE': idle,
        'VISITED': visited,
        'DONE': done,
    }
